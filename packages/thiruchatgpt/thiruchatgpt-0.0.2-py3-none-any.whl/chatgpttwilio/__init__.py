from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai



account_sid = ''                 # Twilio Account SID
auth_token  = ''                 # Twilio Account Auth Token

openai_apikey = ''


if(account_sid and auth_token and openai_apikey):
    client = Client(account_sid, auth_token)

    openai.api_key = openai_apikey  #"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"                                              # OPEN-AI API KEY
    completion = openai.Completion()

    start_chat_log = '''Human: Hello, who are you?
    AI: I am doing great. How can I help you today?
    '''

    def ask(question, chat_log=None):
        if chat_log is None:
            chat_log = start_chat_log
        prompt = f'{chat_log}Human: {question}\nAI:'
        prompt = question
        response = completion.create(
            prompt=prompt, engine="text-davinci-003", stop=['\nHuman'], temperature=0.2,
            top_p=1, frequency_penalty=0.1, presence_penalty=0.0, best_of=1,
            max_tokens=256)
        answer = response.choices[0].text.strip()
        return answer

    def append_interaction_to_chat_log(question, answer, chat_log=None):
        if chat_log is None:
            chat_log = start_chat_log
        return f'{chat_log}Human: {question}\nAI: {answer}\n'


    def sendMessage(body_mess, phone_number):
        message = client.messages.create(
                                    from_='whatsapp:+14155238886',                  # With Country Code
                                    body=body_mess,
                                    to='whatsapp:' + phone_number                   # With Country Code
                                )
        print(message)  