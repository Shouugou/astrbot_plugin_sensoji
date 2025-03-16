import random
from datetime import date
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Star, register

# 导入签文数据
from .sensoji_data import sensoji_results

# 用于存储用户当天的抽签结果
user_daily_results = {}

@register("astrbot_plugin_sensoji", "Shouugou", "浅草寺抽签插件", "1.1.0", "repo url")
class SensojiPlugin(Star):
    @filter.command("抽签")
    async def sensoji(self, event: AstrMessageEvent):
        '''浅草寺抽签'''

        # 获取用户ID
        user_id = event.get_sender_id()

        # 获取当前日期
        today = date.today()

        # 检查用户是否已经有当天的抽签结果
        if user_id in user_daily_results:
            # 如果存储的日期不是今天，清除该用户的抽签结果
            if user_daily_results[user_id]['date'] != today:
                del user_daily_results[user_id]

        # 如果用户没有当天的抽签结果，生成新的结果
        if user_id not in user_daily_results:
            # 随机选择一个签文
            selected_sensoji = random.choice(sensoji_results)

            # 构建输出结果
            result_message = (
                f"抽签结果是：{selected_sensoji['result']}\n"
                f"运势描述：{selected_sensoji['description']}\n"
                f"诗句：{selected_sensoji['poem']}\n"
                f"建议：{selected_sensoji['advice']}"
            )

            # 存储用户当天的抽签结果
            user_daily_results[user_id] = {
                'date': today,
                'result': result_message
            }

        # 返回结果
        yield event.plain_result(user_daily_results[user_id]['result'])