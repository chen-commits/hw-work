import json

from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_loop_single_tool_roundtrip_0004(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_loop_single_tool_roundtrip_0004
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证单函数调用后的完整闭环回复能力
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送天气查询请求并获取tool_calls，有预期结果1
        2. 传入tool_call_id和tool结果进行第二轮对话，有预期结果2
    ExpectedResult:
        1. 首轮response返回 get_weather 对应的tool_calls
        2. 第二轮response返回自然语言总结，不再触发新的tool_calls
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证单函数完整闭环")
        resp1 = self.post_chat(self.build_request(user_content="北京天气怎么样？"))
        tool_call = self.assert_tool_name(resp1, "get_weather")
        messages = [
            {"role": "user", "content": "北京天气怎么样？"},
            self.first_message(resp1),
            {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": json.dumps({"city": "北京", "temperature": "25°C", "condition": "晴"}, ensure_ascii=False),
            },
        ]
        resp2 = self.post_chat(self.build_request(messages=messages))
        self.assert_has_no_tool_calls(resp2)
        content = self.get_content(resp2) or ""
        self.assert_contains_text(content, "25")
        self.assert_contains_text(content, "晴")
