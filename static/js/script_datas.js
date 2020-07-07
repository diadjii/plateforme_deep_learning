$(() => { })

let fieldReshape = $("input[name='RESHAPE']");
let fieldClasses = $("input[name='CLASSES']");
let fieldDataFeed = $("select[name='DATA_FEED']");
let fieldDataType = $("select[name='DATA_TYPE']");
let fieldLabelName = $("input[name='LABEL_NAME']");
let fieldDataFormat = $("select[name='DATA_FORMAT']");
let fieldLabelFormat = $("select[name='LABEL_FORMAT']");
let fieldSelectDataPath = $("#field_path_select");
let fieldInputDataPath = $("#field_path_input");

//SECTION 2 FIELDS
let fieldRescale = $("input[name='RESCALE']");
let fieldImgSizeY_1 = $("input[name='y1']");
let fieldImgSizeY_2 = $("input[name='y2']");
let fieldBatchSize = $("input[name='BATCH_SIZE']");
let fieldClassMode = $("select[name='CLASS_MODE']");

fieldDataFeed.change(e => {
  if (e.currentTarget.value == "KERAS_DATASET") {
    fieldInputDataPath.hide();
    fieldInputDataPath.attr('required', false);
    fieldSelectDataPath.show();
    fieldSelectDataPath.attr('required', true)
    $("#section_reshape").show();
  } else {
    fieldInputDataPath.show();
    fieldInputDataPath.attr('required', true);
    fieldSelectDataPath.hide();
    fieldSelectDataPath.attr('required', false)
    $("#section_reshape").hide();
  }
});

fieldDataFormat.change(e => {
  if (e.currentTarget.value == "GEN" && fieldDataType.val() == "IMG") {
    $("#section_format").show();
    $("#section_classes").show();
    $("#section2").hide();
    disableRequiredFieldsSecyion2();
  } else if (e.currentTarget.value == "VOC") {
    $("#section2").show();
    activeRequiredFieldsSection2();
    $("#section_classes").show();
  } else {
    $("#section_format").hide();
    $("#section2").hide();
    disableRequiredFieldsSecyion2();
  }
});

fieldDataType.change(e => {
  if (e.currentTarget.value == "IMG" && fieldDataFormat.val() == "GEN") {
    $("#section_format").show();
  } else {
    $("#section_format").hide();
  }
});

$("#form-create-datas").submit(e => {
  e.preventDefault();

  let params = generateConfig();

  $.post('/config/generate', params).done(response => {
    console.log(response)
    if (response) {
      $("#btn-download").show();
    }
  }).fail(error => {
    console.log(error);
  })
})

function generateConfig() {
  let dataFormat = fieldDataFormat.val();
  let dataFeed = fieldDataFeed.val();
  let dataType = fieldDataType.val();
  let classes = fieldClasses.val();
  var dataPath;
  var reshape;

  if (dataFeed == "KERAS_DATASET") {
    dataPath = fieldSelectDataPath.val();
    reshape = fieldReshape.is(":visible") ? fieldReshape.is(':checked') : null;
  } else {
    dataPath = fieldInputDataPath.val();
  }

  configurations = {
    "DATA_FORMAT": dataFormat,
    "DATA_FEED": dataFeed,
    "DATA_PATH": dataPath,
    "DATA_TYPE": dataType,
    "RESHAPE": reshape,
    "CLASSES": classes
  }

  if ($("#section2").is(":visible")) {
    let rescale = fieldRescale.is(":checked") ? true : false;
    let targetSize = fieldImgSizeY_1.val() + "x" + fieldImgSizeY_2.val();
    let batchSize = fieldBatchSize.val();
    let classMode = fieldClassMode.val();

    configurations.RESCALE = rescale;
    configurations.TARGET_SIZE = targetSize;
    configurations.BATCH_SIZE = batchSize;
    configurations.CLASS_MODE = classMode;
    configurations.generator = true;
  }

  return configurations;
}

function activeRequiredFieldsSection2() {
  fieldClassMode.attr('required', true);
  fieldImgSizeY_1.attr('required', true);
  fieldImgSizeY_2.attr('required', true);
  fieldBatchSize.attr('required', true);
  fieldRescale.attr('required', true);
}

function disableRequiredFieldsSecyion2() {
  fieldClassMode.attr('required', false);
  fieldImgSizeY_1.attr('required', false);
  fieldImgSizeY_2.attr('required', false);
  fieldBatchSize.attr('required', false);
  fieldRescale.attr('required', false);
}