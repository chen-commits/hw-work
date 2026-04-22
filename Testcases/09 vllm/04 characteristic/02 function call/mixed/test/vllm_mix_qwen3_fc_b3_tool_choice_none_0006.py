from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_b3_tool_choice_none_0006(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证 tool_choice=none")
        response = self.post_chat(self.build_request(user_content="北京天气", tool_choice="none"))
        self.assert_has_no_tool_calls(response)
        assert self.get_content(response), f"期望存在自然语言回复: {response}"
