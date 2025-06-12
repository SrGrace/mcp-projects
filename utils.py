import os
from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_ibm import ChatWatsonx
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams


class ChatWatsonxWithRetry(ChatWatsonx):
    def invoke(self, *args, max_retries=3, **kwargs): 
        """
        Call the invoke method with retry mechanism.
        :param max_retries: Maximum number of retries if invoke fails.
        """
        attempt = 0
        while attempt < max_retries:
            try:
                return super().invoke(*args, **kwargs)
            except Exception as e:
                attempt += 1
                if attempt >= max_retries:
                    raise e  # Raise the last exception after max retries
                print(f"Invoke failed (attempt {attempt}/{max_retries}), retrying...")


def watsonx_chat_model(model_id="meta-llama/llama-3-3-70b-instruct", decoding_method='greedy', max_new_tokens=8192, 
                  min_new_tokens=1, temperature=0.5, top_k=50, top_p=1, repetition_penalty=1):
    params = {
        GenParams.DECODING_METHOD: decoding_method,
        GenParams.MIN_NEW_TOKENS: min_new_tokens,
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.RANDOM_SEED: 42,
        GenParams.TEMPERATURE: temperature,
        GenParams.TOP_K: top_k,
        GenParams.TOP_P: top_p,
        GenParams.REPETITION_PENALTY: repetition_penalty
    }
    ibm_cloud_url = os.getenv("IBM_CLOUD_URL", None)
    project_id = os.getenv("PROJECT_ID", None)
    api_key = os.getenv("API_KEY", None)
    watsonx_llm = ChatWatsonxWithRetry(
        model_id=model_id,
        url=ibm_cloud_url,
        apikey=api_key,
        project_id=project_id,
        params=params,
    )
    return watsonx_llm
