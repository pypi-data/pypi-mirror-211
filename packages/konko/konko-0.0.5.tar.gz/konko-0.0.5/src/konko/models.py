def listModels() -> list:    
    response = ['gpt-4', 'mpt-7b-instruct', 'llama-30b']
    return response

def addModels(models: list) -> bool:    
    [print(f'Adding model {m}') for m in models]
    return True