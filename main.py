import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from openrouter import OpenRouter


def main():
    # print("Hello from ai-agent!")
    load_dotenv()

    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if gemini_api_key == None:
        raise RuntimeError(
            "Gemini API key not found. Please add key to your .env file."
        )

    openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
    if openrouter_api_key == None:
        raise RuntimeError(
            "OpenRouter API key not found. Please add key to your .env file."
        )

    llm_model = os.environ.get("LLM_MODEL")
    if llm_model == None:
        llm_model = "google/gemini-2.5-flash"

    base_url = os.environ.get("OPENROUTER_BASE_URL")
    if base_url == None:
        base_url = "https://openrouter.ai/api/v1"

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose output with user prompt and token usage",
    )
    args = parser.parse_args()

    def use_genai_sdk():
        client = genai.Client(api_key=gemini_api_key)
        messages = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
        ]
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=messages
        )

        prompt_token_count = 0
        response_token_count = 0

        if response.usage_metadata != None:
            prompt_token_count = response.usage_metadata.prompt_token_count
            response_token_count = response.usage_metadata.candidates_token_count

        return prompt_token_count, response_token_count, response.text

    def use_openrouter_sdk():
        client = OpenRouter(api_key=openrouter_api_key)
        messages = [{"role": "user", "content": args.user_prompt}]
        response = client.chat.send(model=llm_model, messages=messages)

        prompt_token_count = 0
        response_token_count = 0

        if response.usage != None:
            prompt_token_count = response.usage.prompt_tokens
            response_token_count = response.usage.completion_tokens

        return (
            prompt_token_count,
            response_token_count,
            response.choices[0].message.content,
        )

    def generate_response(sdk="openrouter"):
        if sdk == "openrouter":
            return use_openrouter_sdk()

        return use_genai_sdk()

    prompt_token_count, response_token_count, response_text = generate_response()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {response_token_count}")
    print("Response:")
    print(response_text)


if __name__ == "__main__":
    main()
