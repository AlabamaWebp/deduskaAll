from pydantic import BaseModel, validator
from pydantic import typing

class AgentBase(BaseModel):
    ag_id: int = 0
    ag_title: str = ""
    ag_priority: int = 0
    ag_type: str = ""
    ag_address: str = ""
    ag_director: str = ""
    ag_email: str = ""
    ag_phone: str = ""
    ag_inn: str = ""
    ag_kpp: str = ""
    ag_logo_path: str = "\\agents\\no_image.png"

    @validator("ag_title")
    def title_valid(cls, v):
        if len(v) < 3:
            # raise ValueError("Наименование может содержать только символы русского и латинского алфавитов")
            raise ValueError("Наименование не может быть меньше 3 символов")
        return v

    @validator("ag_phone")
    def phone_length(cls, v):
        if len(v) != 11:
            raise ValueError("Номер телефона должен быть из 11 цифр")
        return v

    @validator("ag_inn")
    def inn_length(cls, v):
        if len(v) != 10:
            raise ValueError("ИНН должен быть из 10 цифр")
        return v

    @validator("ag_kpp")
    def kpp_length(cls, v):
        if len(v) != 9:
            raise ValueError("КПП должен быть из 9 цифр")
        return v

class AgentFull(AgentBase):
    ag_sales: int = 0
    ag_disc: int = 0
    ag_image_byte: typing.Any = ""