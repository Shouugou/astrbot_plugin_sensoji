import random
import re
from datetime import date
from pathlib import Path

from astrbot.api.all import *
# 导入签文数据
from data.plugins.astrbot_plugin_sensoji.sensoji_data import sensoji_results

from data.plugins.astrbot_plugin_sensoji.templates import TMPL

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


@register("astrbot_plugin_sensoji", "Shouugou", "浅草寺抽签插件", "1.2.4", "repo url")
class SensojiPlugin(Star):

    def remove_escaped_emojis(self,text):
        # 匹配类似 &&confused&& 的转义字符串
        escaped_pattern = re.compile(r"&&\w+&&")
        return escaped_pattern.sub("", text)

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

        user_daily_results = load_data()

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

    async def _llm_fortune_explanation(self, event: AstrMessageEvent, message: str):
        """使用 LLM 对抽签进行解读"""
        # 定义解签提示模板
        fortune_prompt = (
            f"回复要求：\n"
            f"1. 如果用户尚未抽签，告知用户`需要先抽签，再进行解签`。\n"
            f"2. 如果用户已抽签，则分析签文内容并提供详细解释，包括抽签结果的意义、可能的象征以及建议。\n"
            f"3. 基于解签内容提炼出重点建议，提供一些具体与实际问题相关的指导意见。\n"
            f"4. 保持语气友好、亲切，确保签文解析准确且易于理解，尽量使用简短的一段话结束。\n"
            f"5. 基于角色以合适的语气、称呼等，生成符合人设的回答。\n\n"
            f"内容: {message}"
        )

        # 获取当前对话 ID
        curr_cid = await self.context.conversation_manager.get_curr_conversation_id(event.unified_msg_origin)
        context = []

        if curr_cid:
            # 如果当前对话 ID 存在，获取对话对象
            conversation = await self.context.conversation_manager.get_conversation(event.unified_msg_origin, curr_cid)
            if conversation and conversation.history:
                context = json.loads(conversation.history)
        else:
            # 如果当前对话 ID 不存在，创建一个新的对话
            curr_cid = await self.context.conversation_manager.new_conversation(event.unified_msg_origin)
            conversation = await self.context.conversation_manager.get_conversation(event.unified_msg_origin, curr_cid)

        # 调用 LLM 解析签文
        llm_response = await self.context.get_using_provider().text_chat(
            prompt=fortune_prompt,
            contexts=context,
            image_urls=[],
            system_prompt=self.context.provider_manager.selected_default_persona.get("prompt", "")
        )

        url = await self.html_render(TMPL, {"title": "解签结果", "message": self.remove_escaped_emojis(llm_response.completion_text.replace("\n", "<br>"))})
        yield event.image_result(url)


    @command("抽签")
    async def select_fortune(self, event: AstrMessageEvent):
        """浅草寺抽签"""
        user_id = event.get_sender_id()
        today = str(date.today())
        result = self.get_or_generate_result(user_id, today)

        url = await self.html_render(TMPL, {"title": "抽签结果" ,"message": result.replace("\n", "<br>")})
        yield event.image_result(url)

    @command("转运")
    async def change_fortune(self, event: AstrMessageEvent):
        """浅草寺转运"""
        user_id = event.get_sender_id()
        today = str(date.today())
        user_daily_results = load_data()

        # 检查用户是否已有抽签结果；无则抽签，有则重新抽取转运签
        is_change_fortune = user_id in user_daily_results and user_daily_results[user_id]['date'] == today
        result = self.get_or_generate_result(user_id, today, is_change_fortune)

        url = await self.html_render(TMPL, {"title": "转运结果", "message": result.replace("\n", "<br>")})
        yield event.image_result(url)

    @command("解签")
    async def explain_fortune(self, event: AstrMessageEvent):
        """LLM 解签"""
        user_id = event.get_sender_id()
        today = str(date.today())
        user_daily_results = load_data()

        message = (
            self.get_or_generate_result(user_id, today)
            if user_id in user_daily_results and user_daily_results[user_id]['date'] == today
            else "今日尚未抽签"
        )
        async for resp in self._llm_fortune_explanation(event, message):
            yield resp

    @llm_tool("explain_fortune")
    async def explain_fortune_tool(self, event: AstrMessageEvent):
        """Explain the result of a fortune from Sensoji Temple.应当在`解签``解释一下抽的签`时被调用。"""
        user_id = event.get_sender_id()
        today = str(date.today())
        user_daily_results = load_data()

        message = (
            self.get_or_generate_result(user_id, today)
            if user_id in user_daily_results and user_daily_results[user_id]['date'] == today
            else "今日尚未抽签"
        )
        async for resp in self._llm_fortune_explanation(event, message):
            yield resp

