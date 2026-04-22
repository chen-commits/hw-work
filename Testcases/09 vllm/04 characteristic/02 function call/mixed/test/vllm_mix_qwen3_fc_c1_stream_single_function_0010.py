from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_c1_stream_single_function_0010(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证流式模式下单函数调用")
        response = self.post_chat(self.build_request(user_content="北京天气", stream=True))
        events = self.extract_stream_events(response)
        assert events, f"流式响应为空: {response}"
        tool_deltas = []
        for event in events:
            choices = event.get("choices") or []
            if choices and choices[0].get("delta", {}).get("tool_calls"):
                tool_deltas.extend(choices[0]["delta"]["tool_calls"])
        assert tool_deltas, f"未发现流式 tool_calls 增量: {events}"
