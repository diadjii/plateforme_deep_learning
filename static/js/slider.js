var slider = document.getElementById("myRange");
var output = slider.value;

slider.oninput = function () {
  output = this.value;
  let img_name = $("#img").attr('name');

  $.ajax({
    url: '/mask/show?alpha=' + output + '&name=' + img_name,
    type: 'GET',
    success: function (response) {
      console.log(response);
      $("#new").html('<img src="/static/images/imagemasque.jpg" width="100%" height="100%">');
    },
    error: function (error) {
      console.log('False');

    }
  });
} 