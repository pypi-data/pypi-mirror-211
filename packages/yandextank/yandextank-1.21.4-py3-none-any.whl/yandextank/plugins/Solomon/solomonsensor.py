from datetime import datetime
from json import loads
from logging import getLogger
from requests import post
from time import time


logger = getLogger(__name__)


class SolomonSensor(object):
    """
    The SolomonSensor class is intended for obtaining actual discrete values and composing these data into a convenient format for further processing.
    """

    GET_DATA_URI = '/api/v2/projects/{}/sensors/data'

    def __init__(self, api_host, prj, dto, queue, token, priority_labels):
        self.prj = prj
        self.body = self.get_body(dto)
        self.headers = {'Content-Type': "text/plain", 'Accept': "application/json", 'Authorization': token}
        self.data_url = "http://{0}{1}".format(api_host, self.GET_DATA_URI.format(prj))
        self.fromtime = time()
        self.queue = queue
        self.priority_labels = priority_labels
        self.metric_labels = ['app', 'metric', 'name', 'path', 'sensor', 'signal']
        self.ignore_labels = ['cluster', 'project', 'service', 'servant', 'os'] + self.metric_labels + self.priority_labels

    def get_metrics(self):
        now = time()
        fromtime = datetime.utcfromtimestamp(self.fromtime - 5).isoformat()
        totime = datetime.utcfromtimestamp(now).isoformat()
        self.fromtime = now
        self.parse_metrics(self.get_data(fromtime, totime))

    def parse_metrics(self, data):
        if isinstance(data, dict) and 'vector' in data.keys():
            try:
                for vector in data['vector']:
                    labels = vector['timeseries']['labels']
                    values = vector['timeseries']['values']
                    if 'timestamps' in vector['timeseries'].keys():
                        timestamps = vector['timeseries']['timestamps']
                    else:
                        timestamps = list()
                    self.send_metrics(labels, timestamps, values)
            except KeyError as ke:
                logger.warning("Wrong data: {}. {}".format(data, ke), exc_info=True)
        else:
            logger.warning("Wrong data: {}".format(data))

    def send_metrics(self, labels, timestamps, values):
        sensor = self.format_sensor(labels)
        try:
            for order, ts in enumerate(timestamps):
                self.queue.put(
                    {
                        'sensor': sensor,
                        'timestamp': int(ts) / 1000,
                        'value': values[order]
                    }
                )
        except (IOError, OSError) as error:
            logger.warning("Sensor {} send metrics error. {}".format(self.body, error), exc_info=True)

    def get_data(self, fromtime, totime):
        params = {
            'maxPoints': 500,
            'from': "{}Z".format(fromtime),
            'to': "{}Z".format(totime)
        }
        try:
            response = post(self.data_url, params=params, headers=self.headers, data=self.body)
        except ConnectionError as ce:
            logger.error("Error during request. {}".format(ce), exc_info=True)
        else:
            if response.status_code != 200:
                logger.warning('Wrong response code {} for body {}. {}'.format(response.status_code, self.body, response.json()))
                return None
            else:
                return response.json()

    def get_sensors(self):
        sensors = set()
        now = time()
        fromtime = datetime.utcfromtimestamp(now - 1).isoformat()
        totime = datetime.utcfromtimestamp(now).isoformat()
        data = self.get_data(fromtime, totime)
        if isinstance(data, dict) and 'vector' in data.keys():
            for vector in data['vector']:
                sensors.add(self.format_sensor(vector['timeseries']['labels']))
        return sensors

    def format_sensor(self, data):
        if isinstance(data, dict):
            for label in self.metric_labels:
                if label in data.keys():
                    sensor = data[label].replace("/", "-").replace(".", "-")
                    break
            else:
                logger.warning("Wrong labels {}".format(data))
                sensor = "Summary"
            for label in self.priority_labels:
                if label in data.keys():
                    sensor += "-{}".format(data[label].strip(r"\-.*_/").replace("/", "-").replace(".", "-"))
            for key, value in data.items():
                if key in self.ignore_labels:
                    continue
                else:
                    sensor += "_{}".format(str(value).strip(r"\-.*_/").replace("/", "-").replace(".", "-"))
            return sensor
        else:
            return None

    def get_body(self, data):
        if isinstance(data, dict):
            body = self.make_body(data)
        elif isinstance(data, str):
            try:
                body = self.make_body(loads(data))
            except ValueError:
                body = data.strip('\'\\')
        else:
            body = ""
        return body

    def make_body(self, dto):
        bodylist = list()
        if isinstance(dto, dict):
            for key, value in dto.items():
                bodylist.append("{}=\"{}\"".format(key, value))
        return "{{{bl}}}".format(bl=", ".join(bodylist))
