from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_c2_stream_parallel_0011(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证流式模式下多函数并行调用")
        response = self.post_chat(self.build_request(user_content="查询北京的天气和计算99的平方", stream=True))
        events = self.extract_stream_events(response)
        indices_seen = set()
        for event in events:
            choices = event.get("choices") or []
            if not choices:
                continue
            for tool_call in choices[0].get("delta", {}).get("tool_calls") or []:
                if "index" in tool_call:
                    indices_seen.add(tool_call["index"])
        assert len(indices_seen) >= 2, f"未发现至少两个并行 tool_call index: {events}"
