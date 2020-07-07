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

$("#form_load_datas").submit(e => {
  e.preventDefault();

  file = $("#file")[0].files[0]
  reader = new FileReader();
  configurations = {};

  reader.onload = e => {
    let lines = e.target.result;
    configurations = JSON.parse(lines);
  };
  reader.readAsText(file)

  reader.onloadend = e => {

    setDatasToForm(configurations.configuration.DATAS)
  }
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

function setDatasToForm(datas) {
  fieldDataFormat.val(datas.DATA_FORMAT);
  fieldDataFormat.trigger('change');

  fieldDataFeed.val(datas.DATA_FEED);
  fieldDataFeed.trigger('change');

  fieldDataType.val(datas.DATA_TYPE);
  fieldDataType.trigger('change');

  fieldClasses.val(datas.CLASSES);

  if (datas.DATA_FORMAT == "VOC") {
    size = datas.TARGET_SIZE.split('x');
    y1 = size[0];
    y2 = size[1];

    fieldReshape.attr("checked", datas.RESHAPE == 'true' ? true : false);
    fieldRescale.attr("checked", datas.RESCALE == 'true' ? true : false);
    fieldBatchSize.val(datas.BATCH_SIZE);


    fieldImgSizeY_1.val(y1);
    fieldImgSizeY_2.val(y2);
    console.log(fieldReshape);
  }

  console.log(datas)
}