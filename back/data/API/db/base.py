from sqlalchemy import engine, create_engine
from sqlalchemy import Column, Table
from sqlalchemy import String, Integer, DECIMAL, Float, Date
from sqlalchemy import ForeignKey, MetaData

from ...settings import conn_string

engine = create_engine(conn_string, echo=False)
meta = MetaData(engine)

ProductSale = Table(
    "ProductSale", meta,
    Column("ID", Integer, primary_key=True, autoincrement=True),
    Column("AgentID", Integer, ForeignKey("Agent.ID"), nullable=False),
    Column("ProductID", Integer, ForeignKey("Product.ID"), nullable=False),
    Column("SaleDate", Date, nullable=False),
    Column("ProductCount", Integer, nullable=False),
)

Agent = Table(
    "Agent", meta,
    Column("ID", Integer, primary_key=True, autoincrement=True),
    Column("Title", String(150), nullable=False),
    Column("AgentTypeID", Integer, ForeignKey("AgentType.ID"), nullable=False),
    Column("Address", String(300), nullable=False),
    Column("INN", String(12), nullable=False),
    Column("KPP", String(9), nullable=False),
    Column("DirectorName", String(100), nullable=False),
    Column("Phone", String(20), nullable=False),
    Column("Email", String(255), nullable=False),
    Column("Logo", String(100), nullable=False),
    Column("Priority", Integer, nullable=False),
    # ForeignKeyConstraint( ["ID"], [ProductSale.ID], name="FK_ProductSale_Agent" )
)


AgentType = Table(
    "AgentType", meta,
    Column("ID", Integer, primary_key=True, autoincrement=True),
    Column("Title", String(50), nullable=False),
    # ForeignKeyConstraint( ["ID"], [Agent.ID], name="FK_Agent_AgentType" )
)


Product = Table(
    "Product", meta,
    Column("ID", Integer, primary_key=True, autoincrement=True),
    Column("Title", String(150), nullable=False),
    Column("ProductTypeID", Integer, ForeignKey("ProductType.ID"), nullable=False),
    Column("ArticleNumber", String(10), nullable=False),
    Column("Description", String, nullable=True),
    Column("Image", String(100), nullable=True),
    Column("ProductPersonCount", Integer, nullable=False),
    Column("ProductWorkshopCount", Integer, nullable=False),
    Column("MinCostForAgent", DECIMAL(10, 2), nullable=False),
    # ForeignKeyConstraint( ["ID"], [ProductSale.ID], name="FK_ProductSale_Product" )
)


ProductType = Table(
    "ProductType", meta,
    Column("ID", Integer, primary_key=True, autoincrement=True),
    Column("Title", String(50), nullable=False),
    Column("DefectedPercent", Float, nullable=False),
    # ForeignKeyConstraint( ["ID"], [Product.ID], name="FK_Product_ProductType" )
)

def create_tables_if_not_exists():
    meta.create_all()