from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_i3_duplicate_names_0021(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_i3_duplicate_names_0021
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证工具列表中存在重复函数名时的行为
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送包含重复函数名的工具定义请求，有预期结果1
    ExpectedResult:
        1. response中正常返回tool_calls
    Design Description:
        None
    Author:
        w60043782
    """
    def procedure(self):
        self.logStep("2. 验证重复函数名场景")
        response = self.post_chat(
            self.build_request(
                messages=[{"role": "user", "content": "今天是几号"}],
                tool_choice="required",
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_current_time",
                            "description": "获取当前日期和时间",
                            "parameters": {"type": "object", "properties": {}},
                        },
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "get_current_time",
                            "description": "获取当前日期和时间",
                            "parameters": {"type": "object", "properties": {}},
                        },
                    },
                ],
            )
        )
        assert self.get_tool_calls(response), f"重复函数名场景未返回 tool_calls: {response}"
