from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_i6_tool_and_content_0024(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证 tool_calls 与 content 共存行为")
        response = self.post_chat(self.build_request(user_content="请告诉我北京天气，并夸夸这个城市"))
        tool_calls = self.get_tool_calls(response)
        assert tool_calls, f"期望模型调用工具: {response}"
        content = self.get_content(response)
        if content:
            self.logInfo(f"同时存在 content: {content[:100]}")
