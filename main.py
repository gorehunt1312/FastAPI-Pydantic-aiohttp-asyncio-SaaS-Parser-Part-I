from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ConfigDict, field_validator, model_validator, ValidationError  
from typing import Optional, List, Dict, Union
from datetime import datetime, date

app = FastAPI(
    title="app",
    description="without description",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

class ProductSchema(BaseModel):
    product_id: str = Field(min_lenght=5, max_length=12)
    price: float = Field(ge=10.0, le=1000000.0)
    category: str = "unknown"
    discount: int = Field(ge=0, le=90)
    empty_fields: Optional[str] = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
        populate_by_name=True
    )

@app.post(
    "/api/v1/ingest",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True
)
async def ready_data(payload: ProductSchema, response: Response):
    response.headers["X-App-Status"] = "Verified"
    return payload

#Step 1: python -m uvicorn main:app --reload