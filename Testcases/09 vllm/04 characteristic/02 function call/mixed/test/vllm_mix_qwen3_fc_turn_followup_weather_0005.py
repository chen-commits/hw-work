import json

from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_turn_followup_weather_0005(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_turn_followup_weather_0005
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证基于历史上下文的多轮天气工具调用
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 第一轮发送北京天气请求，有预期结果1
        2. 回传tool结果后继续追问上海天气，有预期结果2
    ExpectedResult:
        1. 第一轮response返回北京的 get_weather tool_calls
        2. 第二轮response基于历史继续返回上海的 get_weather tool_calls
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证多轮上下文中的交替调用")
        resp1 = self.post_chat(self.build_request(user_content="北京天气怎么样？"))
        tool_call1 = self.assert_tool_name(resp1, "get_weather")
        args1 = self.get_tool_args(tool_call1)
        self.assertEqual(args1.get("city"), "北京", f"首轮城市识别错误: {args1}")

        messages = [
            {"role": "user", "content": "北京天气怎么样？"},
            self.first_message(resp1),
            {
                "role": "tool",
                "tool_call_id": tool_call1["id"],
                "content": json.dumps({"city": "北京", "temperature": "25°C", "condition": "晴"}, ensure_ascii=False),
            },
            {"role": "user", "content": "那上海呢？"},
        ]
        resp2 = self.post_chat(self.build_request(messages=messages))
        tool_call2 = self.assert_tool_name(resp2, "get_weather")
        args2 = self.get_tool_args(tool_call2)
        self.assertEqual(args2.get("city"), "上海", f"多轮追问城市识别错误: {args2}")
