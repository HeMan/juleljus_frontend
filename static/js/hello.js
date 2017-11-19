$(document).ready(function() {
    $.ajax({
        url: "/api/patterns"
    }).then(function(data) {
        data = $.parseJSON(data);
        $.each(data, function(i, item) {
            source = $("#myButton").html();
            template = Handlebars.compile(source);
            context = {pattern: item};
            rendered = template(context);
            $('.tiles').append(rendered);

       })
    });
});


function run_pattern(pattern) {
    $.ajax({
        url: "/api/run/"+pattern
    });
};
