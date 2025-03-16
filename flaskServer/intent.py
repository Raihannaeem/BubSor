def load_prompt(path): 
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def check_intent(query): 
    prompt = (load_prompt("prompts/intent.txt")).replace("{query}", query)
    response = LLM.send_message(prompt)
    temp = int(response)
    return temp
