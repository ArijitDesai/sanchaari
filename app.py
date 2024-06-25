import gradio as gr
from llm_handler import sanchaari

def handle_query(query):
    thoughts = []
    final_answer = None
    
    for result in sanchaari(query):
        if "thought" in result:
            thoughts.append(result["thought"])
            yield {"Thought Process": thoughts, "Response Text": ""}
        if "final_answer" in result:
            final_answer = result["final_answer"]
            yield {"Thought Process": thoughts, "Response Text": final_answer}

gr.Interface(
    fn=handle_query,
    inputs=gr.Textbox(lines=2, placeholder="Enter your query here..."),
    outputs="json",
    title="Antarjaala Sanchaari: Your Versatile AI Assistant",
    description=""" Meet **Antarjaala Sanchaari**, your versatile AI assistant designed to provide quick and accurate information on various topics. Whether you need to know the latest stock prices, definitions of complex words, or even translations, **Sanchaari** is here to help. With capabilities to fetch real-time data, perform calculations, and retrieve information from Wikipedia, **Sanchaari** is your go-to source for all your informational needs. Explore the power of AI with **Sanchaari**, your intelligent companion for insightful answers and seamless assistance.

**What Sanchaari Can Do:**
- **Calculate**: Perform arithmetic calculations.
- **Find Information**: Search and summarize information from Wikipedia.
- **Tell Time**: Get the current time for any location worldwide.
- **Get Stock Prices**: Check current stock prices for any company.
- **Define Words**: Look up definitions for any word.
- **Provide Latest News**: Retrieve the latest news headlines.
- **Translate Text**: Translate text from English to various languages.


Example:

**Question**: What is the capital of France?
**Answer**: The capital of France is Paris.

**Question**: 2*3
**Answer**: 6
"""
).launch(share=True)
