from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import config
from app.scraper import Scraper
from app.storage import Storage
from app.notifications import Notification
from app.caching import Caching
from typing import Annotated

app = FastAPI()

# Dependency for simple static token authentication
def get_token_header(x_token: Annotated[str, Header(...)]):
    if x_token != config.STATIC_TOKEN:
        raise HTTPException(status_code=400, detail="Invalid Token")

class ScrapeRequest(BaseModel):
    pages: Optional[int] = 5
    proxy: Optional[str] = None

caching = Caching()
storage = Storage()

@app.post("/scrape", dependencies=[Depends(get_token_header)])
async def scrape(request: ScrapeRequest):
    scraper = Scraper(base_url=config.BASE_URL, proxy=request.proxy)
    products = scraper.scrape(pages=request.pages)

    updated_products = []

    for product in products:
        cache_key = product["product_title"]
        cached_product = await caching.get(cache_key)

        if cached_product:
            if cached_product["product_price"] != product["product_price"]:
                await caching.set(cache_key, product)
                updated_products.append(product)
            else:
                print(f"Price unchanged for product: {product['product_title']}")
        else:
            await caching.set(cache_key, product)
            updated_products.append(product)

    storage.save(updated_products)

    notification = Notification()
    notification.notify(f"Scraped {len(updated_products)} products")

    return {"message": f"Scraped {len(updated_products)} products"}
