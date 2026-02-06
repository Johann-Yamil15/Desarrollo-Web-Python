class CarruselItem:
    def __init__(self, id=None, nombre_archivo=None, ruta_relativa=None, fecha_carga=None):
        self.id = id
        self.nombre_archivo = nombre_archivo
        self.ruta_relativa = ruta_relativa
        self.fecha_carga = fecha_carga

    @staticmethod
    def from_dict(data):
        if not data: return None
        return CarruselItem(
            id=data.get('id'),
            nombre_archivo=data.get('nombre_archivo'),
            ruta_relativa=data.get('ruta_relativa'),
            fecha_carga=data.get('fecha_carga')
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_archivo": self.nombre_archivo,
            "ruta_relativa": self.ruta_relativa,
            "fecha_carga": str(self.fecha_carga) if self.fecha_carga else None
        }