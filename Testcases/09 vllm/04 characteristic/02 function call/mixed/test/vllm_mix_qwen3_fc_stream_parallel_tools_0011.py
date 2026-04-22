from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_stream_parallel_tools_0011(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_stream_parallel_tools_0011
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证流式模式下并行工具调用行为
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送流式并行函数请求，有预期结果1
    ExpectedResult:
        1. 流式response中存在至少两个不同index的tool_calls片段
    Design Description:
        None
    Author:
        w60043782
    """
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
