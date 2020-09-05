

def test_encode_auth_token(client, user):
    """Test user jwt encode method """
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)
    assert user.decode_auth_token(auth_token) == 1
