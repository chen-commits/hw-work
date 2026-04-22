from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_g1_disable_parallel_tool_calls_0019(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证 parallel_tool_calls=false")
        response = self.post_chat(
            self.build_request(
                user_content="北京天气和计算99的平方",
                extra_body={"parallel_tool_calls": False},
            )
        )
        tool_calls = self.get_tool_calls(response)
        assert len(tool_calls) == 1, f"parallel_tool_calls=false 时不应并行返回: {tool_calls}"
