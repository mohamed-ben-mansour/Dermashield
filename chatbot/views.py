from django.shortcuts import render
import json

# Create your views here.
# chatbot/views.py
from django.shortcuts import render
from .utils import get_answer

# Charger les réponses JSON
def load_responses():
    with open(
        r"C:\Users\ASUS\Desktop\gl_version2.00\chatbot\static\chatbot\greetings.json",
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)

# Fonction pour trouver une réponse dans les greetings
def get_greeting_response(message, responses):
    for greeting, reply in responses.get("greetings", {}).items():
        if greeting in message.lower():
            return reply
    return None

# Vue du chatbot
def chatbot_view(request):
    response = None
    if request.method == "POST" and "message" in request.POST:
        user_message = request.POST["message"].strip()
        responses = load_responses()

        # Vérifier les greetings
        greeting_response = get_greeting_response(user_message, responses)
        if greeting_response:
            response = greeting_response
        else:
            try:
                # Utilisez une autre fonction pour obtenir une réponse avancée
                response = get_answer(user_message)
            except Exception as e:
                response = f"Erreur lors de la récupération de la réponse : {str(e)}"

    return render(request, "chatbot/chatbot.html", {"response": response})