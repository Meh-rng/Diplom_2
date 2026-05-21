def generate_order_body(ingredients_list):
    """Формирует тело запроса для создания заказа"""
    return {"ingredients": ingredients_list}