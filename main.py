import json
from flask import Flask, request, jsonify, render_template, send_from_directory
from Garden import Garden
from Plant import *
app = Flask(__name__)

Game = Garden()

def defineChoice(info):
    # Define the plant type based on the provided info
    if info == "tomato":
        return Tomato()
    if info == "apple":
        return Apple()
    if info == "watermelon":
        return WaterMelon()
    return None


@app.route("/")
def home():
    # Render the home page
    return render_template("index.html")


@app.route("/styles.css")
def style():
    # Serve the CSS file
    return send_from_directory('static', 'styles.css')


@app.route("/script.js")
def script():
    # Serve the JavaScript file
    return send_from_directory("static", "script.js")


@app.route("/plant", methods=["POST"])
def plant():
    # Plant a new plant in the garden
    data = request.json
    plotId = int(data.get("plotId"))
    plantType = defineChoice(data.get("plantType"))

    if plantType is None:
        return jsonify({"text": "Invalid plant type!", "isError": True})

    if plotId not in Game.plants or Game.plants[plotId] is None:
        Game.plants[plotId] = plantType
        return jsonify(
            {"text": f"You have planted a {data.get('plantType')}!", "isError": False}
        )
    else:
        return jsonify({"text": "This plot is already occupied!", "isError": True})


@app.route("/SpendMoney", methods=["POST"])
def SpendMoney():
    # Spend money to buy resources or add a plot
    data = request.json
    type = data.get("type")
    Game.SpendMoney(type)
    return jsonify({"text":"some bullshit"})

@app.route("/watering", methods=["POST"])
def watering():
    # Water a specific plot
    data = request.json
    plot_id = int(data.get("plot_id"))

    if plot_id in Game.plants and Game.plants[plot_id] is not None:
        plant = Game.plants[plot_id]
        plant.myWatering += 1  # Simulate watering
        return jsonify(
            {
                "emoji": (
                    plant.PlantIcon
                    if plant.status == PlantStatus.PlantShoot
                    else plant.AdultIcon
                )
            }
        )

    return jsonify({"emoji": "❌"})  # Error if no plant


@app.route("/action", methods=["POST"])
def useItem():
    # Perform an action on a specific plot
    data = request.json
    plotId = int(data.get("plotId"))
    actionMade = data.get("action")
    amount = float(data.get("amount", 0))  # Get the amount sent
    print(plotId, actionMade, amount)
    if actionMade == "water":
        result = Game.Watering(plotId, amount)
    elif actionMade == "fertilizer":
        result = Game.Fertilizing(plotId, amount)
    elif actionMade == "Lightning":
        result = Game.Lighting(plotId, False)
    elif actionMade == "hideLight":
        result = Game.Lighting(plotId, True)
    else:
        return jsonify({"text": "Invalid Action !", "isError": True})
    return jsonify(result)


@app.route("/update", methods=["GET"])
def update():
    # Update the game state
    json = jsonify(
        {
            "GameStats": Game.to_dict(),
        }
    )
    Game.IsNewGame = False
    return json


@app.route("/nextDay", methods=["GET"])
def nextDay():
    # Move to the next day in the game
    Game.RemoveDeadPlant()
    Game.UpdateAllPlant()
    Game.event = None
    Game.SetUpNewDay()
    return jsonify({"text": "It's a next Day, go check your plant", "isError": False})


@app.route("/Save", methods=["POST"])
def Save():
    # Save the game state
    data = request.json
    Save(data.get("SaveName"))
    return jsonify({"text": "Game perfectly saved", "isError": False})


@app.route("/openSave", methods=["POST"])
def openSave():
    global Game
    data = request.json
    try:
        with open(data.get("SaveName") + ".txt", "r", encoding="utf-8") as file:
            game_data = json.load(file)
        Game = Garden.from_dict(game_data)
        Game.GenerateEvent(Game.event)
        return jsonify({"text": "Save opened and ready to be played", "isError": False})
    except FileNotFoundError:
        return jsonify({"text": "No save has been found", "isError": True})


def Save(name):
    with open(name + ".txt", "w", encoding="utf8") as file:
        json.dump(Game.to_dict(), file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app.run(debug=True)
