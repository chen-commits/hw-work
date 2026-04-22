import json

from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_call_parallel_tools_0002(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_call_parallel_tools_0002
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证并行调用多个工具的function call能力
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送同时包含天气查询和提醒创建的请求，有预期结果1
    ExpectedResult:
        1. response中返回两个tool_calls，且参数抽取结果符合预期
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证并行调用两个不同工具")
        prompt = (
            "请帮我同时做以下两件事：\n"
            "1. 查询纽约未来3天的天气。\n"
            "2. 给用户123创建一个提醒，标题为开会，内容为'项目讨论'，优先级高，"
            "标签为'工作'和'紧急'，时间范围从下午2点到3点。"
        )
        response = self.post_chat(self.build_request(user_content=prompt))
        tool_calls = self.get_tool_calls(response)
        self.assertEqual(len(tool_calls), 2, f"期望返回 2 个 tool_call，实际为 {tool_calls}")

        args_by_name = {
            tool_call["function"]["name"]: json.loads(tool_call["function"]["arguments"])
            for tool_call in tool_calls
        }
        weather_args = args_by_name["get_weather"]
        self.assertEqual(weather_args.get("city"), "纽约", f"城市识别错误: {weather_args}")
        self.assertEqual(weather_args.get("days"), 3, f"天气天数识别错误: {weather_args}")

        reminder_args = args_by_name["create_reminder"]
        self.assertEqual(reminder_args.get("user_id"), "123", f"user_id 错误: {reminder_args}")
        self.assertEqual(reminder_args.get("title"), "开会", f"title 错误: {reminder_args}")
        self.assertEqual(reminder_args.get("content"), "项目讨论", f"content 错误: {reminder_args}")
        self.assertEqual(reminder_args.get("priority"), "high", f"priority 错误: {reminder_args}")
        self.assertEqual(reminder_args.get("tags"), ["工作", "紧急"], f"tags 错误: {reminder_args}")
        self.assertEqual(
            reminder_args.get("time_range"),
            {"start": "14:00", "end": "15:00"},
            f"time_range 错误: {reminder_args}",
        )
