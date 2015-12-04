from app.models import User


def retrieve_user(user_id):
    user = User(id=1,
                user_name="test@user.com",
                api_key="1234asdf5678",
                org="gov.uk")

    return user
