from openai import AzureOpenAI
    
def call_ai(sys_prompt, user_prompt):
    client = AzureOpenAI(
        api_key='API_KEY',  
        api_version="2024-10-21",
        azure_endpoint ='ENDPOINT'
        )

    completion = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    return completion.choices[0].message.content

def pf_feedback(resolution, transcription):
    prompt = resolution
    return call_ai(prompt, transcription)

def case_feedback(resolution, case):
    prompt = f'You are a public forum debate coach. Your job is to analyze cases provided of high school public forum debate and provide detailed feedback on how it could be improved. The resolution being debated in this round is {resolution} Give as much feedback (4-5 pieces of feedback per contention at MINIMUM) as possible on the content and strategy of the case. Make sure to analyze the uniqueness, link, internal link, and impact of each and every contention. Remember that the case will be delivered in a 4 minute speech.'
    return call_ai(prompt, case)