from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_c1_stream_single_function_0010(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_c1_stream_single_function_0010
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证流式模式下单函数调用行为
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送流式单函数请求，有预期结果1
    ExpectedResult:
        1. 流式response中存在tool_calls增量片段
    Design Description:
        None
    Author:
        w60043782
    """
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
