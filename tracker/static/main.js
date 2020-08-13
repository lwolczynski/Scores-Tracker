function installBurgerListener() {
    document.querySelector("#burger").addEventListener("click", function() {
        const navLinks = document.querySelectorAll(".nav-item");
        const hideClass = "hidden-on-mobile";
        navLinks.forEach(link => {
            link.classList.contains(hideClass) ? link.classList.remove(hideClass) : link.classList.add(hideClass)
        });
    });
}

function makeSuccessAlertsFadeOut() {
    alerts = document.querySelectorAll(".alert-success");
    alerts.forEach(alert => {
        alert.addEventListener('animationend', () => alert.remove());
        setTimeout(() => alert.style.opacity = '0.2', 0);
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
    outerDiv.classList.add("alert", `alert-${msg.tag}`);
    mainMsgDiv.appendChild(outerDiv);
    const innerDiv = document.createElement("div");
    innerDiv.classList.add("main", "message");    
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
    if (msg.tag == 'success') {
        outerDiv.addEventListener('animationend', () => outerDiv.remove());
    }
}

function fadeOutCredit(el) {
    return new Promise(resolve => {
        el.classList.add("zero-opacity");
        const transitionEnded = e => {
            el.removeEventListener('transitionend', transitionEnded);
            el.classList.add("hidden");
            resolve();
        }
        el.addEventListener('transitionend', transitionEnded);
    })
};

function fadeInCredit(el) {
    return new Promise(resolve => {
        el.classList.remove("hidden");
        setTimeout(() => el.classList.remove("zero-opacity"), 0);
        const transitionEnded = e => {
            el.removeEventListener('transitionend', transitionEnded);
            resolve();
        }
        el.addEventListener('transitionend', transitionEnded);
    })
};

function animateCredits() {
    btn = document.querySelector("#show-credits");
    btn.addEventListener("click", function() {
        const spans = document.querySelectorAll(".span-footer");
        (async function loop() {
            for (let i = 0; i < spans.length; i++) {
                if (i!=0) await fadeInCredit(spans[i]);
                await fadeOutCredit(spans[i]);
            }
            await fadeInCredit(spans[0]);
        })();
    });
}

// Run at start

installBurgerListener();
makeSuccessAlertsFadeOut();
installAlertDiscardListeners();
animateCredits();