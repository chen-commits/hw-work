from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_mode_tool_choice_none_0006(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_mode_tool_choice_none_0006
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证tool_choice=none时禁止function call
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送tool_choice=none请求，有预期结果1
    ExpectedResult:
        1. response中不返回tool_calls，返回自然语言内容
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证 tool_choice=none")
        response = self.post_chat(self.build_request(user_content="北京天气", tool_choice="none"))
        self.assert_has_no_tool_calls(response)
        self.assertTrue(self.get_content(response), f"期望存在自然语言回复: {response}")
