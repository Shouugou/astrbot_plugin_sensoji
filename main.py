import random

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Star, register

# 模拟浅草寺的签文
omikuji_results = [
    {"result": "大吉", "description": "万事顺利，好运连连。"},
    {"result": "吉", "description": "事情会顺利进行。"},
    {"result": "中吉", "description": "有些小波折，但总体顺利。"},
    {"result": "小吉", "description": "需要努力，但会有好结果。"},
    {"result": "末吉", "description": "结果一般，需要多加小心。"},
    {"result": "凶", "description": "可能会遇到困难，需谨慎行事。"},
    {"result": "大凶", "description": "运势不佳，需特别小心。"},
]

@register("omikuji", "Shouugou", "浅草寺抽签插件", "1.0.0", "repo url")
class OmikujiPlugin(Star):
    @filter.command("抽签")
    async def omikuji(self, event: AstrMessageEvent):
        '''浅草寺抽签'''

        # 随机选择一个签文
        selected_omikuji = random.choice(omikuji_results)

        # 返回结果
        yield event.plain_result(f"抽签结果是：{selected_omikuji['result']}\n{selected_omikuji['description']}")