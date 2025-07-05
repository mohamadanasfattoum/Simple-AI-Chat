from flask import Flask, render_template
from flask_socketio import SocketIO, emit
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

    user_message = data['message']  # Benutzer-Nachricht aus den empfangenen von javascript Daten extrahieren 

    # store message to user history
    chat_history.append(HumanMessage(content=user_message))  # Benutzer-Nachricht zur Chat-Historie hinzufügen

    # create chain --> invoke
    chain = prompt | llm  # Erstelle eine Kette aus dem Prompt und dem Sprachmodell
    response = chain.invoke({"input":user_message})  # Nimm die Frage des Benutzers als Eingabe, rufe die Kette auf, um eine Antwort zu generieren und speichere die Antwort

    chat_history.append(AIMessage(content=response.content))  # KI-Antwort zur Chat-Historie hinzufügen
    
    # emit response
    emit('response', {'message': response.content})  # Sende die generierte KI-Antwort über WebSocket zurück an den Client, damit sie im Frontend angezeigt werden kann




if __name__=="__main__":
    socketio.run(app,debug=True)