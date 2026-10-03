# aplicacion.py

from flask import Flask, redirect, url_for, session, request, render_template
from basededatos import get_next_question, get_quises
from random import shuffle

app = Flask(__name__)
app.config["SECRET_KEY"] = "ClubFutbol2026"

def start_quiz(quiz_id):
    """Inicia un nuevo cuestionario."""
    session["quiz"] = int(quiz_id)
    session["prev_question"] = 0
    session["totals"] = 0
    session["corrects"] = 0

def end_quiz():
    """Elimina los datos de la partida actual."""
    session.clear()

def check_answer():
    """Comprueba la respuesta enviada por el jugador."""
    user_answer = request.form.get("ans_text")
    correct_answer = session.get("prev_correct_ans")

    if user_answer:
        session["totals"] += 1

        if user_answer == correct_answer:
            session["corrects"] += 1

def cal_stats(totals, corrects):
    """Calcula el porcentaje de respuestas correctas."""
    if totals > 0:
        return round((corrects / totals) * 100, 2)

    return 0

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        end_quiz()
        quises_list = get_quises()

        return render_template(
            "index.html",
            quises=quises_list
        )

    quiz_id = request.form.get("quiz")

    if not quiz_id:
        return redirect(url_for("index"))

    start_quiz(quiz_id)

    return redirect(url_for("test"))

@app.route("/test", methods=["GET", "POST"])
def test():
    if "quiz" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        check_answer()

    result = get_next_question(
        session["prev_question"],
        session["quiz"]
    )

    if result is None:
        return redirect(url_for("result"))

    session["prev_question"] = result[0]
    session["prev_correct_ans"] = result[2]

    question = result[1]

    options = list(result[2:6])
    shuffle(options)

    return render_template(
        "test.html",
        pregunta=question,
        opciones=options,
        numero=session["totals"] + 1
    )

@app.route("/result")
def result():
    if "totals" not in session:
        return redirect(url_for("index"))

    totals = session["totals"]
    corrects = session["corrects"]

    incorrects = totals - corrects

    percent = cal_stats(
        totals,
        corrects
    )

    return render_template(
        "result.html",
        totales=totals,
        correctas=corrects,
        incorrectas=incorrects,
        porcentaje=percent
    )

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )


