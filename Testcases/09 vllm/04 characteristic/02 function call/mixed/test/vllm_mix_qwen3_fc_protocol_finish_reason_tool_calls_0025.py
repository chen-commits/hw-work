from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_protocol_finish_reason_tool_calls_0025(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_protocol_finish_reason_tool_calls_0025
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证触发工具调用时 finish_reason 为 tool_calls
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送会触发工具调用的请求，有预期结果1
    ExpectedResult:
        1. response中返回tool_calls，且finish_reason为tool_calls
    Design Description:
        None
    Author:
        w60043782
    """

    def procedure(self):
        self.logStep("2. 验证触发工具调用时 finish_reason 为 tool_calls")
        response = self.post_chat(self.build_request(user_content="北京天气怎么样？"))
        self.assertTrue(self.get_tool_calls(response), f"期望返回 tool_calls: {response}")
        self.assertEqual(
            self.get_finish_reason(response),
            "tool_calls",
            f"finish_reason 不符合预期: {response}",
        )
