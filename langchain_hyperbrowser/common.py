from typing import Optional, List
from pydantic import BaseModel, Field
from hyperbrowser.models import Country, ScrapeFormat


class SimpleSessionParams(BaseModel):
    use_proxy: bool = Field(default=False, serialization_alias="useProxy")
    proxy_country: Optional[Country] = Field(
        default=None, serialization_alias="proxyCountry"
    )
    solve_captchas: bool = Field(default=False, serialization_alias="solveCaptchas")
    adblock: bool = Field(default=False, serialization_alias="adblock")


class SimpleScrapeOptions(BaseModel):
    formats: List[ScrapeFormat] = Field(default=["markdown"])
