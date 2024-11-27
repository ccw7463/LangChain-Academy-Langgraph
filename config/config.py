from ml_collections import ConfigDict


UsedConfig = ConfigDict()
UsedConfig.MODEL = "Qwen/Qwen2.5-72B-Instruct"
UsedConfig.TOKENIZER = "Qwen/Qwen2.5-72B-Instruct"

IPConfig = ConfigDict()
IPConfig.H100_DGX = "http://192.168.1.20"
IPConfig.A100_DGX = "http://192.168.1.21"
IPConfig.H100_CLOUD_3 = "http://192.168.0.70"
IPConfig.REDIS = IPConfig.H100_DGX.replace("http://","redis://")

PortConfig = ConfigDict()
PortConfig.MODEL = "1330"
PortConfig.REDIS = "6379/0"
PortConfig.EMBEDDING = "11180"

ModelConfig = ConfigDict()
ModelConfig.TOP_K = 1
ModelConfig.TOP_P = 0.001
ModelConfig.TEMPERATURE = 0.001
ModelConfig.MAX_NEW_TOKENS = 4096
ModelConfig.REPETATION_PENALTY = 1.03

HFConfig = ConfigDict()
HFConfig.HF_API_TOKEN = "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"

URLConfig = ConfigDict()
URLConfig.MODEL_URL = f"{IPConfig.H100_DGX}:{PortConfig.MODEL}"
URLConfig.REDIS_URL = f"{IPConfig.REDIS}:{PortConfig.REDIS}"