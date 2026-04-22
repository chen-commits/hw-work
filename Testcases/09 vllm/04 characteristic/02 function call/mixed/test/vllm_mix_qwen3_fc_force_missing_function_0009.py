from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_force_missing_function_0009(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_force_missing_function_0009
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证指定不存在函数名时接口报错
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送指定不存在函数名的tool_choice请求，有预期结果1
    ExpectedResult:
        1. 接口返回400类错误信息
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证指定不存在的函数名时返回 400")
        response = self.post_chat(
            self.build_request(
                user_content="你好",
                tool_choice={"type": "function", "function": {"name": "non_existent_func"}},
            ),
            expect_status=400,
        )
        self.assertIn("400", str(response), f"错误响应不符合预期: {response}")
