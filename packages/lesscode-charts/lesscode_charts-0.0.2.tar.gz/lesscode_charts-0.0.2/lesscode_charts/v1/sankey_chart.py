from typing import List

"""
桑基图
"""


class SankeyChart:
    @staticmethod
    def sankey(data: List[dict], title: str = "", data_key="id", parent_key="parent_id", **kwargs):
        """
        :param parent_key: 父级key
        :param data_key: 数据key
        :param title: 图题
        :param data: 数据,示例：[{"id":"INB133001","title":"感知设备与服务","value":"value1","parent_id":"INB1330","depth":2},
                                {"id":"INB1330","title":"感知设备","value":"value2","parent_id":None,"depth":1}]
        :return:
        """
        data_list = []
        link_list = []
        data_map = {item.get(data_key): item for item in data if item.get(data_key)}
        tmp = dict()
        for item in data:
            tmp.setdefault(item.get(parent_key), []).append(item)
        for parent_id, children in tmp.items():
            if parent_id:
                for child in children:
                    link_list.append(
                        {"source": data_map.get(parent_id, {}).get(data_key), "target": child.get(data_key),
                         "value": child.get("value")})
        for item in data:
            name = item.pop(data_key)
            label = item.pop("title")
            depth = item.pop("depth")
            value = item.pop("value", name)
            other = item.pop("other", {})
            info = {
                "name": name,
                "label": label,
                "value": value,
                "depth": depth
            }
            if other:
                info.update(other)
            data_list.append(info)
        result = {
            "series": [
                {
                    "name": title,
                    "data": data_list,
                    "links": link_list
                }
            ]
        }
        if kwargs:
            result["pool"] = kwargs

        return result
