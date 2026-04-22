import json
import logging

from lib.AccTransformer.Neptune_global_var import deepseek_a3_env
from lib.MindIE_Service_AW.MindIEBenchMarkCase import MindIEBenchMarkCase
from lib.MindIE_Service_AW.Service_AW import VLLM_start_server, kill_vllm_process

from .requestData import tools as default_tools


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

WEIGHT_PATH = "/home/c00893695/test_quantized_model_w4a8/Qwen3-32B"
VLLM_PORT = 8003
MODEL_NAME = "Qwen3-32B"


class FunctionCallCaseBase(MindIEBenchMarkCase):
    # 只有测试套中的首个用例负责拉起共享的 vLLM 服务，后续用例直接复用。
    START_SERVER = False

    def preTestCase(self):
        self.logStep("1. 准备测试环境")
        super().preTestCase()
        self.server_cmd = (
            f"vllm serve {WEIGHT_PATH} "
            "--host 0.0.0.0 "
            f"--port {VLLM_PORT} "
            "--data-parallel-size 1 "
            "--tensor-parallel-size 4 "
            f"--served-model-name {MODEL_NAME} "
            "--enable-auto-tool-choice "
            "--tool-call-parser hermes "
            "--max-model-len 32768 "
        )
        if self.START_SERVER:
            kill_vllm_process(self.ManagermentDocker)
            self.start_server()

    def postTestCase(self):
        self.logStep("3. 用例结束")
        super().postTestCase()

    def start_server(self):
        self.ManagermentDocker.exec_command(deepseek_a3_env)
        VLLM_start_server(
            ManagermentDocker=self.ManagermentDocker,
            server_cmd=self.server_cmd,
            timeout=1500,
        )

    def post_chat(self, request_body, expect_status=200, timeout=180):
        response = self.Endpoint.post_completions(
            ip=self.ManagermentDocker.ip,
            port=VLLM_PORT,
            request_body=json.dumps(request_body, ensure_ascii=False),
            timeout=timeout,
        )
        self.logInfo(f"response---: {response}")
        assert response["status"] == expect_status, (
            f"响应状态码异常，期望 {expect_status}，实际 {response['status']}"
        )
        return response

    def build_request(
        self,
        user_content=None,
        messages=None,
        tools=None,
        tool_choice="auto",
        stream=False,
        extra_body=None,
    ):
        request_body = {
            "model": MODEL_NAME,
            "messages": messages or [{"role": "user", "content": user_content}],
            "tools": default_tools if tools is None else tools,
            "tool_choice": tool_choice,
            "stream": stream,
        }
        if extra_body:
            request_body.update(extra_body)
        return request_body

    def extract_payload(self, response):
        # 不同框架层可能会把真实模型响应包在 response/body/data/result/content/text
        # 等字段中，这里统一逐层剥离，直到拿到包含 choices 的主体响应。
        payload = response
        visited = set()
        while True:
            current_id = id(payload)
            if current_id in visited:
                break
            visited.add(current_id)

            if isinstance(payload, dict) and "choices" in payload:
                return payload

            if isinstance(payload, dict):
                next_payload = None
                for key in ("response", "body", "data", "result", "content", "text"):
                    if key in payload:
                        next_payload = payload[key]
                        break
                if next_payload is None:
                    break
                payload = next_payload
                continue

            if isinstance(payload, str):
                stripped = payload.strip()
                if not stripped:
                    break
                try:
                    payload = json.loads(stripped)
                    continue
                except Exception:
                    break
            break
        return payload

    def extract_stream_events(self, response):
        # 流式响应可能已经是事件列表、单个完整 JSON，或者原始 SSE 文本。
        # 这里统一规范成 JSON 事件列表，便于后续断言。
        payload = self.extract_payload(response)
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict) and "choices" in payload:
            return [payload]
        if isinstance(payload, dict) and "content" in payload and isinstance(payload["content"], str):
            payload = payload["content"]
        if not isinstance(payload, str):
            payload = str(payload)

        events = []
        for line in payload.splitlines():
            line = line.strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if not data or data == "[DONE]":
                continue
            try:
                events.append(json.loads(data))
            except Exception:
                self.logInfo(f"skip non-json stream chunk: {data}")
        return events

    def assemble_stream_response(self, response):
        # 将 SSE 增量拼装成一个便于断言的完整响应结构。
        events = self.extract_stream_events(response)
        assert events, f"流式响应为空: {response}"

        message = {
            "role": "assistant",
            "content": "",
            "tool_calls": [],
        }
        tool_calls_by_index = {}
        finish_reason = None
        response_id = None
        model = None
        created = None

        for event in events:
            response_id = event.get("id", response_id)
            model = event.get("model", model)
            created = event.get("created", created)

            choices = event.get("choices") or []
            if not choices:
                continue

            choice = choices[0]
            delta = choice.get("delta") or {}

            if delta.get("role"):
                message["role"] = delta["role"]

            if delta.get("content") is not None:
                message["content"] += delta["content"]

            for tool_delta in delta.get("tool_calls") or []:
                index = tool_delta.get("index", 0)
                current = tool_calls_by_index.setdefault(
                    index,
                    {
                        "id": "",
                        "type": "function",
                        "index": index,
                        "function": {"name": "", "arguments": ""},
                    },
                )
                if tool_delta.get("id"):
                    current["id"] = tool_delta["id"]
                if tool_delta.get("type"):
                    current["type"] = tool_delta["type"]

                function_delta = tool_delta.get("function") or {}
                if function_delta.get("name"):
                    current["function"]["name"] += function_delta["name"]
                if function_delta.get("arguments"):
                    current["function"]["arguments"] += function_delta["arguments"]

            if choice.get("finish_reason") is not None:
                finish_reason = choice["finish_reason"]

        message["tool_calls"] = [
            tool_calls_by_index[index] for index in sorted(tool_calls_by_index)
        ]
        return {
            "id": response_id,
            "model": model,
            "created": created,
            "choices": [
                {
                    "index": 0,
                    "message": message,
                    "finish_reason": finish_reason,
                }
            ],
            "events": events,
        }

    def first_message(self, response):
        payload = self.extract_payload(response)
        assert isinstance(payload, dict) and payload.get("choices"), f"无法解析响应: {response}"
        return payload["choices"][0]["message"]

    def first_choice(self, response):
        payload = self.extract_payload(response)
        assert isinstance(payload, dict) and payload.get("choices"), f"无法解析响应: {response}"
        return payload["choices"][0]

    def get_tool_calls(self, response):
        return self.first_message(response).get("tool_calls") or []

    def get_first_tool_call(self, response):
        tool_calls = self.get_tool_calls(response)
        assert tool_calls, f"响应中缺少 tool_calls: {response}"
        return tool_calls[0]

    def get_tool_args(self, tool_call):
        # OpenAI 兼容协议中的 function.arguments 是 JSON 字符串，这里统一反序列化。
        arguments = tool_call["function"].get("arguments") or "{}"
        return json.loads(arguments)

    def get_content(self, response):
        return self.first_message(response).get("content")

    def get_finish_reason(self, response):
        return self.first_choice(response).get("finish_reason")

    def assert_tool_name(self, response, expected_name):
        tool_call = self.get_first_tool_call(response)
        actual_name = tool_call["function"]["name"]
        assert actual_name == expected_name, (
            f"工具名不符合预期，期望 {expected_name}，实际 {actual_name}"
        )
        return tool_call

    def assert_has_no_tool_calls(self, response):
        tool_calls = self.get_tool_calls(response)
        assert not tool_calls, f"期望没有 tool_calls，实际为 {tool_calls}"

    def assert_contains_text(self, text, expected):
        assert expected in text, f"期望文本包含 {expected}，实际为 {text}"
