import os
import gradio as gr
from groq import Groq

# Load API key from environment variable
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is missing.")

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Chat function
def chatbot_response(message, history):

    messages = []

    # Add previous chat history
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})

    # Add new user message
    messages.append({"role": "user", "content": message})

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024
        )

        reply = chat_completion.choices[0].message.content

    except Exception as e:
        reply = f"Error: {str(e)}"

    return reply


# Gradio Chat UI
demo = gr.ChatInterface(
    fn=chatbot_response,
    title="AI Chatbot (Groq + Llama 3.3)",
    description="Fast chatbot powered by Groq inference",
)

if __name__ == "__main__":
    demo.launch()
