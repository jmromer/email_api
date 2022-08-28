import os


class Mailer:
    # The mailer service to use. Should be the module name of an API wrapper
    # class that responds to `.send_mail`.
    MAILER_SERVICE = os.getenv("MAILER_SERVICE", "mailgun")

    @classmethod
    def send_mail(cls, **args):
        """Send an email using the configured mailer service."""
        module = getattr(__import__("lib"), cls.MAILER_SERVICE)
        return module.mailer.send_mail(**args)
