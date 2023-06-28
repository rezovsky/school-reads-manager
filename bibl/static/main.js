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

function checkedAllInvent(element){
    if (element.checked){
    $('.action-buttons').show();
    var chekerLen =  $('.checkerInvent').length
    console.log(chekerLen)
    $('.checkerInvent').prop('checked', true);
    } else {
    $('.action-buttons').hide();
    $('.checkerInvent').prop('checked', false);
    }
}

function chekerActionMonitor(len){

}
