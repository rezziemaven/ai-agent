import argparse
import os

from dotenv import load_dotenv
from google import genai


def main():
    # print("Hello from ai-agent!")
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Key not found. Please add key to your .env file.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=args.user_prompt
    )

    prompt_token_count = 0
    response_token_count = 0

    if response.usage_metadata != None:
        prompt_token_count = response.usage_metadata.prompt_token_count
        response_token_count = response.usage_metadata.candidates_token_count

    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {response_token_count}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
