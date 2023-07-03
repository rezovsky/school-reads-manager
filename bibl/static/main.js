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
        $('.checkerInvent').prop('checked', true);
        chekerActionMonitor()
    } else {
        $('.checkerInvent').prop('checked', false);
        chekerActionMonitor()
    }
}

function checkedInvent(element){
    if (element.checked){
        chekerActionMonitor()
    } else {
        chekerActionMonitor()
    }
}

function chekerActionMonitor(){
    len = $('.checkerInvent:checkbox:checked').length
    if (len) {
        $('.action-buttons').show();
        $('.action-buttons').each(function() {
            text = $(this).text().split(' (')[0]
            $(this).text(text + ' (' + len +')')
        });
    } else {
        $('.action-buttons').hide();
        $('.action-buttons').each(function() {
                $(this).text($(this).text().split(' (')[0])
            });
    }
}

function actions(action, url){
    switch(action) {
      case 'arhive':
            actionStr = 'Списать'
            break

      case 'del':
            actionStr = 'Удалить'
            break

      default:
        return
    }
    actionsFunction(actionStr, url)

    function actionsFunction(str, url){
        len = $('.checkerInvent:checkbox:checked').length
        if (confirm(str + ' книги? (всего ' + len + ' шт.)')) {
            actionArray = ''
            $('.checkerInvent:checkbox:checked').each(function(){
                actionArray += $(this).attr('id').split('-')[1] + '.'
                })
            actionArray = actionArray.substring(0, actionArray.length - 1);
            url = url.replace('-1', '-' + actionArray)
            location.href = url;
        }
    }
}

