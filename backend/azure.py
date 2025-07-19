import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
# Use absolute path to ensure it works regardless of working directory
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path, override=True)  # Override system env vars with .env file values
    
def call_ai(messages):
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
        # Validate messages format before sending
        validated_messages = []
        for i, m in enumerate(messages):
            if not isinstance(m.get("content"), str):
                content = str(m.get("content")) if m.get("content") is not None else ""
            else:
                content = m.get("content")
            
            validated_messages.append({
                "role": m["role"], 
                "content": content
            })
        
        completion = client.chat.completions.create(
            model='gpt-4.1',
            messages=validated_messages
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

def pf_feedback(resolution, transcription, side):
    prompt = f'You are a public forum debate coach. Your job is to analyze round recordings provided of high school public forum debate and provide detailed feedback on how it went and how to improve. The resolution being debated in this round is {resolution} Give as much feedback (4-5 pieces of feedback per speech at MINIMUM) as possible on the content and strategy of the round. The team you should focus on analyzing and giving feedback to is on the {side} side of the resolution. Explain which team you would have voted for, explain why, and explain how the team requiring feedback could improve.'
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": transcription}]
    return call_ai(messages)

def case_feedback(resolution, case, side, upload_format="plaintext"):
    # Ensure case is a string
    if not isinstance(case, str):
        if hasattr(case, '__str__'):
            case = str(case)
        else:
            case = "Error: Invalid case format provided"
    
    if upload_format == "card format":
        prompt = f'You are a public forum debate coach. Your job is to analyze structured debate cards provided of high school public forum debate and provide detailed feedback on how they could be improved. The resolution being debated is {resolution}. Give detailed feedback (4-5 pieces of feedback per card at MINIMUM) on the content, evidence quality, and strategic value of each card. The team you are analyzing is debating the {side} side of the resolution. Focus on analyzing the warrant, evidence credibility, impact, and how well each card supports the overall argument structure. Consider how these cards would work in a 4 minute constructive speech and provide suggestions for card organization and presentation. Be warned; the text will likely appear as an incoherent jumble, but in reality it is a case of cards with citations deleted'
    else:
        prompt = f'You are a public forum debate coach. Your job is to analyze cases provided of high school public forum debate and provide detailed feedback on how it could be improved. The resolution being debated in this round is {resolution} Give as much feedback (4-5 pieces of feedback per contention at MINIMUM) as possible on the content and strategy of the case. The team you are analyzing is debating the {side} side of the resolution. Make sure to analyze the uniqueness, link, internal link, and impact of each and every contention. Remember that the case will be delivered in a 4 minute speech.'
    
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": case}]
    return call_ai(messages)