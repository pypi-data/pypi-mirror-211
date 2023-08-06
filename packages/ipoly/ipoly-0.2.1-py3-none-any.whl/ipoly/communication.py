"""Provides routines for communicating by different means."""
from typing import Iterable
from typing import Union

from ipoly.traceback import raiser


def send(
    sender: str,
    password: str,
    receivers: Union[str, list[str]],
    subject: str,
    content: str,
    pngfiles: Iterable[str] = (),
):
    """Send an email to (a/some) receiver(s).

    Args:
        sender: The sender email. Gmail and Outlook emails are supported.
        password: The sender's password.
        receivers: List or single email of the receiver(s).
        subject: The object of the email.
        content: The main text part of the email.
        pngfiles: List of attached files.
    """
    import smtplib
    from email.mime.application import MIMEApplication
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(receivers if isinstance(receivers, list) else [receivers])
    msg.attach(MIMEText(content, "plain"))
    for file in pngfiles:
        extension = file.split(r".")[-1]
        with open(file, "rb") as fp:
            attached_file: MIMEImage | MIMEApplication
            if extension == "png":
                attached_file = MIMEImage(fp.read())
                # Open the files in binary mode.  Let the MIMEImage class automatically
                # guess the specific image type.
            else:
                attached_file = MIMEApplication(fp.read(), Name=file)
        msg.attach(attached_file)

    send_port = 587

    # Send the email via our own SMTP server.
    host = "smtp.gmail.com" if "gmail" in sender else "smtp.office365.com"
    with smtplib.SMTP(host, send_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, password)
        smtp.sendmail(sender, receivers, msg.as_string())
        smtp.quit()


def say(message: str) -> None:
    """Make the computer say the message out loud.

    This function works on Linux/Windows and Mac platforms.

    Args:
        message: The message the computer says.
            For security, the characters used must be in this list:
            0123456789,;:.?!-_ÂÃÄÀÁÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ
    """
    from string import ascii_letters

    if all(
        char
        in ascii_letters
        + "0123456789,;:.?!-_ÂÃÄÀÁÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"
        for char in message
    ):
        raiser(
            "This message will not be said because you used some symbols that may be used for doing some malicious injection :(",
        )
    from platform import system as ps
    from subprocess import run  # nosec

    match ps():
        case "Windows":
            from win32com.client import Dispatch

            speak = Dispatch("SAPI.SpVoice").Speak
            speak(message)
        case "Darwin":
            run(["say", message])  # nosec
        case "Linux":
            run(["spd-say", message])  # nosec
        case syst:
            raise RuntimeError("Operating System '%s' is not supported" % syst)


def notify(message: str, title: str = "Hey !") -> None:
    """Send a notification.

    This function works on Linux/Windows and Mac platforms and uses plyer in backend.

    Args:
        message: The message sent as a notification.
        title: The title of the notification. Defaults to 'Hey !'.
    """
    from plyer import notification
    from os.path import join, dirname

    notification.notify(
        app_name="iPoly",
        app_icon=join(dirname(__file__), r"img\ipoly.ico"),
        title=title,
        message=message,
        ticker="iPoly ticker",
        timeout=15,
    )
