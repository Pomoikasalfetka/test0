
def assert_add_from_basket_result(testcase, result , msg):
    testcase.assertEqual(
        result["basket_response"]["response"]["msg"],
        msg
    )
  

def assert_buy_from_basket_result(testcase, result , msg):
    testcase.assertEqual(
        result["order_response"]["response"]["msg"],
        msg
    )

