import json

from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_stream_parallel_tools_0011(FunctionCallCaseBase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_stream_parallel_tools_0011
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        验证流式模式下并行工具调用可组装为完整响应
    PreCondition:
        1. 在800I A2上安装环境
        2. 使用Qwen3-32B模型
        3. vllm服务已成功拉起
    TestStep:
        1. 发送流式并行函数请求，有预期结果1
    ExpectedResult:
        1. 流式response可组装出完整的多个tool_calls，且不同工具参数可正确解析
    Design Description:
        None
    Author:
        w60043782
    """

    def procedure(self):
        self.logStep("2. 验证流式并行工具响应可组装为完整结果")
        response = self.post_chat(
            self.build_request(
                user_content="查询北京的天气和计算99的平方",
                stream=True,
            )
        )
        assembled = self.assemble_stream_response(response)
        tool_calls = assembled["choices"][0]["message"]["tool_calls"]
        self.assertGreaterEqual(len(tool_calls), 2, f"期望至少组装出两个 tool_call: {assembled}")

        names = [tool_call["function"]["name"] for tool_call in tool_calls]
        self.assertIn("get_weather", names, f"未发现 get_weather: {assembled}")
        self.assertIn("calculate", names, f"未发现 calculate: {assembled}")

        args_by_name = {
            tool_call["function"]["name"]: json.loads(tool_call["function"]["arguments"] or "{}")
            for tool_call in tool_calls
        }
        weather_args = args_by_name["get_weather"]
        calculate_args = args_by_name["calculate"]
        self.assertEqual(weather_args.get("city"), "北京", f"天气参数不符合预期: {assembled}")
        self.assertTrue(calculate_args.get("expression"), f"计算参数不符合预期: {assembled}")
        self.assertEqual(
            assembled["choices"][0]["finish_reason"],
            "tool_calls",
            f"finish_reason 不符合预期: {assembled}",
        )
