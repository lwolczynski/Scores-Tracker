document.addEventListener('DOMContentLoaded', () => {
    modifyFormView();
    lookForErrorMsgs();
})

function modifyFormView() {
    formPs = document.querySelector("form").querySelectorAll("p");
    formPs.forEach(p => {
        const select = p.querySelector("select");
        if (select) {
            const br = document.createElement("br");
            p.insertBefore(br, select);
        }
    });
}

function lookForErrorMsgs() {
    errUl = document.querySelectorAll("ul.errorlist");
    errUl.forEach(ul => {
        const msg = ul.firstChild.innerHTML;
        const nextP = ul.nextElementSibling;
        const br = document.createElement("br");
        const small = document.createElement("small");
        small.classList.add("error");
        small.innerHTML = msg;
        nextP.appendChild(br);
        nextP.appendChild(small);
        ul.remove();
    });
}