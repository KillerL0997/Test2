from app.extensions import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuario"
    id_usuario = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(250), nullable = False, unique = True)
    password_hash = db.Column(db.String(250), nullable = False)
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id_rol"), nullable = False)
    fecha_creacion = db.Column(
        db.DateTime,
        nullable = False, 
        default = lambda: datetime.now(timezone.utc)
    )
    id_cliente = db.Column(
        db.Integer, db.ForeignKey("cliente.id_cliente", ondelete = "CASCADE"), nullable = False
    )

    rol = db.relationship(
        "Rol", back_populates = "usuarios", lazy = "joined"
    )
    cliente = db.relationship("Cliente", back_populates = "usuarios")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Id: {self.id_usuario} - Email: {self.email}'