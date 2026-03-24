from langchain_huggingface.llms import HuggingFacePipeline

# Modelo usado pelo agente
MODEL_ID = "distilgpt2"


def get_llm():
    # config do modelo
    return HuggingFacePipeline.from_model_id(
        model_id=MODEL_ID,
        task="text-generation",
        pipeline_kwargs={
            "max_new_tokens": 200,
            "do_sample": True,
            "temperature": 0.6,
            "return_full_text": False,
            "max_length": None,
        },
        device=-1,
    )
