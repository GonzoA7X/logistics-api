const API_URL = "http://localhost:8000";

// Al cargar la página, revisar si hay sesión
document.addEventListener('DOMContentLoaded', () => {
    checkLoginStatus();
});

// --- NAVEGACIÓN ---
function showTab(tabName) {
    document.getElementById('tab-rastreo').classList.add('hidden');
    document.getElementById('tab-admin').classList.add('hidden');
    document.getElementById('btn-rastreo').classList.remove('active');
    document.getElementById('btn-admin').classList.remove('active');

    document.getElementById(`tab-${tabName}`).classList.remove('hidden');
    document.getElementById(`btn-${tabName}`).classList.add('active');

    if(tabName === 'admin') checkLoginStatus();
}

// --- RASTREO PÚBLICO ---
async function buscarPaquete() {
    const guia = document.getElementById('input-guia').value.trim();
    const errorEl = document.getElementById('error-rastreo');
    const resultEl = document.getElementById('resultado-rastreo');
    
    if(!guia) return;
    
    try {
        const response = await fetch(`${API_URL}/rastreo/${guia}`);
        const data = await response.json();

        if(!response.ok) throw new Error(data.detail || "Error al buscar");

        errorEl.classList.add('hidden');
        resultEl.classList.remove('hidden');

        document.getElementById('res-guia').innerText = `Guía: ${data.paquete.numero_guia}`;
        document.getElementById('res-destino').innerText = `Destino: ${data.paquete.direccion_destino}`;
        
        const badge = document.getElementById('badge-estado');
        badge.innerText = data.paquete.estado_envio;
        badge.className = `status-badge status-${data.paquete.estado_envio}`;

        // Construir Timeline
        const timeline = document.getElementById('timeline-movimientos');
        timeline.innerHTML = '';
        data.historial.forEach(mov => {
            const date = new Date(mov.fecha).toLocaleString('es-MX');
            timeline.innerHTML += `
                <div class="timeline-item">
                    <div class="time-date">${date}</div>
                    <div class="time-loc">${mov.ubicacion}</div>
                    <div class="status-badge status-${mov.estado}" style="font-size: 0.6rem; margin-top: 0.5rem">${mov.estado}</div>
                </div>
            `;
        });

    } catch (err) {
        resultEl.classList.add('hidden');
        errorEl.innerText = err.message;
        errorEl.classList.remove('hidden');
    }
}

// Permitir buscar con Enter
document.getElementById('input-guia').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') buscarPaquete();
});

// --- AUTENTICACIÓN ADMIN ---
function checkLoginStatus() {
    const token = localStorage.getItem('jwt_token');
    if(token) {
        document.getElementById('login-section').classList.add('hidden');
        document.getElementById('dashboard-section').classList.remove('hidden');
        document.getElementById('btn-logout').classList.remove('hidden');
        cargarPaquetesAdmin();
    } else {
        document.getElementById('login-section').classList.remove('hidden');
        document.getElementById('dashboard-section').classList.add('hidden');
        document.getElementById('btn-logout').classList.add('hidden');
    }
}

async function login() {
    const user = document.getElementById('admin-user').value;
    const pass = document.getElementById('admin-pass').value;
    const errorEl = document.getElementById('error-login');

    const formData = new URLSearchParams();
    formData.append('username', user);
    formData.append('password', pass);

    try {
        const response = await fetch(`${API_URL}/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        const data = await response.json();

        if(!response.ok) throw new Error(data.detail || "Error de conexión");

        localStorage.setItem('jwt_token', data.access_token);
        errorEl.classList.add('hidden');
        document.getElementById('admin-pass').value = ''; // Limpiar contraseña
        checkLoginStatus();
    } catch (err) {
        errorEl.innerText = err.message;
        errorEl.classList.remove('hidden');
    }
}

function logout() {
    localStorage.removeItem('jwt_token');
    checkLoginStatus();
}

// --- DASHBOARD ADMIN ---
async function cargarPaquetesAdmin() {
    const token = localStorage.getItem('jwt_token');
    const tbody = document.getElementById('tabla-paquetes');
    tbody.innerHTML = '<tr><td colspan="4">Cargando...</td></tr>';

    try {
        const response = await fetch(`${API_URL}/paquetes/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if(response.status === 401) { logout(); return; }
        
        const paquetes = await response.json();
        tbody.innerHTML = '';
        
        paquetes.forEach(p => {
            tbody.innerHTML += `
                <tr>
                    <td>${p.numero_guia}</td>
                    <td><span class="status-badge status-${p.estado_envio}" style="font-size: 0.7rem">${p.estado_envio}</span></td>
                    <td>${p.direccion_destino}</td>
                    <td><button class="btn-small" onclick="abrirModal(${p.id}, '${p.numero_guia}', '${p.estado_envio}')">Modificar</button></td>
                </tr>
            `;
        });
    } catch (err) {
        console.error(err);
        tbody.innerHTML = '<tr><td colspan="4">Error al cargar paquetes.</td></tr>';
    }
}

// --- MODAL DE ACTUALIZACIÓN ---
function abrirModal(id, guia, estado) {
    document.getElementById('modal-id').value = id;
    document.getElementById('modal-guia').innerText = guia;
    document.getElementById('modal-estado').value = estado;
    document.getElementById('modal-ubicacion').value = '';
    document.getElementById('modal-update').classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modal-update').classList.add('hidden');
}

async function guardarActualizacion() {
    const id = document.getElementById('modal-id').value;
    const estado = document.getElementById('modal-estado').value;
    const ubicacion = document.getElementById('modal-ubicacion').value.trim();

    if(!ubicacion) { alert("La ubicación actual es obligatoria"); return; }

    const token = localStorage.getItem('jwt_token');
    
    try {
        const response = await fetch(`${API_URL}/paquetes/${id}`, {
            method: 'PATCH',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                estado_envio: estado,
                ubicacion_actual: ubicacion
            })
        });

        if(!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Error al actualizar");
        }

        cerrarModal();
        cargarPaquetesAdmin(); // Refrescar la tabla
    } catch (err) {
        alert("Error: " + err.message);
    }
}
