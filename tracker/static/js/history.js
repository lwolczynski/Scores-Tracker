axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

function installExpandListeners() {
    const divs = document.querySelectorAll('div.clickable');
    divs.forEach(div => {
        div.addEventListener('click', expandFunction);
    });
}

function installDeleteListeners() {
    const btns = document.querySelectorAll('.btn-game-delete');
    btns.forEach(btn => {
        btn.addEventListener('click', openDeleteModal);
    });
}

function expandFunction(e) {
    this.classList.remove('clickable');
    this.querySelector('div.hidden').classList.remove('hidden');
    this.removeEventListener('click', expandFunction);
}

function openDeleteModal(e) {
    const modal = document.getElementById("myModal");
    const modalCloseBtn = modal.querySelector('.close-modal');
    const modalDeleteBtn = modal.querySelector('#btn-confirm-delete');
    modal.style.display = "block";
    // When the user clicks on (x), close the modal
    modalCloseBtn.onclick = function(event) {
        modal.style.display = "none";
    }
    // When the user clicks on Delete button, delete player and close the modal
    modalDeleteBtn.onclick = () => {
        gameDeleted = deleteGame(this.dataset.game_id);
        gameDeleted.then((response) => {
            if (response) {
                this.closest(".container").remove();
            }
        });
        modal.style.display = "none";
    }
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function deleteGame(game_id) {
    return axios({
        method: 'post',
        url: 'delete_game',
        data: {game_id: game_id},
    }).then((response) => {
        if (response.data.message.tag === "success") {
            addMessage(response.data.message);
            return true;
        }
    }).catch((error) => {
        addMessage({'tag': 'error', 'text': 'Something went wrong. Try again.'});
    });
}

// Main

installExpandListeners();
installDeleteListeners();