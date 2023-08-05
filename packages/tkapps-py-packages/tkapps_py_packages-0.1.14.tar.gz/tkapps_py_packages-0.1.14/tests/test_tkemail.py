from tests.setup import test_setup
from src.tkemail import Tkemail


def test_email_message():
    email_message = Tkemail()
    email_message.add_sender("noreply@zerospam.club")
    email_message.add_recipient(['gurugyaan@gmail.com'])
    email_message.add_email_in_cc(['ranjan.gyaan@gmail.com'])
    email_message.add_subject("Test Email for common Repository")
    email_message.add_body("Hello")
    email_message.add_html_body("<p>Hello Gyaan</p>")
    email_message.add_attachment(["/Users/gyanranjan/Desktop/python.zip"])
    # email_message.add_attachment_from_s3("/gyaan.pdf", "test_bucket")
    email_response = email_message.send()
    return email_response



test_setup()
test_email_message()
