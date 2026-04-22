from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_f1_bad_tools_json_0014(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证 tools 参数格式错误时返回 400")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "hi"}],
                tools=[{"type": "function", "function": {"name": "bad", "parameters": "not_object"}}],
            ),
            expect_status=400,
        )
        assert "400" in str(response), f"错误响应不符合预期: {response}"
