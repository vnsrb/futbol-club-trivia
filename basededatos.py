#basededatos.py


import sqlite3

# Nombre del archivo de la base de datos
DB = "quises.sqlite"


def open_db():
    """Abre la conexión con la base de datos SQLite."""

    conn = sqlite3.connect(DB)

    # Activa las llaves foráneas
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables():
    """Crea las tablas de cuestionarios y preguntas."""

    conn = open_db()
    cursor = conn.cursor()

    # Tabla de cuestionarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    # Tabla de preguntas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_name TEXT NOT NULL,
            correct TEXT NOT NULL,
            wrong_1 TEXT NOT NULL,
            wrong_2 TEXT NOT NULL,
            wrong_3 TEXT NOT NULL
        );
    """)

    # Tabla que relaciona los cuestionarios
    # con las preguntas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,

            FOREIGN KEY (quiz_id)
            REFERENCES quiz(id)
            ON DELETE CASCADE,

            FOREIGN KEY (question_id)
            REFERENCES question(id)
            ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()

    print("Tablas creadas correctamente.")


def add_quises():
    """Agrega las categorías de trivia de fútbol."""

    quizzes = [
        ("Historia del fútbol",),
        ("Copas del Mundo",),
        ("Leyendas del fútbol",)
    ]

    conn = open_db()

    conn.executemany(
        "INSERT INTO quiz (name) VALUES (?);",
        quizzes
    )

    conn.commit()
    conn.close()

    print("Cuestionarios agregados correctamente.")


def add_questions():
    """Agrega preguntas relacionadas con el fútbol."""

    questions = [

        # HISTORIA DEL FÚTBOL

        (
            "¿En qué país se originó el fútbol moderno?",
            "Inglaterra",
            "Brasil",
            "España",
            "Argentina"
        ),

        (
            "¿Cuántos jugadores tiene un equipo en el campo?",
            "11",
            "9",
            "10",
            "12"
        ),

        (
            "¿Cuánto dura un partido de fútbol reglamentario?",
            "90 minutos",
            "60 minutos",
            "80 minutos",
            "100 minutos"
        ),

        (
            "¿Qué tarjeta expulsa a un jugador?",
            "Tarjeta roja",
            "Tarjeta amarilla",
            "Tarjeta verde",
            "Tarjeta azul"
        ),

        (
            "¿Cómo se llama el jugador que protege la portería?",
            "Portero",
            "Delantero",
            "Defensa",
            "Árbitro"
        ),

        # COPAS DEL MUNDO

        (
            "¿Qué selección ganó el Mundial de 2022?",
            "Argentina",
            "Francia",
            "Croacia",
            "Brasil"
        ),

        (
            "¿Qué país ganó el Mundial de 2010?",
            "España",
            "Alemania",
            "Brasil",
            "Argentina"
        ),

        (
            "¿Qué país tiene más títulos mundiales masculinos?",
            "Brasil",
            "Alemania",
            "Italia",
            "Argentina"
        ),

        (
            "¿En qué país se jugó el Mundial de 2014?",
            "Brasil",
            "Rusia",
            "Sudáfrica",
            "Alemania"
        ),

        (
            "¿Quién ganó el Mundial de 2018?",
            "Francia",
            "Croacia",
            "Argentina",
            "Alemania"
        ),

        # LEYENDAS DEL FÚTBOL

        (
            "¿Quién es conocido como El Rey del Fútbol?",
            "Pelé",
            "Maradona",
            "Messi",
            "Cristiano Ronaldo"
        ),

        (
            "¿Qué jugador es conocido como La Pulga?",
            "Lionel Messi",
            "Cristiano Ronaldo",
            "Neymar",
            "Kylian Mbappé"
        ),

        (
            "¿Quién marcó el gol conocido como La Mano de Dios?",
            "Diego Maradona",
            "Pelé",
            "Zinedine Zidane",
            "Ronaldinho"
        ),

        (
            "¿Qué jugador portugués ha ganado varios Balones de Oro?",
            "Cristiano Ronaldo",
            "Luis Figo",
            "Eusébio",
            "Bernardo Silva"
        ),

        (
            "¿Qué jugador brasileño era conocido como O Fenômeno?",
            "Ronaldo Nazário",
            "Ronaldinho",
            "Neymar",
            "Kaká"
        )
    ]

    conn = open_db()

    conn.executemany("""
        INSERT INTO question (
            question_name,
            correct,
            wrong_1,
            wrong_2,
            wrong_3
        )
        VALUES (?, ?, ?, ?, ?);
    """, questions)

    conn.commit()
    conn.close()

    print("Preguntas de fútbol agregadas correctamente.")


def add_links():
    """
    Relaciona las preguntas con cada cuestionario.
    """

    links = [

        # Cuestionario 1:
        # Historia del fútbol
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),

        # Cuestionario 2:
        # Copas del Mundo
        (2, 6),
        (2, 7),
        (2, 8),
        (2, 9),
        (2, 10),

        # Cuestionario 3:
        # Leyendas del fútbol
        (3, 11),
        (3, 12),
        (3, 13),
        (3, 14),
        (3, 15)
    ]

    conn = open_db()

    conn.executemany("""
        INSERT INTO quiz_content (
            quiz_id,
            question_id
        )
        VALUES (?, ?);
    """, links)

    conn.commit()
    conn.close()

    print("Preguntas relacionadas con los cuestionarios.")


def get_next_question(question_id=0, quiz_id=1):
    """
    Obtiene la siguiente pregunta del cuestionario.
    """

    conn = open_db()
    cursor = conn.cursor()

    query = """
        SELECT
            quiz_content.id,
            question.question_name,
            question.correct,
            question.wrong_1,
            question.wrong_2,
            question.wrong_3

        FROM quiz_content

        INNER JOIN question
        ON quiz_content.question_id = question.id

        WHERE quiz_content.id > ?
        AND quiz_content.quiz_id = ?

        ORDER BY quiz_content.id

        LIMIT 1;
    """

    cursor.execute(
        query,
        (
            question_id,
            quiz_id
        )
    )

    result = cursor.fetchone()

    conn.close()

    return result


def get_quises():
    """
    Obtiene todos los cuestionarios.
    """

    conn = open_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM quiz;"
    )

    result = cursor.fetchall()

    conn.close()

    return result


def reset_database():
    """
    Elimina las tablas anteriores y crea
    una nueva base de datos.
    """

    conn = open_db()
    cursor = conn.cursor()

    cursor.execute(
        "DROP TABLE IF EXISTS quiz_content;"
    )

    cursor.execute(
        "DROP TABLE IF EXISTS question;"
    )

    cursor.execute(
        "DROP TABLE IF EXISTS quiz;"
    )

    conn.commit()
    conn.close()

    # Crear las tablas
    create_tables()

    # Agregar los cuestionarios
    add_quises()

    # Agregar las preguntas
    add_questions()

    # Relacionar preguntas y cuestionarios
    add_links()

    print()
    print("Base de datos creada correctamente.")
    print("Archivo generado: quises.sqlite")


# Este código se ejecuta únicamente
# cuando se abre basededatos.py

if __name__ == "__main__":

    reset_database()

