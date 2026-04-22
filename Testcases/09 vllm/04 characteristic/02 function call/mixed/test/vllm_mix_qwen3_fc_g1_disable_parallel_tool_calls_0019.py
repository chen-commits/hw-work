from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_g1_disable_parallel_tool_calls_0019(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_g1_disable_parallel_tool_calls_0019
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证关闭parallel_tool_calls后仅返回单个工具调用
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送parallel_tool_calls=false请求，有预期结果1
    ExpectedResult:
        1. response中仅返回一个tool_call
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证 parallel_tool_calls=false")
        response = self.post_chat(
            self.build_request(
                user_content="北京天气和计算99的平方",
                extra_body={"parallel_tool_calls": False},
            )
        )
        tool_calls = self.get_tool_calls(response)
        assert len(tool_calls) == 1, f"parallel_tool_calls=false 时不应并行返回: {tool_calls}"
