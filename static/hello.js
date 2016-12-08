$(document).ready(function() {
    $.ajax({
        url: "http://[2002:5f6d:7d2e::5be]:8080/patterns"
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
        url: "http://[2002:5f6d:7d2e::5be]:8080/run/"+pattern
    });
};
