from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_tool_type_missing_0017(FunctionCallCaseBase):
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
        assert "400" in str(response), f"错误响应不符合预期: {response}"
