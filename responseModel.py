from pydantic import BaseModel
from typing import Literal

class Opinion(BaseModel):
    for_or_against: Literal["for", "against", "non-indicative"]
    employee_or_employer: Literal["employee", "employer", "non-indicative"]
    promotional_or_opinion: Literal["promotional", "opinion", "non-indicative"]