from config.database import get_connection
from models.department_model import Departamento

class DepartmentService:
    @staticmethod
    def get_all_departments():
        conn = get_connection()
        cursor = conn.cursor(as_dict=True)
        try:
            cursor.execute("SELECT * FROM Departamentos ORDER BY nombre_depto ASC")
            rows = cursor.fetchall()
            return [Departamento.from_dict(row).to_dict() for row in rows]
        except Exception as e:
            print(f" ERROR en get_all_departments: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def add_department(data):
        """Inserta un nuevo departamento con sus permisos"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Departamentos 
                (nombre_depto, descripcion, can_add, can_edit, can_delete, can_view)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                data.get('nombre'),
                data.get('descripcion'),
                data.get('can_add', False),
                data.get('can_edit', False),
                data.get('can_delete', False),
                data.get('can_view', True)
            )
            cursor.execute(query, params)
            conn.commit()
            return True, "Departamento creado exitosamente"
        except Exception as e:
            print(f" ERROR en add_department: {e}")
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def update_department(depto_id, data):
        """Actualiza nombre, descripción y permisos de un departamento existente"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE Departamentos SET 
                    nombre_depto = %s, 
                    descripcion = %s, 
                    can_add = %s, 
                    can_edit = %s, 
                    can_delete = %s, 
                    can_view = %s
                WHERE Id = %s
            """
            params = (
                data.get('nombre'),
                data.get('descripcion'),
                data.get('can_add', False),
                data.get('can_edit', False),
                data.get('can_delete', False),
                data.get('can_view', True),
                depto_id
            )
            cursor.execute(query, params)
            conn.commit()
            return True, "Departamento actualizado correctamente"
        except Exception as e:
            print(f" ERROR en update_department: {e}")
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def delete_department(depto_id):
        """Elimina un departamento (Ojo: Validar si tiene usuarios asociados primero)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Opcional: Validar si hay usuarios en este depto para evitar errores de FK
            cursor.execute("SELECT COUNT(*) as total FROM Usuarios WHERE departamento_id = %s", (depto_id,))
            if cursor.fetchone()['total'] > 0:
                return False, "No se puede eliminar: Hay usuarios asociados a este departamento"

            cursor.execute("DELETE FROM Departamentos WHERE Id = %s", (depto_id,))
            conn.commit()
            return True, "Departamento eliminado"
        except Exception as e:
            print(f" ERROR en delete_department: {e}")
            return False, str(e)
        finally:
            conn.close()