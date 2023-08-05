from .customBaseModel import CustomBaseModel
from .Price_Logic import Price_Logic


class API_Call(CustomBaseModel):
    header: str
    price_logic : Price_Logic


