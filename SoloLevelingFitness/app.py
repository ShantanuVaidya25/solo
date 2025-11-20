from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# In-memory database (for simplicity)
users = {}
quests = {}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_id = str(len(users) + 1)
    users[user_id] = {
        "age": data.get("age"),
        "height": data.get("height"),
        "weight": data.get("weight"),
        "goals": data.get("goals"),
        "reps": {}
    }
    return jsonify({"user_id": user_id})

@app.route('/max_reps', methods=['POST'])
def max_reps():
    data = request.get_json()
    user_id = data.get("user_id")
    reps = data.get("reps")
    if user_id in users:
        users[user_id]["reps"] = reps
        return jsonify({"status":"saved"})
    return jsonify({"status":"error"}), 400

@app.route('/daily_quest', methods=['POST'])
def daily_quest():
    data = request.get_json()
    user_id = data.get("user_id")
    if user_id not in users:
        return jsonify({"status":"error"}), 400
    
    # Simple adaptive quest generator
    user = users[user_id]
    quest = {}
    for ex, max_rep in user["reps"].items():
        # 50–70% of max as daily goal
        quest[ex] = max(1, int(max_rep * 0.6))
    quests[user_id] = quest
    return jsonify({"quest": quest})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)