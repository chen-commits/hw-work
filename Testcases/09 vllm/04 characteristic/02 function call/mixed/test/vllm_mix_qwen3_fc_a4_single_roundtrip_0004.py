import json

from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_a4_single_roundtrip_0004(FunctionCallCaseBase):
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
