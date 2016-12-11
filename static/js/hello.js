$(document).ready(function() {
    $.ajax({
        url: "api/patterns"
    }).then(function(data) {
        data = $.parseJSON(data);
        $.each(data, function(i, item) {
           $('.greeting-id').append(i);
           $('.greeting-content').append(item);
           $('.buttons').append($('<button/>', {
             text: item, //set text 1 to 10
             id: 'btn_'+i,
             click: function() { run_pattern(item) },
            }));
       })
    });
});


function run_pattern(pattern) {
    $.ajax({
        url: "api/run/"+pattern
    });
};
