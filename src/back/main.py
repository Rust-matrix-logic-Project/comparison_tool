import fastapi
import fastapi.middleware.cors
import src.back.goals as goals, src.back.times as times
from typing import Annotated

app = fastapi.FastAPI()
timer = times.TimeCheker()

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["http://localhost:5173"]
)

@app.get("/timer/start")
def timer_start():
    result = timer.start_checker()
    return result

@app.post("/timer/stop")
def timer_end():
    result = timer.end_checker()
    return result

@app.post("/goals/save")
def goals_set(goal:Annotated[list[str], fastapi.Form()], month):
    result = goals.Goals(goal, status=None, limit=None,month=month).save()
    return result

@app.post("/goals/update")
def goals_update(key, status, limit, month):
    result = goals.Goals(key=key, status=status, limit=limit, month=month).update()
    return result

@app.get("/goals/data")
def get_goals(month):
    result = goals.Goals(month=month).leard_to_jsonl()
    return result
