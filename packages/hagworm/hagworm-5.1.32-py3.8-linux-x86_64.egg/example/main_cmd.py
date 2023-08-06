# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import sys

os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(r'../'))

from hagworm.extend.asyncio.base import Utils, AsyncCirculatorForSecond
from hagworm.extend.asyncio.command import Launcher, MainProcessAbstract, ChildProcessAbstract


class MainProcess(MainProcessAbstract):

    async def _run(self):

        self.maxsize = len(self._pids)

        while True:

            stopped = self._check_pids()

            await self.recv_message()

            if stopped:
                break

    async def recv_message(self):

        while True:

            message = await self._pull_server.recv(True)

            if message is None:
                break
            else:
                await self._push_server.send(message)

    async def _handle_data(self, data):

        await self._push_server.send(data)


class ChildProcess(ChildProcessAbstract):

    async def _run(self):

        async for idx in AsyncCirculatorForSecond(max_times=10):

            await self._push_client.send(f'{self._process_id}_{idx}')

            message = await self._pull_client.recv()

            Utils.log.info(message)


if __name__ == r'__main__':

    Launcher(subprocess=2, daemon=MainProcess()).run(ChildProcess())
