document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("imagenInput");
    const preview = document.getElementById("previewImg");

    if (!input) return;

    input.addEventListener("change", () => {
        const file = input.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = () => {
            preview.src = reader.result;
        };
        reader.readAsDataURL(file);
    });
});

