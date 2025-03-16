import random

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Star, register

# 模拟浅草寺的签文
sensoji_results = [
    {
        "result": "大吉",
        "description": "万事如意，福星高照。今日无论做什么都会顺利，是充满希望的一天。",
        "poem": "春风得意马蹄疾，一日看尽长安花。",
        "advice": "抓住机会，勇敢前行，好运将伴随你左右。"
    },
    {
        "result": "吉",
        "description": "运势平稳，小有收获。虽然不会有大惊喜，但也不会遇到太大的困难。",
        "poem": "山重水复疑无路，柳暗花明又一村。",
        "advice": "保持耐心，稳步前进，终会看到希望。"
    },
    {
        "result": "中吉",
        "description": "虽有波折，但终能成功。今天可能会遇到一些小挑战，但只要努力就能克服。",
        "poem": "不经一番寒彻骨，怎得梅花扑鼻香。",
        "advice": "遇到困难时不要气馁，坚持就是胜利。"
    },
    {
        "result": "小吉",
        "description": "运势平平，需靠努力。今天不会有太大的惊喜，但只要付出努力，就会有所收获。",
        "poem": "欲穷千里目，更上一层楼。",
        "advice": "脚踏实地，努力奋斗，未来会更好。"
    },
    {
        "result": "末吉",
        "description": "运势稍弱，需谨慎行事。今天可能会遇到一些小麻烦，但只要小心应对，问题不大。",
        "poem": "行到水穷处，坐看云起时。",
        "advice": "保持冷静，等待时机，事情会逐渐好转。"
    },
    {
        "result": "凶",
        "description": "运势不佳，需特别小心。今天可能会遇到一些阻碍，但只要冷静应对，就能化险为夷。",
        "poem": "黑云压城城欲摧，甲光向日金鳞开。",
        "advice": "避免冲动决策，谨慎行事，方能渡过难关。"
    },
    {
        "result": "大凶",
        "description": "运势极差，需特别警惕。今天可能会遇到较大的挑战，建议保持低调，避免冒险。",
        "poem": "屋漏偏逢连夜雨，船迟又遇打头风。",
        "advice": "凡事小心，避免与人争执，静待时机。"
    },
    {
        "result": "半吉",
        "description": "运势好坏参半。今天可能会遇到一些好事，但也需要警惕潜在的风险。",
        "poem": "塞翁失马，焉知非福。",
        "advice": "保持乐观，但不可掉以轻心。"
    },
    {
        "result": "末凶",
        "description": "运势低迷，需特别小心。今天可能会遇到一些不顺心的事情，建议保持耐心，等待时机。",
        "poem": "风急天高猿啸哀，渚清沙白鸟飞回。",
        "advice": "避免冒险，静待时机，事情会逐渐好转。"
    },
    {
        "result": "平",
        "description": "运势平稳，没有太大波动。今天适合按部就班地完成日常事务，不要期待太多变化。",
        "poem": "采菊东篱下，悠然见南山。",
        "advice": "保持平常心，享受当下的平静。"
    },
    {
        "result": "小凶",
        "description": "可能会遇到一些小麻烦，但只要小心应对，问题不会太大。",
        "poem": "山雨欲来风满楼，黑云压城城欲摧。",
        "advice": "谨慎行事，避免冲动，问题会逐渐解决。"
    },
    {
        "result": "半凶",
        "description": "运势较差，需多加注意。今天可能会遇到一些挫折，但只要保持冷静，就能找到解决办法。",
        "poem": "路漫漫其修远兮，吾将上下而求索。",
        "advice": "保持耐心，寻找机会，终会看到希望。"
    },
    {
        "result": "末小吉",
        "description": "运势稍有起色，但仍需努力。今天可能会看到一些希望的曙光，但不可掉以轻心。",
        "poem": "长风破浪会有时，直挂云帆济沧海。",
        "advice": "抓住机会，努力奋斗，未来会更好。"
    },
    {
        "result": "末中吉",
        "description": "运势逐渐好转。今天可能会遇到一些机会，抓住它们就能迎来更好的结果。",
        "poem": "千淘万漉虽辛苦，吹尽狂沙始到金。",
        "advice": "坚持不懈，终会迎来成功。"
    },
    {
        "result": "末大吉",
        "description": "运势大幅提升。今天可能会迎来意想不到的好运，抓住机会，迎接美好的未来。",
        "poem": "春风得意马蹄疾，一日看尽长安花。",
        "advice": "勇敢前行，好运将伴随你左右。"
    },
]

@register("astrbot_plugin_sensoji", "Shouugou", "浅草寺抽签插件", "1.1.0", "repo url")
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
