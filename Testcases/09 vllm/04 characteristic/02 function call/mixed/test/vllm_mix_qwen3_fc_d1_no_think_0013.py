from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_d1_no_think_0013(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_d1_no_think_0013
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证no_think模式下直接输出tool_calls
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送带/no_think指令的请求，有预期结果1
    ExpectedResult:
        1. response中返回tool_calls，且不包含reasoning_content字段
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证 /no_think 模式")
        response = self.post_chat(self.build_request(user_content="北京天气\n\n/no_think"))
        message = self.first_message(response)
        assert message.get("tool_calls"), f"no_think 场景未返回 tool_calls: {response}"
        assert "reasoning_content" not in message, f"不应返回 reasoning_content: {message}"
