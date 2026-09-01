CREATE TABLE IF NOT EXISTS vendas_transformadas (
    id_venda INTEGER PRIMARY KEY,
    quantidade INTEGER NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL
);
