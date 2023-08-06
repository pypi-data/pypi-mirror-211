from starlette.background import BackgroundTasks

from script_master.main import app
from script_master.service import scheduler, schedule_stop_event


@app.get("/start-scheduler")
async def start_schedule(background_tasks: BackgroundTasks):
    if schedule_stop_event.is_set():
        schedule_stop_event.clear()
        background_tasks.add_task(scheduler)


@app.get("/stop-scheduler")
async def stop_schedule():
    schedule_stop_event.set()
