from app.extensions import db
from datetime import datetime, timezone

class Cliente(db.Model):
    __tablename__ = "cliente"

    # Valores comunes
    id_cliente = db.Column(db.Integer, primary_key = True)
    tipo = db.Column(
        db.Enum("persona", "empresa", name = "tipo_cliente_enum"), nullable = False
    )
    telefono = db.Column(db.String(20), nullable = False)
    email_contacto = db.Column(db.String(100), nullable = False)
    fecha_creacion = db.Column(
        db.DateTime,
        nullable = False,
        default = lambda: datetime.now(timezone.utc)
    )
    fecha_actualizacion = db.Column(
        db.DateTime, nullable = False,
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc)
    )

    # Valores exclusivos de personas fisicas
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    documento = db.Column(db.String(20), unique = True)

    # Valores exclusivos de empresas
    razon_social = db.Column(db.String(100))
    cuit = db.Column(db.String(20), unique = True)
    direccion = db.Column(db.String(100))

    # La separacion de personas - empresas se realiza mediante logica y no sql

    usuarios = db.relationship(
        "Usuario", back_populates = "cliente",
        cascade = "all, delete-orphan"
    )

    __table_args__ = (
        db.Index("ix_cliente_documento", "documento"),
        db.Index("ix_cliente_cuil", "cuit")
    )

    def validar(self):
        if self.tipo == "persona":
            if not self.nombre or not self.apellido or not self.documento:
                raise ValueError("Los campos nombre, apellido y documento son obligatorios")
        elif self.tipo == "empresa":
            if not self.razon_social or not self.cuit or not self.direccion:
                raise ValueError("Los campos razon social, cuit y direccion son obligatorios")
            
    def actualizar(self, datos: dict):
        campos_permitidos = {
            "telefono", "email_contacto", "nombre",
            "apellido", "documento", "razon_social",
            "cuit", "direccion",
        }

        for campo, valor in datos.items():
            if campo in campos_permitidos:
                setattr(self, campo, valor)
        self.validar()
    
    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "tipo": self.tipo,
            "telefono": self.telefono,
            "email_contacto": self.email_contacto,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "documento": self.documento,
            "razon_social": self.razon_social,
            "cuit": self.cuit,
            "direccion": self.direccion,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_actualizacion": self.fecha_actualizacion.isoformat(),
        }