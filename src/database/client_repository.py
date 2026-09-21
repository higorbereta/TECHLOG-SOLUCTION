from src.cliente import Cliente

class ClientRepository():
    def __init__(self, db):
        self.db = db

    async def list_client(self) -> list[Cliente]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            rows = cursor.fetchall()
            return [Cliente(id_=row[0], nome=row[1], email=row[2], telefone=row[3]) for row in rows]


    async def get_client_by_id(self, client_id: int) -> Cliente | None:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes WHERE id = ?", (client_id,))
            row = cursor.fetchone()
            if row:
                return Cliente(id_=row[0], nome=row[1], email=row[2], telefone=row[3])
            return None

    async def create_client(self, client: Cliente) -> Cliente:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                (client.nome, client.email, client.telefone)
            )
            conn.commit()
            client.id_ = cursor.lastrowid
            return Cliente(id_=client.id_, nome=client.nome, email=client.email, telefone=client.telefone)

    async def update_client(self, client: Cliente) -> Cliente | None:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
                (client.nome, client.email, client.telefone, client.id_)
            )
            conn.commit()
            if cursor.rowcount > 0:
                return Cliente(id_=client.id_, nome=client.nome, email=client.email, telefone=client.telefone)
            return None

    async def delete_client(self, client_id: int) -> bool:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = ?", (client_id,))
            conn.commit()
            return cursor.rowcount > 0