

$("#btn-display").click(() => {
    $("#btn-display").addClass("loading");

    $.get('/display-graphe').done(response => {
        $("#images").html(`
        <div class="ui six wide column">
            <img class="ui image" src="static/images/outputs/mnistaccuracy.png">
        </div>
        <div class="ui six wide column">
            <img  class="ui image" src="static/images/outputs/mnistloss.png">
        </div>`);

        $("#btn-display").removeClass("loading")
        $("#images").load();
    }).fail(error => {
        console.log(error)
    })
});
