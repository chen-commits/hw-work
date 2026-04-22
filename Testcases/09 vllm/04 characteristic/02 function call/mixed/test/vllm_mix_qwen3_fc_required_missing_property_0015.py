from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_required_missing_property_0015(FunctionCallCaseBase):
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
