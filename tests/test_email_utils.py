from unittest import mock

from test_constants import SAMPLE_MESSAGE
import email_utils


def test_get_top_consecutive_capitalized_words():
    test_cases = {
        (
            ("Hello", 10),  # capitalized, highest frequency, prioritize
            ("World", 8),  # capitalized, lower frequency, ignore
        ): "Hello",
        (
            ("Hello", 10),  # capitalized, highest frequency, prioritize
            ("World", 10),  # capitalized, highest frequency, add to result
            ("How", 5),  # capitalized, lower frequency, ignore
        ): "Hello World",
        (
            ("hello", 5),  # not capitalized, highest frequency, ignore
            ("World", 5),  # capitalized, highest frequency, prioritize
            ("How", 5),  # capitalized, highest frequency, add to result
            ("are", 5),  # not capitalized, highest frequency, ignore
        ): "World How",
        (
            ("hello", 5),  # not capitalized, highest frequency, ignore
            ("world", 5),  # capitalized, highest frequency, prioritize
            ("how", 5),  # capitalized, highest frequency, add to result
            ("are", 5),  # not capitalized, highest frequency, ignore
        ): "",  # no consecutive capitalized words
    }
    for word_list, expected_value in test_cases.items():
        result = email_utils.get_top_consecutive_capitalized_words(word_list)
        assert result == expected_value


def test_is_valid_email():
    email_test_cases = {
        "no-reply@gmail.com": True,
        "no-reply@example.com": False,  # Invalid domain
        "no-reply.com": False,  # Missing @
    }
    for email, expected_value in email_test_cases.items():
        is_valid = email_utils.is_valid_email(email)
        assert is_valid == expected_value, f" email: {email}"


def test_is_email_automated():
    email_test_cases = {
        "no-reply@example.com": True,
        "team@hi.wellfound.com": True,
        "hello@otta.com": True,
        "do-not-reply@example.com": True,
        "notifications@smartrecruiters.com": True,
        "person@yesimreal.com": False,
    }
    for email, expected_value in email_test_cases.items():
        is_automated = email_utils.is_automated_email(email)
        assert is_automated == expected_value, f" email: {email}"


def test_get_email_subject_line():
    subject_line = email_utils.get_email_subject_line(SAMPLE_MESSAGE)
    assert (
        subject_line
        == "Invitation from an unknown sender: Interview with \
            TestCompanyName @ Thu May 2, 2024 11:00am - 12pm (PDT) \
                (appuser@gmail.com)"
    )


def test_get_email_from_address():
    from_address = email_utils.get_email_from_address(SAMPLE_MESSAGE)
    assert from_address == "recruitername@testcompanyname.com"


def test_get_email_domain():
    from_email_domain = email_utils.get_email_domain_from_address(
        "recruitername@testcompanyname.com"
    )
    assert from_email_domain == "testcompanyname.com"


def test_get_company_name_returns_email_domain():
    company_name = email_utils.get_company_name(id="abc123", msg=SAMPLE_MESSAGE)
    assert company_name == "testcompanyname"


def test_get_company_name_returns_top_word():
    """Default behavior for company name is to return the 
    highest frequency word that appears in the email body."""
    with mock.patch("email_utils.get_top_word_in_email_body", return_value="fake"):
        company_name = email_utils.get_company_name(id="abc123", msg=SAMPLE_MESSAGE)
        assert company_name == "fake"


def test_get_email_received_at_timestamp():
    received_at = email_utils.get_received_at_timestamp(1, SAMPLE_MESSAGE)
    assert received_at == "Thu, 2 May 2024 16:45:00 +0000"
