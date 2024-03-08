$('#search').keyup(function () {
    var query;
    query = $(this).val();

    $.get('/rango/search/',
        { 'suggestion': query },
        function (data) {
            $('#search_results').html(data);
        })
});