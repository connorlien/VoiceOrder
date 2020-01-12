import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.dialog.delegate_directive import DelegateDirective
from ask_sdk_model.dialog_state import DialogState
from ask_sdk_model.dialog.elicit_slot_directive import ElicitSlotDirective
from ask_sdk_model import Response

from api_handler import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, say begin order to start ordering"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class ConfirmOrderIntentHandler(AbstractRequestHandler):
    """Handler for Order Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #
        return ask_utils.is_intent_name("ConfirmOrderIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        session_attr = handler_input.attributes_manager.session_attributes
        '''
        success = process_user_order(session_attr["user_order"], get_authorization_token())
        if success :
            return (handler_input.response_builder.speak("Okay, your order " + session_attr["user_order"] + " is being processed. Have a nice day!")
                .set_should_end_session(True)
                .response)
        else :
            session_attr["user_order"] = ""
            return (handler_input.response_builder.speak("Sorry, your order appears to be invalid. Please say begin order again to restart.")
                .set_should_end_session(False)
                .response)
        '''
        return (handler_input.response_builder.speak("Okay, your order is being processed. Have a nice day!")
                .set_should_end_session(True)
                .response)


class CancelOrderIntentHandler(AbstractRequestHandler):
    """Handler for Order Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #
        return ask_utils.is_intent_name("BelayOrderIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["user_order"] = ""

        init_table()
        return (handler_input.response_builder.speak(
            "Okay, your order has been cancelled. Say begin order to begin your order.")
                .set_should_end_session(False)
                .response)


class ContinueOrderIntentHandler(AbstractRequestHandler):
    """Handler for Order Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #
        return ask_utils.is_intent_name("ContinueOrderIntent")(handler_input)

    def handle(self, handler_input):
        state = handler_input.request_envelope.request.dialog_state
        slots = handler_input.request_envelope.request.intent.slots
        session_attr = handler_input.attributes_manager.session_attributes
        input = slots["user_input"].value

        if state == DialogState.STARTED:
            # return (handler_input.response_builder.add_directive(DelegateDirective(handler_input.request_envelope.request.intent)).response)
            handler_input.response_builder.add_directive(DelegateDirective())
            return (handler_input.response_builder.response)
        else:
            session_attr["user_order"] = input
            # insert automl call here
            success, subprice = process_user_order(session_attr["user_order"], get_authorization_token())
            if success:
                price_str = ""
                if (subprice * 100) % 100 == 0:
                    price_str = str(int(subprice // 1)) + " dollars"
                else:
                    price_str = str(int(subprice // 1)) + " dollars and " + str(int((subprice * 100) % 100)) + " cents"
                return (
                    handler_input.response_builder.speak("Okay, your order is " + session_attr["user_order"].strip() + \
                                                         ". The price of this will be " + price_str + ". Would you like to continue or confirm your order?")
                    .set_should_end_session(False)
                    .response)
            else:
                session_attr["user_order"] = ""
                return (handler_input.response_builder.speak(
                    "Sorry, your order appears to be invalid. Please say begin order again to restart.")
                        .set_should_end_session(False)
                        .response)


class OrderIntentHandler(AbstractRequestHandler):
    """Handler for Order Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #
        return ask_utils.is_intent_name("OrderIntent")(handler_input)

    def handle(self, handler_input):
        '''
        slots = handler_input.request_envelope.request.intent.slots
        user_input = slots["user_input"].value
        '''
        state = handler_input.request_envelope.request.dialog_state
        slots = handler_input.request_envelope.request.intent.slots
        session_attr = handler_input.attributes_manager.session_attributes
        input = slots["user_input"].value

        init_table()
        if state == DialogState.STARTED:
            handler_input.response_builder.add_directive(DelegateDirective())
            session_attr["user_order"] = ""
            return (handler_input.response_builder.response)

        else:
            session_attr["user_order"] += input + " "
            # insert automl call here
            success, subprice = process_user_order(session_attr["user_order"], get_authorization_token())
            if success:
                price_str = ""
                if (subprice * 100) % 100 == 0:
                    price_str = str(int(subprice // 1)) + " dollars"
                else:
                    price_str = str(int(subprice // 1)) + " dollars and " + str(int((subprice * 100) % 100)) + " cents"
                return (
                    handler_input.response_builder.speak("Okay, your order is " + session_attr["user_order"].strip() + \
                                                         ". The price of this will be " + price_str + ". Would you like to continue or confirm your order?")
                    .set_should_end_session(False)
                    .response)
            else:
                session_attr["user_order"] = ""
                return (handler_input.response_builder.speak(
                    "Sorry, your order appears to be invalid. Please say begin order again to restart.")
                        .set_should_end_session(False)
                        .response)


'''
class AskMoreIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input) and handler_input.request_envelope.request.intent.slots["user_input"].value === "test"

    def handle(self, handler_input):

        slots = handler_input.request_envelope.request.intent.slots
        user_input = slots["user_input"].value


        return (handler_input.response_builder
            .speak("did you say " + user_input)
            .response
        )
'''


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can use this program to order boba! Say begin order to start ordering."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Thank you for visiting and have a nice day."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CancelOrderIntentHandler())
sb.add_request_handler(ConfirmOrderIntentHandler())
sb.add_request_handler(ContinueOrderIntentHandler())
sb.add_request_handler(OrderIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()