import json
import logging
import os
import unittest

from openai import OpenAI

os.environ["NO_PROXY"] = "80.48.9.138"

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 工具定义
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如北京、上海"},
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位，默认celsius",
                    },
                    "days": {
                        "type": "integer",
                        "description": "预报天数，1-7之间，默认1",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2+3*4'",
                    },
                    "precision": {"type": "integer", "description": "小数精度，默认2"},
                },
                "required": ["expression"],
            },
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
    {
        "type": "function",
        "function": {
            "name": "create_reminder",
            "description": "为用户创建一个提醒任务",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "用户ID，例如：user123",
                    },
                    "title": {"type": "string", "description": "提醒标题"},
                    "content": {"type": "string", "description": "提醒详细内容"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "优先级，不提供时默认 medium",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": '标签列表，例如：["工作", "紧急"]',
                    },
                    "time_range": {
                        "type": "object",
                        "description": "提醒的时间范围",
                        "properties": {
                            "start": {
                                "type": "string",
                                "description": "开始时间，格式 HH:MM",
                            },
                            "end": {
                                "type": "string",
                                "description": "结束时间，格式 HH:MM",
                            },
                        },
                    },
                },
                "required": ["user_id", "title", "content"],
            },
        },
    },
]

# 初始化客户端
client = OpenAI(
    base_url="http://80.48.9.138:8003/v1",
    api_key="your-api-key-here",
)
# client = OpenAI(
#     base_url="http://141.63.59.8:1999/v1",
#     api_key="your-api-key-here",
# )


class FunctionCallTest(unittest.TestCase):
    """Function Call 功能测试集（假设语义理解正常）"""

    model_name = "Qwen3-32B"
    # model_name = "glm5"

    def _call(self, user_content, tool_choice="auto", stream=False, extra_body=None):
        """封装调用，返回响应（非流式）或流式迭代器"""
        messages = [{"role": "user", "content": user_content}]
        request = {
            "model": self.model_name,
            "messages": messages,
            "tools": tools,
            "tool_choice": tool_choice,
            "stream": stream,
        }
        if extra_body:
            request.update(extra_body)
        if stream:
            return client.chat.completions.create(**request)
        else:
            return client.chat.completions.create(**request)

    # ==================== 大类 A：基础功能正确性 ====================
    def test_A1_无参数函数(self):
        """场景：无参数函数 get_current_time"""
        response = self._call("现在几点了？")
        logging.info(response.model_dump_json(indent=2))
        self.assertIsNotNone(response.choices[0].message.tool_calls)
        tool_call = response.choices[0].message.tool_calls[0]
        self.assertEqual(tool_call.function.name, "get_current_time")
        args = json.loads(tool_call.function.arguments)
        self.assertEqual(args, {})

    def test_A2_并行调用(self):
        """并行调用两个不同工具"""
        prompt = (
            "请帮我同时做以下两件事：\n"
            "1. 查询纽约未来3天的天气。\n"
            "2. 给用户123创建一个提醒，标题为'开会'，内容为'项目讨论'，优先级高，"
            "标签为'工作'和'紧急'，时间范围从下午2点到3点。"
        )
        response = self._call(prompt)
        tool_calls = response.choices[0].message.tool_calls
        self.assertEqual(len(tool_calls), 2)

        logging.info(response.model_dump_json(indent=2))

        # 按函数名解析参数
        args_by_name = {}
        for tc in tool_calls:
            args_by_name[tc.function.name] = json.loads(tc.function.arguments)

        # 验证 get_weather
        self.assertIn("get_weather", args_by_name)
        weather_args = args_by_name["get_weather"]
        self.assertEqual(weather_args.get("city"), "纽约")
        self.assertEqual(weather_args.get("days"), 3)

        # 验证 create_reminder
        self.assertIn("create_reminder", args_by_name)
        reminder_args = args_by_name["create_reminder"]
        self.assertEqual(reminder_args.get("user_id"), "123")
        self.assertEqual(reminder_args.get("title"), "开会")
        self.assertEqual(reminder_args.get("content"), "项目讨论")
        self.assertEqual(reminder_args.get("priority"), "high")
        self.assertEqual(reminder_args.get("tags"), ["工作", "紧急"])
        self.assertEqual(
            reminder_args.get("time_range"), {"start": "14:00", "end": "15:00"}
        )

    def test_A3_无匹配函数(self):
        """场景：用户需求不在工具范围内，不应调用任何函数"""
        response = self._call("播放一首周杰伦的歌")
        logging.info(response.model_dump_json(indent=2))
        self.assertFalse(response.choices[0].message.tool_calls)
        self.assertIsNotNone(response.choices[0].message.content)

    def test_A4_完整闭环_单函数(self):
        """
        场景：模型发起调用 -> 模拟返回结果 -> 模型生成总结且不再调用
        """
        # 第一轮：发起调用
        resp1 = self._call("北京天气怎么样？")
        logging.info(resp1.model_dump_json(indent=2))
        self.assertTrue(resp1.choices[0].message.tool_calls)
        tool_call = resp1.choices[0].message.tool_calls[0]
        self.assertEqual(tool_call.function.name, "get_weather")

        # 构造第二轮：携带工具结果返回
        messages = [
            {"role": "user", "content": "北京天气怎么样？"},
            resp1.choices[0].message,  # 助手的function call请求
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    {"city": "北京", "temperature": "25°C", "condition": "晴"}
                ),
            },
        ]
        resp2 = client.chat.completions.create(
            model=self.model_name, messages=messages, tools=tools, stream=False
        )
        logging.info(resp2.model_dump_json(indent=2))
        # 验证第二轮不再发起调用，且包含自然语言总结
        self.assertFalse(resp2.choices[0].message.tool_calls)
        self.assertIn("25", resp2.choices[0].message.content)
        self.assertIn("晴", resp2.choices[0].message.content)

    def test_H1_multi_turn_alternating_calls(self):
        """多轮交替调用：第一轮查天气，第二轮查另一个城市（基于历史）"""
        # 第一轮：查询北京天气 -> 应调用 get_weather
        resp1 = self._call("北京天气怎么样？")
        self.assertTrue(resp1.choices[0].message.tool_calls)
        tool_call1 = resp1.choices[0].message.tool_calls[0]
        self.assertEqual(tool_call1.function.name, "get_weather")
        args1 = json.loads(tool_call1.function.arguments)
        self.assertEqual(args1.get("city"), "北京")

        # 模拟工具返回结果
        messages = [{"role": "user", "content": "北京天气怎么样？"}, resp1.choices[0].message, {
            "role": "tool",
            "tool_call_id": tool_call1.id,
            "content": json.dumps(
                {"city": "北京", "temperature": "25°C", "condition": "晴"}
            ),
        }, {"role": "user", "content": "那上海呢？"}]

        # 第二轮：用户接着问上海，模型应基于对话历史再次调用 get_weather
        resp2 = client.chat.completions.create(
            model=self.model_name, messages=messages, tools=tools, stream=False
        )
        logging.info(resp2.model_dump_json(indent=2))
        self.assertTrue(resp2.choices[0].message.tool_calls)
        tool_call2 = resp2.choices[0].message.tool_calls[0]
        self.assertEqual(tool_call2.function.name, "get_weather")
        args2 = json.loads(tool_call2.function.arguments)
        self.assertEqual(args2.get("city"), "上海")

    # ==================== 大类 B：tool_choice 配置 ====================
    def test_B3_tool_choice_none(self):
        """场景：tool_choice=none，强制禁止调用 -> 无tool_calls"""
        response = self._call("北京天气", tool_choice="none")
        logging.info(response.model_dump_json(indent=2))
        self.assertFalse(response.choices[0].message.tool_calls)
        self.assertIsNotNone(response.choices[0].message.content)

    def test_B4_tool_choice_required_未指定函数(self):
        """场景：tool_choice=required，未指定具体函数 -> 必须调用至少一个"""
        response = self._call("你好", tool_choice="required")
        logging.info(response.model_dump_json(indent=2))
        self.assertTrue(response.choices[0].message.tool_calls)
        # 调用哪个函数不限，只要存在即可

    def test_B5_tool_choice_required_指定函数名(self):
        """场景：tool_choice 指定函数名 calculate -> 强制调用 calculate"""
        tool_choice = {"type": "function", "function": {"name": "calculate"}}
        response = self._call(
            "计算1111111111乘以2222222222222", tool_choice=tool_choice
        )
        logging.info(response.model_dump_json(indent=2))
        tool_call = response.choices[0].message.tool_calls[0]
        self.assertEqual(tool_call.function.name, "calculate")

    def test_B6_tool_choice_required_指定不存在函数(self):
        """场景：tool_choice 指定不存在的函数 -> API应返回错误（期望4xx）"""
        tool_choice = {"type": "function", "function": {"name": "non_existent_func"}}
        with self.assertRaises(Exception) as context:
            self._call("你好", tool_choice=tool_choice)
        logging.info(context.exception)
        self.assertIn("400", str(context.exception))

    # ==================== 大类 C：流式模式 ====================
    def test_C1_stream_单函数(self):
        """场景：流式模式，单函数调用 -> 所有chunk能拼接成完整调用"""
        stream_response = self._call("北京天气", stream=True)
        collected_chunks = []
        for chunk in stream_response:
            logging.info(chunk)
            if chunk.choices[0].delta.tool_calls:
                collected_chunks.append(chunk.choices[0].delta.tool_calls[0])
        # 简单验证：至少有一个chunk，并且最终能拼出函数名
        self.assertTrue(len(collected_chunks) > 0)
        # TODO 实际拼接逻辑较复杂，此处仅验证流式返回非空
        # 更严格测试可收集所有arguments片段拼接后解析JSON

    def test_C2_stream_多函数并行(self):
        """场景：流式模式，多函数并行 -> 不同index的chunk能区分"""
        stream_response = self._call("查询北京的天气和计算99的平方", stream=True)
        indices_seen = set()
        for chunk in stream_response:
            if chunk.choices[0].delta.tool_calls:
                for tc in chunk.choices[0].delta.tool_calls:
                    indices_seen.add(tc.index)
        self.assertTrue(len(indices_seen) >= 2)  # 应有两个不同的index

    def test_C3_stream_无函数调用(self):
        """场景：流式模式，无函数调用 -> 只有content增量"""
        stream_response = self._call("你好", stream=True)
        has_tool_calls = False
        for chunk in stream_response:
            if chunk.choices[0].delta.tool_calls:
                has_tool_calls = True
                break
        self.assertFalse(has_tool_calls)

    # ==================== 大类 D：思考模式 ====================
    def test_D1_非思考模式(self):
        """场景：默认非思考模式 -> 直接输出tool_calls，无reasoning字段"""
        response = self._call("北京天气\n\n/no_think")
        logging.info(response.model_dump_json(indent=2))
        self.assertIsNotNone(response.choices[0].message.tool_calls)
        self.assertFalse(hasattr(response.choices[0].message, "reasoning_content"))

    # ==================== 大类 E：tools定义异常 ====================
    def test_F1_tools_json格式错误(self):
        """场景：tools定义中JSON格式错误 -> API应返回400"""
        bad_tools = [
            {
                "type": "function",
                "function": {"name": "bad", "parameters": "not_object"},
            }
        ]
        with self.assertRaises(Exception) as ctx:
            client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "hi"}],
                tools=bad_tools,
            )
        self.assertIn("400", str(ctx.exception))

    def test_required_with_missing_properties_ignored(self):
        """工具定义的 required 中包含 properties 中不存在的字段时，API 应忽略无效字段，仍能正常调用并传参"""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_delivery_date",
                    "description": "Get the delivery date for an order",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The customer's order ID",
                            }
                        },
                        "required": [
                            "order_id",  # 有效字段
                            "missing_param",  # properties 中不存在的字段（应被忽略）
                        ],
                        "additionalProperties": False,
                    },
                },
            }
        ]

        resp = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": "What's the delivery date for order 999888?",
                },
            ],
            tools=tools,
            tool_choice="auto"
        )
        logging.info(resp.model_dump_json(indent=2))
        # 验证正常返回了 tool_calls
        self.assertTrue(resp.choices[0].message.tool_calls)
        tool_call = resp.choices[0].message.tool_calls[0]
        self.assertEqual(tool_call.function.name, "get_delivery_date")

    def test_J4_function_object_missing_name(self):
        """function 对象中缺少 name 字段 -> 报错"""
        bad_tools = [
            {
                "type": "function",
                "function": {
                    "description": "no name",
                    "parameters": {"type": "object", "properties": {}},
                },
            }
        ]
        with self.assertRaises(Exception) as ctx:
            resp = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "hi"}],
                tools=bad_tools,
            )
        logging.info(ctx.exception)
        self.assertIn("400", str(ctx.exception))

    def test_tool_type_missing(self):
        """工具定义中缺少 type 字段 -> 应报错 400"""
        bad_tool = {
            "type": "",
            "function": {  # 缺少 type
                "name": "get_delivery_date",
                "parameters": {
                    "type": "object",
                    "properties": {"order_id": {"type": "string"}},
                    "required": ["order_id"],
                },
            }
        }
        with self.assertRaises(Exception) as ctx:
            resp = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "Hi"}],
                tools=[bad_tool],
            )
        logging.info(ctx.exception)
        self.assertIn("400", str(ctx.exception))

    def test_tool_type_no_function(self):
        """工具定义中type不是function -> 应报错 400"""
        bad_tool = {
            "type": "aaa",
            "function": {
                "name": "get_delivery_date",
                "parameters": {
                    "type": "object",
                    "properties": {"order_id": {"type": "string"}},
                    "required": ["order_id"],
                },
            }
        }
        with self.assertRaises(Exception) as ctx:
            resp = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "Hi"}],
                tools=[bad_tool],
            )
        logging.info(ctx.exception)
        self.assertIn("400", str(ctx.exception))

    # ==================== 大类 F：其他边界 ====================
    def test_G1_parallel_tool_calls_false(self):
        """场景：parallel_tool_calls=false -> 多需求只返回一个tool_call"""
        response = self._call(
            "北京天气和计算99的平方", extra_body={"parallel_tool_calls": False}
        )
        tool_calls = response.choices[0].message.tool_calls
        logging.info(response.model_dump_json(indent=2))
        self.assertEqual(len(tool_calls), 1)

    def test_I2_large_tools_list(self):
        """动态生成 100 个工具，模型仍能正确选择指定的工具"""
        # 生成 100 个简单工具，名称从 tool_0 到 tool_99
        large_tools = []
        for i in range(100):
            large_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": f"tool_{i}",
                        "description": f"工具{i}，返回字符串 '{i}'",
                        "parameters": {"type": "object", "properties": {}},
                    },
                }
            )
        # 在最后添加一个实际有用的工具
        large_tools.append(
            {
                "type": "function",
                "function": {
                    "name": "get_city_weather",
                    "description": "获取城市天气",
                    "parameters": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                        "required": ["city"],
                    },
                },
            }
        )
        resp = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": "查询上海的天气"}],
            tools=large_tools,
            tool_choice="auto",
        )
        logging.info(resp.model_dump_json(indent=2))
        self.assertTrue(resp.choices[0].message.tool_calls)
        tool_name = resp.choices[0].message.tool_calls[0].function.name
        self.assertEqual(tool_name, "get_city_weather")

    def test_I3_duplicate_function_name(self):
        """工具列表中存在同名函数"""
        duplicate_tools = [
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
        ]

        resp = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": "今天是几号"}],
            tool_choice="required",
            tools=duplicate_tools,
        )
        logging.info(resp.model_dump_json(indent=2))
        self.assertTrue(resp.choices[0].message.tool_calls)

    def test_I4_tool_choice_invalid_string(self):
        """tool_choice 为非法字符串（非 none/auto/required） -> 400"""
        with self.assertRaises(Exception) as ctx:
            self._call("hi", tool_choice="invalid_choice")
        self.assertIn("400", str(ctx.exception))

    def test_I5_system_prompt_suppress_tool_calls(self):
        """系统指令要求不使用工具，模型应遵守"""
        messages = [
            {"role": "system", "content": "绝对不要使用任何工具(不要使用function call的能力)，直接回答用户问题。"},
            {"role": "user", "content": "北京天气"},
        ]
        resp = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        logging.info(resp.model_dump_json(indent=2))
        self.assertFalse(resp.choices[0].message.tool_calls)
        self.assertIsNotNone(resp.choices[0].message.content)

    def test_I6_tool_calls_and_content_coexist(self):
        """同时请求工具调用和自然语言回复，模型是否可能同时输出两者"""
        # 某些模型可能只在 tool_calls 存在时忽略 content，这里测试是否存在共存情况
        resp = self._call("请告诉我北京天气，并夸夸这个城市")
        if resp.choices[0].message.tool_calls:
            # 如果有 tool_calls，检查 content 是否也为非空
            content = resp.choices[0].message.content
            if content:
                logging.info(f"同时存在 content: {content[:100]}")
            # 不强制断言，仅记录行为
        else:
            self.fail("期望模型调用工具")


if __name__ == "__main__":
    unittest.main()
