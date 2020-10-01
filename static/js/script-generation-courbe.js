$("#btn-display").click(() => {
    $("#loader").show();

    $.get('/display-metriques').done(response => {
        console.log(response);
        
        $("#images").html(`
        <div class="ui ten wide column">
            <img class="ui image" src="../static/images/outputs/metriquePR.png">
        </div>
        <div class="ui ten wide column">
            <img src="../static/images/outputs/metriqueROC.png">
        </div>`);

        $("#images").load()
    }).fail(error => {
        console.log(error)
    })
});