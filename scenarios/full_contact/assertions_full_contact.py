def assert_created_full_contact(testcase, result, full_contact_data):
    testcase.assertEqual(
        result["contact"]["email"],
        full_contact_data["email"],
    )
    testcase.assertEqual(
        result["card"]["cardNumber"],
        full_contact_data["card_number"],
    )
    testcase.assertEqual(result["link"]["status"], 1)
