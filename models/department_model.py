class Departamento:
    def __init__(self, id=None, nombre=None, descripcion=None,
                 can_add=False, can_edit=False, can_delete=False, can_view=True):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.can_add = bool(can_add)
        self.can_edit = bool(can_edit)
        self.can_delete = bool(can_delete)
        self.can_view = bool(can_view)

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return Departamento(
            id=data.get('id') or data.get('Id'),
            nombre=data.get('nombre_depto') or data.get('NombreDepto'),
            descripcion=data.get('descripcion') or data.get('Descripcion'),
            can_add=data.get('can_add'),
            can_edit=data.get('can_edit'),
            can_delete=data.get('can_delete'),
            can_view=data.get('can_view')
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "permisos": {
                "crear": self.can_add,
                "editar": self.can_edit,
                "eliminar": self.can_delete,
                "ver": self.can_view
            }
        }
