import hashlib
from config.database import get_connection
# Asegúrate de que el modelo esté en la carpeta correcta
from models.user_model import User 

class UserService:
    @staticmethod
    def get_all_users():
        print("\n--- INICIANDO GET_ALL_USERS ---")
        conn = get_connection()
        cursor = conn.cursor(as_dict=True)
        try:
            cursor.execute("SELECT * FROM Usuarios ORDER BY Id DESC")
            rows = cursor.fetchall()
            print(f" DEBUG: Filas encontradas en DB: {len(rows)}")
            
            users_list = []
            for row in rows:
                obj = User.from_dict(row)
                users_list.append(obj.to_dict())
            
            print(f" DEBUG: Lista final a retornar: {users_list}")
            return users_list
        except Exception as e:
            print(f" ERROR en get_all_users: {e}")
            return []
        finally:
            conn.close()
            print("--- CONEXIÓN CERRADA ---\n")

    @staticmethod
    def register_user(user_data):
        print("\n--- INICIANDO REGISTER_USER ---")
        print(f" DEBUG: Datos recibidos del front: {user_data}")
        
        user = User.from_dict(user_data)
        pwd = user_data.get('password') or user_data.get('Password') or ""
        user.password_hash = hashlib.sha256(pwd.encode()).hexdigest()

        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """INSERT INTO Usuarios (Nombre, ApellidoP, ApellidoM, Email, FechaNacimiento, PasswordHash, FechaRegistro) 
                       VALUES (%s, %s, %s, %s, %s, %s, GETDATE())"""
            params = (user.nombre, user.ap, user.am, user.email, user.fecha_nac, user.password_hash)
            print(f" DEBUG: Ejecutando INSERT con: {params}")
            
            cursor.execute(query, params)
            conn.commit()
            print(" DEBUG: Registro exitoso en DB")
            return True
        except Exception as e:
            print(f" ERROR en registro: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        print(f"\n--- BUSCANDO USUARIO ID: {user_id} ---")
        conn = get_connection()
        cursor = conn.cursor(as_dict=True)
        try:
            cursor.execute("SELECT * FROM Usuarios WHERE Id = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                print(f" DEBUG: Usuario encontrado: {row}")
                return User.from_dict(row).to_dict()
            print(" DEBUG: No se encontró el usuario")
            return None
        except Exception as e:
            print(f" ERROR en get_user_by_id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update_existing_user(user_data):
        print("\n--- INICIANDO UPDATE ---")
        user = User.from_dict(user_data)
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """UPDATE Usuarios SET Nombre=%s, ApellidoP=%s, ApellidoM=%s, Email=%s, FechaNacimiento=%s 
                       WHERE Id=%s"""
            params = (user.nombre, user.ap, user.am, user.email, user.fecha_nac, user.id)
            print(f" DEBUG: Actualizando ID {user.id} con datos: {params}")
            
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            print(f" ERROR en update: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete_user(user_id):
        print(f"\n--- ELIMINANDO USUARIO ID: {user_id} ---")
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Usuarios WHERE Id = %s", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f" ERROR en delete: {e}")
            return False
        finally:
            conn.close()