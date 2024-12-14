from pydantic import BaseModel


class CompanySchema(BaseModel):
    company_id: int
    name: str

    class Config:
        from_attributes = True
