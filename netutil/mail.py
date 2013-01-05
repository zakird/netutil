import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def sendmail(subject, message, sender='eecs398@umich.edu', to=[], cc=[], 
                bcc=[], attachments=[], priority=3, type_="plain", 
                smtp_server="smtp.eecs.umich.edu"):
    assert priority in range(1,6)
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(to)
    msg['Cc'] = COMMASPACE.join(cc)
    msg['X-Priority'] = str(priority)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, type_)) 

    for f in attachments:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f,"rb").read()) 
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'\
                        % os.path.basename(f))
        msg.attach(part)

    to.extend(cc)
    to.extend(bcc)
    smtp = smtplib.SMTP(smtp_server)
    smtp.sendmail(sender, to, msg.as_string())
    smtp.close()
