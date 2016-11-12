import os
import smtplib
from zipfile import ZipFile, ZIP_DEFLATED
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class Mailer:
    # Logger
    def __init__(self):
        pass

    def mail(self, text, folder_to_zip, mail_settings):

        zip_file = None
        folder_to_zip_name = folder_to_zip + ".zip"
        try:
            zip_file = self._create_zip_file(folder_to_zip, folder_to_zip_name)
            mail_msg = MIMEMultipart()
            mail_msg['Subject'] = mail_settings['subject']
            mail_msg['To'] = " ,".join(mail_settings['to'])
            mail_msg['From'] = mail_settings['from']

            mime_zip = MIMEBase("application", "zip")
            mime_zip.set_payload(zip_file.read())
            encoders.encode_base64(mime_zip)
            mime_zip.add_header("Content-Disposition", "attachment", filename=folder_to_zip_name)
            mail_msg.attach(mime_zip)

            mime_text = MIMEBase("text", "plain")
            mime_text.set_payload(text)
            mail_msg.attach(mime_text)

            self._send_mail(mail_msg, mail_settings)
        except Exception as e:
            # Log?
            print "EXCEPTION: {}".format(e)
            return False
        finally:
            if zip_file:
                zip_file.close()

        return True

    @staticmethod
    def _send_mail(mail_msg, mail_settings):

        # http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
        smtp = smtplib.SMTP_SSL(host=mail_settings['smtp_server'], port=mail_settings['smtp_port'])
        smtp.ehlo()
        smtp.login(mail_settings['smtp_user'], mail_settings['smtp_password'])
        smtp.sendmail(mail_settings['from'], mail_settings['to'], mail_msg.as_string())
        smtp.close()

    @staticmethod
    def _create_zip_file(folder_to_zip, folder_to_zip_name):

        zip_file = ZipFile(folder_to_zip_name, "w", ZIP_DEFLATED)

        for root, dirs, files in os.walk(folder_to_zip):
            for f in files:
                zip_file.write(os.path.join(folder_to_zip, f))

        zip_file.close()
        zip_file = open(folder_to_zip_name, "r")

        return zip_file
