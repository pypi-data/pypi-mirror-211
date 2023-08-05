from tests.setup import test_setup
from src.tkaws import TkS3


def test_s3():
    s3 = TkS3()
    file = s3.get_file_content("gurugyaan", "wide.webp")
    return True



test_setup()
test_s3()
