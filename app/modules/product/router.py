from idlelib.query import Query
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from typing import Annotated
from app.infra.database import get_session
from app.modules.product.models import Product
from app.modules.product.schemas import ProductResponse
from app.modules.product.service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["products"])


async def get_product_service(
    session: AsyncSession = Depends(get_session),
) -> ProductService:
    yield ProductService(session)


@router.get("", response_model=list[ProductResponse])
async def list_products(
    category: str | None = None,
     service:ProductService=Depends(get_product_service)
) -> list[Product]:
    # 2.查询并返回产品列表
    return await service.list_products(category)

@router.get("/candidates", response_model=list[ProductResponse])
async def list_candidates(
    categories: list[str] = Query(min_length=1),
    premium_min: Decimal | None = None,
    limit_per_category: int = 5,
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponse]:
    return await service.list_candidates(
        categories=categories,
        premium_min=premium_min,
        limit_per_category=limit_per_category,
    )