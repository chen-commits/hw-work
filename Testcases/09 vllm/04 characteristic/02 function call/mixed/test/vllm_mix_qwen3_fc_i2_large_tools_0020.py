from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_i2_large_tools_0020(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证大工具列表下仍能命中目标工具")
        large_tools = []
        for i in range(100):
            large_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": f"tool_{i}",
                        "description": f"工具{i}，返回字符串 {i}",
                        "parameters": {"type": "object", "properties": {}},
                    },
                }
            )
        large_tools.append(
            {
                "type": "function",
                "function": {
                    "name": "get_city_weather",
                    "description": "获取城市天气",
                    "parameters": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                        "required": ["city"],
                    },
                },
            }
        )
        response = self.post_chat(self.build_request(messages=[{"role": "user", "content": "查询上海的天气"}], tools=large_tools))
        self.assert_tool_name(response, "get_city_weather")
