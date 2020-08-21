function listenToPageChange() {
    const select = document.querySelector('#my_account_dropdown');
    select.addEventListener('change', function() {
        window.location.href = this.value;
    });
}

listenToPageChange();