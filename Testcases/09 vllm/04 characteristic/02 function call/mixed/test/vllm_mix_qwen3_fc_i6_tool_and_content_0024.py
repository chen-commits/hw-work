from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_i6_tool_and_content_0024(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_i6_tool_and_content_0024
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证tool_calls与自然语言content的共存行为
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送既需要工具调用又希望自然语言回复的请求，有预期结果1
    ExpectedResult:
        1. response中返回tool_calls；若同时存在content，则记录共存行为
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证 tool_calls 与 content 共存行为")
        response = self.post_chat(self.build_request(user_content="请告诉我北京天气，并夸夸这个城市"))
        tool_calls = self.get_tool_calls(response)
        assert tool_calls, f"期望模型调用工具: {response}"
        content = self.get_content(response)
        if content:
            self.logInfo(f"同时存在 content: {content[:100]}")
