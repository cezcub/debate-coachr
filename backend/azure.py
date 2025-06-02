import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../.env', override=True)  # Override system env vars with .env file values
    
def call_ai(sys_prompt, user_prompt):
    # Get Azure OpenAI credentials from environment variables
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    
    if not api_key or not endpoint:
        raise ValueError("Azure OpenAI credentials not found. Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT environment variables.")
    
    client = AzureOpenAI(
        api_key=api_key,  
        api_version="2024-12-01-preview",
        azure_endpoint=endpoint
        )
    try:
        completion = client.chat.completions.create(
            model='gpt-4.1',
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Enhanced error handling for Azure OpenAI connection issues
        error_msg = str(e)
        if "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower():
            raise ValueError("Azure OpenAI authentication failed. Please check your API key.")
        elif "not found" in error_msg.lower() or "404" in error_msg:
            raise ValueError("Azure OpenAI endpoint not found. Please check your endpoint URL.")
        elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            raise ValueError("Connection to Azure OpenAI failed. Please check your internet connection and endpoint URL.")
        else:
            raise ValueError(f"Azure OpenAI API error: {error_msg}")

def pf_feedback(resolution, transcription):
    prompt = resolution
    return call_ai(prompt, transcription)

def case_feedback(resolution, case):
    prompt = f'You are a public forum debate coach. Your job is to analyze cases provided of high school public forum debate and provide detailed feedback on how it could be improved. The resolution being debated in this round is {resolution} Give as much feedback (4-5 pieces of feedback per contention at MINIMUM) as possible on the content and strategy of the case. Make sure to analyze the uniqueness, link, internal link, and impact of each and every contention. Remember that the case will be delivered in a 4 minute speech.'
    return call_ai(prompt, case)