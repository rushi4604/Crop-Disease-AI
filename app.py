from flask import Flask, request, render_template
from ultralytics import YOLO
from crop_agent import generate_agent_response

import os
import uuid
import json
from datetime import datetime, timedelta
app = Flask(__name__)


# =========================================================
# SCAN HISTORY
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HISTORY_FILE = os.path.join(
    BASE_DIR,
    "scan_history.json"
)


def load_scan_history():

    try:

        if not os.path.exists(HISTORY_FILE):
            return []

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        if isinstance(data, list):
            return data

        return []

    except Exception as e:

        print("History load error:", e)

        return []


def save_scan(
    disease,
    confidence,
    risk="Unknown"
):

    history = load_scan_history()

    scan = {

        "id": str(uuid.uuid4()),

        "disease": str(disease),

        "confidence": round(
            float(confidence),
            2
        ),

        "risk": str(risk),

        "timestamp": datetime.now().isoformat()

    }

    history.append(scan)

    # Keep only latest 1000 real scans
    history = history[-1000:]

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=4
        )

    print("\n================================")
    print("SCAN SAVED")
    print("================================")
    print("File:", HISTORY_FILE)
    print("Disease:", disease)
    print("Confidence:", confidence)
    print("Risk:", risk)
    print("Total scans:", len(history))
    print("================================\n")

    return scan


def get_time_ago(timestamp):

    try:

        scan_time = datetime.fromisoformat(
            timestamp
        )

        now = datetime.now()

        seconds = int(
            (now - scan_time).total_seconds()
        )

        if seconds < 60:
            return "Just now"

        minutes = seconds // 60

        if minutes < 60:
            return f"{minutes} min ago"

        hours = minutes // 60

        if hours < 24:
            return f"{hours} hr ago"

        days = hours // 24

        if days == 1:
            return "Yesterday"

        return f"{days} days ago"

    except Exception:

        return "Unknown"


# =========================================================
# LOAD YOLO MODEL
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "best.pt"
)

yolo_model = YOLO(MODEL_PATH)

# =========================================================
# UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# DETECT PAGE
# =========================================================

@app.route("/detect")
def detect():
    return render_template("detect.html")


# =========================================================
# PREDICTION + AI AGENT
# =========================================================

@app.route("/predict-ui", methods=["POST"])
def predict_ui():

    # -----------------------------------------------------
    # CHECK FILE
    # -----------------------------------------------------

    if "image" not in request.files:

        return "No file uploaded"

    file = request.files["image"]

    if file.filename == "":

        return "No file selected"

    # -----------------------------------------------------
    # SAVE IMAGE
    # -----------------------------------------------------

    filename = (
        str(uuid.uuid4())
        + "_"
        + file.filename
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    print("\n================================")
    print("NEW IMAGE")
    print("================================")
    print("Image:", filepath)

    # -----------------------------------------------------
    # YOLO PREDICTION
    # -----------------------------------------------------

    try:

        result = yolo_model.predict(
            source=filepath,
            verbose=False
        )[0]

        # Top prediction index
        top1 = result.probs.top1

        # Disease name
        disease = result.names[top1]

        # Confidence
        confidence = float(
            result.probs.top1conf.item() * 100
        )

        # -------------------------------------------------
        # CLEAN DISEASE NAME
        # -------------------------------------------------

        display_disease = disease

        display_disease = display_disease.replace(
            "Tomato___",
            ""
        )

        display_disease = display_disease.replace(
            "Tomato__",
            ""
        )

        display_disease = display_disease.replace(
            "_",
            " "
        )

        display_disease = display_disease.strip()

        # -------------------------------------------------
        # RISK
        # -------------------------------------------------

        if "healthy" in display_disease.lower():

            risk = "None"

        elif confidence >= 90:

            risk = "High"

        elif confidence >= 75:

            risk = "Medium"

        else:

            risk = "Low"

        # -------------------------------------------------
        # SAVE REAL PREDICTION
        # -------------------------------------------------

        save_scan(
            display_disease,
            confidence,
            risk
        )

        print("\n================================")
        print("YOLO PREDICTION")
        print("================================")
        print("Raw:", disease)
        print("Display:", display_disease)
        print("Confidence:", confidence)
        print("Risk:", risk)

    except Exception as e:

        print("\nYOLO ERROR:")
        print(e)

        return f"Prediction error: {e}"

    # -----------------------------------------------------
    # AI AGRICULTURAL AGENT
    # -----------------------------------------------------

    print("\n================================")
    print("STARTING AGRICULTURAL AI AGENT")
    print("================================")

    agent_result = generate_agent_response(

        disease=display_disease,

        confidence=confidence,

        crop="Tomato",

        location="India"

    )

    # -----------------------------------------------------
    # RESULT PAGE
    # -----------------------------------------------------

    return render_template(

        "result.html",

        image_path="/" + filepath.replace(
            "\\",
            "/"
        ),

        disease=display_disease,

        confidence=f"{confidence:.2f}",

        risk=risk,

        agent_answer=agent_result["answer"],

        sources=agent_result["sources"]

    )

# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route('/dashboard')
def dashboard():

    history = load_scan_history()

    # Latest scans first
    history = sorted(
        history,
        key=lambda x: x.get("timestamp", ""),
        reverse=True
    )

    # -----------------------------------------------------
    # BASIC COUNTS
    # -----------------------------------------------------

    total_scans = len(history)

    disease_scans = [
        scan for scan in history
        if scan.get("disease", "").lower() != "healthy"
    ]

    healthy_scans = [
        scan for scan in history
        if "healthy" in scan.get("disease", "").lower()
    ]

    diseases_detected = len(disease_scans)
    healthy_count = len(healthy_scans)

    # -----------------------------------------------------
    # AVERAGE CONFIDENCE
    # -----------------------------------------------------

    if history:
        avg_confidence = round(
            sum(float(x.get("confidence", 0)) for x in history)
            / len(history),
            1
        )
    else:
        avg_confidence = 0

    # -----------------------------------------------------
    # DISEASE FREQUENCY
    # -----------------------------------------------------

    disease_counts = {}

    for scan in disease_scans:

        disease = scan.get("disease", "Unknown")

        # Remove Tomato__ / Tomato - prefixes for cleaner display
        clean_name = disease.replace("Tomato__", "")
        clean_name = clean_name.replace("Tomato - ", "")
        clean_name = clean_name.replace("_", " ")

        disease_counts[clean_name] = (
            disease_counts.get(clean_name, 0) + 1
        )

    disease_frequency = [
        {
            "name": name,
            "count": count
        }
        for name, count in disease_counts.items()
    ]

    disease_frequency.sort(
        key=lambda x: x["count"],
        reverse=True
    )

    # -----------------------------------------------------
    # RECENT SCANS
    # -----------------------------------------------------

    recent_scans = []

    for scan in history[:10]:

        disease = scan.get("disease", "Unknown")

        clean_name = disease.replace("Tomato__", "")
        clean_name = clean_name.replace("Tomato - ", "")
        clean_name = clean_name.replace("_", " ")

        recent_scans.append({
            "disease": "Tomato - " + clean_name,
            "confidence": scan.get("confidence", 0),
            "risk": scan.get("risk", "Unknown"),
            "time": get_time_ago(scan.get("timestamp", ""))
        })

    # -----------------------------------------------------
    # WEEKLY SCAN ACTIVITY
    # -----------------------------------------------------

    from datetime import timedelta

    today = datetime.now().date()

    weekly_activity = []

    for i in range(6, -1, -1):

        current_date = today - timedelta(days=i)

        total = 0
        diseases = 0

        for scan in history:

            timestamp = scan.get("timestamp", "")

            try:

                scan_date = datetime.fromisoformat(
                    timestamp
                ).date()

            except Exception:

                continue

            if scan_date == current_date:

                total += 1

                disease_name = scan.get(
                    "disease",
                    ""
                ).lower()

                if "healthy" not in disease_name:

                    diseases += 1

        weekly_activity.append({

            "day": current_date.strftime("%a"),

            "total": total,

            "diseases": diseases

        })


    # Maximum value used for chart scaling

    max_weekly_scans = max(

        [
            x["total"]
            for x in weekly_activity
        ],

        default=0

    )

    if max_weekly_scans == 0:

        max_weekly_scans = 1
    # -----------------------------------------------------
    # DASHBOARD STATS
    # -----------------------------------------------------

    stats = {

    "total_scans":
        total_scans,

    "diseases_detected":
        diseases_detected,

    "healthy_count":
        healthy_count,

    "avg_confidence":
        avg_confidence,

    "disease_frequency":
        disease_frequency,

    "recent_scans":
        recent_scans,

    "weekly_activity":
        weekly_activity,

    "max_weekly_scans":
        max_weekly_scans

}

    return render_template(
        "dashboard.html",
        stats=stats
    )
# =========================================================
# DISEASES
# =========================================================

@app.route("/diseases")
def diseases():
    return render_template("diseases.html")


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)