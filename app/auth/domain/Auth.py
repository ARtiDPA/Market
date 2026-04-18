from app.auth.security.jwt import jwt_manager
from app.auth.security.hash import PasswordHasher
from app.auth.database.repository.user import UserRepo
from app.auth.schemas.user import UserLogin, UserRegister
from app.auth.schemas.tokens import TokenPair

class AuthService:
    @staticmethod
    async def register(user_data: UserRegister) -> TokenPair:
        hash_password = PasswordHasher.hash_password(user_data.password)

        try:
            user = await (
                UserRepo.create_user(
                    user_data.login,
                    hash_password,
                    user_data.email,
                    user_data.name,
                    user_data.last_name,
                )
            )
        except ValueError as e:
            raise ValueError('error: as {e}') from e

        return TokenPair(
            access_token=jwt_manager.create_access_token({'user_id': user.id}),
            refresh_token=jwt_manager.create_refresh_token({'user_id': user.id}),
        )
    
    @staticmethod
    async def login(user_data: UserLogin) -> TokenPair:
        user = await UserRepo.login_user(user_data.login)
        if PasswordHasher.verify_password(user_data.password, user.hash_password):
            return TokenPair(
                access_token=jwt_manager.create_access_token({'user_id': user.id}),
                refresh_token=jwt_manager.create_refresh_token({'user_id': user.id}),
            )
        raise ValueError('Password not corect')
