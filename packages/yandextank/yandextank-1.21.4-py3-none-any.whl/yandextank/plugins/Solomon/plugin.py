from yandextank.common.interfaces import MonitoringPlugin
from .solomonreceiver import SolomonReceiver
from logging import getLogger
from re import match


logger = getLogger(__name__)


def set_timeout(timestring):
    if match(r"^\d+s$", timestring):
        return int(timestring[:-1])
    elif match(r"^\d+m$", timestring):
        return 60 * int(timestring[:-1])
    elif match(r"^\d+h$", timestring):
        return 3600 * int(timestring[:-1])
    else:
        return 30


class Plugin(MonitoringPlugin):

    def __init__(self, core, cfg, name):
        super(Plugin, self).__init__(core, cfg, name)
        try:
            self.timeout = int(self.get_option('timeout'))
        except ValueError:
            self.timeout = set_timeout(self.get_option('timeout'))

    def send_collected_data(self, data):
        self.core.publish_monitoring_data(data)

    def is_test_finished(self):   # noqa: PLE0202
        data = self.solomon.get_buffered_data()
        if len(data) > 0:
            for metric in data:
                self.send_collected_data([metric])
        return -1

    def prepare_test(self):
        try:
            with open(self.get_option('token_file'), 'r') as tfile:
                token = "{}".format(tfile.read()).strip("\n")
        except (OSError, IOError):
            error = "Solomon plugin: Authorization token is not set! File {} is not found or can't to read.".format(self.get_option('token_file'))
            logger.warning(error)
            token = None
        if token:
            self.solomon = SolomonReceiver(self.get_option('api_host'), self.get_option('panels'), self.timeout, token)
            self.solomon.prepare()
        elif self.get_option('enforce_check_token'):
            raise RuntimeError(error)
        else:
            self.start_test = lambda *a, **kw: None
            self.is_test_finished = self.stub
            self.end_test = self.stub

    def start_test(self):   # noqa: PLE0202
        self.solomon.run()

    def end_test(self, retcode):   # noqa: PLE0202
        self.solomon.stop_now()
        self.send_rest()
        return retcode

    def send_rest(self):
        data = self.solomon.get_buffered_data()
        if len(data) > 0:
            for metric in data:
                self.send_collected_data([metric])

    def stub(self, *a, **kwa):
        return -1
