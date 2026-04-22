from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_stream_required_tools_0028(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_stream_required_tools_0028
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证 stream 与 tool_choice=required 组合场景
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送 stream=true 且 tool_choice=required 的请求，有预期结果1
    ExpectedResult:
        1. 流式response中存在 tool_calls 增量片段
    Design Description:
        None
    Author:
        w60043782
    """

    def procedure(self):
        self.logStep("2. 验证 stream 与 tool_choice=required 组合场景")
        response = self.post_chat(
            self.build_request(
                user_content="现在几点了？",
                tool_choice="required",
                stream=True,
            )
        )
        events = self.extract_stream_events(response)
        assert events, f"流式响应为空: {response}"
        has_tool_delta = any(
            event.get("choices")
            and event["choices"][0].get("delta", {}).get("tool_calls")
            for event in events
        )
        assert has_tool_delta, f"未发现 tool_calls 增量: {events}"
