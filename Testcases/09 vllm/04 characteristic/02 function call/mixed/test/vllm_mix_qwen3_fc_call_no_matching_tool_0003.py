from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_call_no_matching_tool_0003(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_call_no_matching_tool_0003
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证无匹配工具时模型返回自然语言回复
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送不在工具范围内的请求，有预期结果1
    ExpectedResult:
        1. response中不返回tool_calls，仅返回自然语言内容
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证无匹配函数时不触发工具调用")
        response = self.post_chat(self.build_request(user_content="播放一首周杰伦的歌"))
        self.assert_has_no_tool_calls(response)
        self.assertTrue(self.get_content(response), f"期望存在自然语言回复: {response}")
