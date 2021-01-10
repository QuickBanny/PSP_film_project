from api.request.create_user import RequestCreateUserDto
from db.database import DBSession
from db.models import DBUserModel


def create_user(session: DBSession, user: RequestCreateUserDto) -> DBUserModel:
    new_user = DBUserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        email=user.email
    )

    session.add_model(new_user)

    return new_user