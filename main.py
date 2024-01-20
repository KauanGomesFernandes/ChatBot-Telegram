import requests
import time
import json
import os
import dotenv
import re
import emoji

dotenv.load_dotenv()

class ApiTelegram:
    def __init__(self):
        self.seconds = 5
        self.idUpdate = None
        self.token = os.getenv("TOKEN_API")
        self.urlApiTelegramBot = f'https://api.telegram.org/bot{self.token}/'
        self.urlGetUpdates = f'getUpdates'
        self.urlTimeOut = f'?timeout={self.seconds}'
        self.urlOffset = f'&offset='
        self.urlSendMessage = f'sendMessage?chat_id='
        self.urlText = f'&text='
        self.urlSendPhoto = f'sendPhoto?chat_id='
        self.urlPhoto = f'&photo='
        self.updates = None
        self.greeting = None
        self.treatedResults = None
        self.resultsRequest = None
        self.results = None
        self.messageReceived = None
        self.replyMessage = None
        self.messageResults = {}

    
    def getUpdates(self):

        if self.idUpdate:
            urlGetUpdates = f'{self.urlApiTelegramBot}{self.urlGetUpdates}{self.urlTimeOut}{self.urlOffset}{self.idUpdate}'
        else:
            urlGetUpdates = f'{self.urlApiTelegramBot}{self.urlGetUpdates}{self.urlTimeOut}'

        self.updates = requests.get(urlGetUpdates)
        self.updates = json.loads(self.updates.content)

        if 'result' in self.updates:

            for result in self.updates['result']:

                if 'update_id' in result:
                    self.idUpdate = result['update_id']
                    self.idUpdate = self.idUpdate + 1

            self.resultsRequest = self.updates['result']
            return self.resultsRequest
        
        else: 
            return self.resultsRequest
    
    def treatmentResults(self):

        if self.resultsRequest:

            for self.results in self.resultsRequest:

                if 'message' in self.results:

                    self.messageReceived = self.results['message']

                    try:
                        if 'message_id' in self.messageReceived:
                            try:
                                self.messageResults['id_message'] = self.messageReceived['message_id']
                            except KeyError:
                                pass

                            try:
                                if self.messageReceived['message_id'] == 1:
                                    self.messageResults['first_message'] = True
                                else:
                                    self.messageResults['first_message'] = False

                            except KeyError:
                                pass

                    except KeyError:
                        pass

                    try:
                        if 'chat' in self.messageReceived:
                            try:
                                if 'id' in self.messageReceived['chat']:
                                    self.messageResults['id_chat'] = self.messageReceived['chat']['id']
                            except KeyError:
                                pass
                    
                    except KeyError:
                        pass

                    try:
                        if 'from' in self.messageReceived:
                            try:
                                if 'first_name' in self.messageReceived['from']:
                                    self.messageResults['first_name'] = self.messageReceived['from']['first_name']
                                else:
                                    self.messageResults['first_name'] = "Visitante"
                            except KeyError:
                                pass
                            
                            try:
                                if 'last_name' in self.messageReceived['from']:
                                    self.messageResults['last_name'] = self.messageReceived['from']['last_name']
                                else:
                                    self.messageResults['last_name'] = "Foxy"
                            except KeyError:
                                pass

                            try:
                                if 'username' in self.messageReceived['from']:
                                    self.messageResults['username'] = self.messageReceived['from']['username']
                            except KeyError:
                                pass

                    except KeyError:
                        pass

                    try:
                        if 'text' in self.messageReceived:
                            self.messageResults['message'] = self.messageReceived['text']
                            self.messageResults['type'] = 'text'

                    except KeyError:
                        pass

                    try:
                        if 'voice' in self.messageReceived:
                            try:
                                if 'file_unique_id' in self.messageReceived['voice']:
                                    self.messageResults['message'] = self.messageReceived['voice']['file_unique_id']
                                    self.messageResults['type'] = 'voice'
                            except KeyError:
                                pass
                    except KeyError:
                        pass

                    try:
                        if 'photo' in self.messageReceived:
                            try:
                                for photo in self.messageReceived['photo']:
                                    self.messageResults['message'] = photo['file_unique_id']
                                    self.messageResults['type'] = 'photo'
                            except KeyError:
                                pass
                    except KeyError: 
                         
                        pass

                    try:
                        if 'document' in self.messageReceived:
                            try:
                                if 'file_unique_id' in self.messageReceived['document']:
                                    self.messageResults['message'] = self.messageReceived['document']['file_unique_id']
                                    self.messageResults['type'] = 'document'
                            except KeyError:
                                pass
                    except KeyError:
                        pass

                    try:
                        if 'poll' in self.messageReceived:
                            try:
                                self.messageResults['message'] = False
                                self.messageResults['type'] = 'poll'
                            except KeyError:
                                pass

                    except KeyError:
                        pass

                self.createMessage(self.messageResults)



    def createMessage(self, message):
        try:
            if message:
                messageReceived = message
                messageReceived['type_of_answer'] = 'text'

                try:
                    if messageReceived['message'] =='/start' and messageReceived['first_message']:
                        self.replyMessage = f'🤖: Olá {messageReceived['first_name']}, seja bem-vindo me chamo Foxy, como posso ajudar?'

                    elif messageReceived['type'] != 'text':
                        self.replyMessage = f'🤖: {messageReceived['first_name']}, infelizmente ainda não consigo processar alguns tipos de messagem...'
                        
                    elif messageReceived['type'] == 'text':

                        if re.match('/', messageReceived['message']):

                            if messageReceived['message'] =='/start':

                                self.replyMessage = '🤖: eu estou On-line, pronto para responder, como posso ajudar?'
                            
                            elif messageReceived['message'] == '/dev':
                                self.replyMessage = '👨‍💻:💤💤💤'
                            
                            elif messageReceived['message'] == '/commands':
                                self.replyMessage = '🤖: Esta aqui os comandos disponiveis para uso'

                            elif messageReceived['message'] == '/info':
                                self.replyMessage = f'🤖:💤💤💤'

                            elif messageReceived['message'] == '/donation':
                                self.replyMessage = f'🤖:💤💤💤'
                            
                            else:
                                self.replyMessage = '🤖: Desculpa não fui capaz de compreender seu comando.'
                        
                        else:
                            self.replyMessage = '🤖: Desculpa não fui capaz de compreender.'

                except KeyError:
                    pass

                if self.replyMessage:
                    self.sendMessage(self.replyMessage, messageReceived)


        except KeyError:
            pass


    def sendMessage(self, replyMessage, messageReceived):

        if replyMessage and messageReceived:

            if messageReceived['type_of_answer'] == 'text':
                
                setMessage = f'{self.urlApiTelegramBot}{self.urlSendMessage}{messageReceived['id_chat']}{self.urlText}{replyMessage}'

                self.messageReceived = None
                self.replyMessage = None

                
            try:
                requests.post(setMessage)
                pass
            except KeyError:
                pass

        pass

try:
    botTelegram = ApiTelegram()
    if isinstance(botTelegram, ApiTelegram):

        print(emoji.emojize("🤖"), "Foxy: eu estou On-line, pronto para responder...")

        while True:
            botTelegram.getUpdates()
            botTelegram.treatmentResults()
            time.sleep(botTelegram.seconds)

except KeyError:

    print(emoji.emojize("🤖"), "Ola eu sou a Foxy, eu estou Off-line", emoji.emojize("💤💤💤"))