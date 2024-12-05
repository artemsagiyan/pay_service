from typing import Literal

from pydantic import BaseModel


class HealthcheckSchema(BaseModel):
    status: Literal["OK"]
    version: str
