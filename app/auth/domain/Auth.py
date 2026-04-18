from auth.security.jwt import jwt_manager
from auth.security.hash import PasswordHasher
from auth.database.repository.user import UserRepo
from auth.models.user import UserLogin, UserRegister
from auth.models.tokens import TokenPair

class AuthServiсe:
    @staticmethod
    async def register(UserData: UserRegister) -> TokenPair:
        hash_password = PasswordHasher.hash_password(UserData.password)

        try:
            user = await (
                UserRepo.create_user(
                    UserData.login,
                    hash_password,
                    UserData.email,
                    UserData.name,
                    UserData.last_name,
                )
            )
        except ValueError as e:
            raise ValueError('error: as {e}') from e

        return TokenPair(
            access_token=jwt_manager.create_access_token({'user_id': user.id}),
            refresh_token=jwt_manager.create_refresh_token({'user_id': user.id}),
        )

    async def login(UserData: UserLogin) -> TokenPair:
        user = await UserRepo.login_user(UserData.login)
        if PasswordHasher.verify_password(UserData.password, user.hash_password):
            return TokenPair(
                access_token=jwt_manager.create_access_token({'user_id': user.id}),
                refresh_token=jwt_manager.create_refresh_token({'user_id': user.id}),
            )
        raise ValueError('Password not corect')