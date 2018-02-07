from rqalpha.interface import AbstractMod
from .data_source import TushareKDataSource

class HelloWorldMod(AbstractMod):
    def start_up(self, env, mod_config):
        print(">>> HelloWorldMod.start_up")

    def tear_down(self, success, exception=None):
        print(">>> HelloWorldMod.tear_down")
