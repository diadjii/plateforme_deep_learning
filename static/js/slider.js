var slider = document.getElementById("myRange");
var output = slider.value; // Display the default slider value
console.log(output)
// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output = this.value;
  $.ajax({
    url: '/mask/show?alpha=' + output,
    type: 'GET',
    success: function (response) {
        console.log(response);
    },
    error: function (error) {
        console.log('False');
        
    }
 });
} 