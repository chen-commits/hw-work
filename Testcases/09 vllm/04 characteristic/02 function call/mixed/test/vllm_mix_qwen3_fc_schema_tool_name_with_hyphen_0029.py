from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_schema_tool_name_with_hyphen_0029(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_schema_tool_name_with_hyphen_0029
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证工具名称包含连字符时仍可正常触发function call
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送工具名称包含连字符的请求，有预期结果1
    ExpectedResult:
        1. response中正常返回 tool_calls，且工具名为 get-weather
    Design Description:
        None
    Author:
        w60043782
    """

    def procedure(self):
        self.logStep("2. 验证工具名称包含连字符时仍可正常触发 function call")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "请查询北京天气"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get-weather",
                            "description": "获取城市天气",
                            "parameters": {
                                "type": "object",
                                "properties": {"city": {"type": "string"}},
                                "required": ["city"],
                            },
                        },
                    }
                ],
            )
        )
        tool_call = self.assert_tool_name(response, "get-weather")
        self.assertEqual(
            self.get_tool_args(tool_call).get("city"),
            "北京",
            f"工具参数不符合预期: {tool_call}",
        )
