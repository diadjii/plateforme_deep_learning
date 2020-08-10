
//SECTION DATAS FIELDS
let fieldReshape = $("input[name='RESHAPE']");
let fieldClasses = $("input[name='CLASSES']");
let fieldDataFeed = $("select[name='DATA_FEED']");
let fieldDataType = $("select[name='DATA_TYPE']");
let fieldLabelName = $("input[name='LABEL_NAME']");
let fieldDataFormat = $("select[name='DATA_FORMAT']");
let fieldLabelFormat = $("select[name='LABEL_FORMAT']");
let fieldInputDataPath = $("#field_path_input");
let fieldSelectDataPath = $("#field_path_select");
let sectionSelectDataPath = $("#section_path_select");

//SECTION GENERATOR FIELDS
let fieldRescale = $("input[name='RESCALE']");
let fieldBatchSize = $("input[name='BATCH_SIZE']");
let fieldClassMode = $("select[name='CLASS_MODE']");
let fieldImgSizeSortieY_1 = $("input[name='imgSizeSortiey1']");
let fieldImgSizeSortieY_2 = $("input[name='imgSizeSortiey2']");

//SECTION MODEL FIELDS
let fieldTask = $("select[name='TASK']");
let fieldEpochs = $("input[name='EPOCHS']");
let fieldOptName = $("select[name='OPT_NAME']");
let fieldMetrics = $("select[name='METRICS']");
let fieldLossName = $("select[name='LOSS_NAME']");
let fieldLogsPath = $("input[name='LOGS_PATH']");
let fieldModelType = $("select[name='MODEL_TYPE'");
let fieldWeightPath = $("input[name='WEIGHTS_PATH']");
let fieldSpecDataType = $("select[name='SPEC_DATA_TYPE']");
let fieldSpecBatchSize = $("input[name='SPEC_BATCH_SIZE']");
let fieldModelBatchSize = $("input[name='MODEL_BATCH_SIZE");
let fieldImgSizeEntreeY_1 = $("input[name='imgSizeEntreey1']");
let fieldImgSizeEntreeY_2 = $("input[name='imgSizeEntreey2']");

$('.ui.accordion').accordion();

$("#load-config-file").click(e => {
  $('.ui.modal').modal('show');
})

fieldDataFeed.change(e => {
  if (e.currentTarget.value == "KERAS_DATASET") {
    fieldInputDataPath.hide();
    fieldInputDataPath.attr('required', false);
    sectionSelectDataPath.show();
    fieldSelectDataPath.attr('required', true)
    $("#section_reshape").show();
  } else {
    fieldInputDataPath.show();
    fieldInputDataPath.attr('required', true);
    sectionSelectDataPath.hide();
    fieldSelectDataPath.attr('required', false)
    $("#section_reshape").hide();
  }
});

fieldDataFormat.change(e => {
  if (e.currentTarget.value == "GEN" && fieldDataType.val() == "IMG") {
    $("#section_format, #section_classes").show();
    $("#section2").hide();

    disableRequiredFieldsSecyion2();
  } else if (e.currentTarget.value == "VOC") {
    $("#section_generateur, #section_classes").show();

    activeRequiredFieldsSection2();
  } else {
    $("#section_format, #section_generateur, #section_classes").hide();
    disableRequiredFieldsSection2();
  }
});

fieldDataType.change(e => {
  if (e.currentTarget.value == "IMG" && fieldDataFormat.val() == "GEN") {
    $("#section_format").show();
  } else {
    $("#section_format").hide();
  }
});

fieldTask.change(evt => {
  let currentTask = evt.currentTarget.value;

  switch (currentTask) {
    case "TRAIN":
      $("#section_compilation, #section_logs").show();
      break;
    case "FIND_LR":
      $("#section_compilation").show();
      break;
    default:
      $("#section_compilation").hide();
      break;
  }
});

fieldModelType.change(e => {
  let modelType = e.currentTarget.value;

  if (modelType == "SSD300") {
    $("#section_modele_img, #section_modele_batch, #section_compilation").show();
  }
})

$("#form-create-datas").submit(e => {
  e.preventDefault();

  let params = generateConfig();
  console.log(params);
  $.post('/config/generate', params).done(response => {
    if (response) {
      $("#btn-download").show();
    }
  }).fail(error => {
    alert("Une erreur s'est produite lors de la creation du fichier de configuration.")
  })
})

//chargement des données du fichier de configuration dans le formulaire
$("#form_load_datas").submit(e => {
  e.preventDefault();

  var file = $("#file")[0].files[0]
  var reader = new FileReader();
  var configurations = {};

  //evenement declenché si toutefois le fichier est chargé
  reader.onload = evt => {
    let lines = evt.target.result;
    //recuperation du contenu du fichier de configuration
    configurations = JSON.parse(lines);
  };

  //lecture des lignes
  reader.readAsText(file)

  reader.onloadend = () => {
    /*Appel de la fonction qui recupere les données du
    fichier de config et le rempli le formulaire avec ces données*/
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

  let modelType = fieldModelType.val();
  let weightPath = fieldWeightPath.val();
  var task = fieldTask.val();
  var logsPath = null;
  var modelClasses = null;
  var modelImgShape = null;
  var modelBatchSize = null;
  var metrics = null;
  var lossName = null;
  var optName = null;
  var specDataType = fieldSpecDataType.val();
  var specBatchSize = fieldSpecBatchSize.val();
  var epochs = fieldEpochs.val();

  if (task == "TRAIN" && modelType == "RCNN") {
    logsPath = fieldLogsPath.val();
  }

  switch (modelType) {
    case 'SSD300':
      modelClasses = classes;
      modelImgShape = fieldImgSizeEntreeY_1.val() + "x" + fieldImgSizeEntreeY_2.val();
      modelBatchSize = parseInt(fieldModelBatchSize.val());
      break;
    case 'RCNN':
      modelClasses = classes;
      break;
  }

  if (dataFeed == "KERAS_DATASET") {
    dataPath = fieldSelectDataPath.val();
    reshape = false;
    if (fieldReshape.is(":visible")) {
      reshape = fieldReshape.is(':checked') ? true : false;
    }

  } else {
    dataPath = fieldInputDataPath.val();
  }

  var configurations = {
    "DATA_FORMAT": dataFormat,
    "DATA_FEED": dataFeed,
    "DATA_PATH": dataPath,
    "DATA_TYPE": dataType,
    "RESHAPE": reshape,
    "CLASSES": classes
  }

  if ($("#section_generateur").is(":visible")) {
    let rescale = fieldRescale.is(":checked") ? true : false;
    let targetSize = fieldImgSizeSortieY_1.val() + "x" + fieldImgSizeSortieY_2.val();
    let batchSize = fieldBatchSize.val();
    let classMode = fieldClassMode.val();

    configurations.RESCALE = rescale;
    configurations.TARGET_SIZE = targetSize;
    configurations.BATCH_SIZE = batchSize;
    configurations.CLASS_MODE = classMode;

    configurations.generator = true;
  }

  configurations.MODEL = {
    "MODEL_TYPE": modelType,
    "WEIGHTS_PATH": weightPath,
    "TASK": task,
    "LOGS_PATH": logsPath,
    "CLASSES": modelClasses,
    "IMG_SHAPE": modelImgShape,
    "BATCH_SIZE": modelBatchSize == '1' ? parseInt(modelBatchSize) : null,
    "CALLBACKS": {},
  }

  if ($("#section_compilation").is(':visible')) {
    lossName = fieldLossName.val();
    optName = fieldOptName.val();
    metrics = fieldMetrics.val();

    configurations.compilation = true;

    configurations.MODEL.COMPILATION = {
      "LOSS": {
        "NAME": lossName,
      },
      "OPT": {
        "NAME": optName,
      },
      "METRICS": metrics,
    }
  }

  configurations.TASK = {
    "TASK_NAME": task,
    "TASK_SPEC": {
      "EPOCHS": parseInt(epochs),
      "BATCH_SIZE": parseInt(specBatchSize)
    }
  }

  return configurations;
}

function activeRequiredFieldsSection2() {
  fieldClassMode.attr('required', true);
  fieldImgSizeSortieY_1.attr('required', true);
  fieldImgSizeSortieY_2.attr('required', true);
  fieldBatchSize.attr('required', true);
  fieldRescale.attr('required', true);
}

function disableRequiredFieldsSection2() {
  fieldClassMode.attr('required', false);
  fieldImgSizeSortieY_1.attr('required', false);
  fieldImgSizeSortieY_2.attr('required', false);
  fieldBatchSize.attr('required', false);
  fieldRescale.attr('required', false);
}

//fonction qui remplit le formulaire avec les données du fichier de configuration
function setDatasToForm(datas) {
  fieldDataFormat.val(datas.DATA_FORMAT);
  fieldDataFormat.trigger('change');

  fieldDataFeed.val(datas.DATA_FEED);
  fieldDataFeed.trigger('change');

  fieldDataType.val(datas.DATA_TYPE);
  fieldDataType.trigger('change');

  fieldClasses.val(datas.CLASSES);

  if (datas.DATA_FORMAT == "VOC") {
    let size = datas.TARGET_SIZE.split('x');
    let y1 = size[0];
    let y2 = size[1];

    fieldReshape.attr("checked", datas.RESHAPE == 'true' ? true : false);
    fieldRescale.attr("checked", datas.RESCALE == 'true' ? true : false);
    fieldBatchSize.val(datas.BATCH_SIZE);

    fieldImgSizeSortieY_1.val(y1);
    fieldImgSizeSortieY_2.val(y2);
  }

}
