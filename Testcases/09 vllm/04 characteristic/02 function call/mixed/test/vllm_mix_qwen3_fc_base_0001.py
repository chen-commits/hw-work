import json
from lib.MindIE_Service_AW.MindIEBenchMarkCase import MindIEBenchMarkCase
from lib.AccTransformer.Neptune_global_var import dataset_vllm_path, deepseek_a3_env
from lib.MindIE_Service_AW.Service_AW import kill_vllm_process, VLLM_start_server

weight_path_DeepSeek_R1_0528_w8a8_mtpmix_rot = "/home/c00893695/test_quantized_model_w4a8/Qwen3-32B"
VLLM_port = 8003
model_name = "Qwen3-32B"


# vllm_mix_qwen3_fc_base_0001
class vllm_mix_qwen3_fc_base_0001(MindIEBenchMarkCase):
    """
    CaseNumber:
        vllm_mix_qwen3_fc_base_0001
    RunLevel:
        Level 1
    EnvType:
        None
    CaseName:
        测试混部DeepSeek-r1带functioncall功能_01
    PreCondition:
        1. 准备好800I A3环境，DeepSeek-r1-w8a8-0528-旋转矩阵-mtp量化权重
    TestStep:
        1. 根据特性叠加配置：最佳性能场景叠加，拉起服务，有预期结果1
        2. 发送单条functioncall请求，有预期结果2
    ExpectedResult:
        1. 服务拉起成功
        2. 流式与非流式均返回正常
    Design Description:
        None
    Author:
        w60043782
    """

    def preTestCase(self):
        self.logStep('1.前置条件，进入容器')
        super().preTestCase()

        self.sever_cmd = (
            f"vllm serve {weight_path_DeepSeek_R1_0528_w8a8_mtpmix_rot} "
            "--host 0.0.0.0 "
            f"--port {VLLM_port} "
            "--data-parallel-size 1 "
            "--tensor-parallel-size 4 "
            f"--served-model-name {model_name} "
            "--enable-auto-tool-choice "
            "--tool-call-parser hermes "
            "--max-model-len 32768 "
        )
        kill_vllm_process(self.ManagermentDocker)

    def procedure(self):
        self.logStep('2.测试步骤')
        self.logStep('2.1 设置环境变量拉起服务')
        self.ManagermentDocker.exec_command(deepseek_a3_env)
        VLLM_start_server(ManagermentDocker=self.ManagermentDocker, server_cmd=self.sever_cmd, timeout=1500)

        from .requestData import tools
        self.logStep('2.2 发送推理请求')
        messages = [{"role": "user", "content": "现在几点了"}]
        request_body = {
            "model": model_name,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "stream": False,
        }

        # request_body['stream'] = s
        response = self.Endpoint.post_completions(ip=self.ManagermentDocker.ip, port=VLLM_port,
                                                  request_body=json.dumps(request_body),
                                                  timeout=180)
        self.logInfo(f'response---: {response}')

        assert response["status"] == 200, f'推理请求发送失败，失败原因为{response["status"]}'

        request_body["stream"] = True
        stream_resp = self.Endpoint.post_completions(ip=self.ManagermentDocker.ip, port=VLLM_port,
                                                     request_body=json.dumps(request_body),
                                                     timeout=180)
        self.logInfo(f'stream response---: {stream_resp}')
        assert response["status"] == 200, f'推理请求发送失败，失败原因为{response["status"]}'


    def postTestCase(self):
        self.logStep('3.恢复环境')
        super().postTestCase()
