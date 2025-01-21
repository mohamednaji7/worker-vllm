FROM nvidia/cuda:12.1.0-base-ubuntu22.04

RUN apt-get update -y \
    && apt-get install -y python3-pip

RUN ldconfig /usr/local/cuda-12.1/compat/

# Install Python dependencies
COPY builder/requirements.txt /requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r /requirements.txt

# Install vLLM (switching back to pip installs since issues that required building fork are fixed and space optimization is not as important since caching) and FlashInfer 
RUN python3 -m pip install vllm==0.6.6.post1 && \
    python3 -m pip install flashinfer -i https://flashinfer.ai/whl/cu121/torch2.3



ENV BASE_PATH="/runpod-volume" \
    HF_DATASETS_CACHE="/runpod-volume/huggingface-cache/datasets" \
    HUGGINGFACE_HUB_CACHE="/runpod-volume/huggingface-cache/hub" \
    HF_HOME="/runpod-volume/huggingface-cache/hub" \
    HF_HUB_ENABLE_HF_TRANSFER=1 
    
# LLM 
# ## Tokiner Settings 
# ENV TOKENIZER_NAME="your-tokenizer"
# ENV TOKENIZER_REVISION="your-tokenizer-revision"

## Model Settings
ENV MODEL_NAME="Commercer/Llama-3.1-8B-Instruct-Tuned-not-4bit-Content-Creator"
# ENV MODEL_REVISION="your-revision"

## LoRA Settings
ENV ENABLE_LORA = true
ENV MAX_LORA_RANK = 64

## Weights Settings
ENV TRUST_REMOTE_CODE=true \
    LOAD_FORMAT="bitsandbytes" \
    MAX_MODEL_LEN=512 \
    QUANTIZATION="bitsandbytes"
ENV DTYPE="bfloat16"


# ENV MODEL_REVISION="your-revision"
# ENV TOKENIZER_NAME="your-tokenizer"
# ENV TOKENIZER_REVISION="your-tokenizer-revision"

ENV PYTHONPATH="/:/vllm-workspace"


COPY src /src

# Start the handler
CMD ["python3", "/src/handler.py"]