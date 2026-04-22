from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_boot_time_no_args_0001(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_boot_time_no_args_0001
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证无参数函数 get_current_time 的 function call 能力
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. 首个用例负责拉起vllm服务，后续用例复用该服务
    TestStep:
        1. 配置Qwen3-32B并启动服务，有预期结果1
        2. 发送 get_current_time 的 function call 请求，有预期结果2
    ExpectedResult:
        1. 服务拉起成功
        2. response中返回 get_current_time 对应的tool_calls，且arguments为空对象
    Design Description:
        None
    Author:
        w60043782
    """
    START_SERVER = True

    def procedure(self):
        self.logStep("2. 验证无参数函数 get_current_time")
        response = self.post_chat(self.build_request(user_content="现在几点了？"))
        tool_call = self.assert_tool_name(response, "get_current_time")
        self.assertEqual(self.get_tool_args(tool_call), {}, f"无参工具参数应为空: {tool_call}")
