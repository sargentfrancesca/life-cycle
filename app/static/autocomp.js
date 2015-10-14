$( document ).ready(function() {
    $.ajax({
        url: '{{ url_for("researchersjson") }}'
        }).done(function (data) {
            
            console.log(data.json_list)
   
        });
});