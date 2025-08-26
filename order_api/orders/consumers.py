import json
from typing import TYPE_CHECKING
from typing import cast

from channels.generic.websocket import AsyncWebsocketConsumer

if TYPE_CHECKING:
    from order_api.users.models import User


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        if not self.channel_layer:
            await self.close()
            return

        if cast("User", self.user).role == "worker":
            self.group_name = "workers"
            self.individual_group = f"worker_{self.user.id}"
        elif cast("User", self.user).role == "client":
            self.group_name = f"client_{self.user.id}"
        else:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        if hasattr(self, "individual_group"):
            await self.channel_layer.group_add(
                self.individual_group,
                self.channel_name,
            )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )

        if hasattr(self, "individual_group"):
            await self.channel_layer.group_discard(
                self.individual_group,
                self.channel_name,
            )

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(
            text_data=json.dumps(
                {
                    "message": f"Received: {text_data}",
                },
            ),
        )

    async def new_order(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "new_order",
                    "order_id": event["order_id"],
                    "message": event["message"],
                },
            ),
        )

    async def order_status_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "order_status_update",
                    "order_id": event["order_id"],
                    "status": event["status"],
                    "message": event["message"],
                },
            ),
        )
