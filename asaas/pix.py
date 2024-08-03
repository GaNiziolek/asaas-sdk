from typing import Optional
from urllib.parse import urljoin
from datetime import datetime

class Pix:
    def __init__(self,
        success: bool,
        encodedImage: str,
        payload: str,
        expirationDate: datetime | str
    ) -> None:
        
        self.success         = success 
        self.expirationDate = expirationDate if type(expirationDate) == datetime else datetime.fromisoformat(expirationDate)
        self.encodedImage   = encodedImage 
        self.payload        = payload 

    def __repr__(self) -> str:
        return f'Pix(success={self.success}, expirationDate={self.expirationDate})'