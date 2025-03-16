import random

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Star, register

# 导入签文数据
from .sensoji_data import sensoji_results

@register("astrbot_plugin_sensoji", "Shouugou", "浅草寺抽签插件", "1.0.1", "repo url")
class SensojiPlugin(Star):
    @filter.command("抽签")
    async def sensoji(self, event: AstrMessageEvent):
        '''浅草寺抽签'''

        # 随机选择一个签文
        selected_sensoji = random.choice(sensoji_results)

        # 构建输出结果
        result_message = (
            f"抽签结果是：{selected_sensoji['result']}\n"
            f"运势描述：{selected_sensoji['description']}\n"
            f"诗句：{selected_sensoji['poem']}\n"
            f"建议：{selected_sensoji['advice']}"
        )

        # 返回结果
        yield event.plain_result(result_message)
