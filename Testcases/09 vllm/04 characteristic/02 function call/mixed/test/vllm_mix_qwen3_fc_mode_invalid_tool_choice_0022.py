from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_mode_invalid_tool_choice_0022(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_mode_invalid_tool_choice_0022
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证非法tool_choice字符串时接口报错
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送非法tool_choice请求，有预期结果1
    ExpectedResult:
        1. 接口返回400类错误信息
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证非法 tool_choice 字符串返回 400")
        response = self.post_chat(
            self.build_request(user_content="hi", tool_choice="invalid_choice"),
            expect_status=400,
        )
        assert "Invalid value for `tool_choice`" in str(response), f"错误信息不符合预期: {response}"
