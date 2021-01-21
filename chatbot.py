import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
class ChatBot:
  def __init__(self, emails, passd, name):
    self.email = emails
    self.passd = passd
    self.name = name
  def reply(self, text):
    return 'hey'
  def send_text(self, to_who, subject, to_who_provider, message):
    sms_gateway = to_who + to_who_provider
    smtp = 'smtp.gmail.com'
    port = 587
    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.login(self.email, self.passd)
    msg = MIMEMultipart()
    msg['From'] = self.email
    msg['To'] = sms_gateway
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    sms = msg.as_string()
    server.sendmail(self.email, sms_gateway, sms)
    server.quit()
