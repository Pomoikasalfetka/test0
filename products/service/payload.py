def payload_create_brand(
    *,
    name: str = "Test brand",
    description: str = "Test brand description",
):
    payload = {
        "name": name,
        "description": description,
    }
    return payload


def payload_create_category(
    *,
    name: str = "Test category",
    productTypeId: int = 1,
):
    payload = {
        "name": name,
        "productTypeId": productTypeId,
    }
    return payload


def payload_create_product(
    *,
    productId: str = "TEST001",
    productTypeId: int = 1,
    brandId: int = 1,
    providerId: int = 1,
    priority: int = 100,
    name: str = "Test product",
    categoryId: int = 1,
    salePrice: int | float = 1000,
    supplierPrice: int | float = 500,
    quantityInStock: str = "Много",
    active: int = 1,
    showOnLand: int = 1,
    img: list | None = None,
    descriptionAnnounce: str = "Новинка",
    descriptionDetail: str = "Подробное описание товара",
    comment: str | None = None,
    formId: int | None = None,
    descAny: dict | None = None,
    subCategoryId: int | None = None,
    vat: int = 5,
    keywords: str | None = None,
):
    product_data = {
        "productId": productId,
        "productTypeId": productTypeId,
        "brandId": brandId,
        "providerId": providerId,
        "name": name,
        "categoryId": categoryId,
        "salePrice": salePrice,
        "supplierPrice": supplierPrice,
        "quantityInStock": quantityInStock,
        "active": active,
        "showOnLand": showOnLand,
        "img": img or [{"imgType": "url", "imgData": "https://www.yandex.ru"}],
        "descriptionAnnounce": descriptionAnnounce,
        "descriptionDetail": descriptionDetail,
        "vat": vat,
        "descAny": descAny or {},
    }

    if priority is not None:
        product_data["priority"] = priority
    if comment is not None:
        product_data["comment"] = comment
    if formId is not None:
        product_data["formId"] = formId
    if subCategoryId is not None:
        product_data["subCategoryId"] = subCategoryId
    if keywords is not None:
        product_data["keywords"] = keywords

    payload = {
        "data": [product_data],
    }
    return payload
