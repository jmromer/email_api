from pydantic import BaseModel, Field


class Email(BaseModel):
    to_email: str = Field(str, alias="to")
    to_name: str
    from_email: str = Field(str, alias="from")
    from_name: str
    subject: str
    body: str
