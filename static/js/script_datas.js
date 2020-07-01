$(() => {

})

let fieldReshape = $("input[name='RESHAPE']");
let fieldDataFeed = $("select[name='DATA_FEED']");
let fieldDataType = $("select[name='DATA_TYPE']");
let fieldLabelName = $("input[name='LABEL_NAME']");
let fieldDataFormat = $("select[name='DATA_FORMAT']");
let fieldLabelFormat = $("select[name='LABEL_FORMAT']");


fieldDataFeed.change(e => {
  if (e.currentTarget.value == "KERAS_DATASET") {
    $("#section_reshape").show();
  } else {
    $("#section_reshape").hide()
  }
});

fieldDataFormat.change(e => {
  if (e.currentTarget.value == "GEN" && fieldDataType.val() == "IMG") {
    $("#section_format").show();
    $("#section_classes").show();
    $("#section2").hide();

  } else if (e.currentTarget.value == "VOC") {
    $("#section2").show();
    $("#section_classes").show();
  } else {
    $("#section_format").hide();
    $("#section2").hide();

  }
});

fieldDataType.change(e => {
  if (e.currentTarget.value == "IMG" && fieldDataFormat.val() == "GEN") {
    $("#section_format").show();
  } else {
    $("#section_format").hide();
  }
});
