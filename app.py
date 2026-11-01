from datetime import date
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, abort

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "presenca.db"

app = Flask(__name__)
app.secret_key = "troque-esta-chave-por-uma-chave-segura"


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_banco():
    with conectar() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL UNIQUE,
            turma TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS presencas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Presente', 'Ausente', 'Justificado')),
            UNIQUE(aluno_id, data),
            FOREIGN KEY(aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
        );
        """)


@app.route("/")
def inicio():
    hoje = date.today().isoformat()
    with conectar() as conn:
        total_alunos = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
        total_turmas = conn.execute("SELECT COUNT(DISTINCT turma) FROM alunos").fetchone()[0]
        chamada_hoje = conn.execute(
            "SELECT COUNT(*) FROM presencas WHERE data = ?", (hoje,)
        ).fetchone()[0]
        presentes_hoje = conn.execute(
            "SELECT COUNT(*) FROM presencas WHERE data = ? AND status = 'Presente'", (hoje,)
        ).fetchone()[0]
    return render_template(
        "index.html", total_alunos=total_alunos, total_turmas=total_turmas,
        chamada_hoje=chamada_hoje, presentes_hoje=presentes_hoje, hoje=hoje
    )


@app.route("/alunos")
def listar_alunos():
    busca = request.args.get("q", "").strip()
    with conectar() as conn:
        alunos = conn.execute(
            """SELECT * FROM alunos
               WHERE nome LIKE ? OR matricula LIKE ? OR turma LIKE ?
               ORDER BY turma, nome""",
            (f"%{busca}%", f"%{busca}%", f"%{busca}%")
        ).fetchall()
    return render_template("alunos.html", alunos=alunos, busca=busca)


@app.route("/alunos/novo", methods=["GET", "POST"])
def novo_aluno():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        matricula = request.form.get("matricula", "").strip()
        turma = request.form.get("turma", "").strip()

        if not nome or not matricula or not turma:
            flash("Preencha todos os campos.", "erro")
            return render_template("aluno_form.html", aluno=None)

        try:
            with conectar() as conn:
                conn.execute(
                    "INSERT INTO alunos (nome, matricula, turma) VALUES (?, ?, ?)",
                    (nome, matricula, turma)
                )
            flash("Aluno cadastrado com sucesso.", "sucesso")
            return redirect(url_for("listar_alunos"))
        except sqlite3.IntegrityError:
            flash("Esta matrícula já está cadastrada.", "erro")

    return render_template("aluno_form.html", aluno=None)


@app.route("/alunos/<int:aluno_id>/editar", methods=["GET", "POST"])
def editar_aluno(aluno_id):
    with conectar() as conn:
        aluno = conn.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,)).fetchone()
    if aluno is None:
        abort(404)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        matricula = request.form.get("matricula", "").strip()
        turma = request.form.get("turma", "").strip()

        if not nome or not matricula or not turma:
            flash("Preencha todos os campos.", "erro")
            return render_template("aluno_form.html", aluno=aluno)

        try:
            with conectar() as conn:
                conn.execute(
                    "UPDATE alunos SET nome = ?, matricula = ?, turma = ? WHERE id = ?",
                    (nome, matricula, turma, aluno_id)
                )
            flash("Cadastro atualizado.", "sucesso")
            return redirect(url_for("listar_alunos"))
        except sqlite3.IntegrityError:
            flash("Esta matrícula já pertence a outro aluno.", "erro")

    return render_template("aluno_form.html", aluno=aluno)


@app.route("/alunos/<int:aluno_id>/excluir", methods=["POST"])
def excluir_aluno(aluno_id):
    with conectar() as conn:
        conn.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
    flash("Aluno excluído.", "sucesso")
    return redirect(url_for("listar_alunos"))


@app.route("/chamada", methods=["GET", "POST"])
def chamada():
    data_chamada = request.values.get("data", date.today().isoformat())
    turma_selecionada = request.values.get("turma", "").strip()

    # Valida o formato da data para evitar consultas com valores inesperados.
    try:
        date.fromisoformat(data_chamada)
    except ValueError:
        data_chamada = date.today().isoformat()

    with conectar() as conn:
        turmas = [r["turma"] for r in conn.execute(
            "SELECT DISTINCT turma FROM alunos ORDER BY turma"
        ).fetchall()]

        if request.method == "POST":
            alunos = conn.execute(
                "SELECT id FROM alunos WHERE turma = ? ORDER BY nome",
                (turma_selecionada,)
            ).fetchall()
            for aluno in alunos:
                status = request.form.get(f"status_{aluno['id']}", "Ausente")
                if status not in ("Presente", "Ausente", "Justificado"):
                    status = "Ausente"
                conn.execute(
                    """INSERT INTO presencas (aluno_id, data, status)
                       VALUES (?, ?, ?)
                       ON CONFLICT(aluno_id, data) DO UPDATE SET status = excluded.status""",
                    (aluno["id"], data_chamada, status)
                )
            flash("Chamada salva com sucesso.", "sucesso")
            return redirect(url_for("chamada", data=data_chamada, turma=turma_selecionada))

        if turma_selecionada and turma_selecionada in turmas:
            alunos = conn.execute(
                """SELECT a.*, p.status FROM alunos a
                   LEFT JOIN presencas p ON p.aluno_id = a.id AND p.data = ?
                   WHERE a.turma = ? ORDER BY a.nome""",
                (data_chamada, turma_selecionada)
            ).fetchall()
        else:
            alunos = []

    return render_template(
        "chamada.html", turmas=turmas, turma_selecionada=turma_selecionada,
        alunos=alunos, data_chamada=data_chamada
    )


@app.route("/relatorios")
def relatorios():
    turma = request.args.get("turma", "").strip()
    with conectar() as conn:
        turmas = [r["turma"] for r in conn.execute(
            "SELECT DISTINCT turma FROM alunos ORDER BY turma"
        ).fetchall()]
        sql = """
            SELECT a.id, a.nome, a.matricula, a.turma,
                   COUNT(p.id) AS aulas_registradas,
                   SUM(CASE WHEN p.status = 'Presente' THEN 1 ELSE 0 END) AS presentes,
                   SUM(CASE WHEN p.status = 'Ausente' THEN 1 ELSE 0 END) AS ausentes,
                   SUM(CASE WHEN p.status = 'Justificado' THEN 1 ELSE 0 END) AS justificados
            FROM alunos a
            LEFT JOIN presencas p ON p.aluno_id = a.id
        """
        params = []
        if turma:
            sql += " WHERE a.turma = ?"
            params.append(turma)
        sql += " GROUP BY a.id ORDER BY a.turma, a.nome"
        resultados = conn.execute(sql, params).fetchall()

    linhas = []
    for r in resultados:
        registradas = r["aulas_registradas"] or 0
        presentes = r["presentes"] or 0
        percentual = round((presentes / registradas) * 100, 1) if registradas else None
        linhas.append({
            "nome": r["nome"], "matricula": r["matricula"], "turma": r["turma"],
            "registradas": registradas, "presentes": presentes,
            "ausentes": r["ausentes"] or 0, "justificados": r["justificados"] or 0,
            "percentual": percentual
        })

    return render_template("relatorios.html", turmas=turmas, turma=turma, linhas=linhas)


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)
