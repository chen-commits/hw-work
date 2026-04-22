from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_policy_system_suppress_tools_0023(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_policy_system_suppress_tools_0023
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证系统指令可抑制function call
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送带系统抑制指令的请求，有预期结果1
    ExpectedResult:
        1. response中不返回tool_calls，返回自然语言内容
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证系统指令可抑制工具调用")
        response = self.post_chat(
            self.build_request(
                messages=[
                    {"role": "system", "content": "绝对不要使用任何工具(不要使用function call的能力)，直接回答用户问题。"},
                    {"role": "user", "content": "北京天气"},
                ]
            )
        )
        self.assert_has_no_tool_calls(response)
        self.assertTrue(self.get_content(response), f"期望存在自然语言回复: {response}")
