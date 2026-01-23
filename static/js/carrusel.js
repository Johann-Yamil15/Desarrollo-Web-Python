const inputFile = document.getElementById("imagenInput");
const previewImg = document.getElementById("previewImg");
const btnGuardar = document.getElementById("btnGuardar");
const fileError = document.getElementById("fileError");

// Extensiones permitidas
const allowedExtensions = ["jpg", "jpeg", "png", "webp"];

// Tipos MIME permitidos (más seguro)
const allowedMimeTypes = [
    "image/jpeg",
    "image/png",
    "image/webp"
];

inputFile.addEventListener("change", function () {
    const file = this.files[0];

    // Reset
    btnGuardar.disabled = true;
    previewImg.src = "";
    fileError.classList.add("d-none");

    if (!file) return;

    const extension = file.name.split(".").pop().toLowerCase();
    const mimeType = file.type;

    // Validación fuerte
    if (
        !allowedExtensions.includes(extension) ||
        !allowedMimeTypes.includes(mimeType)
    ) {
        this.value = ""; // borra archivo
        fileError.classList.remove("d-none");
        return;
    }

    // Preview seguro
    const reader = new FileReader();
    reader.onload = e => {
        previewImg.src = e.target.result;
    };
    reader.readAsDataURL(file);

    // Archivo válido → habilitar botón
    btnGuardar.disabled = false;
});
