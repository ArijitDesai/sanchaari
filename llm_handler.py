import anthropic
import os
import re
from actions import known_actions

# Initialize the Anthropic client with your API key
client = anthropic.Anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY'),
)

# Specify the model
model = 'claude-3-5-sonnet-20240620'

# Define the ChatBot class
class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.messages.create(
            system=self.system,
            model=model,
            messages=self.messages,
            max_tokens=500
        )
        return completion.content[0].text

# Define the prompt template
prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.
Your available actions are:
calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary.
wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia.
current_time:
e.g. current_time: America/New_York
Returns the current time of a specific place. The place should be specified in 'Area/Location' format.
dictionary:
e.g. dictionary: serendipity
Returns the definition of a word.
news:
e.g. news: technology
Returns the latest news headlines for a given topic.
stock_price:
e.g. stock_price: AAPL
Returns the current stock price for a given company.
translate:
e.g. translate: Hello, es
Translates text from English to the specified language (e.g., 'es' for Spanish).
Always look things up on Wikipedia if you have the opportunity to do so.
Example session:
Question: What is the capital of France?
Thought: I should look up France on Wikipedia.
Action: wikipedia: France
PAUSE
You will be called again with this:
Observation: France is a country. The capital is Paris.
You then output:
Answer: The capital of France is Paris.
""".strip()

# Compile the action regex
action_re = re.compile(r'^Action: (\w+): (.*)$')

# List of sensitive keywords and phrases
sensitive_keywords = [
    "guardrails", "internal workings", "prompt", "how do you work", 
    "how are you built", "system prompt", "behind the scenes", 
    "security measures", "limitations", "rules"
]

def contains_sensitive_keywords(question):
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in sensitive_keywords)

def extract_translation_request(question):
    match = re.search(r'what is (\w+) in (\w+)', question.lower())
    if match:
        return match.group(1), match.group(2)
    return None, None

def sanchaari(question, max_turns=5):
    bot = ChatBot(prompt)
    next_prompt = question

    # Guardrail check
    if contains_sensitive_keywords(question):
        yield {"final_answer": "I'm here to assist you with information and tasks. If you have a specific query, feel free to ask!"}
        return

    for _ in range(max_turns):
        result = bot(next_prompt)
        yield {"thought": result}
        
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        
        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(f"Unknown action: {action}: {action_input}")

            if action == "translate":
                parts = action_input.split(", ")
                if len(parts) == 2:
                    observation = known_actions[action](parts[0], parts[1])
                else:
                    observation = "Translation requires both text and target language."
            else:
                observation = known_actions[action](action_input)
            
            next_prompt = f"Observation: {observation}"
            yield {"thought": f"Action: {action}, Input: {action_input}, Observation: {observation}"}
        else:
            # Separate the final answer from the thought process
            final_answer_index = result.find("Answer:")
            if final_answer_index != -1:
                yield {"thought": result[:final_answer_index].strip()}
                final_answer = result[final_answer_index + len("Answer:"):].strip()
            else:
                final_answer = result
            yield {"final_answer": final_answer}
            return
    
    # Final loop in case max_turns is reached without explicit "Answer:"
    final_answer_index = result.find("Answer:")
    if final_answer_index != -1:
        yield {"thought": result[:final_answer_index].strip()}
        final_answer = result[final_answer_index + len("Answer:"):].strip()
    else:
        final_answer = result
    yield {"final_answer": final_answer}
