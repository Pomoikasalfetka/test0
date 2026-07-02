SCENARIO_RUNNERS = {
    "full_contact": {
        "runner_module": "scenarios.full_contact.test_create_full_contact",
        "runner_function": "run_full_contact_scenario",
    },
    "create_product": {
        "runner_module": "scenarios.create_product.test_create_product",
        "runner_function": "run_create_product_scenario",
    },
    "create_provider": {
        "runner_module": "scenarios.create_product.test_create_entities",
        "runner_function": "run_create_provider_scenario",
    },
    "create_brand": {
        "runner_module": "scenarios.create_product.test_create_entities",
        "runner_function": "run_create_brand_scenario",
    },
    "create_category": {
        "runner_module": "scenarios.create_product.test_create_entities",
        "runner_function": "run_create_category_scenario",
    },
    "add_to_basket": {
        "runner_module": "scenarios.work_with_basket.test_add_to_basket",
        "runner_function": "run_add_to_basket_scenario",
    },
    "buy_from_basket": {
        "runner_module": "scenarios.work_with_basket.test_buy_from_basket",
        "runner_function": "run_buy_from_basket_scenario",
    },
    "create_promotion": {
        "runner_module": "scenarios.promotions.test_create_promotion",
        "runner_function": "run_create_promotion_scenario",
    },
    "create_coupons": {
        "runner_module": "scenarios.promotions.test_create_coupons",
        "runner_function": "run_create_coupons_scenario",
    },
    "create_operation": {
        "runner_module": "scenarios.operations.test_create_operation",
        "runner_function": "run_create_operation_scenario",
    },
    "insert_operation": {
        "runner_module": "scenarios.operations.test_insert_operation",
        "runner_function": "run_insert_operation_scenario",
    },
    "update_operation_source_id": {
        "runner_module": "scenarios.operations.test_update_operation_source_id",
        "runner_function": "run_update_operation_source_id_scenario",
    },
    "activate_coupon": {
        "runner_module": "scenarios.promotions.test_create_activation",
        "runner_function": "run_create_activation_coupon",
    },
    "auto_activate_coupons_by_operations": {
        "runner_module": "scenarios.promotions.test_auto_activate_coupons_by_operations",
        "runner_function": "run_auto_activate_coupons_by_operations_scenario",
    },
    "check_contact_status": {
        "runner_module": "scenarios.new_condition.test_check_contact_status",
        "runner_function": "run_check_contact_status_scenario",
    },
    "check_card_status": {
        "runner_module": "scenarios.new_condition.test_check_card_status",
        "runner_function": "run_check_card_status_scenario",
    },
    "check_contact_lock_date": {
        "runner_module": "scenarios.new_condition.test_check_contact_lock_date",
        "runner_function": "run_check_contact_lock_date_scenario",
    },
    "check_contact_count_ops": {
        "runner_module": "scenarios.new_condition.test_check_contact_count_ops",
        "runner_function": "run_check_contact_count_ops_scenario",
    },
    "check_contact_token_burn_date": {
        "runner_module": "scenarios.new_condition.test_check_contact_token_burn_date",
        "runner_function": "run_check_contact_token_burn_date_scenario",
    },
    "check_contact_date_of_demotion": {
        "runner_module": "scenarios.new_condition.test_check_contact_date_of_demotion",
        "runner_function": "run_check_contact_date_of_demotion_scenario",
    },
    "check_contact_last_add_operation_id": {
        "runner_module": "scenarios.new_condition.test_check_contact_last_add_operation_id",
        "runner_function": "run_check_contact_last_add_operation_id_scenario",
    },
    "calculate_client_status": {
        "runner_module": "scenarios.new_condition.test_calculate_client_status",
        "runner_function": "run_calculate_client_status_scenario",
    },
    "reset_contact": {
        "runner_module": "scenarios.new_condition.test_reset_contact",
        "runner_function": "run_reset_contact_scenario",
    },
    "delay": {
        "runner_module": "scenarios.new_condition.test_delay",
        "runner_function": "run_delay_scenario",
    },
    "section_header": {
        "runner_module": "scenarios.new_condition.test_section_header",
        "runner_function": "run_section_header_scenario",
    },
    "check_rabbit_lp_status_recalc_b24": {
        "runner_module": "scenarios.new_condition.test_check_rabbit_lp_status_recalc_b24",
        "runner_function": "run_check_rabbit_lp_status_recalc_b24_scenario",
    },
    "show_deal_info": {
        "runner_module": "scenarios.new_condition.test_show_deal_info",
        "runner_function": "run_show_deal_info_scenario",
    },
}
