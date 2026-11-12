"""Учёт заказов: Flask + SQLite."""
import sqlite3
from pathlib import Path
from flask import Flask, g, redirect, render_template, request, url_for, abort

BASE = Path(__file__).parent
DB_PATH = BASE / "orders.db"
STATUSES = ["Новый", "В работе", "Выполнен"]

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.executescript((BASE / "schema.sql").read_text(encoding="utf-8"))


@app.get("/")
def index():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    sql, params = "SELECT * FROM orders WHERE 1=1", []
    if q:
        sql += " AND (client LIKE ? OR item LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if status in STATUSES:
        sql += " AND status = ?"
        params.append(status)
    rows = get_db().execute(sql + " ORDER BY id DESC", params).fetchall()
    stats = get_db().execute(
        "SELECT COUNT(*) AS total, COALESCE(SUM(amount), 0) AS money, "
        "COALESCE(SUM(status != 'Выполнен'), 0) AS active FROM orders"
    ).fetchone()
    return render_template("index.html", rows=rows, stats=stats,
                           statuses=STATUSES, q=q, status=status)


@app.post("/orders")
def create():
    client = request.form.get("client", "").strip()
    item = request.form.get("item", "").strip()
    try:
        amount = int(request.form.get("amount", ""))
    except ValueError:
        abort(400, "Сумма должна быть целым числом")
    if not client or not item or amount < 0:
        abort(400, "Заполните все поля корректно")
    db = get_db()
    db.execute("INSERT INTO orders (client, item, amount) VALUES (?, ?, ?)",
               (client, item, amount))
    db.commit()
    return redirect(url_for("index"))


@app.post("/orders/<int:order_id>/next")
def next_status(order_id):
    db = get_db()
    row = db.execute("SELECT status FROM orders WHERE id = ?", (order_id,)).fetchone()
    if row is None:
        abort(404)
    new = STATUSES[(STATUSES.index(row["status"]) + 1) % len(STATUSES)]
    db.execute("UPDATE orders SET status = ? WHERE id = ?", (new, order_id))
    db.commit()
    return redirect(url_for("index"))


@app.post("/orders/<int:order_id>/delete")
def delete(order_id):
    db = get_db()
    db.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    db.commit()
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
