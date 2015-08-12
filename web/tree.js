$(function ($) {
    var container = $('#container'),
        add = $('#add'),
        key = $('#key');

    function populate(element, data) {
        if (typeof data == 'string') {
            $('<li>' + data + '</li>').appendTo(element);
        } else {
            $.each(data, function (key, value) {
                var li = $('<li><ul><li><b>' + key + '</b></li></ul></li>'), ul;
                li.appendTo(element);
                ul = li.children('ul').get(0);
                populate(ul, value);
            });
        }
    }
    
    function reset(data) {
        container.empty();
        populate(container, data);
    }
    
    $.post('/categories/get', reset);

    add.click(function () {
        $.post('/categories/put', key.val(), reset, 'json');
    });
});
