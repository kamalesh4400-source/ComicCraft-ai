document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("comic-form");
    if (!form) return;
    form.addEventListener("submit", () => {
        const button = document.getElementById("generate-btn");
        if (!button) return;
        button.disabled = true;
        button.querySelector(".btn-text").hidden = true;
        button.querySelector(".btn-loading").hidden = false;
    });
});
