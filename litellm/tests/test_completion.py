import sys, os
import traceback
from dotenv import load_dotenv

load_dotenv()
import os

sys.path.insert(
    0, os.path.abspath("../..")
)  # Adds the parent directory to the system path
import pytest
import litellm
from litellm import embedding, completion, text_completion

litellm.vertex_project = "pathrise-convert-1606954137718"
litellm.vertex_location = "us-central1"
litellm.use_client = True
# from infisical import InfisicalClient

# litellm.set_verbose = True
# litellm.secret_manager_client = InfisicalClient(token=os.environ["INFISICAL_TOKEN"])

user_message = "Write a short poem about the sky"
messages = [{"content": user_message, "role": "user"}]


def logger_fn(user_model_dict):
    print(f"user_model_dict: {user_model_dict}")


def test_completion_custom_provider_model_name():
    try:
        response = completion(
            model="together_ai/togethercomputer/llama-2-70b-chat",
            messages=messages,
            logger_fn=logger_fn,
        )
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


# test_completion_custom_provider_model_name()


def test_completion_claude():
    try:
        response = completion(
            model="claude-instant-1", messages=messages, logger_fn=logger_fn
        )
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

# aleph alpha
# def test_completion_aleph_alpha():
#     try:
#         response = completion(
#             model="luminous-base", messages=messages, logger_fn=logger_fn
#         )
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")
# test_completion_aleph_alpha()


# def test_completion_aleph_alpha_control_models():
#     try:
#         response = completion(
#             model="luminous-base-control", messages=messages, logger_fn=logger_fn
#         )
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")
# test_completion_aleph_alpha_control_models()

def test_completion_with_litellm_call_id():
    try:
        litellm.use_client = False
        response = completion(
            model="gpt-3.5-turbo", messages=messages)
        print(response)
        if 'litellm_call_id' in response:
            pytest.fail(f"Error occurred: litellm_call_id in response objects")
        
        litellm.use_client = True
        response2 = completion(
            model="gpt-3.5-turbo", messages=messages)
        
        if 'litellm_call_id' not in response2:
            pytest.fail(f"Error occurred: litellm_call_id not in response object when use_client = True")
        # Add any assertions here to check the response
        print(response2)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_claude_stream():
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "how does a court case get to the Supreme Court?",
            },
        ]
        response = completion(model="claude-2", messages=messages, stream=True)
        # Add any assertions here to check the response
        for chunk in response:
            print(chunk["choices"][0]["delta"])  # same as openai format
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")



# def test_completion_hf_api():
#     try:
#         user_message = "write some code to find the sum of two numbers"
#         messages = [{ "content": user_message,"role": "user"}]
#         response = completion(model="stabilityai/stablecode-completion-alpha-3b-4k", messages=messages, custom_llm_provider="huggingface", logger_fn=logger_fn)
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         if "loading" in str(e):
#             pass
#         pytest.fail(f"Error occurred: {e}")

# test_completion_hf_api()

# def test_completion_hf_deployed_api():
#     try:
#         user_message = "There's a llama in my garden 😱 What should I do?"
#         messages = [{ "content": user_message,"role": "user"}]
#         response = completion(model="huggingface/https://ji16r2iys9a8rjk2.us-east-1.aws.endpoints.huggingface.cloud", messages=messages, logger_fn=logger_fn)
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")


# def test_completion_cohere(): # commenting for now as the cohere endpoint is being flaky
#     try:
#         response = completion(
#             model="command-nightly",
#             messages=messages,
#             max_tokens=100,
#             logit_bias={40: 10},
#         )
#         # Add any assertions here to check the response
#         print(response)
#         response_str = response["choices"][0]["message"]["content"]
#         print(f"str response{response_str}")
#         response_str_2 = response.choices[0].message.content
#         if type(response_str) != str:
#             pytest.fail(f"Error occurred: {e}")
#         if type(response_str_2) != str:
#             pytest.fail(f"Error occurred: {e}")
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")


def test_completion_cohere_stream():
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "how does a court case get to the Supreme Court?",
            },
        ]
        response = completion(
            model="command-nightly", messages=messages, stream=True, max_tokens=50
        )
        # Add any assertions here to check the response
        for chunk in response:
            print(chunk["choices"][0]["delta"])  # same as openai format
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_openai():
    try:
        response = completion(model="gpt-3.5-turbo", messages=messages)

        response_str = response["choices"][0]["message"]["content"]
        response_str_2 = response.choices[0].message.content
        assert response_str == response_str_2
        assert type(response_str) == str
        assert len(response_str) > 1
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_openai_prompt():
    try:
        response = text_completion(
            model="gpt-3.5-turbo", prompt="What's the weather in SF?"
        )
        response_str = response["choices"][0]["message"]["content"]
        response_str_2 = response.choices[0].message.content
        print(response)
        assert response_str == response_str_2
        assert type(response_str) == str
        assert len(response_str) > 1
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_text_openai():
    try:
        response = completion(model="text-davinci-003", messages=messages)
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_openai_with_optional_params():
    try:
        response = completion(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5,
            top_p=0.1,
            user="ishaan_dev@berri.ai",
        )
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

# commented out for now, as openrouter is quite flaky - causing our deployments to fail. Please run this before pushing changes.
# def test_completion_openrouter():
#     try:
#         response = completion(
#             model="google/palm-2-chat-bison",
#             messages=messages,
#             temperature=0.5,
#             top_p=0.1,
#         )
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")

def test_completion_openai_with_more_optional_params():
    try:
        response = completion(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5,
            top_p=0.1,
            n=2,
            max_tokens=150,
            presence_penalty=0.5,
            frequency_penalty=-0.5,
            logit_bias={123: 5},
            user="ishaan_dev@berri.ai",
        )
        # Add any assertions here to check the response
        print(response)
        response_str = response["choices"][0]["message"]["content"]
        response_str_2 = response.choices[0].message.content
        print(response["choices"][0]["message"]["content"])
        print(response.choices[0].message.content)
        if type(response_str) != str:
            pytest.fail(f"Error occurred: {e}")
        if type(response_str_2) != str:
            pytest.fail(f"Error occurred: {e}")
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_openai_with_stream():
    try:
        response = completion(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5,
            top_p=0.1,
            n=2,
            max_tokens=150,
            presence_penalty=0.5,
            stream=True,
            frequency_penalty=-0.5,
            logit_bias={27000: 5},
            user="ishaan_dev@berri.ai",
        )
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_openai_with_functions():
    function1 = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    try:
        response = completion(
            model="gpt-3.5-turbo", messages=messages, functions=function1
        )
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_azure():
    try:
        print("azure gpt-3.5 test\n\n")
        response = completion(
            model="azure/chatgpt-v-2",
            messages=messages,
        )
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


def test_completion_azure_deployment_id():
    try:
        response = completion(
            deployment_id="chatgpt-v-2",
            model="gpt-3.5-turbo",
            messages=messages,
        )
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

# # Replicate API endpoints are unstable -> throw random CUDA errors -> this means our tests can fail even if our tests weren't incorrect.
# def test_completion_replicate_llama_stream():
#     model_name = "replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1"
#     try:
#         response = completion(model=model_name, messages=messages, stream=True)
#         # Add any assertions here to check the response
#         for result in response:
#             print(result)
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")


# def test_completion_replicate_stability_stream():
#     model_name = "stability-ai/stablelm-tuned-alpha-7b:c49dae362cbaecd2ceabb5bd34fdb68413c4ff775111fea065d259d577757beb"
#     try:
#         response = completion(
#             model=model_name,
#             messages=messages,
#             stream=True,
#             custom_llm_provider="replicate",
#         )
#         # Add any assertions here to check the response
#         for chunk in response:
#             print(chunk["choices"][0]["delta"])
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")


def test_completion_replicate_llama_2():
    model_name = "replicate/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf"
    try:
        response = completion(
            model=model_name, messages=messages, custom_llm_provider="replicate"
        )
        print(response)
        # Add any assertions here to check the response
        response_str = response["choices"][0]["message"]["content"]
        print(response_str)
        if type(response_str) != str:
            pytest.fail(f"Error occurred: {e}")
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

# test_completion_replicate_llama_2()


######## Test TogetherAI ########
def test_completion_together_ai():
    model_name = "togethercomputer/llama-2-70b-chat"
    try:
        response = completion(model=model_name, messages=messages, max_tokens=256, logger_fn=logger_fn)
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


# def test_customprompt_together_ai():
#     try:
#         litellm.register_prompt_template(
#             model="OpenAssistant/llama2-70b-oasst-sft-v10",
#             roles={"system":"<|im_start|>system", "assistant":"<|im_start|>assistant", "user":"<|im_start|>user"}, # tell LiteLLM how you want to map the openai messages to this model
#             pre_message_sep= "\n",
#             post_message_sep= "\n"
#         )
#         response = completion(model="together_ai/OpenAssistant/llama2-70b-oasst-sft-v10", messages=messages)
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")

def test_completion_sagemaker():
    try:
        response = completion(
            model="sagemaker/jumpstart-dft-meta-textgeneration-llama-2-7b", 
            messages=messages,
            temperature=0.2,
            max_tokens=80,
        )
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")


# def test_completion_custom_api_base():
#     try:
#         response = completion(
#             model="custom/meta-llama/Llama-2-13b-hf", 
#             messages=messages,
#             temperature=0.2,
#             max_tokens=10,
#             api_base="https://api.autoai.dev/inference",
#             request_timeout=300,
#         )
#         # Add any assertions here to check the response
#         print("got response\n", response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")

# test_completion_custom_api_base()

# def test_vertex_ai():
#     model_name = "chat-bison"
#     try:
#         response = completion(model=model_name, messages=messages, logger_fn=logger_fn)
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")

# def test_petals():
#     model_name = "stabilityai/StableBeluga2"
#     try:
#         response = completion(
#             model=model_name,
#             messages=messages,
#             custom_llm_provider="petals",
#             force_timeout=120,
#         )
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")



def test_completion_with_fallbacks():
    fallbacks = ["gpt-3.5-turb", "gpt-3.5-turbo", "command-nightly"]
    try:
        response = completion(
            model="bad-model", messages=messages, force_timeout=120, fallbacks=fallbacks
        )
        # Add any assertions here to check the response
        print(response)
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

# def test_baseten():
#     try:

#         response = completion(model="baseten/RqgAEn0", messages=messages, logger_fn=logger_fn)
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")

# def test_baseten_falcon_7bcompletion():
#     model_name = "qvv0xeq"
#     try:
#         response = completion(model=model_name, messages=messages, custom_llm_provider="baseten")
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")
# test_baseten_falcon_7bcompletion()

# def test_baseten_falcon_7bcompletion_withbase():
#     model_name = "qvv0xeq"
#     litellm.api_base = "https://app.baseten.co"
#     try:
#         response = completion(model=model_name, messages=messages)
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")
#     litellm.api_base = None

# test_baseten_falcon_7bcompletion_withbase()


# def test_baseten_wizardLMcompletion_withbase():
#     model_name = "q841o8w"
#     litellm.api_base = "https://app.baseten.co"
#     try:
#         response = completion(model=model_name, messages=messages)
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")

# test_baseten_wizardLMcompletion_withbase()

# def test_baseten_mosaic_ML_completion_withbase():
#     model_name = "31dxrj3"
#     litellm.api_base = "https://app.baseten.co"
#     try:
#         response = completion(model=model_name, messages=messages)
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")


#### Test A121 ###################
# def test_completion_ai21():
#     model_name = "j2-light"
#     try:
#         response = completion(model=model_name, messages=messages)
#         # Add any assertions here to check the response
#         print(response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")

# test config file with completion #
# def test_completion_openai_config():
#     try:
#         litellm.config_path = "../config.json"
#         litellm.set_verbose = True
#         response = litellm.config_completion(messages=messages)
#         # Add any assertions here to check the response
#         print(response)
#         litellm.config_path = None
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")


# import asyncio
# def test_completion_together_ai_stream():
#     user_message = "Write 1pg about YC & litellm"
#     messages = [{ "content": user_message,"role": "user"}]
#     try:
#         response = completion(model="togethercomputer/llama-2-70b-chat", messages=messages, stream=True, max_tokens=800)
#         print(response)
#         asyncio.run(get_response(response))
#         # print(string_response)
#     except Exception as e:
#         pytest.fail(f"Error occurred: {e}")


# async def get_response(generator):
#     async for elem in generator:
#         print(elem)
#     return

# test_completion_together_ai_stream()
