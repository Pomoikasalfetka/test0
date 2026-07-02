from products.service.methods_service import (
    create_brand,
    create_category,
)
from products.service.payload import payload_create_brand, payload_create_category
from providers.service.methods_service import create_provider
from providers.service.payload import payload_create_provider


def _prepare_provider_info(provider_info):
    partner = provider_info.get("partner", {})
    return {
        "id": provider_info["id"],
        "name": provider_info["name"],
        "description": provider_info["description"],
        "partnerId": provider_info.get("partnerId", partner.get("id")),
    }


def _prepare_brand_info(brand_info):
    return {
        "id": brand_info["id"],
        "name": brand_info["name"],
        "description": brand_info["description"],
    }


def _prepare_category_info(category_info):
    return {
        "id": category_info["id"],
        "name": category_info["name"],
        "productTypeId": category_info["productTypeId"],
    }


def create_provider_entity(
    *,
    headers,
    partner_id: int,
    provider_name: str,
    provider_description: str,
):
    provider_payload = payload_create_provider(
        name=provider_name,
        description=provider_description,
        partnerId=partner_id,
    )
    provider_response = create_provider(
        payload=provider_payload,
        headers=headers,
        raw_response=False,
    )

    provider_info = provider_response["response"]["providers"][0]
    return _prepare_provider_info(provider_info)


def create_brand_entity(
    *,
    headers,
    brand_name: str,
    brand_description: str,
):
    brand_payload = payload_create_brand(
        name=brand_name,
        description=brand_description,
    )
    brand_response = create_brand(
        payload=brand_payload,
        headers=headers,
        raw_response=False,
    )

    brand_info = brand_response["response"]["brands"][0]
    return _prepare_brand_info(brand_info)


def create_category_entity(
    *,
    headers,
    product_type_id: int,
    category_name: str,
):
    category_payload = payload_create_category(
        name=category_name,
        productTypeId=product_type_id,
    )
    category_response = create_category(
        payload=category_payload,
        headers=headers,
        raw_response=False,
    )

    category_info = category_response["response"]["categories"][0]
    return _prepare_category_info(category_info)


def prepare_base_product_entities(
    *,
    headers,
    partner_id: int,
    product_type_id: int,
    provider_name: str,
    provider_description: str,
    brand_name: str,
    brand_description: str,
    category_name: str,
):
    prepared_provider = create_provider_entity(
        headers=headers,
        partner_id=partner_id,
        provider_name=provider_name,
        provider_description=provider_description,
    )
    prepared_brand = create_brand_entity(
        headers=headers,
        brand_name=brand_name,
        brand_description=brand_description,
    )
    prepared_category = create_category_entity(
        headers=headers,
        product_type_id=product_type_id,
        category_name=category_name,
    )

    return {
        "provider": prepared_provider,
        "brand": prepared_brand,
        "category": prepared_category,
    }
