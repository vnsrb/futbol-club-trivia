#cuestionario.py


from flask import (
    Flask,
    redirect,
    url_for,
    session,
    request
)

from basededatos import (
    get_next_question,
    get_quises
)

app = Flask(__name__)

app.config[
    "SECRET_KEY"
] = "CuestionarioFutbol"

def start_quiz(quiz_id):

    session["quiz"] = int(
        quiz_id
    )

    session[
        "prev_question"
    ] = 0

def end_quiz():

    session.clear()

def form_html():

    quises = get_quises()

    options = ""

    for quiz_id, name in quises:

        options += (
            f'<option value="{quiz_id}">'
            f'{name}'
            f'</option>'
        )

    return f"""
    <!DOCTYPE html>

    <html lang="es">

    <head>

        <meta charset="UTF-8">

        <title>
            Cuestionario de fútbol
        </title>

    </head>

    <body>

        <h1>
            Trivia de fútbol
        </h1>

        <form
            action="/"
            method="POST"
        >

            <label>

                Selecciona un cuestionario:

            </label>

            <select name="quiz">

                {options}

            </select>

            <button type="submit">

                Comenzar

            </button>

        </form>

    </body>

    </html>
    """

@app.route(
    "/",
    methods=[
        "GET",
        "POST"
    ]
)

def index():

    if request.method == "GET":

        end_quiz()

        return form_html()

    quiz_id = request.form.get(
        "quiz"
    )

    start_quiz(
        quiz_id
    )

    return redirect(
        url_for(
            "test"
        )
    )

@app.route(
    "/test"
)

def test():

    if "quiz" not in session:

        return redirect(
            url_for(
                "index"
            )
        )

    result = get_next_question(

        session[
            "prev_question"
        ],

        session[
            "quiz"
        ]

    )

    if result is None:

        return redirect(

            url_for(
                "result"
            )

        )

    session[
        "prev_question"
    ] = result[0]

    return f"""

    <h1>
        {result[1]}
    </h1>

    <p>

        Respuesta correcta:

        <strong>

            {result[2]}

        </strong>

    </p>

    <a href="/test">

        Siguiente pregunta

    </a>

    """

@app.route(
    "/result"
)

def result():

    return """

    <h1>

        Cuestionario terminado

    </h1>

    <a href="/">

        Volver al inicio

    </a>

    """

if __name__ == "__main__":

    app.run(
        debug=True
    )
