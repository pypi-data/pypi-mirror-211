import asyncio

from asyncio import Task


def run_in_background_task(fn) -> Task:
    return asyncio.get_event_loop().create_task(fn)
