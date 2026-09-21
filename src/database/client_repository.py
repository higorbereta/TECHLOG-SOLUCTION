from cliente import Cliente

class ClientRepository():
    def __init__(self, db):
        self.db = db

    async def list_client(self) -> list[Cliente]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            rows = cursor.fetchall()
            return [Cliente(id_=row[0], nome=row[1], email=row[2], telefone=row[3]) for row in rows]