const UserManager = {
    allUsers: [], // Lista original para filtrado local
    allDepartments: [],

    init() {
        this.form = document.getElementById('userForm');
        this.tableBody = document.getElementById('userTableBody');
        this.modal = document.getElementById('userModal');
        this.btnNew = document.getElementById('btnNewUser');

        this.deptoSelect = document.getElementById('deptoSelect');

        // Inputs de búsqueda y filtros
        this.searchInput = document.getElementById('searchInput');
        this.dateFrom = document.getElementById('dateFrom');
        this.dateTo = document.getElementById('dateTo');
        this.btnToggle = document.getElementById('btnToggleFilters');
        this.advancedFilters = document.getElementById('advancedFilters');
        this.btnClear = document.getElementById('btnClearFilters');

        // Elementos de validación
        this.birthdateInput = document.getElementById('birthdateInput');
        this.emailInput = document.getElementById('emailInput');

        this.bindEvents();
        this.setupValidations();
        this.loadDepartments();
        this.loadUsers();
    },

    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.btnNew.onclick = () => this.openModal();

        // Alternar visibilidad de filtros de fecha
        if (this.btnToggle) {
            this.btnToggle.onclick = () => {
                const pill = document.getElementById('searchPill');
                const isNowCollapsed = this.advancedFilters.classList.toggle('collapsed');
                pill.classList.toggle('expanded', !isNowCollapsed);
            };
        }

        // Botón Limpiar filtros
        if (this.btnClear) {
            this.btnClear.onclick = () => this.resetFilters();
        }

        // Búsqueda en tiempo real
        [this.searchInput, this.dateFrom, this.dateTo].forEach(el => {
            if (el) el.addEventListener('input', () => this.applyFilters());
        });
    },

    renderSkeleton() {
        const skeletonRow = `
            <tr>
                <td><div class="skeleton skeleton-text"></div></td>
                <td><div class="skeleton skeleton-text"></div></td>
                <td><div class="skeleton skeleton-text"></div></td>
                <td><div class="skeleton skeleton-text"></div></td> 
                <td>
                    <div class="skeleton skeleton-btn"></div>
                    <div class="skeleton skeleton-btn"></div>
                </td>
            </tr>
        `;
        // Repetimos la fila 5 veces para llenar la tabla
        this.tableBody.innerHTML = skeletonRow.repeat(5);
    },

    // --- CARGAR DEPARTAMENTOS ---
    async loadDepartments() {
        try {
            const res = await fetch('/api/departments'); // Asegúrate de tener esta ruta en tu API
            const data = await res.json();
            this.allDepartments = Array.isArray(data) ? data : [];
            this.renderDeptos();
        } catch (e) {
            console.error("Error cargando departamentos:", e);
        }
    },

    renderDeptos() {
        if (!this.deptoSelect) return;

        const options = this.allDepartments.map(d =>
            `<option value="${d.id}">${d.nombre}</option>`
        ).join('');

        this.deptoSelect.innerHTML = `<option value="">Seleccione un departamento...</option>` + options;
    },

    // --- RENDERIZADO DE TABLA ---
    renderTable(users) {
        if (Array.isArray(users) && users.length > 0) {
            this.tableBody.innerHTML = users.map(u => {
                // Buscamos el nombre del departamento para mostrarlo en la tabla
                const depto = this.allDepartments.find(d => d.id == u.departamento_id);
                const deptoNombre = depto ? depto.nombre : '<span class="text-muted">Sin asignar</span>';

                return `
                <tr>
                    <td>${u.nombre} ${u.ap} ${u.am || ''}</td>
                    <td>${u.email}</td>
                    <td>${deptoNombre}</td>
                    <td>${u.fecha_nac}</td>
                    <td>
                        <button class="btn-edit" onclick="UserManager.openModal(${u.id})">Editar</button>
                        <button class="btn-delete" onclick="UserManager.delete(${u.id})">Eliminar</button>
                    </td>
                </tr>
            `}).join('');
        } else {
            this.tableBody.innerHTML = '<tr><td colspan="5">No se encontraron registros.</td></tr>';
        }
    },

    async loadUsers() {
        this.renderSkeleton(); // <--- Agregado: Mostrar skeletons antes del fetch
        try {
            const res = await fetch('/api/users');
            const data = await res.json();
            // El renderTable sustituirá los skeletons automáticamente al terminar
            this.allUsers = Array.isArray(data) ? data : [];
            this.renderTable(this.allUsers);
        } catch (e) {
            this.showToast("Error de conexión al cargar lista", 'error');
            this.tableBody.innerHTML = '<tr><td colspan="4">Error al cargar datos.</td></tr>';
        }
    },

    // --- FILTRADO ---
    applyFilters() {
        const term = this.searchInput.value.toLowerCase().trim();
        const from = this.dateFrom.value;
        const to = this.dateTo.value;

        const filtered = this.allUsers.filter(u => {
            const fullName = `${u.nombre} ${u.ap} ${u.am || ''}`
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "");

            const matchesTerm = term === "" || fullName.includes(term);

            const userDate = u.fecha_nac;
            let matchesDate = true;
            if (from && userDate < from) matchesDate = false;
            if (to && userDate > to) matchesDate = false;

            return matchesTerm && matchesDate;
        });

        this.renderTable(filtered);
    },

    resetFilters() {
        this.searchInput.value = "";
        this.dateFrom.value = "";
        this.dateTo.value = "";
        this.renderTable(this.allUsers);
    },

    // --- VALIDACIONES ---
    setupValidations() {
        const nameInput = document.getElementById('name');
        const apPaterno = document.getElementById('ap_paterno');
        const apMaterno = document.getElementById('ap_materno');

        const soloLetras = function () {
            this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]/g, '');
        };

        const prevenirEspacioInicial = function (e) {
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

        if (this.birthdateInput) {
            const todayLocal = new Date().toISOString().split('T')[0];
            this.birthdateInput.max = todayLocal;
        }

        this.birthdateInput.addEventListener('blur', () => {
            const selectedDate = new Date(this.birthdateInput.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (selectedDate > today) {
                document.getElementById('error_birthdate').innerText = "No se permiten fechas futuras";
                this.birthdateInput.value = "";
            }
        });
    },

    // --- ACCIONES CRUD ---
    async openModal(id = null) {
        this.form.reset();
        this.clearErrors();

        // Importante: Resetear el estado del botón al abrir
        const submitBtn = this.form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = "1";
            submitBtn.innerText = id ? 'Guardar Cambios' : 'Registrar Usuario';
        }

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
                if (this.deptoSelect) {
                    this.deptoSelect.value = u.departamento_id || "";
                }
            } catch (e) {
                this.showToast("Error al obtener datos", 'error');
            }
        }
        this.modal.style.display = 'flex';
    },

    // --- ELIMINAR ---
    async delete(id) {
        this.userToDeleteId = id;
        const deleteModal = document.getElementById('deleteModal');

        // Resetear botón de confirmar por si acaso quedó trabado
        const confirmBtn = document.getElementById('confirmDeleteBtn');
        confirmBtn.disabled = false;
        confirmBtn.innerText = "Sí, eliminar";

        deleteModal.style.display = 'flex';
        confirmBtn.onclick = () => this.executeDelete();
    },

    async executeDelete() {
        const id = this.userToDeleteId;
        if (!id) return;

        const confirmBtn = document.getElementById('confirmDeleteBtn');
        if (confirmBtn.disabled) return;

        confirmBtn.disabled = true;
        confirmBtn.innerText = "Eliminando...";

        try {
            const res = await fetch('/api/users', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: id })
            });
            const result = await res.json();

            if (result.success) {
                this.showToast(result.msg, 'warning');
                await this.loadUsers();
                this.closeDeleteModal();
            } else {
                this.showToast(result.msg, 'error');
                // Re-habilitar si falló el borrado por lógica de negocio
                confirmBtn.disabled = false;
                confirmBtn.innerText = "Confirmar";
            }
        } catch (e) {
            this.showToast("Error al eliminar", 'error');
            confirmBtn.disabled = false;
            confirmBtn.innerText = "Confirmar";
        } finally {
            this.closeDeleteModal();
        }
    },

    closeDeleteModal() {
        const deleteModal = document.getElementById('deleteModal');
        deleteModal.style.display = 'none';
        this.userToDeleteId = null;
    },

    async handleSubmit(e) {
        e.preventDefault();
        this.clearErrors();

        // 1. Identificar y bloquear el botón
        const submitBtn = this.form.querySelector('button[type="submit"]');
        if (!submitBtn || submitBtn.disabled) return; // Si ya está bloqueado, salir

        const originalText = submitBtn.innerText;
        submitBtn.disabled = true; // Bloqueo funcional
        submitBtn.style.opacity = "0.7";
        submitBtn.innerText = "Guardando..."; // Feedback visual

        const data = Object.fromEntries(new FormData(this.form));

        try {
            const res = await fetch('/api/users', {
                method: data.id ? 'PUT' : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.success) {
                this.showToast(result.msg, 'success');
                this.closeModal();
                await this.loadUsers();
                // Nota: Al cerrar el modal y resetear el form, el botón vuelve a su estado natural solo
            } else {
                // Error de validación (ej. correo duplicado)
                this.handleBackendErrors(result.errors);
                this.showToast(result.msg || "Error de validación", 'error');

                // RE-HABILITAMOS para que el usuario corrija y vuelva a intentar
                submitBtn.disabled = false;
                submitBtn.style.opacity = "1";
                submitBtn.innerText = originalText;
            }
        } catch (e) {
            console.error("Detalle técnico:", e);
            this.showToast("Error de conexión. Intente de nuevo.", 'error');

            // RE-HABILITAMOS en caso de error de red
            submitBtn.disabled = false;
            submitBtn.style.opacity = "1";
            submitBtn.innerText = originalText;
        }
    },

    // --- UTILIDADES ---
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

    // --- SISTEMA DE NOTIFICACIONES TOAST ---
    showToast(msg, type = 'success') {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        // --- LÓGICA ANTISPAM ---
        // Buscamos si ya existe un toast con el mismo mensaje exacto
        const existingToasts = Array.from(container.querySelectorAll('.toast-message'));
        const isDuplicate = existingToasts.some(t => t.innerText === msg);

        if (isDuplicate) return; // Si ya existe uno igual, no hacemos nada
        // -----------------------

        const config = {
            success: { icon: 'fa-check-circle', title: 'Éxito' },
            error: { icon: 'fa-times-circle', title: 'Error' },
            warning: { icon: 'fa-exclamation-triangle', title: 'Atención' },
            info: { icon: 'fa-info-circle', title: 'Info' }
        };

        const typeKey = typeof type === 'boolean' ? (type ? 'success' : 'error') : type;
        const { icon, title } = config[typeKey] || config.success;

        const toast = document.createElement('div');
        toast.className = `toast ${typeKey}`;

        toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <div class="toast-content">
            <span class="toast-title">${title}</span>
            <span class="toast-message">${msg}</span>
        </div>
        <i class="fas fa-times" style="cursor:pointer; font-size: 12px; opacity: 0.7;" onclick="this.parentElement.remove()"></i>
    `;

        container.appendChild(toast);

        // Auto-eliminar con salida suave
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                toast.style.transition = 'all 0.4s ease';
                setTimeout(() => toast.remove(), 400);
            }
        }, 4000);
    }
};

document.addEventListener('DOMContentLoaded', () => UserManager.init());