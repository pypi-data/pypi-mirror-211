from .solomonsensor import SolomonSensor
from logging import getLogger
from multiprocessing import Queue
from re import match, findall
from threading import Thread, Event
from time import sleep, time


logger = getLogger(__name__)


def convert_name(name):
    NAME_MAP = {r'conv\(.+\)': r'(?<=conv\().+?(?=,)'}
    for pattern, mask in NAME_MAP.items():
        if match(pattern, name):
            name = findall(mask, name)[0]
            break
    return 'custom:{}'.format(name)[:100]


def monitoring_data(pname, metrics, comment=""):
    try:
        return {
            "timestamp": tuple(metrics)[0],
            "data": {
                pname: {
                    "comment": comment,
                    "metrics": {convert_name(name): value for name, value in tuple(metrics.values())[0].items()}}}}
    except (IndexError, ValueError) as ve:
        logger.warning("Can't format. Wrong data {}. {}".format(metrics, ve), exc_info=True)


class SolomonReceiver(object):

    """
    The SolomonReceiver class collects metrics for all sensors and aggregates them together.
    """

    def __init__(self, api_host, config, timeout, token):
        self.api_host = api_host
        self.config = config
        self.token = token
        self.stop = Event()
        self.timeout = timeout
        self.sensors = list()
        self.panels = list()
        self._data_buffer = list()

    def get_buffered_data(self):
        data, self._data_buffer = self._data_buffer, []
        return data

    def prepare(self):
        for name, data in self.config.items():
            panel = Panel(name, self.timeout)
            senset = set()
            for dto in data['sensors']:
                sensor = SolomonSensor(self.api_host, data['project'], dto, panel.queue, self.token, data['priority_labels'])
                senset.update(sensor.get_sensors())
                self.sensors.append(Thread(target=self.run_sensor, args=(sensor,)))
            panel.set_sensors(senset)
            self.panels.append(Thread(target=self.run_panel, args=(panel,)))

    def run(self):
        for thread in self.panels:
            if not thread.is_alive():
                thread.start()
        for thread in self.sensors:
            if not thread.is_alive():
                thread.start()

    def stop_now(self):
        logger.info("Waiting for finish the Solomon plugin after {} second".format(self.timeout))
        sleep(self.timeout + 1)
        self.stop.set()
        for thread in self.sensors:
            if thread.is_alive():
                thread.join()
        for thread in self.panels:
            if thread.is_alive():
                thread.join()

    def run_sensor(self, sensor):
        while not self.stop.is_set() and not sensor.queue._closed:
            sleep(self.timeout)
            sensor.get_metrics()

    def run_panel(self, panel):
        try:
            while not self.stop.is_set():
                panel.process_queue()
                for metric in panel.ready_metrics():
                    self._data_buffer.append(monitoring_data(panel.name, metric))
                sleep(5)
        except Exception as ex:
            logger.error("Error {} for Solomon panel {}. {}".format(type(ex), panel.name, ex), exc_info=True)
        finally:
            logger.info("Solomon panel {} will be closed after {} second".format(panel.name, self.timeout))
            sleep(self.timeout)
            panel.process_queue()
            for ts, metrics in panel.buffer.items():
                self._data_buffer.append(monitoring_data(panel.name, {ts: metrics}))


class Panel(object):

    """
    The class Panel is used for initializing and managing structural levels for collecting monitoring data passed through the configuration file.
    """

    def __init__(self, name, timeout):
        self.name = name
        self.queue = Queue()
        self.timeout = timeout
        self.sensors = set()
        self.buffer = dict()

    def set_sensors(self, sensors):
        self.sensors = sensors

    def process_queue(self):
        try:
            while not self.queue.empty():
                self.compose_metrics(self.queue.get())
        except (IOError, OSError) as error:
            logger.warning("Panel {} get metrics from queue error. {}".format(self.name, error), exc_info=True)

    def compose_metrics(self, metric):
        if isinstance(metric, dict) and 'timestamp' in metric:
            if metric['timestamp'] in self.buffer:
                self.buffer[metric['timestamp']].update({metric['sensor']: metric['value']})
            else:
                self.buffer[metric['timestamp']] = {metric['sensor']: metric['value']}

    def ready_metrics(self):
        now = time()
        outbuffer = list()
        complite_ts = list()
        for ts, metrics in self.buffer.items():
            if self.sensors.issubset(set(metrics.keys())) or (now - ts) > self.timeout:
                outbuffer.append({ts: metrics})
                complite_ts.append(ts)
        for ts in complite_ts:
            self.buffer.pop(ts)
        return outbuffer
