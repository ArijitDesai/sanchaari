from flask import Flask, request, render_template, jsonify
from llm_handler import sanchaari

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    question = request.form.get('question')
    response_generator = sanchaari(question)
    thoughts = []
    final_response = None

    for result in response_generator:
        if "thought" in result:
            thoughts.append(result["thought"])
        if "final_answer" in result:
            final_response = result["final_answer"]

    return jsonify({
        "thought_process": thoughts,
        "final_response": final_response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
