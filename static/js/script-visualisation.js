

$("#btn-display").click(() => {
    $("#loader").show();

    $.get('/display-graphe').done(response => {
        console.log(response);
        
        $("#images").html(`
        <div class="ui ten wide column">
            <img class="ui image" src="static/images/mnistaccuracy.png">
        </div>
        <div class="ui ten wide column">
            <img src="static/images/mnistloss.png">
        </div>`);

        $("#images").load()
    }).fail(error => {
        console.log(error)
    })
});