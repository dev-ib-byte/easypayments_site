# import datetime
#
# import jwt
#
# from src.config.settings import JWTSettings
#
#
# class JWTManager:
#     def __init__(self, settings: JWTSettings):
#         self.jwt_settigns = settings.jwt
#
#     def create_access_token(self, data: UserCreateDTO) -> str:
#         payload = self.create_payload(data, token_type=TokenType.ACCESS)
#         return jwt.encode(
#             payload,
#             self.jwt_settigns.secret_key,
#             algorithm=self.jwt_settigns.algorithm,
#         )
#
#     def create_refresh_token(self, data: UserCreateDTO) -> str:
#         payload = self.create_payload(data, token_type=TokenType.REFRESH)
#         return jwt.encode(
#             payload,
#             self.jwt_settigns.secret_key,
#             algorithm=self.jwt_settigns.algorithm,
#         )
#
#     def verify_token(self, token: str) -> dict:
#         try:
#             payload = jwt.decode(
#                 token,
#                 self.jwt_settigns.secret_key,
#                 algorithms=[self.jwt_settigns.algorithm],
#             )
#             return payload
#         except jwt.ExpiredSignatureError:
#             raise ValueError("Token has expired")
#         except jwt.InvalidTokenError:
#             raise ValueError("Invalid token")
#
#     def decode_refresh_token(self, token: str) -> dict:
#         payload = self.verify_token(token)
#
#         if payload.get("token_type") != TokenType.REFRESH.value:
#             raise ValueError("Provided token is not a refresh token")
#
#         return payload
#
#     def create_payload(self, data: UserCreateDTO, token_type: TokenType) -> dict:
#         if token_type == TokenType.REFRESH:
#             expire = datetime.datetime.now() + datetime.timedelta(
#                 days=self.jwt_settigns.refresh_token_expire_days
#             )
#         else:
#             expire = datetime.datetime.now() + datetime.timedelta(
#                 minutes=self.jwt_settigns.access_token_expire_minutes
#             )
#
#         return {
#             "token_type": token_type.value,
#             "email": data.email,
#             "exp": expire,
#             "user_id": data.user_id,
#             "role": data.role,
#         }
