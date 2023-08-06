import pytest

from cbu_tools.src.cbu import CBU

def test_valid_cbu():
    valid_cbu_numbers = [
        "0170099220000067797370",
        "0290000111000558907080",
        "0290000111000558907080",
        "0170508920000000000417",
        "0340100800100586333009"
    ]

    for cbu_number in valid_cbu_numbers:
        cbu = CBU(cbu_number)
        assert cbu.is_valid() == True

def test_invalid_cbu():
    invalid_cbu_numbers = [
        "0170099220000067797371",
        "0290000111000558907081",
        "0290000111000558907081",
        "0170508920000000000418",
        "0340100800100586333000"
    ]

    for cbu_number in invalid_cbu_numbers:
        cbu = CBU(cbu_number)
        assert cbu.is_valid() == False

@pytest.mark.parametrize(
    "cbu_number, error_type, expected_error",
    [
        ("01700992200000677973A0", ValueError, "CBU can't contain non-numeric characters (such as spaces, dots, hyphens, etc)"),
        ("01700 99220000067797370", ValueError, "CBU can't contain non-numeric characters (such as spaces, dots, hyphens, etc)"),
        ("01700-99220000067797370", ValueError, "CBU can't contain non-numeric characters (such as spaces, dots, hyphens, etc)"),
        ("0170099220000067797370123", ValueError, "CBU must be exactly 22 digits"),
        (1234567890, TypeError, "CBU must be provided in string format"),
    ],
)
def test_cbu_errors(cbu_number, error_type, expected_error):
    with pytest.raises(error_type) as exc_info:
        cbu = CBU(cbu_number)
        cbu.is_valid()

    assert str(exc_info.value) == expected_error