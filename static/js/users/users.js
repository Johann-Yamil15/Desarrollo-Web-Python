const UserManager = {
    init() {
        // Referencias al DOM
        this.form = document.getElementById('userForm');
        this.tableBody = document.getElementById('userTableBody');
        this.modal = document.getElementById('userModal');
        this.btnNew = document.getElementById('btnNewUser');
        
        // Elementos de validación específicos
        this.birthdateInput = document.getElementById('birthdateInput');
        this.emailInput = document.getElementById('emailInput');

        this.bindEvents();
        this.setupValidations();
        this.loadUsers();
    },

    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.btnNew.onclick = () => this.openModal();
    },

    setupValidations() {
        // 1. NOMBRE Y APELLIDOS: solo letras y espacios
        const nameInput = document.getElementById('name');
        const apPaterno = document.getElementById('ap_paterno');
        const apMaterno = document.getElementById('ap_materno');

        const soloLetras = function(e) {
            this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]/g, '');
        };

        const prevenirEspacioInicial = function(e) {
            if (e.key === ' ' && this.value.length === 0) {
                e.preventDefault();
            }
        };

        [nameInput, apPaterno, apMaterno].forEach(input => {
            if (input) {
                input.addEventListener('input', soloLetras);
                input.addEventListener('keydown', prevenirEspacioInicial);
            }
        });

        // 2. FECHA: Configurar límite dinámico (Hoy)
        if (this.birthdateInput) {
            this.birthdateInput.max = new Date().toISOString().split("T")[0];
        }

        // 3. LIMPIEZA DE ERRORES: Quitar mensajes rojos al escribir
        [this.birthdateInput, this.emailInput].forEach(input => {
            if (input) {
                input.addEventListener('input', () => {
                    const errorId = input.id === 'birthdateInput' ? 'error_birthdate' : 'error_email';
                    const errorDiv = document.getElementById(errorId);
                    if (errorDiv) errorDiv.innerText = "";
                });
            }
        });
    },

    async loadUsers() {
        try {
            const res = await fetch('/api/users');
            const data = await res.json();

            if (Array.isArray(data) && data.length > 0) {
                this.tableBody.innerHTML = data.map(u => `
                    <tr>
                        <td>${u.id}</td>
                        <td>${u.nombre} ${u.ap}</td>
                        <td>${u.email}</td>
                        <td>
                            <button class="btn-edit" onclick="UserManager.openModal(${u.id})">Editar</button>
                            <button class="btn-delete" onclick="UserManager.delete(${u.id})">Eliminar</button>
                        </td>
                    </tr>
                `).join('');
            } else {
                this.tableBody.innerHTML = '<tr><td colspan="4">No hay usuarios registrados.</td></tr>';
            }
        } catch (e) {
            this.showToast("Error de conexión al cargar lista", false);
        }
    },

    async openModal(id = null) {
        this.form.reset();
        this.clearErrors(); // Limpiar errores visuales al abrir
        this.form.id.value = id || "";
        document.getElementById('modalTitle').innerText = id ? 'Editar Usuario' : 'Nuevo Usuario';

        if (id) {
            try {
                const res = await fetch(`/api/users?id=${id}`);
                const u = await res.json();
                
                this.form.nombre.value = u.nombre || "";
                this.form.ap.value = u.ap || "";
                this.form.am.value = u.am || "";
                this.form.email.value = u.email || "";
                this.form.fecha_nac.value = u.fecha_nac || "";
            } catch (e) {
                this.showToast("Error al obtener datos", false);
            }
        }
        this.modal.style.display = 'flex';
    },

    async delete(id) {
        if (!confirm("¿Estás seguro de que deseas eliminar este usuario?")) return;

        try {
            const res = await fetch('/api/users', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: id })
            });
            const result = await res.json();
            this.showToast(result.msg, result.success);
            if (result.success) this.loadUsers();
        } catch (e) {
            this.showToast("Error al eliminar", false);
        }
    },

    async handleSubmit(e) {
        e.preventDefault();
        this.clearErrors();
        
        const data = Object.fromEntries(new FormData(this.form));
        const method = data.id ? 'PUT' : 'POST';

        try {
            const res = await fetch('/api/users', {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await res.json();
            
            if (result.success) {
                this.showToast(result.msg, true);
                this.closeModal();
                this.loadUsers();
            } else {
                // Si el backend manda errores específicos de validación
                this.handleBackendErrors(result.errors);
                this.showToast(result.msg || "Verifica los datos", false);
            }
        } catch (e) {
            this.showToast("Error al guardar datos", false);
        }
    },

    handleBackendErrors(errors) {
        if (!errors) return;
        if (errors.email) document.getElementById('error_email').innerText = errors.email;
        if (errors.fecha_nac) document.getElementById('error_birthdate').innerText = errors.fecha_nac;
    },

    clearErrors() {
        document.querySelectorAll('.error-text').forEach(div => div.innerText = "");
    },

    closeModal() {
        this.modal.style.display = 'none';
    },

    showToast(msg, success) {
        let container = document.querySelector('.toast-container') || (() => {
            const c = document.createElement('div');
            c.className = 'toast-container';
            document.body.appendChild(c);
            return c;
        })();

        const toast = document.createElement('div');
        toast.className = `toast ${success ? 'success' : 'error'}`;
        toast.innerText = msg;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }
};

document.addEventListener('DOMContentLoaded', () => UserManager.init());