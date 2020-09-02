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
      $("#new").attr('src', '/static/images/imagemasque.jpg');
    },
    error: function (error) {
      console.log('False');

    }
  });
}
