from pydantic import BaseModel, validator

class Product(BaseModel):
    prod_id: int = 0
    prod_title: str = "product"
    prod_min_cost: int = 500

    @validator
    def min_cost_check(cls, v):
        if v < 0:
            raise ValueError("Цена ниже 0")
        return v