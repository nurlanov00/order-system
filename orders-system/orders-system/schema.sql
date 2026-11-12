CREATE TABLE IF NOT EXISTS orders (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    client     TEXT    NOT NULL,
    item       TEXT    NOT NULL,
    amount     INTEGER NOT NULL CHECK (amount >= 0),
    status     TEXT    NOT NULL DEFAULT 'Новый'
               CHECK (status IN ('Новый', 'В работе', 'Выполнен')),
    created_at TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
