from rest_framework.exceptions import ValidationError


class OrderValidator:
    @classmethod
    def validate(cls, attrs):
        table_number = attrs.get("table_number")
        cls.validate_table(table_number)

        order_items = attrs.get("order_items", [])
        if not order_items:
            raise ValidationError(
                {"order_items": "Заказ должен содержать хотя бы одну позицию."}
            )
        for item in order_items:
            OrderItemValidator.validate(item)

        return attrs

    @staticmethod
    def validate_table(table_number):
        try:
            table_number = int(table_number)
            if table_number <= 0:
                raise ValidationError(
                    {"table_number": "Номер стола должен быть больше нуля."}
                )
        except ValueError:
            raise ValidationError(
                {"table_number": "Номер стола должен числом больше нуля."}
            )


class OrderItemValidator:
    @staticmethod
    def validate(attrs):
        dish = attrs.get("dish")
        if not dish:
            raise ValidationError({"dish": "Блюдо обязательно."})

        DishValidator.validate(dish)
        return attrs


class DishValidator:
    @classmethod
    def validate(cls, attrs):
        price = attrs.get("price")
        name = attrs.get("name")
        cls.validate_price(price)
        cls.validate_dish_name(name)
        return attrs

    @staticmethod
    def validate_price(price_value):
        try:
            price_value = float(price_value)
            if price_value <= 0:
                raise ValidationError("Цена блюда должна быть больше нуля.")
        except ValueError:
            raise ValidationError(
                "Цена должна быть числом или строкой, содержащей число."
            )

    @staticmethod
    def validate_dish_name(name):
        if not name:
            raise ValidationError("Название блюда обязательно.")
