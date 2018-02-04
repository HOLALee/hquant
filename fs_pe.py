# -*- coding: utf-8 -*-

from gmsdk.api import StrategyBase

class Mystrategy(StrategyBase):
    def __init__(self, *args, **kwargs):
        super(Mystrategy, self).__init__(*args, **kwargs)


    def on_login(self):
        pass

    def on_error(self, code, msg):
        pass

    def on_tick(self, tick):
        pass

    def on_bar(self, bar):
        pass

    def on_execrpt(self, res):
        pass

    def on_order_status(self, order):
        pass

    def on_order_new(self, res):
        pass

    def on_order_filled(self, res):
        pass

    def on_order_partiall_filled(self, res):
        pass

    def on_order_stop_executed(self, res):
        pass

    def on_order_canceled(self, res):
        pass

    def on_order_cancel_rejected(self, res):
        pass


if __name__ == '__main__':
    myStrategy = Mystrategy(
        username='-',
        password='-',
        strategy_id='4786a29b-09b7-11e8-bce8-76dfbf6cddb5',
        subscribe_symbols='SZSE.000513.tick,SZSE.000513.bar.15',
        mode=4,
        td_addr='127.0.0.1:8001'
    )
    myStrategy.backtest_config(
        start_time='2000-02-01 09:30:00',
        end_time='2017-12-31 15:00:00',
        initial_cash=500000,
        transaction_ratio=0.5,
        commission_ratio=0.0003,
        slippage_ratio=0.001,
        price_type=1)
    ret = myStrategy.run()
    print('exit code: ', ret)