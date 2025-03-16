import random
import json
from datetime import date
from pathlib import Path
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Star, register

# 导入签文数据
from .sensoji_data import sensoji_results

# 定义 JSON 文件路径（存储在插件目录下）
DATA_FILE = Path(__file__).parent / "user_daily_results.json"

# 加载数据
def load_data():
    """从 JSON 文件加载用户抽签结果"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 保存数据
def save_data(data):
    """将用户抽签结果保存到 JSON 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 初始化数据
user_daily_results = load_data()

@register("astrbot_plugin_sensoji", "Shouugou", "浅草寺抽签插件", "1.1.2", "repo url")
class SensojiPlugin(Star):
    @filter.command("抽签")
    async def sensoji(self, event: AstrMessageEvent):
        '''浅草寺抽签'''

        # 获取用户ID
        user_id = event.get_sender_id()

        # 获取当前日期
        today = str(date.today())

        # 检查用户是否已经有当天的抽签结果
        if user_id in user_daily_results:
            # 如果存储的日期不是今天，清除该用户的抽签结果
            if user_daily_results[user_id]['date'] != today:
                del user_daily_results[user_id]
                save_data(user_daily_results)  # 更新文件

        # 如果用户没有当天的抽签结果，生成新的结果
        if user_id not in user_daily_results:
            # 随机选择一个签文
            selected_sensoji = random.choice(sensoji_results)

            # 构建输出结果
            result_message = (
                f"抽签结果是：{selected_sensoji['result']}\n\n"
                f"诗文：{selected_sensoji['poetry']}\n\n"
                f"解释：{selected_sensoji['interpretation']}\n\n"
                f"建议：{selected_sensoji['suggestion']}\n\n"
                f"运势细节：{selected_sensoji['horoscope_details']}"
            )

            # 存储用户当天的抽签结果
            user_daily_results[user_id] = {
                'date': today,
                'result': result_message
            }
            save_data(user_daily_results)  # 更新文件

        # 返回结果
        yield event.plain_result(user_daily_results[user_id]['result'])