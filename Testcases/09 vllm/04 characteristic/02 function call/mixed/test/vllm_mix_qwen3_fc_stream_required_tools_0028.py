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
        验证 stream 与 tool_choice=required 组合场景可组装完整响应
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送 stream=true 且 tool_choice=required 的请求，有预期结果1
    ExpectedResult:
        1. 流式response可组装出完整tool_calls，且finish_reason为tool_calls
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
        assembled = self.assemble_stream_response(response)
        tool_calls = assembled["choices"][0]["message"]["tool_calls"]
        self.assertTrue(tool_calls, f"期望组装出 tool_calls: {assembled}")
        self.assertTrue(tool_calls[0]["function"]["name"], f"工具名不应为空: {assembled}")
        self.assertEqual(
            assembled["choices"][0]["finish_reason"],
            "tool_calls",
            f"finish_reason 不符合预期: {assembled}",
        )
