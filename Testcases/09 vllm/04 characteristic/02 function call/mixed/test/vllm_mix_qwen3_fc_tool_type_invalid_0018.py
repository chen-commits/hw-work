from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_tool_type_invalid_0018(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_tool_type_invalid_0018
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证工具type非function时接口报错
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送type非function的工具定义请求，有预期结果1
    ExpectedResult:
        1. 接口返回400类错误信息
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证 type 非 function 时返回 400")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "Hi"}],
                tools=[
                    {
                        "type": "aaa",
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
        assert "400" in str(response), f"错误响应不符合预期: {response}"
