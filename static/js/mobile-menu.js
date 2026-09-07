document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".mobile-menu-button");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            const nav = button.parentElement.querySelector("nav");

            if (nav) {
                nav.classList.toggle("mobile-open");

                const isOpen = nav.classList.contains("mobile-open");
                button.setAttribute("aria-expanded", isOpen);
            }
        });
    });
});
