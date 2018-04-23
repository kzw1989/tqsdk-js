#!/usr/bin/env python
#coding=utf-8

import unittest
from wh.test.base import TestConvert



class TestConvertIndicator(TestConvert):
    def test_dmi(self):
        case = {
            "id": "ATR",
            "cname": "真实波幅",
            "type": "SUB",
            "src": """
        //该模型仅仅用来示范如何根据指标编写简单的模型
        //用户需要根据自己交易经验，进行修改后再实际应用!!!
        // //后为文字说明，编写模型时不用写出
        TR : MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));//求最高价减去最低价，一个周期前的收盘价减去最高价的绝对值，一个周期前的收盘价减去最低价的绝对值，这三个值中的最大值
        ATR : MA(TR,N),COLORYELLOW;//求N个周期内的TR的简单移动平均""",
            "params": [
                ("N", 1, 300, 26),
            ],
            "expected": """

function* ATR(C){
C.DEFINE({
type: "SUB",
cname: "真实波幅",
state: "KLINE",
yaxis: [],
});
let N = C.PARAM(26.000000, "N", {"MIN": 1.000000, "MAX":300.000000});
let TR = C.OUTS("LINE", "TR", {color: RED});
let ATR = C.OUTS("LINE", "ATR", {color: YELLOW});

while(true){
let i = yield;
TR[i]=MAX(MAX((C.DS.high[i] - C.DS.low[i]), ABS((REF(i, C.DS.close, 1) - C.DS.high[i]))), ABS((REF(i, C.DS.close, 1) - C.DS.low[i])));
ATR[i]=MA(i, TR, N, ATR);
}
}        
           
            
         """,
        }

        self.assert_convert(case)


if __name__ == '__main__':
    unittest.main()
