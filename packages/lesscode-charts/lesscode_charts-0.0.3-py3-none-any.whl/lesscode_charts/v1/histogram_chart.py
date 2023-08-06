from typing import List

"""
柱状图/直方图/折线图
"""


class HistogramChart:
    @staticmethod
    def list2single_histogram(data: List[dict], title: str = "", unit: str = "",
                              x_name: str = "", y_name: str = None, **kwargs):
        """
        单柱状图
        :param data: 数据，示例：[{"key":"2020","value":10}]
        :param title: 图题
        :param unit: 数据单位
        :param x_name: x轴名称
        :param y_name: y轴名称
        :param kwargs: 额外数据，放在pool里
        :return:
        """
        x = []
        y = []
        for item in data:
            x.append(item.get("key"))
            y.append(item.get("value"))
        result = {
            "xName": x_name,
            "yName": y_name,
            "title": title,
            "x": x,
            "series": [
                {
                    "name": title,
                    "data": y,
                    "unit": unit
                }
            ]
        }
        if kwargs:
            result["pool"] = kwargs

        return result

    @staticmethod
    def list2more_histogram(data: List[dict], title: str = "", unit: str = "",
                            x_name: str = "", y_name: str = None, **kwargs):
        """
        多柱状图
        :param data: 数据，示例：[{"key":"2020","value":[10]}]
        :param title: 图题
        :param unit: 数据单位
        :param x_name: x轴名称
        :param y_name: y轴名称
        :param kwargs: 额外数据，放在pool里
        :return:
        """
        x = []
        y = []
        for item in data:
            x.append(item.get("key"))
            y.append(item.get("value"))
        result = {
            "xName": x_name,
            "yName": y_name,
            "title": title,
            "x": x,
            "series": [
                {
                    "name": title,
                    "data": y,
                    "unit": unit
                }
            ]
        }
        if kwargs:
            result["pool"] = kwargs

        return result
