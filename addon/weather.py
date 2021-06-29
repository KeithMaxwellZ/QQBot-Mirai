from p_var import ENV

import requests
from typing import Dict
from pprint import pprint

ACTIVATE = True


class WeatherManager:
    @staticmethod
    def load():
        ENV['cmd'].extend([("天气", WeatherManager.weather_wrapper)])

    @staticmethod
    def weather_wrapper(rd, args):
        res = []
        if len(args) == 1:
            res.append({"type": "Plain", "text": "参数数量错误"})
        else:
            res.append(WeatherManager.weather_forecast(args[1]))
        return res, True

    @staticmethod
    def weather_forecast(city_name: str) -> Dict:
        res = requests.get(f"http://wthrcdn.etouch.cn/weather_mini?city={city_name}")
        rj = res.json()
        pprint(rj)
        if rj['status'] != 1000:
            return {"type": "Plain", "text": "城市名错误"}
        else:
            s = f"{city_name}三日天气\n============\n"
            for i in range(3):
                d = rj['data']['forecast'][i]
                s += f"日期：{d['date']}\n{d['high']}\n{d['low']}\n=========\n"
            return {"type": "Plain", "text": s}


ENV['wm'] = WeatherManager()
if ACTIVATE:
    ENV['wm'].load()
print("Weather module imported")
