import os
import sys
import string
import config
from config import available_functions, system_prompt
from functions.call_function import call_function
from dotenv import load_dotenv
from google import genai

from google.genai import types

def main():
    load_dotenv()

    if len(sys.argv) < 2:
        print("You have to provide an argument for this function to work.")
        sys.exit(1)
    
    args = sys.argv[1:]
    if len(args) == 0:
        print("You can't prompt nothing, your message needs a minimum lenght.")
        sys.exit(1)

    flags = []
    text = []
    for arg in args:
        if arg.startswith("--"):
            flags.append(arg)
        else:
            text.append(arg)
    
    prompt = " ".join(text)

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    i = 0
    while i < 20:
        i += 1

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        prompt_token = response.usage_metadata.prompt_token_count
        response_token = response.usage_metadata.candidates_token_count

        
        if "--verbose" in flags:
            print(f"User prompt: {prompt}\nPrompt tokens: {prompt_token}\nResponse tokens: {response_token}\n")

        if response.function_calls:
            for function_call_part in response.function_calls:
                try:
                    function_call_result = call_function(function_call_part, verbose=("--verbose" in flags))
                    messages.append(function_call_result)
                    response_dict = function_call_result.parts[0].function_response.response
                    if "--verbose" in flags:
                        print(f"-> {response_dict}")
                    if "result" in response_dict:
                        print(response_dict["result"])
                    elif "error" in response_dict:
                        print(response_dict["error"])
                except Exception as e:
                    types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=getattr(function_call_part, 'name', 'unknown'),
                                response={"error": f"Fatal error: {e}"},
                            )
                        ],
                    )
                    print(f"error: Fatal error: {e}")
                
        else:
            print(response.text)
            break

if __name__ == "__main__":
    main()
