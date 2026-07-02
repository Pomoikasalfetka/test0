from products.service.methods_service import create_product
from products.service.payload import payload_create_product


def create_product_type_1_scenario(
    *,
    headers,
    product_type_id: int,
    product_id: str,
    product_name: str,
    sale_price: int | float,
    supplier_price: int | float,
    quantity_in_stock: str,
    active: int,
    show_on_land: int,
    description_announce: str,
    description_detail: str,
    vat: int,
    provider: dict | None = None,
    brand: dict | None = None,
    category: dict | None = None,
):

    if provider is None or brand is None or category is None:
        raise AssertionError(
            "Base product entities are not prepared. "
            "Run create_product scenario setup first."
        )

    product_payload = payload_create_product(
        productId=product_id,
        productTypeId=product_type_id,
        brandId=brand["id"],
        providerId=provider["id"],
        name=product_name,
        categoryId=category["id"],
        salePrice=sale_price,
        supplierPrice=supplier_price,
        quantityInStock=quantity_in_stock,
        active=active,
        showOnLand=show_on_land,
        descriptionAnnounce=description_announce,
        descriptionDetail=description_detail,
        vat=vat,
    )
    product_response = create_product(
        payload=product_payload,
        headers=headers,
        raw_response=False,
    )
    product_info = product_response["response"]["products"][0]
    prepared_product = {
        "id": product_info["id"],
        "productId": product_info["productId"],
        "productTypeId": product_info["productTypeId"],
        "brandId": product_info["brandId"],
        "providerId": product_info["providerId"],
        "name": product_info["name"],
        "categoryId": product_info["categoryId"],
        "salePrice": product_info["salePrice"], 
    }

    return {
        "provider": provider,
        "brand": brand,
        "category": category,
        "product_payload": product_payload,
        "product_response": product_response,
        "product": prepared_product,
    }
