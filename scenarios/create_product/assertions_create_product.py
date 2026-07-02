def assert_prepared_base_product_entities(testcase, result, prepare_data):
    testcase.assertGreater(result["provider"]["id"], 0)
    testcase.assertEqual(result["provider"]["name"], prepare_data["provider_name"])
    testcase.assertGreater(result["brand"]["id"], 0)
    testcase.assertEqual(result["brand"]["name"], prepare_data["brand_name"])
    testcase.assertGreater(result["category"]["id"], 0)
    testcase.assertEqual(result["category"]["name"], prepare_data["category_name"])


def assert_created_product_matches_entities(testcase, result):
    product = result["product"]
    category = result["category"]
    product_payload = result["product_payload"]

    testcase.assertEqual(product["productTypeId"], category["productTypeId"])
    testcase.assertEqual(
        product["productTypeId"],
        product_payload["data"][0]["productTypeId"],
    )
    testcase.assertEqual(product["categoryId"], category["id"])
    testcase.assertEqual(product["providerId"], result["provider"]["id"])
    testcase.assertEqual(product["brandId"], result["brand"]["id"])
