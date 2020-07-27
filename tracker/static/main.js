document.addEventListener('DOMContentLoaded', () => {
    installBurgerListener();
    makeAlertsFadeOut();
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

function makeAlertsFadeOut() {
    alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        fadeOut(alert);
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

function addMessage(msg) {
    const mainMsgDiv = document.querySelector("#messages");
    const outerDiv = document.createElement("div");
    outerDiv.classList.add("container", "alert", `alert-${msg.tag}`);
    mainMsgDiv.appendChild(outerDiv);
    const innerDiv = document.createElement("div");
    innerDiv.classList.add("main", "container", "message");    
    outerDiv.appendChild(innerDiv);
    const msgDiv = document.createElement("div");
    msgDiv.innerHTML = `${msg.text}`;    
    innerDiv.appendChild(msgDiv);
    const btn = document.createElement("button");
    btn.setAttribute('type', 'button');
    btn.setAttribute('class', 'close');
    btn.setAttribute('data-dismiss', 'alert'); 
    btn.setAttribute('aria-label', 'Close');    
    innerDiv.appendChild(btn);
    const span = document.createElement("span");
    span.setAttribute('aria-hidden', 'true');
    span.innerHTML = `×`;
    btn.appendChild(span);
    btn.addEventListener("click", function() {
        this.closest("div").remove();
    });
    fadeOut(outerDiv);
}

function fadeOut(element) {
    var op = 1;  // initial opacity
    var timer = setTimeout(function () {
        setInterval(function () {
            if (op <= 0.1){
                clearInterval(timer);
                element.remove();
            }
            element.style.opacity = op;
            element.style.filter = 'alpha(opacity=' + op * 100 + ")";
            op -= op * 0.1;
        }, 100);
    }, 1000);
}