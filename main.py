import random
from datetime import date
from pathlib import Path

from astrbot.api.all import *
# 导入签文数据
from data.plugins.astrbot_plugin_sensoji.sensoji_data import sensoji_results

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
    def get_fortune_message(self, selected_result):
        """构建签文结果信息

        Args:
            selected_result (dict): 抽签结果数据.

        Returns:
            str: 构建的签文消息.
        """
        return (
            f"{selected_result['result']}\n\n"
            f"诗文：{selected_result['poetry']}\n\n"
            f"解析：{selected_result['interpretation']}\n\n"
            f"建议：{selected_result['suggestion']}\n\n"
            f"运势细节：{selected_result['horoscope_details']}"
        )

    def get_or_generate_result(self, user_id, today, is_change_fortune=False, result_data=sensoji_results):
        """获取用户的抽签结果或生成新的签文

        Args:
            user_id (str): 用户 ID.
            today (str): 当前日期.
            result_data (list): 用于生成签文的列表数据.
            is_change_fortune (bool): 是否生成转运签.

        Returns:
            str: 返回当前用户的抽签或转运结果.
        """
        # 检查用户是否已有当天结果
        if user_id in user_daily_results:
            if user_daily_results[user_id]['date'] != today:  # 如果日期过期，清除旧记录
                del user_daily_results[user_id]
                save_data(user_daily_results)

        # 如果用户没有当天的结果，或生成的签为转运签
        if user_id not in user_daily_results or is_change_fortune:
            selected_result = random.choice(result_data)
            result_message = self.get_fortune_message(selected_result)

            user_daily_results[user_id] = {
                'date': today,
                'result': result_message
            }
            save_data(user_daily_results)  # 保存结果

        return user_daily_results[user_id]['result']

    @command("抽签")
    async def select_fortune(self, event: AstrMessageEvent):
        """浅草寺抽签"""
        user_id = event.get_sender_id()
        today = str(date.today())
        result = self.get_or_generate_result(user_id, today)
        yield event.plain_result(result)

    @command("转运")
    async def change_fortune(self, event: AstrMessageEvent):
        """浅草寺转运"""
        user_id = event.get_sender_id()
        today = str(date.today())

        # 检查用户是否已有抽签结果；无则抽签，有则重新抽取转运签
        is_change_fortune = user_id in user_daily_results and user_daily_results[user_id]['date'] == today
        result = self.get_or_generate_result(user_id, today, is_change_fortune)
        yield event.plain_result(result)

    @command("解签")
    async def explain_fortune(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        today = str(date.today())
        result = self.get_or_generate_result(user_id, today)
        logger.info(result)
        return result

    # @llm_tool("select_fortune_tool")
    # async def select_fortune_tool(self, event: AstrMessageEvent):
    #     """Randomly draw a fortune from Sensoji Temple."""
    #     async for result in self.select_fortune(event):
    #         yield result
    #
    # @llm_tool("change_fortune_tool")
    # async def change_fortune_tool(self, event: AstrMessageEvent):
    #     """Randomly change a fortune from Sensoji Temple. For changing fortune and improving luck."""
    #     async for result in self.change_fortune(event):
    #         yield result


