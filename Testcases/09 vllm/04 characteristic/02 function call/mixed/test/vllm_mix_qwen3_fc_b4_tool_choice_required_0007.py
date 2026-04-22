from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_b4_tool_choice_required_0007(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_b4_tool_choice_required_0007
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证tool_choice=required时至少触发一个工具
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送tool_choice=required请求，有预期结果1
    ExpectedResult:
        1. response中返回至少一个tool_calls
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证 tool_choice=required 未指定函数时至少调用一个工具")
        response = self.post_chat(self.build_request(user_content="你好", tool_choice="required"))
        assert self.get_tool_calls(response), f"required 模式未触发工具: {response}"
