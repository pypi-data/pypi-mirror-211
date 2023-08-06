import requests
from datetime import datetime

url = "http://me8014.asuscomm.com:8088/engines" 
messages = []
i = 0

def savechat(messages):

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    filename = f"messages_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for i, message in enumerate(messages):
            linemessage = message['content']
            linemessage.replace('\\n', '\n')
            f.write(f"{i}: {linemessage}\n")

def playchat(amessage, pref=''):

    global messages, i
    
    if amessage == 'reset':
        savechat(messages)
        messages = []
        i = 0
        return '이전 대화를 파일로 저장하고, 다시 대화를 시작합니다..'
    
    messages.append({"role": "user","content": amessage})

    response = requests.post(
            url,
            json={"model": "gpt-3.5-turbo", 
                  "messages": messages,
                 },
            )
    output = response.json()["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content" : output})
    i += 2
    return  print('[', i-2, ']', amessage, '\n[', i-1, ']', output)
    