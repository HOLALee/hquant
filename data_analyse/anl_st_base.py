# -*- coding: UTF-8 -*-

import pandas as pd
import json

class AnlStBase(object):
    """docstring for AnlStBase."""
    def __init__(self, root):
        super(AnlStBase, self).__init__()
        self.root = root

    def importJSON(self, filename):
        path = self.root+"\data\\" + filename
        print "to load file:",path
        #编码转换
        f = open(path,'r')
        r = f.read()
        r = r.decode("utf-8-sig")
        data = json.loads(r)
        #a_js = json.dumps(data)
        df = pd.DataFrame(data)
        print(df.head(1))

if __name__ == "__main__":
    a = AnlStBase("D:\py\\ts")
    a.importJSON("get_stock_basics.json")
