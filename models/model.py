from config.config import UsedConfig, HFConfig, URLConfig, ModelConfig
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

LLM = ChatHuggingFace(
    llm=HuggingFaceEndpoint(
    endpoint_url=URLConfig.MODEL_URL,
    huggingfacehub_api_token=HFConfig.HF_API_TOKEN,
    max_new_tokens=ModelConfig.MAX_NEW_TOKENS,
    top_k=ModelConfig.TOP_K,
    top_p=ModelConfig.TOP_P,
    temperature=ModelConfig.TEMPERATURE,
    repetition_penalty=ModelConfig.REPETATION_PENALTY,
    model_kwargs={},
    stop_sequences=["<|im_end|>"]
    ),
    model_id=UsedConfig.MODEL
)