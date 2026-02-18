const DeptoManager = {
    allDeptos: [],

    // --- SISTEMA DE NOTIFICACIONES TOAST ---
    showToast(msg, type = 'success') {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const existingToasts = Array.from(container.querySelectorAll('.toast-message'));
        if (existingToasts.some(t => t.innerText === msg)) return;

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

        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                toast.style.transition = 'all 0.4s ease';
                setTimeout(() => toast.remove(), 400);
            }
        }, 4000);
    },

    async init() {
        this.tableBody = document.getElementById('deptoTableBody');
        await this.loadDeptos();
    },

    // --- NUEVA FUNCIÓN SKELETON ---
    renderSkeleton() {
        const skeletonRow = `
            <tr>
                <td><div class="skeleton skeleton-text" style="width: 70%"></div></td>
                <td><div class="skeleton skeleton-text" style="width: 90%"></div></td>
                <td>
                    <div style="display: flex; gap: 5px;">
                        <div class="skeleton" style="width: 25px; height: 20px; border-radius: 4px;"></div>
                        <div class="skeleton" style="width: 25px; height: 20px; border-radius: 4px;"></div>
                        <div class="skeleton" style="width: 25px; height: 20px; border-radius: 4px;"></div>
                        <div class="skeleton" style="width: 25px; height: 20px; border-radius: 4px;"></div>
                    </div>
                </td>
                <td>
                    <div class="skeleton skeleton-btn" style="width: 80px;"></div>
                </td>
            </tr>
        `;
        // Llenamos la tabla con 5 filas de carga
        this.tableBody.innerHTML = skeletonRow.repeat(5);
    },

    async loadDeptos() {
        try {
            this.renderSkeleton();
            // Mostrar skeleton o limpiar tabla mientras carga
            const res = await fetch('/api/departments');
            const data = await res.json();
            this.allDeptos = Array.isArray(data) ? data : [];
            this.renderTable();
        } catch (e) {
            this.showToast("Error al conectar con el servidor", 'error');
        }
    },

    renderTable() {
        if (this.allDeptos.length === 0) {
            this.tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:#64748b;">No hay departamentos registrados.</td></tr>';
            return;
        }

        this.tableBody.innerHTML = this.allDeptos.map(d => `
            <tr id="row-${d.id}">
                <td><input type="text" class="inline-input bold" value="${d.nombre}" onchange="DeptoManager.quickUpdate(${d.id}, 'nombre', this.value)"></td>
                <td><input type="text" class="inline-input" value="${d.descripcion || ''}" placeholder="Añadir descripción..." onchange="DeptoManager.quickUpdate(${d.id}, 'descripcion', this.value)"></td>
                <td>
                    <div class="inline-permissions">
                        ${this.renderCheck(d.id, 'can_view', d.permisos.ver, 'R')}
                        ${this.renderCheck(d.id, 'can_add', d.permisos.crear, 'C')}
                        ${this.renderCheck(d.id, 'can_edit', d.permisos.editar, 'U')}
                        ${this.renderCheck(d.id, 'can_delete', d.permisos.eliminar, 'D')}
                    </div>
                </td>
                <td class="actions-cell">
                    <button class="btn-delete" onclick="DeptoManager.delete(${d.id})" title="Eliminar">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                </td>
            </tr>
        `).join('');
    },

    renderCheck(id, field, value, label) {
        return `
            <label class="custom-check">
                <input type="checkbox" ${value ? 'checked' : ''} onchange="DeptoManager.quickUpdate(${id}, '${field}', this.checked)">
                <span>${label}</span>
            </label>
        `;
    },

    addNewInlineRow() {
        if (document.getElementById('new-row-form')) return;

        const tr = document.createElement('tr');
        tr.id = 'new-row-form';
        tr.className = 'new-row-highlight';
        tr.innerHTML = `
            <td><input type="text" id="new-nombre" class="inline-input bold" placeholder="Nombre..."></td>
            <td><input type="text" id="new-desc" class="inline-input" placeholder="Descripción..."></td>
            <td>
                <div class="inline-permissions">
                    <label class="custom-check"><input type="checkbox" id="new-view" checked> <span>R</span></label>
                    <label class="custom-check"><input type="checkbox" id="new-add"> <span>C</span></label>
                    <label class="custom-check"><input type="checkbox" id="new-edit"> <span>U</span></label>
                    <label class="custom-check"><input type="checkbox" id="new-delete"> <span>D</span></label>
                </div>
            </td>
            <td class="actions-cell">
                <button class="btn-save-inline" onclick="DeptoManager.saveNew()">Guardar</button>
                <button class="btn-cancel-inline" onclick="this.parentElement.parentElement.remove()">X</button>
            </td>
        `;
        this.tableBody.appendChild(tr);
        document.getElementById('new-nombre').focus();
    },

    async saveNew() {
        const data = {
            nombre: document.getElementById('new-nombre').value,
            descripcion: document.getElementById('new-desc').value,
            can_view: document.getElementById('new-view').checked,
            can_add: document.getElementById('new-add').checked,
            can_edit: document.getElementById('new-edit').checked,
            can_delete: document.getElementById('new-delete').checked
        };

        if (!data.nombre) {
            this.showToast("El nombre es obligatorio", 'error');
            return;
        }

        try {
            const res = await fetch('/api/departments', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                this.showToast("Departamento creado con éxito", 'success');
                await this.loadDeptos();
            } else {
                this.showToast("Error al guardar el departamento", 'error');
            }
        } catch (e) {
            this.showToast("Error de conexión", 'error');
        }
    },

    async quickUpdate(id, field, value) {
        const depto = this.allDeptos.find(d => d.id == id);
        const data = {
            id: id,
            nombre: field === 'nombre' ? value : depto.nombre,
            descripcion: field === 'descripcion' ? value : depto.descripcion,
            can_view: field === 'can_view' ? value : depto.permisos.ver,
            can_add: field === 'can_add' ? value : depto.permisos.crear,
            can_edit: field === 'can_edit' ? value : depto.permisos.editar,
            can_delete: field === 'can_delete' ? value : depto.permisos.eliminar
        };

        try {
            const res = await fetch('/api/departments', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                this.showToast("Cambio guardado", 'info');
                // Actualización local
                const idx = this.allDeptos.findIndex(d => d.id == id);
                if (field === 'nombre' || field === 'descripcion') {
                    this.allDeptos[idx][field] = value;
                } else {
                    const map = { 'can_view': 'ver', 'can_add': 'crear', 'can_edit': 'editar', 'can_delete': 'eliminar' };
                    this.allDeptos[idx].permisos[map[field]] = value;
                }
            }
        } catch (e) {
            this.showToast("Error al actualizar", 'error');
        }
    },

    async delete(id) {
        if (!confirm("¿Seguro que desea eliminar este departamento?")) return;

        try {
            const res = await fetch('/api/departments', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: id })
            });

            if (res.ok) {
                this.showToast("Departamento eliminado", 'warning');
                await this.loadDeptos();
            } else {
                this.showToast("No se pudo eliminar", 'error');
            }
        } catch (e) {
            this.showToast("Error de conexión", 'error');
        }
    }
};

document.addEventListener('DOMContentLoaded', () => DeptoManager.init());