from pydantic import BaseModel, EmailStr, SecretStr, Field, ConfigDict

class RegisterUserRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    first_name: str
    last_name: str
    password: SecretStr = Field(min_length=8)
    confirm_password: SecretStr = Field(min_length=8)

class LoginUserRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: SecretStr

class CreateStoreRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    email: EmailStr
    description: str = ''

class CreateAddressRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    country: str
    address: str
    city: str
    province: str
    zip_code: int
    type: str
    is_active: bool = False