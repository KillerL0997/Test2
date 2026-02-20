from app.extensions import db
from app.models.cliente import Cliente
from sqlalchemy.exc import IntegrityError

class ClienteService():

    @staticmethod
    def crear(data: dict) -> Cliente:
        cliente = Cliente(**data)
        cliente.validar()
        db.session.add(cliente)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Conflicto de integridad con base de datos")
        
        return cliente
    
    @staticmethod
    def listar(pag_ini: int = 1, pag_fin: int = 10):
        paginacion = Cliente.query.paginate(
            page= pag_ini,
            per_page= pag_fin,
            error_out= False
        )
        return paginacion
    
    @staticmethod
    def actualizar(id_cliente: int, data: dict) -> Cliente:
        cliente = Cliente.query.get(id_cliente)
        if not cliente:
            raise LookupError("Cliente no encontrado")
        cliente.actualizar(data)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Conflicto de integridad con la base de datos")
        return cliente
    
    @staticmethod
    def eliminar(id_cliente: int) -> None:
        cliente = Cliente.query.get(id_cliente)
        if not cliente:
            raise LookupError("Cliente no encontrado")
        db.session.delete(cliente)
        db.session.commit()