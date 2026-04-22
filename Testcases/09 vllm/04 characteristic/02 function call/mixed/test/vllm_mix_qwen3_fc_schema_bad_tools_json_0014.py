from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_schema_bad_tools_json_0014(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_schema_bad_tools_json_0014
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证非法tools schema时接口报错
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送非法tools定义请求，有预期结果1
    ExpectedResult:
        1. 接口返回400类错误信息
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证 tools 参数格式错误时返回 400")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "hi"}],
                tools=[{"type": "function", "function": {"name": "bad", "parameters": "not_object"}}],
            ),
            expect_status=400,
        )
        assert "400" in str(response), f"错误响应不符合预期: {response}"
