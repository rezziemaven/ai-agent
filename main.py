import argparse
import os

from dotenv import load_dotenv

from sdks.genai import use_genai_sdk
from sdks.ollama import use_ollama_sdk


def main():
    load_dotenv()

    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if gemini_api_key == None:
        raise RuntimeError(
            "Gemini API key not found. Please add key to your .env file."
        )

    ollama_api_key = os.environ.get("OLLAMA_API_KEY")
    if ollama_api_key == None:
        print(
            "Ollama API key not found but optional. Please add key to your .env file for cloud model usage."
        )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, nargs="?", help="User prompt")
    parser.add_argument(
        "-s",
        "--sdk",
        type=str,
        default="ollama",
        help="SDK to use to generate response")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose output with user prompt, function calls and arguments and token usage",
    )
    args = parser.parse_args()

    if not args.user_prompt:
        print("Noodle: AI Coding Agent")
        print('Usage: uv run main.py "<user_prompt>" [-s | --sdk=sdk-name] [--verbose]')
        print('Example: uv run main.py "Why is the sky blue?"')
        return

    available_sdks = ["genai", "ollama"]

    if args.sdk not in available_sdks:
        print("Error: SDK not recognised. Please check the Usage section of README.md for acceptable SDK values.")
        return

    def generate_response(sdk="ollama"):
        if sdk == "genai":
            return use_genai_sdk(gemini_api_key, args.user_prompt, verbose=args.verbose)

        # Add any additional SDKs here

        return use_ollama_sdk(args.user_prompt, args.verbose)

    prompt_token_count, response_token_count, response_text, function_calls = (
        generate_response(args.sdk)
    )

    if len(function_calls) == 0:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_token_count}")
            print(f"Response tokens: {response_token_count}")
        print("Final response:")
        print(response_text)


if __name__ == "__main__":
    main()
