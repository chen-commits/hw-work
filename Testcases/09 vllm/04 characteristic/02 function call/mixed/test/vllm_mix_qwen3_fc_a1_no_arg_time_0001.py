from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_a1_no_arg_time_0001(FunctionCallCaseBase):
    START_SERVER = True

    def procedure(self):
        self.logStep("2. 验证无参数函数 get_current_time")
        response = self.post_chat(self.build_request(user_content="现在几点了？"))
        tool_call = self.assert_tool_name(response, "get_current_time")
        assert self.get_tool_args(tool_call) == {}, f"无参工具参数应为空: {tool_call}"
