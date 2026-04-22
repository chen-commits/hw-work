from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_catalog_large_toolset_0020(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_catalog_large_toolset_0020
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证大工具列表场景下仍能正确命中目标工具
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 构造大工具列表并发送天气请求，有预期结果1
    ExpectedResult:
        1. response中返回 get_city_weather 对应的tool_calls
    Design Description:
        None
    Author:
        w60043782
    """
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
