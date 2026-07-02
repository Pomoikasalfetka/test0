from basket.service.methods_service import add_product_to_basket, create_order_from_basket
from basket.service.payload import (
    payload_add_product_to_basket,
    payload_create_order_from_basket,
)


def add_to_basket_scenario(
    *,
    user_headers,
    product_id,
    quantity,
):
    basket_payload = payload_add_product_to_basket(
        productId=product_id,
        quantity=quantity,
    )
    basket_response = add_product_to_basket(
        payload=basket_payload,
        headers=user_headers,
        raw_response=False,
    )

    return {
        "basket_payload": basket_payload,
        "basket_response": basket_response,
    }


def buy_from_basket_scenario(
    *,
    user_headers,
    contact_id,
    product_type_id,
    comment,
    delivery_type_id,
    skip_send_2_sd,
    coupon_id=None,
):
    order_payload = payload_create_order_from_basket(
        productTypeId=product_type_id,
        comment=comment,
        contactId=contact_id,
        deliveryTypeId=delivery_type_id,
        skipSend2SD=skip_send_2_sd,
        couponId=coupon_id,
    )
    order_response = create_order_from_basket(
        payload=order_payload,
        headers=user_headers,
        raw_response=False,
    )

    return {
        "order_payload": order_payload,
        "order_response": order_response,
    }
