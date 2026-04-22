import json

from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_h1_multi_turn_weather_0005(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证多轮上下文中的交替调用")
        resp1 = self.post_chat(self.build_request(user_content="北京天气怎么样？"))
        tool_call1 = self.assert_tool_name(resp1, "get_weather")
        args1 = self.get_tool_args(tool_call1)
        assert args1.get("city") == "北京", f"首轮城市识别错误: {args1}"

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
        assert args2.get("city") == "上海", f"多轮追问城市识别错误: {args2}"
