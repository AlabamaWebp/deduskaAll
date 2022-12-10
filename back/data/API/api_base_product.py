

from sqlalchemy import select, delete
from .db.base import Product, ProductSale, ProductType, engine


def get_product_sales_for_agent(ag_id: int = 1) -> dict:
    query = select(
            ProductSale.c.ID,
            ProductSale.c.SaleDate,
            select(Product.c.Title).where(ProductSale.c.ProductID == Product.c.ID).label("Product"),
            select(Product.c.MinCostForAgent * ProductSale.c.ProductCount).where(ProductSale.c.ProductID == Product.c.ID).label("PriceForAll"),
        ).where(
            ProductSale.c.AgentID == ag_id
        )
    values = engine.execute(query).fetchall()
    return values