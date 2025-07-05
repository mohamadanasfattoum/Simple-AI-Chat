from flask import Flask, render_template
from flask_socketio import SocketIO
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage , AIMessage


app = Flask(__name__)
socketio = SocketIO(app)

# AI
llm = ChatOllama(model="llama3.2:3b")
prompt = ChatPromptTemplate.from_messages([
    ("system","You are a helpfull assistant"),
    ("human","{input}")
])

# save history
chat_history = []

@app.route('/')
def chat_home():
    return render_template("chat.html")


@socketio.on('message') # Wird ausgelöst, wenn ein WebSocket-Event vom Typ "message" empfangen wird
def handle_message(data): # Empfängt Daten über WebSocket und führt anschließend eine POST-Anfrage aus
    pass


if __name__=="__main__":
    socketio.run(app,debug=True)