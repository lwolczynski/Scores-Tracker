function installExpandListners() {
    const divs = document.querySelectorAll('div.clickable');
    divs.forEach(div => {
        div.addEventListener('click', expandFunction);
    });
}

function expandFunction(e) {
    this.classList.remove('clickable');
    this.querySelector('div.hidden').classList.remove('hidden');
    this.removeEventListener('click', expandFunction);
}

installExpandListners();