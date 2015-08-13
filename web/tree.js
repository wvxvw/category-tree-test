$(function ($) {
    var container = $('#container'),
        add = $('#add'),
        key = $('#key');

    function isEmpty(dict) {
        var result = true;
        for (var key in dict) {
            result = false;
            break;
        }
        return result;
    }

    function populate(element, data) {
        $.each(data, function (key, value) {
            if (isEmpty(value)) {
                $('<li>' + key + '</li>').appendTo(element);
            } else {
                var li = $('<li><ul><li><b>' + key + '</b></li></ul></li>'), ul;
                li.appendTo(element);
                ul = li.children('ul').get(0);
                populate(ul, value);
            }
        });
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
