from os import system
from random import randint
from typing import Optional
from threading import Thread
from contextlib import suppress
from urllib.parse import urlencode
from time import sleep as delay, time
from ujson import loads, dumps, JSONDecodeError

from .context import EventHandler
from .dispatcher import MessageDispatcher
from .entities.wsevents import EventTypes, NotifTypes
from .entities.userprofile import OnlineMembers
from .entities.messages import Channel, Message, NNotification
from .entities.exceptions import WrongWebSocketPackage
from .utilities.generate import device_id, generate_signature
from .entities.handlers import run_alive_loop, orjson_exists

if orjson_exists():
    from orjson import (
        loads as orjson_loads, dumps as orjson_dumps
        )


try:
    from websocket import WebSocket, WebSocketApp
except ImportError as e:
    system("pip uninstall websocket -y")
    system("pip install websocket-client==1.5.2")
    raise WrongWebSocketPackage from e


class WSClient(EventHandler):
    """
    `WSClient` is a class that handles the websocket.
    """
    def __init__(self):
        self.ws:            WebSocketApp = None
        self.online_status: bool = True        
        self._communities:  set = set()
        self.event_types:   dict =  EventTypes().events
        self.notif_types:   dict =  NotifTypes().notifs
        self.dispatcher:    MessageDispatcher = MessageDispatcher()
        self.channel:       Optional[Channel] = None
        self.orjson:        bool = orjson_exists()
        
        self.dispatcher.register(10, self._handle_notification)
        self.dispatcher.register(201, self._handle_agora_channel)
        self.dispatcher.register(400, self._handle_user_online)
        self.dispatcher.register(1000, self._handle_message)
        EventHandler.__init__(self)


    def fetch_ws_url(self) -> str:
        return f"wss://ws{randint(1, 4)}.aminoapps.com"


    def connect(self) -> None:
        """Connects to the websocket."""
        self.run_forever()
        return self.emit("ready")


    def run_forever(self) -> None:
        """Runs the websocket forever."""
        ws_data = f"{device_id()}|{int(time() * 1000)}"
        self.ws = WebSocketApp(
            url = f"{self.fetch_ws_url()}/?{urlencode({'signbody': ws_data})}",
            on_open=self.on_websocket_open,
            on_message=self.on_websocket_message,
            on_error=self.on_websocket_error,
            on_close=self.on_websocket_close,
            header={
            "NDCDEVICEID": device_id(),
            "NDCAUTH": f"sid={self.sid}",
            "NDC-MSG-SIG": generate_signature(ws_data)
            })
        return self.start_processes()


    def start_processes(self) -> None:
        """Starts the websocket processes."""
        websocket_thread = Thread(target=self.ws.run_forever)
        websocket_thread.start()

        aalive_thread = Thread(target=run_alive_loop, args=(self,))
        aalive_thread.start()


    def on_websocket_error(self, ws: WebSocket, error: Exception) -> None:
        """Handles websocket errors."""
        with suppress(KeyError):
            self._events["error"](error)


    def on_websocket_message(self, ws: WebSocket, message: dict) -> None:
        """Handles websocket messages."""
        try:
            raw_message = orjson_loads(message) if self.orjson else loads(message)
        except JSONDecodeError:
            raw_message = loads(message)

        self.dispatcher.handle(raw_message)


    def _handle_message(self, message: dict) -> None:
        """Sends the message to the event handler."""
        _message: Message = Message(message)

        if self.userId == _message.userId: return None
        None if any(
            [_message.ndcId is None, _message.ndcId == 0]
        ) else self._communities.add(_message.ndcId)

        key = self.event_types.get(f"{_message.type}:{_message.mediaType}")
        if key != None:
            return Thread(target=self._handle_event, args=(key, _message)).start()


    def _handle_notification(self, message: dict) -> None:
        """Handles notifications."""
        notification: NNotification = NNotification(message)
        key = self.notif_types.get(notification.notifType)
        if key != None:
            return Thread(target=self._handle_event, args=(key, notification)).start()


    def _handle_agora_channel(self, message: dict) -> None:
        """Sets the agora channel."""
        self.channel: Channel = Channel(message)


    def _handle_user_online(self, message: dict) -> None:
        """Handles user online events."""
        return self._handle_event("user_online", OnlineMembers(message))


    def on_websocket_close(self, ws: WebSocket, close_status_code: int, close_msg: str) -> None:
        """Handles websocket close events."""
        if [close_status_code, close_msg] == [None, None]:
            return self.run_forever() 


    def send_websocket_message(self, message: dict) -> None:
        """Sends a websocket message."""
        return self.ws.send(orjson_dumps(message).decode() if self.orjson else dumps(message))


    def stop_websocket(self) -> None:
        """Stops the websocket."""
        return self.ws.close()


    def on_websocket_open(self, ws: WebSocket) -> None:
        """Handles websocket open events."""
        if all([self.community_id != None, "user_online" in self._events]):
            return self.send_websocket_message({
                "t": 300,
                "o": {
                    "ndcId": self.community_id,
                    "topic": f"ndtopic:x{self.community_id}:online-members",
                    "id": int(time() * 1000)
                }})


    def _last_active(self, last_activity_time: float) -> bool:
        """Returns True if the last activity was 5 minutes ago."""""
        return time() - last_activity_time >= 300


    def _last_message(self, last_message_time: float) -> bool:
        """Returns True if the last message was 30 seconds ago."""
        return time() - last_message_time >= 30


    def _send_message(self) -> None:
        """Sends a message to the websocket."""
        self.send_websocket_message({
            "o":{
                "threadChannelUserInfoList": [],
                "id": randint(1, 100)},
                "t": 116
                })


    def _activity_status(self) -> None:
        """Sets the user's activity status to online."""
        for comId in self._communities:

            if self.online_status:
                try:
                    self.community.online_status(comId=comId)
                    self.community.send_active(comId=comId,
                    timers=[{"start": int(time()), "end": int(time()) + 300}]
                    )
                except Exception:
                    self.online_status = False

            delay(randint(5, 10))