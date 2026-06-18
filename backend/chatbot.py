import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6IhqBAMzsI9fm1QG0JgTuhZmnsOw-E8o8wyUhWenJH0qQ")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.post("/chat")
def chat(message: str):

    response = model.generate_content(message)

    return {
        "response": response.text
    }