import os
import runpod


# Environment variable to control dummy mode
TEMPLATE_HANDLER = os.getenv("TEMPLATE_HANDLER", "false").lower() == "true"

if TEMPLATE_HANDLER:
    # Example handler file. 

    def handler(job):
        """ Handler function that will be used to process jobs. """
        job_input = job['input']

        name = job_input.get('name', 'World')

        return f"Hello, {name}!"


    runpod.serverless.start({"handler": handler})
else:
    from utils import JobInput
    from engine import vLLMEngine, OpenAIvLLMEngine

    vllm_engine = vLLMEngine()
    OpenAIvLLMEngine = OpenAIvLLMEngine(vllm_engine)

    async def handler(job):
        job_input = JobInput(job["input"])
        engine = OpenAIvLLMEngine if job_input.openai_route else vllm_engine
        results_generator = engine.generate(job_input)
        async for batch in results_generator:
            yield batch

    runpod.serverless.start(
        {
            "handler": handler,
            "concurrency_modifier": lambda x: vllm_engine.max_concurrency,
            "return_aggregate_stream": True,
        }
    )