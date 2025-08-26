from order_api.orders.routing import websocket_urlpatterns as orders_patterns

websocket_urlpatterns = [
    *orders_patterns,
]
