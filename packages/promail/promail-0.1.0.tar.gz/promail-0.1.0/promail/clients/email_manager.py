"""Abstract Classes for Inbound and outbound mail."""
import abc


class OutBoundManager(abc.ABC):
    """Outbound Mail class template."""

    def send_email(
        self: object,
        recipients: str,
        cc: str,
        bcc: str,
        subject: str,
        htmltext: str,
        plaintext: str,
    ) -> None:
        """Send an email.

        Args:
            recipients: semicolon seperated string of recipients will show in
                to section
                "Example Foo <bar@example.com>;Example2 Bar <foo@example.com"
            cc: semicolon seperated string of recipients will  be cc'd on email
                "Example Foo <bar@example.com>;Example2 Bar <foo@example.com"
            bcc: semicolon seperated string of recipients will be bcc'd on
                email:
                "Example Foo <bar@example.com>;Example2 Bar <foo@example.com"
            subject: Subject of the email
            htmltext: An HTML string of text
            plaintext: A plain text alternative text
        """
        pass


class InBoundManager(abc.ABC):
    """Outbound Mail class template."""

    def retrieve_last_items(self: object, max_items: int) -> list:
        """Get a list of last n items received in inbox.

        Args:
            max_items: The Maximum number of items to return
        """
        pass
