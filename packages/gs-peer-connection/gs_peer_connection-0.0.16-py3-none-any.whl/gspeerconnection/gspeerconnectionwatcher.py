import ast
import json
import logging

import socketio
from aiortc import MediaStreamTrack, RTCPeerConnection
from aiortc.rtcrtpreceiver import RemoteStreamTrack

from pitrack import PiH264Relay


class GSPeerConnectionWatcher:
    class PiH264Relay(MediaStreamTrack):
        kind = "video"

        def __init__(self, track: RemoteStreamTrack, gsdbs, source, onframe):
            super().__init__()
            self.track = track
            self.onframe = onframe
            self.source = source
            self.gsdbs = gsdbs

        #
        async def recv(self):
            # frame = await self.track.recv()
            frame = await self.track._queue.get()
            # self.onframe(self.gsdbs, self.source, frame)
            return frame

    @classmethod
    async def create(cls, gsdbs, target, onframe=None, onmessage=None, ontrack=None):
        self = GSPeerConnectionWatcher()
        self.sio = socketio.AsyncClient()
        self.gsdbs = gsdbs
        self.onframe = onframe
        self.target = target
        self.onmessage = onmessage
        self.ontrack = ontrack
        self.logger = logging.getLogger(__name__)

        @self.sio.event
        async def connect():
            self.logger.info('connection established')

        @self.sio.event
        async def joined():
            await self.sio.emit("watcher", {"target": self.target})

        @self.sio.event
        async def broadcaster():
            await self.sio.emit("watcher", {"target": self.target})

        @self.sio.event
        async def offer(id, description):
            self.peerConnections = RTCPeerConnection()

            @self.peerConnections.on("datachannel")
            def on_datachannel(channel):
                @channel.on("message")
                def on_message(message):
                    self.onmessage(self.gsdbs, self.target, message)

            @self.peerConnections.on("iceconnectionstatechange")
            async def on_iceconnectionstatechange():
                if self.peerConnections.iceConnectionState == "failed":
                    await self.peerConnections.close()

            @self.peerConnections.on("track")
            def on_track(track):
                if track.kind == "video":
                    if self.ontrack is not None:
                        self.ontrack(self.gsdbs, track)
                    # local_video = self.VideoTransformTrack(track, gsdbs=self.gsdbs, source=self.target,
                    #                                        onframe=self.onframe)
                    local_video = PiH264Relay(30)
                    self.peerConnections.addTrack(local_video)

                @track.on("ended")
                async def on_ended():
                    pass
                    # await recorder.stop()

            desc = type('new_dict', (object,), ast.literal_eval(description))
            await self.peerConnections.setRemoteDescription(desc)

            answer = await self.peerConnections.createAnswer()
            await self.peerConnections.setLocalDescription(answer)
            await self.sio.emit("answer", {"id": id,
                                           "message": json.dumps(
                                               {"type": self.peerConnections.localDescription.type,
                                                "sdp": self.peerConnections.localDescription.sdp})})

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}&target={self.target}')
        await self.sio.wait()
