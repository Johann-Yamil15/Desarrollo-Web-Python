const inputFile = document.getElementById("imagenInput");
const previewImg = document.getElementById("previewImg");
const previewContainer = document.getElementById("previewContainer");
const btnGuardar = document.getElementById("btnGuardar");
const fileError = document.getElementById("fileError");

inputFile.addEventListener("change", function () {
    const file = this.files[0];
    
    // Reset de estados con validación de existencia
    btnGuardar.disabled = true;
    if (fileError) fileError.classList.add("d-none");
    previewContainer.classList.add("d-none");

    if (!file) return;

    const allowed = ["jpg", "jpeg", "png", "webp"];
    const ext = file.name.split(".").pop().toLowerCase();

    if (!allowed.includes(ext)) {
        if (fileError) fileError.classList.remove("d-none");
        this.value = "";
        return;
    }

    // Lector para la vista previa
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        previewContainer.classList.remove("d-none");
        btnGuardar.disabled = false;
    };
    reader.readAsDataURL(file);
});

// Limpiar modal al cerrar
const modalEl = document.getElementById('uploadModal');
if (modalEl) {
    modalEl.addEventListener('hidden.bs.modal', function () {
        inputFile.value = "";
        previewContainer.classList.add("d-none");
        btnGuardar.disabled = true;
        if (fileError) fileError.classList.add("d-none");
    });
}