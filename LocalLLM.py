import ollama

#Establish connection to local LLM
def call_llm(input):
    response =ollama.chat(
        model="viratLow",
        messages=[
            {
                "role":"user",
                "content":input
            }
        ]       
    )

    return response["message"]["content"]

user_input =input("Enter your instructions : ")
print("User Input ::",user_input)

result =call_llm(user_input)
print("AI Output :: \n",result)
