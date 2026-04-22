from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_schema_missing_tool_choice_name_0027(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_schema_missing_tool_choice_name_0027
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证 tool_choice 对象缺少函数名时接口报错
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送缺少 function.name 的 tool_choice 请求，有预期结果1
    ExpectedResult:
        1. 接口返回400类错误信息
    Design Description:
        None
    Author:
        w60043782
    """

    def procedure(self):
        self.logStep("2. 验证 tool_choice 对象缺少函数名时接口报错")
        response = self.post_chat(
            self.build_request(
                user_content="北京天气",
                tool_choice={"type": "function", "function": {}},
            ),
            expect_status=400,
        )
        assert "400" in str(response), f"错误响应不符合预期: {response}"
