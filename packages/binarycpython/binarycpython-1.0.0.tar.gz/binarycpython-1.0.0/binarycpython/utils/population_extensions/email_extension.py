"""
Email handling class extension for population

might be interesting to make sure it handles SIGKILL and stuff properly
https://code.activestate.com/recipes/577997-handle-exit-context-manager/
"""

from binarycpython.utils.email_utils import send_error_email, send_succes_email


class Email:
    """
    Email class-extension for binary_c-python population class
    """

    def __init__(self):
        pass

    def send_error_email(self, exc, tb):
        """
        Function to send error email
        """

        message = "binary_c-python population failed."

        if (
            self.population_options["email_notification_extra_info_function_hook"]
            is not None
        ):
            extra_info = self.population_options[
                "email_notification_extra_info_function_hook"
            ](self)

            message += extra_info

        send_error_email(
            config=self.population_options,
            error=exc,
            traceback=tb,
            message=message,
            class_object=self,
        )

    def send_success_email(self):
        """
        Function to send an email about the grid success
        """

        message = "binary_c-python population finished without errors."

        if (
            self.population_options["email_notification_extra_info_function_hook"]
            is not None
        ):
            extra_info = self.population_options[
                "email_notification_extra_info_function_hook"
            ](self)

            message += extra_info

        #
        send_succes_email(
            config=self.population_options, message=message, class_object=self
        )
