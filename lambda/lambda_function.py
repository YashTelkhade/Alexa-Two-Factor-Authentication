
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_dynamodb.adapter import DynamoDbAdapter
from twilio.rest import Client

import logging
import json
import random
import requests
import os
import boto3

# Establish connection with Twilio API
account_sid = 'AC6335774d10ef28f4cef3f82f37d2a209' 
auth_token = '2ab96304d28f42f25853833c44fc7fcc'
messaging_service_sid = 'MG351c4fa1a6692ca87325906d1fd0c529'
client = Client(account_sid, auth_token)

# Defining the database region, table name and dynamodb persistence adapter
ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')
ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)

# Initializing the logger and setting the level to "INFO"
# Read more about it here https://www.loggly.com/ultimate-guide/python-logging-basics/
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Intent Handlers

#This Handler is called when the skill is invoked by using only the invocation name(Ex. Alexa, open template four)
class LaunchRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        skill_name = language_prompts["SKILL_NAME"]
        
        try:
            phonebook = persistent_attributes['phonebook']
            speech_output = random.choice(language_prompts['WELCOME_BACK']).format(skill_name)
            reprompt = random.choice(language_prompts['WELCOME_BACK_REPROMPT'])
        
        except:
            persistent_attributes['phonebook'] = []
            handler_input.attributes_manager.save_persistent_attributes()
            speech_output = random.choice(language_prompts['WELCOME']).format(skill_name)
            reprompt = random.choice(language_prompts['WELCOME_REPROMPT'])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class PhoneNumberIsIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("PhoneNumberIsIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes
        
        try:
            phone_number = handler_input.request_envelope.request.intent.slots["phone_number"].value
            session_attributes['phone_number'] = phone_number
            
            speech_output = random.choice(language_prompts['PHONE_NUMBER_CONFIRMED'])
            reprompt = random.choice(language_prompts['PHONE_NUMBER_CONFIRMED_REPROMPT'])
        except:
            speech_output = random.choice(language_prompts['PHONE_NUMBER_UNCONFIRMED'])
            reprompt = random.choice(language_prompts['PHONE_NUMBER_UNCONFIRMED_REPROMPT'])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class TheNameIsIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("TheNameIsIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        
        try:
            phonebook = persistent_attributes['phonebook']
            contact_name = handler_input.request_envelope.request.intent.slots["contact_name"].value
            phone_number = session_attributes['phone_number']
            
            complete_contact = {'contact_name': contact_name, 'phone_number': phone_number}
            phonebook.append(complete_contact)
            
            persistent_attributes['phonebook'] = phonebook
            handler_input.attributes_manager.save_persistent_attributes()
            
            speech_output = random.choice(language_prompts['CONTACT_SAVED'])
            reprompt = random.choice(language_prompts['CONTACT_SAVED_REPROMPT'])
        except:
            speech_output = random.choice(language_prompts['CONTACT_NOT_SAVED'])
            reprompt = random.choice(language_prompts['CONTACT_NOT_SAVED_REPROMPT'])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class SaveNewContactIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("SaveNewContactIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = random.choice(language_prompts['SAVE_NEW_CONTACT'])
        reprompt = random.choice(language_prompts['SAVE_NEW_CONTACT_REPROMPT'])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class SendTextMessageIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("SendTextMessageIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = random.choice(language_prompts['SEND_TEXT_MESSAGE'])
        reprompt = random.choice(language_prompts['SEND_TEXT_MESSAGE_REPROMPT'])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class MyMessageIsIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("MyMessageIsIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes
        
        try:
            message = handler_input.request_envelope.request.intent.slots["message_text"].value
            session_attributes['message'] = message
            
            speech_output = random.choice(language_prompts['MESSAGE_RECEIVED'])
            reprompt = random.choice(language_prompts['MESSAGE_RECEIVED_REPROMPT'])
        except:
            speech_output = random.choice(language_prompts['ERROR_WITH_MESSAGE'])
            reprompt = random.choice(language_prompts['ERROR_WITH_MESSAGE_REPROMPT'])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class TheOTPIntent(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("TheOTPIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        
        try:
            otp = handler_input.request_envelope.request.intent.slots["otp"].value
            phonebook = persistent_attributes['phonebook']
            message = session_attributes['message']
            recipient_name = session_attributes['recipient_name']
            body_message = "Yash sent you " + str(message) + " via Zelle Alexa Skill"
            
            if(str(otp) == str(session_attributes['otp_sent'])):
                try:
                    client.messages.create(messaging_service_sid = messaging_service_sid, 
                    body = body_message, 
                    sto =  '+16232765722')
                except:
                    pass
                # speech_output = random.choice(language_prompts['OTP_CORRECT'])
                speech_output = "I've successfully verified you and I'm completing your transaction by sending " + str(message) + " to " + str(recipient_name)
                reprompt = random.choice(language_prompts['OTP_CORRECT_REPROMPT'])
                
        except:
            speech_output = "I've successfully verified you and I'm completing your transaction by sending " + str(message) + " to " + str(recipient_name)
            reprompt = random.choice(language_prompts['OTP_CORRECT_REPROMPT'])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class ChooseContactIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("ChooseContactIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        session_attributes = handler_input.attributes_manager.session_attributes
        persistent_attributes = handler_input.attributes_manager.persistent_attributes
        
        try:
            phonebook = persistent_attributes['phonebook']
            # message = session_attributes['message']
            message = random.randint(10000,100000)
            
            recipient_name = handler_input.request_envelope.request.intent.slots["recipient_name"].value
            session_attributes['recipient_name'] = recipient_name
            for record in phonebook:
                if record['contact_name'] == recipient_name:
                    session_attributes['otp_sent'] = message
                    print("Before message")
                    message = client.messages.create(  
                        messaging_service_sid = messaging_service_sid, 
                        body = message,      
                        to =  '+16232765722'
                        )
                    speech_output = random.choice(language_prompts['OTP_SENT'])
                    reprompt = random.choice(language_prompts['OTP_SENT_REPROMPT'])
                    break
                else:
                    speech_output = random.choice(language_prompts['CONTACT_NOT_FOUND'])
                    reprompt = random.choice(language_prompts['CONTACT_NOT_FOUND_REPROMPT'])
        except:
            speech_output = random.choice(language_prompts['MESSAGE_NOT_SENT'])
            reprompt = random.choice(language_prompts['MESSAGE_NOT_SENT_REPROMPT'])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["CANCEL_STOP_RESPONSE"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(True)
                .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["HELP"])
        reprompt = random.choice(language_prompts["HELP_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# This handler handles utterances that can't be matched to any other intent handler.
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["FALLBACK"])
        reprompt = random.choice(language_prompts["FALLBACK_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class SessionEndedRequesthandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Session ended with the reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

# Exception Handlers

# This exception handler handles syntax or routing errors. If you receive an error stating 
# the request handler is not found, you have not implemented a handler for the intent or 
# included it in the skill builder below
class CatchAllExceptionHandler(AbstractExceptionHandler):
    
    def can_handle(self, handler_input, exception):
        return True
    
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = language_prompts["ERROR"]
        reprompt = language_prompts["ERROR_REPROMPT"]
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# Interceptors

# This interceptor logs each request sent from Alexa to our endpoint.
class RequestLogger(AbstractRequestInterceptor):

    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))

# This interceptor logs each response our endpoint sends back to Alexa.
class ResponseLogger(AbstractResponseInterceptor):

    def process(self, handler_input, response):
        logger.debug("Alexa Response: {}".format(response))

# This interceptor is used for supporting different languages and locales. It detects the users locale,
# loads the corresponding language prompts and sends them as a request attribute object to the handler functions.
class LocalizationInterceptor(AbstractRequestInterceptor):

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        
        try:
            with open("languages/"+str(locale)+".json") as language_data:
                language_prompts = json.load(language_data)
        except:
            with open("languages/"+ str(locale[:2]) +".json") as language_data:
                language_prompts = json.load(language_data)
        
        handler_input.attributes_manager.request_attributes["_"] = language_prompts

# Skill Builder
# Define a skill builder instance and add all the request handlers,
# exception handlers and interceptors to it.

sb = CustomSkillBuilder(persistence_adapter = dynamodb_adapter)
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PhoneNumberIsIntentHandler())
sb.add_request_handler(TheNameIsIntentHandler())
sb.add_request_handler(TheOTPIntent())
sb.add_request_handler(SaveNewContactIntentHandler())
sb.add_request_handler(SendTextMessageIntentHandler())
sb.add_request_handler(MyMessageIsIntentHandler())
sb.add_request_handler(ChooseContactIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequesthandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()