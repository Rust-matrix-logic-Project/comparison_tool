import fastapi
import fastapi.middleware.cors
import back.goals as goals, back.times as times

app = fastapi.FastAPI()
timer = times.TimeCheker()

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["https://localhost:5173"]
)

@app.get("/timer/start")
def timer_start():
    timer.start_checker()

@app.post("/timer/stop")
def timer_end():
    result = timer.end_checker()
    return result

@app.post("/goals/save")
def goals_set(date, goal, states):
    goals.Goals(date, goal, states).save()

@app.post("/goals/update")
def goals_set(goal, updated_at, states):
    goals.Goals(goal, updated_at, states).update()