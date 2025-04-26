import base64
import os
from enum import Enum
from io import BytesIO
from textwrap import dedent
from typing import Optional, Union

import requests
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
from pydantic import BaseModel


class OpenaiModelNames(Enum):
    gpt4o_mini = "gpt-4o-mini"


FoundationModelNames = Union[OpenaiModelNames]

load_dotenv()


# TODO: Make two classes SyncClient and AsyncClient like OAI
class LLMResponse(BaseModel):
    content: str
    llm_costs: float


def get_llm_completion(system_prompt: str, user_prompt: str, model: FoundationModelNames, image_url=None, timeout=60):
    system_prompt = dedent(system_prompt)
    user_prompt = dedent(user_prompt)
    if isinstance(model, OpenaiModelNames):
        return _get_openai_completion(system_prompt, user_prompt, model, image_url, timeout)
    else:
        raise NotImplementedError(f"Model {model} not supported")


def get_llm_structured_response(system_prompt, user_prompt, schema: BaseModel, model: FoundationModelNames, image_url=None, timeout=60):
    if isinstance(model, OpenaiModelNames):
        return _get_openai_structured_response(system_prompt, user_prompt, schema, model, image_url, timeout)
    else:
        raise NotImplementedError(f"Model {model} not supported")


def _get_openai_completion(system_prompt, user_prompt, model: OpenaiModelNames, image_url: Optional[str] = None, timeout: int = 60) -> LLMResponse:
    # Only expected to be invoked by get_llm_completion
    assert isinstance(model, OpenaiModelNames), f"Model {model} not supported"
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if image_url:
        if os.path.isfile(image_url):
            image = Image.open(image_url)
        else:
            image = download_image(image_url)

        base_64_image = resize_and_encode_image(image, 512, 512)
        response = client.chat.completions.create(
            model=model.value,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": system_prompt + user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_64_image}"}},
                    ],
                }
            ],
            timeout=timeout,
        )
    else:
        response = client.chat.completions.create(
            model=model.value,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=timeout,
        )

    llm_costs = compute_llm_cost(response, model)
    return LLMResponse(content=response.choices[0].message.content, llm_costs=llm_costs)


def _get_openai_structured_response(system_prompt, user_prompt, schema: BaseModel, model: OpenaiModelNames, image_url, timeout) -> LLMResponse:
    # Only expected to be invoked by get_llm_completion
    assert isinstance(model, OpenaiModelNames), f"Model {model} not supported"
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if image_url:
        base_64_image = resize_and_encode_image(image_url, 512, 512)  # Resize image to 512x512 for cheaper input tokens
        response = client.beta.chat.completions.parse(
            model=model.value,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": system_prompt + user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_64_image}"}},
                    ],
                }
            ],
            response_format=schema,
            timeout=timeout,
        )
    else:
        response = client.beta.chat.completions.parse(
            model=model.value,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=schema,
            timeout=timeout,
        )

    llm_costs = compute_llm_cost(response, model)
    return LLMResponse(content=response.choices[0].message.content, llm_costs=llm_costs)


def compute_llm_cost(response, model: FoundationModelNames):
    if model == OpenaiModelNames.gpt4o_mini:
        prompt_price = 0.15 / 1e6
        prompt_tokens = response.usage.prompt_tokens
        completion_price = 0.6 / 1e6
        completion_tokens = response.usage.completion_tokens
        return prompt_price * prompt_tokens + completion_price * completion_tokens
    else:
        raise NotImplementedError(f"Model {model} not supported")


def download_image(image_url: str) -> str:
    """
    Downloads an image from the provided URL, resizes it, and converts it to Base64.

    :param image_url: URL of the image to download
    :param width: Desired width of the resized image
    :param height: Desired height of the resized image
    :return: Base64-encoded string of the processed image
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }

        # Download the image
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()

        # Open the image
        image = Image.open(BytesIO(response.content))

        return image
    except Exception as e:
        raise RuntimeError(f"Failed to process image from URL {image_url}: {e}")


def resize_and_encode_image(image: Image, width: int, height: int):
    try:
        # Resize the image
        image = image.resize((width, height))

        # Save image to a buffer in PNG format
        buffered = BytesIO()
        image.save(buffered, format="PNG")

        # Convert to Base64
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return base64_image
    except Exception as e:
        raise RuntimeError(f"Failed to process image: {e}")
