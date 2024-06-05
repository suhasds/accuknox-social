#! /usr/bin/python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from main.settings.settings import EMAIL_CONFIG


def send_mail(to_email, subject=None, text_message=None, html_message=None):
    # me == my email address
    # you == recipient's email address
    from_email = EMAIL_CONFIG["sender_email"]

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Create the body of the message (a plain-text and an HTML version).
    text = text_message
    html = html_message

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP_SSL(host=EMAIL_CONFIG["host"], port=EMAIL_CONFIG["port"])
    s.login(from_email, EMAIL_CONFIG["sender_password"])
    s.sendmail(from_email, to_email, msg.as_string())
    s.quit()


if __name__ == '__main__':
    pass
