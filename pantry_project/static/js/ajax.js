$('#search').keyup(function () {
    var query;
    query = $(this).val();

    $.get('/rango/search/',
        { 'suggestion': query },
        function (data) {
            $('#search_results').html(data);
        })
});

$(document).ready(function() {
    $('#bookmark').click(function() {
        var recipeIdVar;
        recipeIdVar = $(this).attr('data-recipeid');

        $.get('/rango/save_recipe/',
            {'recipe_id': recipeIdVar}
        )
    });
});

$(document).ready(function() {
    $('#review-heart').click(function() {
        var reviewIdVar;
        reviewIdVar = $(this).attr('data-reviewid');

        $.get('/rango/like_review/',
            {'review_id': reviewIdVar}
            )
    });
});