import smtplib
from email.message import EmailMessage
# import Config file
from config import Config

def sendMail(recipient: list, textbody: str, smtppw: str):
    msg = EmailMessage()
    msg.set_content(textbody)

    # extra case if there is more than one mail address
    if len(recipient) > 1:
        # ensure the right format for sendMail()
        recipient = ",".join(recipient)

    msg['Subject'] = Config.MAIL_SUBJECT
    msg['From'] = Config.MAIL_SENDER
    msg['To'] = recipient

    # Send the message via SMTP server.
    s = smtplib.SMTP(Config.SMTP_SERVER)
    s.starttls()
    s.login("certcheck-notifications",smtppw)
    # comment next line for debugging, no mails will be send
    s.send_message(msg)
    s.quit()
