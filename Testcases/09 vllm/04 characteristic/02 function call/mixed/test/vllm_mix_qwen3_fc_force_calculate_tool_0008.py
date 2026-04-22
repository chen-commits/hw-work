from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_force_calculate_tool_0008(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_force_calculate_tool_0008
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证指定函数名时强制调用calculate
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送指定calculate的tool_choice请求，有预期结果1
    ExpectedResult:
        1. response中返回calculate对应的tool_calls
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证指定函数名 calculate 时强制调用 calculate")
        response = self.post_chat(
            self.build_request(
                user_content="计算1111111111乘以2222222222222",
                tool_choice={"type": "function", "function": {"name": "calculate"}},
            )
        )
        self.assert_tool_name(response, "calculate")
