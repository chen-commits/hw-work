from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_c3_stream_no_function_0012(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证流式模式下无函数调用")
        response = self.post_chat(self.build_request(user_content="你好", stream=True))
        events = self.extract_stream_events(response)
        has_tool_calls = False
        for event in events:
            choices = event.get("choices") or []
            if choices and choices[0].get("delta", {}).get("tool_calls"):
                has_tool_calls = True
                break
        assert not has_tool_calls, f"期望仅返回 content 增量，实际发现 tool_calls: {events}"
