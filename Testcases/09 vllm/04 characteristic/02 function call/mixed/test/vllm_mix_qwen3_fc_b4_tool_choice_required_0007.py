from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_b4_tool_choice_required_0007(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证 tool_choice=required 未指定函数时至少调用一个工具")
        response = self.post_chat(self.build_request(user_content="你好", tool_choice="required"))
        assert self.get_tool_calls(response), f"required 模式未触发工具: {response}"
