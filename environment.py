import json

with open("data/careers.json") as f:
    CAREERS = json.load(f)

class AdvipilotEnv:

    def __init__(self):
        self.state_data = None

    def reset(self):
        self.state_data = {
            "student": {
                "marks": 78,
                "interest": "Tech",
                "budget": "low",
                "country": "India"
            },
            "history": [],
            "progress": 0
        }
        return self.state_data

    def step(self, action):
        reward = 0
        done = False
        student = self.state_data["student"]

        # career
        if action["type"] == "career":
            match = next((c for c in CAREERS if c["name"] == action["value"]), None)
            if match:
                if match["interest"] == student["interest"]:
                    reward += 0.3
                if student["marks"] >= match["min_marks"]:
                    reward += 0.2
            else:
                reward -= 0.3

        # feasibility
        elif action["type"] == "feasibility":
            if student["marks"] >= 75:
                reward += 0.3
            else:
                reward -= 0.2

        # roadmap
        elif action["type"] == "roadmap":
            roadmap = action["value"]

            if "JEE" in roadmap and "B.Tech" in roadmap:
                reward += 0.2
            if "Skills" in roadmap:
                reward += 0.1
            if "Alternative" in roadmap:
                reward += 0.1
            if "IELTS" in str(roadmap):
                reward += 0.1

            done = True

        # reason scoring
        reason = action.get("reason", "")
        for k in ["interest", "marks", "budget", "growth"]:
            if k in reason.lower():
                reward += 0.05

        # confidence penalty
        conf = action.get("confidence", 0)
        if conf > 0.9 and reward < 0.3:
            reward -= 0.2

        # diversity penalty
        prev = [h.get("value") for h in self.state_data["history"]]
        if action.get("value") in prev:
            reward -= 0.2

        # risk logic
        if action.get("risk") == "high" and student["marks"] < 70:
            reward -= 0.2

        self.state_data["history"].append(action)
        self.state_data["progress"] += reward

        return self.state_data, reward, done, {}