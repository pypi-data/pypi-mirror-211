from .customBaseModel import CustomBaseModel
from .Price_Logic import Price_Logic
import json

class API_Call(CustomBaseModel):
    spotOn_API_code: str
    price_logic : Price_Logic

    def as_json(self,escaped=False):

        API_Call_dict = self.to_dict()
        json_str = json.dumps(API_Call_dict)
        if escaped:
            json_str = json.dumps(json_str)

        return json_str