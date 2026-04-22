from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_protocol_finish_reason_stop_0026(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_protocol_finish_reason_stop_0026
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证纯文本回复场景 finish_reason 为 stop
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送 tool_choice=none 请求，有预期结果1
    ExpectedResult:
        1. response中不返回tool_calls，且finish_reason为stop
    Design Description:
        None
    Author:
        w60043782
    """

    def procedure(self):
        self.logStep("2. 验证纯文本回复场景 finish_reason 为 stop")
        response = self.post_chat(
            self.build_request(user_content="北京天气", tool_choice="none")
        )
        self.assert_has_no_tool_calls(response)
        self.assertEqual(
            self.get_finish_reason(response),
            "stop",
            f"finish_reason 不符合预期: {response}",
        )
