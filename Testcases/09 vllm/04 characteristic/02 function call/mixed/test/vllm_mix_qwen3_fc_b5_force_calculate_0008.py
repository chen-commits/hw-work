from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_b5_force_calculate_0008(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证指定函数名 calculate 时强制调用 calculate")
        response = self.post_chat(
            self.build_request(
                user_content="计算1111111111乘以2222222222222",
                tool_choice={"type": "function", "function": {"name": "calculate"}},
            )
        )
        self.assert_tool_name(response, "calculate")
