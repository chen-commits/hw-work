from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_schema_missing_tool_type_0017(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_schema_missing_tool_type_0017
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证工具type缺失时接口报错
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送type非法为空的工具定义请求，有预期结果1
    ExpectedResult:
        1. 接口返回400类错误信息
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证缺少 type 时返回 400")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "Hi"}],
                tools=[
                    {
                        "type": "",
                        "function": {
                            "name": "get_delivery_date",
                            "parameters": {
                                "type": "object",
                                "properties": {"order_id": {"type": "string"}},
                                "required": ["order_id"],
                            },
                        },
                    }
                ],
            ),
            expect_status=400,
        )
        self.assertIn("400", str(response), f"错误响应不符合预期: {response}")
