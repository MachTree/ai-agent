import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERATIONS

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Gemini API key could not be loaded.")
    

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )

            if not response.usage_metadata:
                raise RuntimeError("Gemini API response failure: missing metadata.")
            
            if args.verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            results = []
            if response.function_calls:
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call, args.verbose)
                    if (
                        not function_call_result.parts
                        or not function_call_result.parts[0].function_response
                        or not function_call_result.parts[0].function_response.response
                    ):
                        raise RuntimeError(f"Function response is None for {function_call.name}({function_call.args})")
                    results.append(function_call_result.parts[0])
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(types.Content(role="user", parts=results))
            else:
                print(f"Response:\n{response.text}")
                break
        except Exception as ex:
            print(f"Error in model call processing: {ex}")

    else:
        print(f"Gemini was not able to produce a final response in the permitted number of iterations ({MAX_ITERATIONS})")
        exit(1)


if __name__ == "__main__":
    main()
