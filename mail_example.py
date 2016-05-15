import smtplib
import os
 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
 
gmail_user = "[FROM:EMAIL]"
gmail_pwd = "[FROM:EMAILPAWSSWORD]"
 
def mail(to, subject, text, attach):
   msg = MIMEMultipart()
 
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
 
   msg.attach(MIMEText(text))
 
   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   encoders.encode_base64(part)
   part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)
 
   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()
 
mail("[TO:EMAIL]","Hello from python!","This is a email sent with python","README.md")