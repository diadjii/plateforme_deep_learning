$("#btn-display").click(() => {
  $("#btn-display").addClass("loading");

  $.get('/display-metriques').done(response => {
    console.log(response);

    $("#images").html(`
      <div class="ui six wide column">
      <img class="ui image" src="../static/images/outputs/metriquePR.png">
      </div>
      <div class="ui six wide column">
      <img src="../static/images/outputs/metriqueROC.png">
      </div>`);
      $("#btn-display").removeClass("loading")
      $("#images").load()
    }).fail(error => {
      alert("Une erreur s'est produite au niveau du serveur")
      console.log(error)
    })
  });
