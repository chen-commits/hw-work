## self.Endpoint.post_completions方法流式相应示例

{'status': 200,
 'content': 'data: {"id":"chatcmpl-89d2f8cbe75e7fc9","object":"chat.completion.chunk","created":1776847823,"model":"Qwen3-32B","choices":[{"index":0,"delta":{"role":"assistant","content":""},"logprobs":null,"finish_reason":null}],"prompt_token_ids":null}\n\ndata: {"id":"chatcmpl-89d2f8cbe75e7fc9","object":"chat.completion.chunk","created":1776847823,"model":"Qwen3-32B","choices":[{"index":0,"delta":{"content":"<think>"},"logprobs":null,"finish_reason":null,"token_ids":null}]}\n\ndata: [DONE]\n\n'}


命名体系：

boot_*：启动相关
call_*：基础调用命中
loop_* / turn_*：闭环与多轮
mode_*：模式与控制项
stream_*：流式
schema_*：协议/schema 异常
catalog_*：工具集规模与重名
policy_*：系统策略抑制
observe_*：行为观察类
protocol_*：协议字段校验
force_*：强制指定函数