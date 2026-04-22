from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_j4_missing_function_name_0016(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证 function 对象缺少 name 时返回 400")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "hi"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "description": "no name",
                            "parameters": {"type": "object", "properties": {}},
                        },
                    }
                ],
            ),
            expect_status=400,
        )
        assert "400" in str(response), f"错误响应不符合预期: {response}"
