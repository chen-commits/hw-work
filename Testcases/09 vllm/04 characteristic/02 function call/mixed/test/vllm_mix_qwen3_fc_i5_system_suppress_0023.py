from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_i5_system_suppress_0023(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证系统指令可抑制工具调用")
        response = self.post_chat(
            self.build_request(
                messages=[
                    {"role": "system", "content": "绝对不要使用任何工具(不要使用function call的能力)，直接回答用户问题。"},
                    {"role": "user", "content": "北京天气"},
                ]
            )
        )
        self.assert_has_no_tool_calls(response)
        assert self.get_content(response), f"期望存在自然语言回复: {response}"
