from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order_api.orders"

    def ready(self):
        from . import signals  # noqa: F401, PLC0415
