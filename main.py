import imaplib
import email
import email.header
import sys
from chatbot import ChatBot 


class ImapClient:
  def __init__(self, recipent, server='imap.gmail.com', use_ssl=True, move_to_trash=True):
    # Check if to_who has been set
    if not recipent:
      raise ValueError('You must tell me who you sending it to retard')
    self.to_who = recipent
    self.user_ssl = use_ssl
    self.move_to_trash = move_to_trash
    self.to_who_folder = 'INBOX'
    if self.user_ssl:
      self.imap = imaplib.IMAP4_SSL(server)
    else:
      self.imap = imaplib.IMAP4(server)
  def login(self, passw):
    try:
      rv, data = self.imap.login(self.to_who, passw)
    except (imaplib.IMAP4_SSL.error, imaplib.IMAP4.error) as err:
      print('Failed how can you forget your own login')
      print(err)
      sys.exit(1)
  def logout(self):
    self.imap.close()
    self.imap.logout()
  def get_folder(self, folder):
    # Select forlder to read defualt is INBOX
    self.to_who_folder = folder
  def get_messages(self, sender, subject=''):
    if not sender:
      raise ValueError('You must provide a email address stupid')
    resp, _ = self.imap.select(self.to_who_folder)
    if resp != 'OK':
      print(f'Error: can not open the  {self.to_who_folder} folder')
      sys.exit(1)
    messages = []
    mbox_response, msgnums = self.imap.search(None, 'FROM', sender)
    if mbox_response == 'OK':
      for num in msgnums[0].split():
        retval, rawmsg =  self.imap.fetch(num, '(RFC822)')
        if retval != 'OK':
          print('Error getting message', num)
          continue
        msg = email.message_from_bytes(rawmsg[0][1])
        body = ""
        if msg.is_multipart():
          for part in msg.walk():
            type = part.get_content_type()
            disp = str(part.get('Content-Disposition'))
            if type == 'text/plain' and 'attachment' not in disp:
              charset = part.get_content_charset()
              # decode base 64 unicode bytestring into plain text
              body = part.get_payload(decode=True).decode(encoding=charset, errors='ignore')
              messages.append({'num':num, 'body': body})
        else:
          # if not is_multipart
          charset = msg.get_content_charset()
          body = msg.get_payload(decode=True).decode(encoding=charset, errors='ignore')
          messages.append({'num': num, 'body':body})
    return messages
  def delete_msg(self, msg_id):
    if not msg_id:
      return
    if self.move_to_trash:
      self.imap.store(msg_id, '+X-GM-Labels', '\\Trash')
      self.imap.expunge()
    else:
      self.imap.store(msg_id, 'FLAGS', '\\Deleted')
      self.imap.expunge()
def main(helper):
  while True:
    imap = ImapClient(recipent=helper.email)
    imap.login(helper.passd)
    messages = imap.get_messages(sender='yournum and num provider')
    recents = []
    for msg in messages:
      # msg is dict {'num': num, 'body': body}
      recents.append(msg['body'])
      imap.delete_msg(msg['num'])
    imap.logout()
    message = " ".join(recents)
    reply = helper.reply(message)
    if message != '':
      print('User said:', message)
      print('I replied:', reply)
      helper.send_text(to_who='your num', subject='Your Assitant'+helper.name, to_who_provider='your num provider', message=reply)
    del imap


if __name__ == "__main__":
  print('Starting')
  helper = ChatBot(emails='your email', passd='your pass', name='CJ')
  main(helper)
