

$("#btn-display").click(() => {
    $("#loader").show();

    $.get('/display-graphe').done(response => {
        console.log(response);
        
        $("#images").html(`
        <div class="ui six wide column">
            <img class="ui image" src="static/images/outputs/mnistaccuracy.png">
        </div>
        <div class="ui six wide column">
            <img src="static/images/outputs/mnistloss.png">
        </div>`);

        $("#images").load()
    }).fail(error => {
        console.log(error)
    })
});