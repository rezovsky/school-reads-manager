function delbookconfirm(inv, isbn, url){
if (confirm('Удалить книгу с инвентарным номером ' + inv + '?')) {
    location.href = url;
    }
}

function arhivbookconfirm(inv, isbn, url){
if (confirm('Списать книгу с инвентарным номером ' + inv + '?')) {
    location.href = url;
    }
}