from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_stream_single_tool_0010(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_stream_single_tool_0010
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证流式模式下单函数调用可组装为完整响应
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送流式单函数请求，有预期结果1
    ExpectedResult:
        1. 流式response可组装出完整tool_calls，且finish_reason为tool_calls
    Design Description:
        None
    Author:
        w60043782
    """

    def procedure(self):
        self.logStep("2. 验证流式单函数响应可组装为完整结果")
        response = self.post_chat(
            self.build_request(user_content="现在几点了？", stream=True)
        )
        assembled = self.assemble_stream_response(response)
        tool_calls = assembled["choices"][0]["message"]["tool_calls"]
        assert len(tool_calls) == 1, f"期望组装出一个 tool_call: {assembled}"
        tool_call = tool_calls[0]
        assert tool_call["function"]["name"] == "get_current_time", (
            f"工具名不符合预期: {assembled}"
        )
        assert tool_call["function"]["arguments"] in ("", "{}"), (
            f"无参工具 arguments 不符合预期: {assembled}"
        )
        assert assembled["choices"][0]["finish_reason"] == "tool_calls", (
            f"finish_reason 不符合预期: {assembled}"
        )
