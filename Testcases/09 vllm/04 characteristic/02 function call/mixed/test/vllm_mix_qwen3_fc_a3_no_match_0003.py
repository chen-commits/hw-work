from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_a3_no_match_0003(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证无匹配函数时不触发工具调用")
        response = self.post_chat(self.build_request(user_content="播放一首周杰伦的歌"))
        self.assert_has_no_tool_calls(response)
        assert self.get_content(response), f"期望存在自然语言回复: {response}"
