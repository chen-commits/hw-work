from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_i3_duplicate_names_0021(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证重复函数名场景")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "今天是几号"}],
                tool_choice="required",
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_current_time",
                            "description": "获取当前日期和时间",
                            "parameters": {"type": "object", "properties": {}},
                        },
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "get_current_time",
                            "description": "获取当前日期和时间",
                            "parameters": {"type": "object", "properties": {}},
                        },
                    },
                ],
            )
        )
        assert self.get_tool_calls(response), f"重复函数名场景未返回 tool_calls: {response}"
