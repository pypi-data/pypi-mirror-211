import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from ..tkaws import Tks3, Tkses



class Tkemail:
    def __init__(self, from_email=None):
        # Create a multipart/alternative child container.
        self.message = MIMEMultipart('mixed')
        self.message_body = MIMEMultipart('alternative')
        # The character encoding for the email.
        self.from_email = from_email
        self.to_emails = list()
        self.cc_emails = list()
        self.bcc_emails = list()
        self.subject = ""
        self.CHARSET = "utf-8"

    def add_sender(self, from_email):
        self.from_email = from_email
        return self

    def add_recipient(self, email_address_list):
        self.to_emails = email_address_list
        self.message['To'] = ','.join([str(elem) for elem in email_address_list])
        return self

    def add_email_in_cc(self, email_address_list):
        if type(email_address_list) == type(list()):
            self.cc_emails = email_address_list
            self.message['Cc'] = ','.join([str(elem) for elem in email_address_list])
        else:
            raise ValueError("Email address is not a list")
        return self

    def add_email_in_bcc(self, email_address_list):
        self.bcc_emails = email_address_list
        self.message['Bcc'] = ','.join([str(elem) for elem in email_address_list])
        return self

    def add_subject(self, email_subject):
        self.subject = email_subject
        self.message['Subject'] = email_subject
        return self

    def add_attachment(self, file_path):
        file_path_list = file_path
        if type(file_path) == type(""):
            file_path_list = [file_path]
        elif type(file_path) != type(list()):
            raise ValueError("File path must be a string or list of string.")
        # The full path to the file that will be attached to the email.
        for attachment in file_path_list:
            # Define the attachment part and encode it using MIMEApplication.
            att = MIMEApplication(open(attachment, 'rb').read())
            # Add a header to tell the email client to treat this part as an attachment,
            # and to give the attachment a name.
            att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
            self.message.attach(att)
        return self

    def add_attachment_from_s3(self, s3_bucket, s3_key):
        s3_file = Tks3().get_file_content(s3_bucket, s3_key)
        # Define the attachment part and encode it using MIMEApplication.
        att = MIMEApplication(s3_file)
        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        att.add_header('Content-Disposition', 'attachment', filename=os.path.basename("/"))
        return self

    def add_body(self, body_text):
        textpart = MIMEText(body_text.encode(self.CHARSET), 'plain', self.CHARSET)
        self.message_body.attach(textpart)
        return self

    def add_html_body(self, html_body):
        htmlpart = MIMEText(html_body.encode(self.CHARSET), 'html', self.CHARSET)
        self.message_body.attach(htmlpart)
        return self

    def send(self):
        self.message.attach(self.message_body)
        email_response = Tkses().send_email(self)
        return email_response
