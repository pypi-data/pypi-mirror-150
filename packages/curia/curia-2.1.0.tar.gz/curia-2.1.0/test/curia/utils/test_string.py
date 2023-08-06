from curia.utils.string import to_camel_case, to_snake_case, to_lower_camel_case


def test_to_camel_case():
    assert to_camel_case("snake_string") == "SnakeString"
    assert to_camel_case("a_snake_string") == "ASnakeString"
    assert to_camel_case("asnake_string") == "AsnakeString"
    assert to_camel_case("longer_snake_string") == "LongerSnakeString"
    assert to_camel_case("short") == "Short"
    assert to_camel_case("") == ""
    assert to_camel_case("55052_12321_123") == "5505212321123"


def test_to_lower_camel_case():
    assert to_lower_camel_case("snake_string") == "snakeString"
    assert to_lower_camel_case("a_snake_string") == "aSnakeString"
    assert to_lower_camel_case("asnake_string") == "asnakeString"
    assert to_lower_camel_case("longer_snake_string") == "longerSnakeString"
    assert to_lower_camel_case("short") == "short"
    assert to_lower_camel_case("") == ""
    assert to_lower_camel_case("55052_12321_123") == "5505212321123"


def test_to_snake_case():
    assert to_snake_case("SnakeString") == "snake_string"
    assert to_snake_case("ASnakeString") == "a_snake_string"
    assert to_snake_case("AsnakeString") == "asnake_string"
    assert to_snake_case("LongerSnakeString") == "longer_snake_string"
    assert to_snake_case("Short") == "short"
    assert to_snake_case("") == ""
    assert to_snake_case("5505212321123") == "5505212321123"
    assert to_snake_case("55052123211B23") == "55052123211_b23"