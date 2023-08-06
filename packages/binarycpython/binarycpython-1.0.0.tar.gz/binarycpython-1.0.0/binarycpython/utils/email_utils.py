"""
Script to send an email when a function or simulation is finished.

https://leimao.github.io/blog/Python-Send-Gmail/
- I make use of the 'new authentication - less secure: app password' method
"""

import datetime
import smtplib
import ssl
import traceback
from email.message import EmailMessage


def send_email(config, body_text, subject):
    """
    Main function to handle sending the email
    """

    # Handle checking the configuration
    if not config["email_notifications_enabled"]:
        return

    corresponding_email = config["email_notifications_corresponding_email"]
    assert corresponding_email != ""

    # configuration
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    password = config["email_notifications_APP_password"]
    receiver_emails = [corresponding_email] + config[
        "email_notifications_recipients"
    ]  # Enter receiver address
    sender_email = corresponding_email  # Enter your address

    # set content
    datetimestring = datetime.datetime.utcnow().isoformat()
    body_text = (
        "Message from binary_c-python population sent on {}\n\n".format(datetimestring)
        + body_text
    )

    # Set up email object
    for receiver_email in receiver_emails:
        msg = EmailMessage()
        msg.set_content(body_text)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        print(
            "sending email from {} to {} with subject {}".format(
                sender_email, receiver_email, subject
            )
        )

        # Allow for testing
        if not config.get("email_notifications_testing"):
            # Send email
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.send_message(
                        msg, from_addr=sender_email, to_addrs=receiver_email
                    )
            except BaseException as error:
                print("An exception occurred: {}".format(error))
                print(f"Exception Name: {type(error).__name__}")
                print(f"Exception Desc: {error}")
                print(f"Exception traceback: {traceback.print_exc()}")
        else:
            print("with body text:\n{}".format(body_text))


def send_error_email(config, error, traceback, message, class_object=None):
    """
    Function to send a general error email. Optionally uses class object
    """

    #
    class_object_text = (
        "class {} population_id {}".format(
            class_object.__class__.__name__, config["_population_id"]
        )
        if class_object is not None
        else ""
    )

    subject = "binary_c-python population " + class_object_text + " failed"

    body_text = """
binary_c-python class: {}

Exception Name: {}

An exception occurred: {}

Traceback: {}

Message: {}
""".format(
        class_object_text, error, type(error).__name__, traceback, message
    )

    # Send the email
    send_email(config=config, body_text=body_text, subject=subject)


def send_succes_email(config, message, class_object=None):
    """
    Function to send a general success email. Optionaly uses class object
    """

    #
    class_object_text = (
        "class {} population_id {}".format(
            class_object.__class__.__name__, config["_population_id"]
        )
        if class_object is not None
        else ""
    )

    subject = (
        "binary_c-python population " + class_object_text + " completed without errors!"
    )

    body_text = """
binary_c-python class: {}

Message: {}
""".format(
        class_object_text, message
    )

    # Send the email
    send_email(config=config, body_text=body_text, subject=subject)


class Email_context_manager:
    def __init__(self, config, class_object):
        self.config = config
        self.class_object = class_object

    def __enter__(self):
        self.start = datetime.datetime.now()
        # We don't return anything here because we don't use the class instance anyway

    def __exit__(self, exc, value, exc_traceback):
        if not exc:
            self.class_object.send_success_email()
        else:
            actual_traceback_obj = traceback.format_exc()
            self.class_object.send_error_email(value, actual_traceback_obj)
