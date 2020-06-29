document.addEventListener('DOMContentLoaded', () => {
    installBurgerListener();
    installAlertDiscardListeners();
})

function installBurgerListener() {
    document.querySelector("#burger").addEventListener("click", function() {
        const navLinks = document.querySelectorAll(".nav-item");
        const hideClass = "hidden-on-mobile";
        navLinks.forEach(link => {
            link.classList.contains(hideClass) ? link.classList.remove(hideClass) : link.classList.add(hideClass)
        });
    });
}

function installAlertDiscardListeners() {
    discardBtns = document.querySelectorAll(".close");
    discardBtns.forEach(btn => {
        btn.addEventListener("click", function() {
            this.closest("div").remove();
        });
    });
}