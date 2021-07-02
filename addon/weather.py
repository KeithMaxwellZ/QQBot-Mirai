from p_var import ENV, Msg_Comp, DEBUG
from util.util import text_payload_gen

import requests
from typing import Dict, Tuple, List
from pprint import pprint

ACTIVATE = True


class WeatherManager:
    """
    Module for weather forecast
    """
    @staticmethod
    def load():
        """
        Load the command into the environment
        :return:
        """
        ENV['cmd'].extend([("天气", WeatherManager.weather_wrapper)])

    @staticmethod
    def weather_wrapper(rd: Dict, args: Tuple) -> Tuple[Msg_Comp, bool]:
        """
        Wrapper function for weather_forecast function
        :param rd: original dictionary from the request
        :param args: should have exactly one, which is city name
        :return:
        """
        res = []
        if len(args) == 1:
            res.append(text_payload_gen("参数数量错误"))
        else:
            res.append(WeatherManager.weather_forecast(args[1]))
        return res, True

    @staticmethod
    def weather_forecast(city_name: str) -> Msg_Comp:
        """
        function for forecasting the weather in specific city
        :param city_name: target city
        :return: return a message component
        """
        # TODO: change to another API that supports foreign cities
        res = requests.get(f"http://wthrcdn.etouch.cn/weather_mini?city={city_name}")
        rj = res.json()
        if DEBUG:
            pprint(rj)

        # Check the status of the request result and form message components
        if rj['status'] != 1000:
            return [{"type": "Plain", "text": "城市名错误"}]
        else:
            s = f"{city_name}三日天气\n============\n"
            for i in range(3):
                d = rj['data']['forecast'][i]
                s += f"日期：{d['date']}\n{d['high']}\n{d['low']}\n=========\n"
            return [text_payload_gen(s)]


# Initialization
ENV['wm'] = WeatherManager()
if ACTIVATE:
    ENV['wm'].load()
print("Weather module imported")
