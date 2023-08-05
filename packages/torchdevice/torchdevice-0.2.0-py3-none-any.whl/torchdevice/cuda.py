import json
import os
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from queue import PriorityQueue
from typing import List

from filelock import FileLock


def get_queue(device_count: int) -> PriorityQueue:
    path = Path.home() / f'.{socket.gethostname()}.QUEUE'

    if path.exists():
        with path.open(mode='r', encoding='utf-8') as fp:
            devices = json.load(fp=fp)
    else:
        devices = [
            (datetime.now().isoformat(), index)
            for index in range(device_count)
        ]

    queue = PriorityQueue()

    for stamp, index in devices:
        queue.put((stamp, index))
    return queue


def set_queue(queue: PriorityQueue, free: List[int], n: int) -> List[int]:
    new_queue = []

    devices = []
    while not queue.empty():
        stamp, index = queue.get()
        if len(devices) < n and index in free:
            stamp = datetime.now().isoformat()
            devices.append(index)

        new_queue.append((stamp, index))

    path = Path.home() / f'.{socket.gethostname()}.QUEUE'
    with path.open(mode='w', encoding='utf-8') as fp:
        json.dump(new_queue, fp=fp, indent=2, ensure_ascii=False)

    return devices


def set_cuda_visible_devices(n: int = 1) -> List[int]:
    CUDA_VISIBLE_DEVICES = 'CUDA_VISIBLE_DEVICES'

    with FileLock(str(Path.home() / f'.{socket.gethostname()}.{CUDA_VISIBLE_DEVICES}')):
        devices = subprocess.check_output('nvidia-smi -q -d PIDS | grep Processes', shell=True).splitlines()
        free = [index for index, process in enumerate(devices) if b': None' in process]

        if len(free) < n:
            raise RuntimeError(f'the number of free devices ({free})) are not enough < {n}')

        queue = get_queue(device_count=len(devices))
        devices = set_queue(queue=queue, free=free, n=n)

        os.environ[CUDA_VISIBLE_DEVICES] = ','.join(map(str, devices))
        print(f'{CUDA_VISIBLE_DEVICES} <- {os.environ[CUDA_VISIBLE_DEVICES]}')

    return free
