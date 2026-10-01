from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

INITIAL_TELEMETRY = {
    "fuel": 100.0, "temp": 25.0, "voltage": 28.0,
    "battery": 100.0, "deviation": 0.1, "radiation": 2.0, "oxygen": 100.0
}

# Backup tanks / batteries used during automatic recovery
INITIAL_BACKUP = {"fuel": 40.0, "battery": 40.0, "oxygen": 30.0}

RECOVERY_THRESHOLDS = {
    "temp":      38.0,
    "radiation":  6.0,
    "deviation":  1.0,
}

telemetry  = dict(INITIAL_TELEMETRY)
backup     = dict(INITIAL_BACKUP)
status     = "NORMAL"
mode       = "AUTOMATIC"
step       = 0
running    = True
auto_event = None


def is_recovered():
    return (
        telemetry["temp"]      < RECOVERY_THRESHOLDS["temp"]      and
        telemetry["radiation"] < RECOVERY_THRESHOLDS["radiation"] and
        telemetry["deviation"] < RECOVERY_THRESHOLDS["deviation"]
    )


def cool_down():
    telemetry["temp"]      = max(telemetry["temp"]      - random.uniform(0.8, 1.5), 25.0)
    telemetry["radiation"] = max(telemetry["radiation"] - random.uniform(0.3, 0.6), 2.0)
    telemetry["deviation"] = max(telemetry["deviation"] - random.uniform(0.05, 0.1), 0.1)


def use_backup():
    """Move resources from backup into the main system (max 1 unit per call)."""
    used = False
    for k in ("fuel", "battery", "oxygen"):
        if backup[k] > 0 and telemetry[k] < 100:
            amt = min(1.0, backup[k], 100 - telemetry[k])
            backup[k]    -= amt
            telemetry[k] += amt
            used = True
    return used


def update_resources():
    global telemetry, status, step, running, auto_event

    auto_event = None

    # Simulation is stopped
    if not running:
        # AUTOMATIC mode: take resources from backup and cool down by itself
        if status == "ANOMALY" and mode == "AUTOMATIC":
            use_backup()
            cool_down()
            if is_recovered():
                status     = "NORMAL"
                step       = 0
                running    = True
                auto_event = "auto_started"
        # MANUAL mode: nothing happens, operator must use /cooldown
        return

    step += 1

    telemetry["fuel"]      = max(telemetry["fuel"]    - random.uniform(0.2, 0.6), 0)
    telemetry["battery"]   = max(telemetry["battery"] - random.uniform(0.1, 0.3), 0)
    telemetry["oxygen"]    = max(telemetry["oxygen"]  - random.uniform(0.05, 0.1), 0)
    telemetry["temp"]      += random.uniform(-0.2, 0.5)
    telemetry["voltage"]   += random.uniform(-0.1, 0.1)
    telemetry["deviation"] += random.uniform(-0.01, 0.02)
    telemetry["radiation"] += random.uniform(-0.1, 0.3)

    if step < 40:
        status = "NORMAL"
    elif step < 80:
        status = "THRESHOLD"
        telemetry["temp"] += random.uniform(0.5, 1.0)
    else:
        status = "ANOMALY"
        telemetry["radiation"] += random.uniform(0.5, 1.0)
        telemetry["deviation"] += random.uniform(0.05, 0.1)
        telemetry["temp"]      += random.uniform(0.3, 0.7)
        # Only AUTOMATIC mode stops the simulation by itself
        if mode == "AUTOMATIC":
            running    = False
            auto_event = "auto_stopped"


def predict_future():
    return {
        "fuel":      max(telemetry["fuel"]    - 5, 0),
        "temp":           telemetry["temp"]      + 3,
        "voltage":        telemetry["voltage"]   - 1,
        "battery":   max(telemetry["battery"] - 3, 0),
        "deviation":      telemetry["deviation"] + 0.2,
        "radiation":      telemetry["radiation"] + 2,
        "oxygen":    max(telemetry["oxygen"]  - 4, 0)
    }


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/telemetry")
def telemetry_data():
    update_resources()
    return jsonify({
        "telemetry":  telemetry,
        "backup":     backup,
        "prediction": predict_future(),
        "status":     status,
        "mode":       mode,
        "running":    running,
        "auto_event": auto_event
    })


@app.route("/toggle_mode")
def toggle_mode():
    global mode
    mode = "MANUAL" if mode == "AUTOMATIC" else "AUTOMATIC"
    return jsonify({"mode": mode})


@app.route("/start")
def start_sim():
    global running
    running = True
    return jsonify({"running": running})


@app.route("/stop")
def stop_sim():
    global running
    running = False
    return jsonify({"running": running})


@app.route("/cooldown")
def manual_cooldown():
    """MANUAL mode: operator triggers one cool-down step using backup."""
    global status, step
    if mode == "MANUAL":
        use_backup()
        cool_down()
        if is_recovered():
            status = "NORMAL"
            step   = 0
    return jsonify({
        "temp":   telemetry["temp"],
        "mode":   mode,
        "status": status
    })


@app.route("/reset")
def reset_sim():
    global telemetry, backup, status, step, running, auto_event
    telemetry  = dict(INITIAL_TELEMETRY)
    backup     = dict(INITIAL_BACKUP)
    status     = "NORMAL"
    step       = 0
    running    = True
    auto_event = None
    return jsonify({"reset": True})


if __name__ == "__main__":
    app.run(debug=True)