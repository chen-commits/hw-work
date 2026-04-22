from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_schema_tool_name_with_non_ascii_0030(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_schema_tool_name_with_non_ascii_0030
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证工具名称包含中文时接口报错
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送工具名称包含中文的请求，有预期结果1
    ExpectedResult:
        1. 接口返回400类错误信息
    Design Description:
        None
    Author:
        w60043782
    """

    def procedure(self):
        self.logStep("2. 验证工具名称包含中文时接口报错")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "请查询北京天气"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "获取天气",
                            "description": "获取城市天气",
                            "parameters": {
                                "type": "object",
                                "properties": {"city": {"type": "string"}},
                                "required": ["city"],
                            },
                        },
                    }
                ],
            ),
            expect_status=400,
        )
        self.assertIn("400", str(response), f"错误响应不符合预期: {response}")
