from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_required_missing_property_0015(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_required_missing_property_0015
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证required中无效字段被忽略后仍可正常调用
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送required中含不存在字段的工具定义请求，有预期结果1
    ExpectedResult:
        1. response中正常返回tool_calls，且有效参数抽取正确
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证 required 中包含不存在字段时仍可正常调用")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "What's the delivery date for order 999888?"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_delivery_date",
                            "description": "Get the delivery date for an order",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "order_id": {
                                        "type": "string",
                                        "description": "The customer's order ID",
                                    }
                                },
                                "required": ["order_id", "missing_param"],
                                "additionalProperties": False,
                            },
                        },
                    }
                ],
            )
        )
        tool_call = self.assert_tool_name(response, "get_delivery_date")
        assert self.get_tool_args(tool_call).get("order_id") == "999888", f"order_id 抽取异常: {tool_call}"
