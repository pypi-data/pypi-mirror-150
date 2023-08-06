"""Gmail Mail Client."""
import smtplib

from promail.clients.email_manager import OutBoundManager


class GmailClient(OutBoundManager):
    """Gmail Client."""

    def __init__(self, account: str, password: str) -> None:
        """Initiates Gmail Client.

        Args:
            account: Gmail Email Address
            password: Password for gmail account create app specific password
                https://security.google.com/settings/security/apppasswords
        """
        self._account = account
        self._password = password

    def send_email(
        self,
        recipients: str,
        cc: str,
        bcc: str,
        subject: str,
        htmltext: str,
        plaintext: str,
    ) -> None:
        """Send Email email using Outlook client in windows.

        Args:
            recipients: semicolon seperated string of recipients will show in to section
                "Example Foo <bar@example.com>;Example2 Bar <foo@example.com"
            cc: semicolon seperated string of recipients will  be cc'd on email
                "Example Foo <bar@example.com>;Example2 Bar <foo@example.com"
            bcc: semicolon seperated string of recipients will be bcc'd on email
                "Example Foo <bar@example.com>;Example2 Bar <foo@example.com"
            subject: Subject of the email
            htmltext: An HTML string of text
            plaintext: A plain text alternative text
        """
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(self._account, self._password)
        server.sendmail(self._account, recipients, htmltext)
        server.close()
        print("successfully sent the mail")
