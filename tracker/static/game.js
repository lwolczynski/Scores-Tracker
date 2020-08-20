axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

const makeScoreKeeper = (holesNumber, editable) => {
    return {
        holesNumber: holesNumber,
        scores: [],
        editable: editable,
        table: document.querySelector('table'),
        async getScore() {
            await axios({
                method: 'get',
                url: 'get_scores'
            }).then((response) => {
                for (let score of response.data.scores) this.scores.push(score);
            }).catch((error) => {
                console.log(error);
            });
        },
        addTableClass() {
            if (window.innerWidth > 840) {
                this.table.classList.add('rtable-wide');
            } else {
                this.table.classList.add('rtable-long');
            }
        },
        createTopRow() {
            const thead = this.table.querySelector('thead');
            const trHeader = document.createElement("tr");
            thead.appendChild(trHeader);
            const th = document.createElement("th");
            trHeader.appendChild(th);
            th.innerHTML = '&nbsp';
            const tbody = document.querySelector('tbody');
            for (let i=0; i<this.holesNumber; i++) {
                const tr = document.createElement("tr");
                tbody.appendChild(tr);
                const td = document.createElement("td");
                tr.appendChild(td);
                td.innerHTML = `Hole ${i+1}`;
                td.classList.add("score");
            }
            const trTotal = document.createElement("tr");
            tbody.appendChild(trTotal);
            const tdTotal = document.createElement("td");
            trTotal.appendChild(tdTotal);
            tdTotal.innerHTML = `Total`;
        },
        addButtonListeners() {
            const viewBtn = document.querySelector('#btn-change-view');
            viewBtn.addEventListener("click", () => {
                this.table.classList.toggle('rtable-wide');
                this.table.classList.toggle('rtable-long');
            });
            if (this.editable) {
                const addPlayerBtn = document.querySelector('#btn-add-player');
                addPlayerBtn.addEventListener("click", () => {
                    this.addPlayer();
                });
            }
        },
        initiatePlayerRows() {
            if (this.editable) {
                for (let score of this.scores) this.createEditablePlayerRow(score);
            } else {
                for (let score of this.scores) this.createFixedPlayerRow(score);
            }
        },
        showTable() {
            document.querySelector('#table-spinner').remove();
            this.table.classList.remove('hidden');
        },
        createFixedPlayerRow(score) {
            const thead = this.table.querySelector('thead');
            const trHeader = thead.querySelector("tr");
            const th = document.createElement("th");
            trHeader.appendChild(th);
            th.innerHTML = `${score.name}`;
            const tbody = this.table.querySelector('tbody');
            const trs = tbody.querySelectorAll('tr');
            const keys = Object.keys(score.scoring);
            for (let i=0; i<trs.length; i++) {
                const td = document.createElement("td");
                trs[i].appendChild(td);
                if (score.scoring[keys[i]] !== undefined) {
                    td.innerHTML = (score.scoring[keys[i]] === null) ? `&nbsp;` : `${score.scoring[keys[i]]}`; 
                } else {
                    td.innerHTML = sum(Object.values(score.scoring));
                }
            }
        },
        createEditablePlayerRow(score) {
            const thead = this.table.querySelector('thead');
            const trHeader = thead.querySelector("tr");
            const th = document.createElement("th");
            th.dataset.score_id = score.id;
            trHeader.appendChild(th);
            const input = this.createNameInput(score);
            th.appendChild(input);
            if (!(score.par_tracker)) {
                th.appendChild(this.createDeletePlayerBtn(score));
            }            
            const tbody = this.table.querySelector('tbody');
            const trs = tbody.querySelectorAll('tr');
            const keys = Object.keys(score.scoring);
            for (let i=0; i<trs.length; i++) {
                const td = document.createElement("td");
                trs[i].appendChild(td);
                if (score.scoring[keys[i]] !== undefined) {
                    const input = this.createScoreInput(score, keys[i]);
                    td.appendChild(input);
                } else {
                    td.innerHTML = sum(Object.values(score.scoring));
                    td.classList.add('total');
                }
                td.dataset.score_id = score.id;
            }
        },
        createNameInput(score) {
            const input = document.createElement("input");
            input.setAttribute('type', 'text');
            input.setAttribute('minlength', 1);
            input.setAttribute('maxlength', 30);
            input.value = score.name;
            if (score.par_tracker) {
                input.setAttribute('disabled', true);
            } else {
                input.addEventListener('change', (e) => {
                    score.name = e.target.value;
                });
            }
            return input;
        },
        createDeletePlayerBtn(score) {
            const btn = document.createElement("button");
            btn.setAttribute('type', 'button');
            btn.setAttribute('class', 'delete');
            btn.setAttribute('aria-label', 'Delete');    
            const span = document.createElement("span");
            span.setAttribute('aria-hidden', 'true');
            span.innerHTML = `×`;
            btn.appendChild(span);
            btn.addEventListener('click', (e) => {
                this.showDeleteModal(score);
            });
            return btn;
        },
        showDeleteModal(score) {
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
                this.deletePlayer(score);
                modal.style.display = "none";
            }
            // When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }
        },
        createScoreInput(score, key) {
            const input = document.createElement("input");
            input.setAttribute('min', 0);
            input.setAttribute('max', 99);
            input.value = (score.scoring[key] === null) ? "" : score.scoring[key]; 
            setInputFilter(input, function(value) {
                return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 99); // Allow only integer between 0 and 99
            });
            input.addEventListener('click', (e) => {
                input.select();
            });
            input.addEventListener('input', (e) => {
                if (e.target.value !== "") {
                    score.scoring[key] = parseInt(e.target.value);
                } else {
                    score.scoring[key] = 0;
                }
                this.updateTotal(score);
            });
            return input;
        },
        updateTotal(score) {
            const totalField = document.querySelector(`.total[data-score_id='${score.id}']`);
            totalField.innerHTML = sum(Object.values(score.scoring));
        },
        addSaveListener() {
            if (this.editable) {
                const form = document.querySelector(`form`);
                form.addEventListener("submit", (e) => {
                    e.preventDefault();
                    this.saveToDatabase();
                });
            }
        },
        saveToDatabase() {
            axios({
                method: 'post',
                url: 'save_scores',
                data: {
                    holesNumber: this.holesNumber,
                    scores: this.scores,
                    notes: document.querySelector('#notes').value,
                }
            }).then((response) => {
                addMessage(response.data.message);
            }).catch((error) => {
                addMessage({'tag': 'error', 'text': 'Something went wrong. Try again.'});
            });
        },
        addPlayer() {
            axios({
                method: 'post',
                url: 'add_player',
                data: {},
            }).then((response) => {
                if (response.data.message.tag === "success") {
                    this.scores.push(response.data.score);
                    this.createEditablePlayerRow(response.data.score);
                }
                addMessage(response.data.message);
            }).catch((error) => {
                addMessage({'tag': 'error', 'text': 'Something went wrong. Try again.'});
            });
        },
        deletePlayer(score) {
            axios({
                method: 'post',
                url: 'delete_player',
                data: {score_id: score.id},
            }).then((response) => {
                if (response.data.message.tag === "success") {
                    this.scores.pop(score);
                    this.table.querySelectorAll(`[data-score_id='${score.id}']`).forEach(el => el.remove());
                    addMessage(response.data.message);
                }
            }).catch((error) => {
                addMessage({'tag': 'error', 'text': 'Something went wrong. Try again.'});
            });
        },
    }
} 

const sum = (arr) => arr.reduce((a,b) => a + b, 0);

// Restricts input for the given textbox to the given inputFilter function.
function setInputFilter(textbox, inputFilter) {
    ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
        textbox.addEventListener(event, function() {
            if (inputFilter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            } else {
                this.value = "";
            }
        });
    });
}

// Run at start

const scoreKeeper = makeScoreKeeper(holesNumber, editable);
scoreKeeper.addTableClass();
scoreKeeper.addButtonListeners();
scoreKeeper.createTopRow();
scoreKeeper.getScore().then(() => {
    scoreKeeper.initiatePlayerRows();
    scoreKeeper.showTable();
});
scoreKeeper.addSaveListener();