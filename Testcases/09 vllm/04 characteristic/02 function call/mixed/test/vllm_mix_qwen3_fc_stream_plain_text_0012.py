from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_stream_plain_text_0012(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_stream_plain_text_0012
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证流式纯文本响应可组装为完整回复
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送流式普通问答请求，有预期结果1
    ExpectedResult:
        1. 流式response可组装出完整文本，不存在tool_calls，finish_reason为stop
    Design Description:
        None
    Author:
        w60043782
    """

    def procedure(self):
        self.logStep("2. 验证流式纯文本响应可组装为完整结果")
        response = self.post_chat(self.build_request(user_content="你好", stream=True))
        assembled = self.assemble_stream_response(response)
        message = assembled["choices"][0]["message"]
        assert not message["tool_calls"], f"纯文本场景不应存在 tool_calls: {assembled}"
        assert message["content"], f"纯文本场景 content 不应为空: {assembled}"
        assert assembled["choices"][0]["finish_reason"] == "stop", (
            f"finish_reason 不符合预期: {assembled}"
        )
