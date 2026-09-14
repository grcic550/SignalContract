from signalcontract.privacy import contains_private_fields


def test_contains_private_fields_with_dict():
    """Test that contains_private_fields returnes True
    when a dictionary contains a private field."""

    data = {"username": "user1", "password": "secret"}

    assert contains_private_fields(data) is True


def test_contains_private_fields_with_nested_dict():
    """Test that contains_private_fields returnes True
    when a nested dictionary contains a private field."""

    data = {"user": {"username": "user1", "password": "p@ssw0rd"}}

    assert contains_private_fields(data) is True


def test_contains_private_fields_with_list():
    """Test that contains_private_fields returnes True
    when a list contains a dictionary with a private fields."""

    data = [{"username": "user1", "password": "secret"}]

    assert contains_private_fields(data) is True


def test_contains_private_fields_with_nested_list():
    """Test that contains_private_fields returnes True
    when a nested list contains a dictionary with a
    private fields."""

    data = [{"users": [{"username": "user1", "password": "p@ssw0rd"}]}]

    assert contains_private_fields(data) is True


def test_contains_private_fields_returns_false_for_safe_dict():
    """Test that contains_private_fields returnes False
    when a dictionary does not contain any private fields."""

    data = {"username": "user1", "email": "user@user.com"}

    assert contains_private_fields(data) is False


def test_contains_private_fields_returns_false_for_nested_dict():
    """Test that contains_private_fields returnes False
    when a nested dictionary foes not contain any private fields."""

    data = {"user": {"username": "user1", "email": "user@user.com"}}

    assert contains_private_fields(data) is False


def test_contains_private_fields_returns_false_for_list():
    """Test that contains_private_fields returnes False
    when a list does not contain any private fields."""

    data = [{"username": "user", "email": "user@user.com"}]

    assert contains_private_fields(data) is False


def test_contains_private_fields_returns_false_for_nested_list():
    """Test that contains_private_fields returnes False
    when a nested list does not contain any private fields."""

    data = [{"users": [{"username": "user", "email": "user@user.com"}]}]

    assert contains_private_fields(data) is False


def test_contains_private_fields_is_case_instensitive():
    """Test that contains_private_fields is case
    insensitive when checking for private fields."""

    data = {"username": "user", "PASSWORD": "p@ssw0rd"}

    assert contains_private_fields(data) is True


def test_contains_private_fields_does_not_treat_values_as_field_names():
    """Test that contains_private_fields does not treat
    values as field names."""

    data = {"reason": "password"}

    assert contains_private_fields(data) is False


def test_contains_private_fields_returns_false_for_non_container():
    """Test that contains_private_fields returns False
    for non-container types"""

    assert contains_private_fields("hello") is False
