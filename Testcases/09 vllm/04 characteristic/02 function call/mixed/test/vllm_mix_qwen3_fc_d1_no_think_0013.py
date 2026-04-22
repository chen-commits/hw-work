from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_d1_no_think_0013(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证 /no_think 模式")
        response = self.post_chat(self.build_request(user_content="北京天气\n\n/no_think"))
        message = self.first_message(response)
        assert message.get("tool_calls"), f"no_think 场景未返回 tool_calls: {response}"
        assert "reasoning_content" not in message, f"不应返回 reasoning_content: {message}"
