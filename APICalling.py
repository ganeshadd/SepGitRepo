from openai import OpenAI

# Establish Connection
client =OpenAI(api_key="Your API Key")

def call_llm(input):
    response =client.responses.create(
        model="gpt-4o-mini",
        input=input
    )
    return response.output_text

user_input =input("Enter your instructions: ")
print("User Input :", user_input)

result = call_llm(user_input)
print("AI Output : \n", result)



