from pydantic import BaseModel


class UserSchema(BaseModel):
    tg_id: int
    city: str
    address: str
    fio: str
    nickname: str

