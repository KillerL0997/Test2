from app.extensions import db

class Rol(db.Model):
    __tablename__ = "rol"

    id_rol = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False, unique = True)
    descripcion = db.Column(db.String(250), nullable = True)

    usuarios = db.relationship(
        "Usuario", back_populates = "rol", lazy = "selectin"
    )

    def __repr__(self):  
        return f'Id: {self.id_rol} - Nombre: {self.nombre}'