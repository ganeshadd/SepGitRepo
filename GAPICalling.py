from google import genai

# Establish Connection
client =genai.Client(api_key="Your API Key")

def call_llm(input):
    response =client.models.generate_content(
        model="gemini-3.6-flash",
        contents=input
    )
    return response.text


user_input =input("Enter your instructions: ")
print("User Input :", user_input)

result = call_llm(user_input)
print("AI Output : \n", result)