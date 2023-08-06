import random
def generate(prompt: str = None, 
             models: list = ['gpt-4', 'mpt-7b-instruct', 'llama-30b'], 
             optimize: dict = {"cost" : 10} ) -> dict:    

    response = {"response" : f"Prompt: {prompt} Response: Hello World",
                "model" : models[random.randrange(0,len(models)-1)],
                "cost" : "$" + str(round(random.random(),2)),
                "quality" : random.randint(0,10),
                "latency" : str(round(random.random(),2)) + 's'
                }        
    return response

#print(generate(prompt='Testing', optimize={"cost":50}))