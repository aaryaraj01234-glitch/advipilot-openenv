import json
from environment import AdvipilotEnv
from tasks import tasks
from grader import grade

env = AdvipilotEnv()

print("[START]")

for task in tasks:
    env.reset()

    if task["name"] == "easy":
        action = {
            "type":"career",
            "value":"Software Engineer",
            "reason":"based on interest and marks growth",
            "confidence":0.8
        }

    elif task["name"] == "medium":
        action = {
            "type":"feasibility",
            "value":"feasible",
            "reason":"marks ok but budget low",
            "confidence":0.7
        }

    else:
        action = {
            "type":"roadmap",
            "value":["JEE","B.Tech","Skills","Alternative"],
            "reason":"india path with backup",
            "confidence":0.85
        }

    _, reward, _, _ = env.step(action)
    score = grade(action["value"], task["expected"])

    print("[STEP]", task["name"], reward, score)

print("[END]")

# leaderboard
try:
    with open("leaderboard.json") as f:
        lb = json.load(f)
except:
    lb = []

lb.append({"name":"agent","score":env.state_data["progress"]})
lb = sorted(lb, key=lambda x: x["score"], reverse=True)

with open("leaderboard.json","w") as f:
    json.dump(lb,f,indent=2)

print("🏆 LEADERBOARD:", lb[:3])