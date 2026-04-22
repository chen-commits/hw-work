from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_i4_invalid_tool_choice_0022(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证非法 tool_choice 字符串返回 400")
        response = self.post_chat(
            self.build_request(user_content="hi", tool_choice="invalid_choice"),
            expect_status=400,
        )
        assert "Invalid value for `tool_choice`" in str(response), f"错误信息不符合预期: {response}"
