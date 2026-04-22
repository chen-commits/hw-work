from .fc_test_common import FunctionCallCaseBase


class vllm_mix_qwen3_fc_b6_force_missing_function_0009(FunctionCallCaseBase):
    def procedure(self):
        self.logStep("2. 验证指定不存在的函数名时返回 400")
        response = self.post_chat(
            self.build_request(
                user_content="你好",
                tool_choice={"type": "function", "function": {"name": "non_existent_func"}},
            ),
            expect_status=400,
        )
        assert "400" in str(response), f"错误响应不符合预期: {response}"
