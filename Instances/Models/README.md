#Models

L'intérêt de cette plateforme est de rendre le code transparent pour l'utilisateur.
Ainsi, tout interaction entre l'utilisateur et le code a lieu au travers d'une configuration.
Ces fichiers de configuration possèdent des paramètres obligatoires et d'autres optionnels - seule une combinaison valide de ces paramètres permettra d'utiliser correctement cette plateforme.

## Les modèles
Les modèles sont le coeur des algorithmes du deep learning ; ce sont ces derniers qui sont entrainés et utilisés par la suite pour fournir les résultats. Ces derniers sont conçus par des équipes scientifiques ou par des passionnés, et on peut compter un certain nombre d'architectures qui sont aujourd'hui devenues classiques ou réputées.

Cette plateforme permettra de charger un certain nombre de modèles prédéfinis, en plus des modèles préchargés dans keras. Ces modèles sont listés ci-dessous :

SSD300 (implémentation originale de l'architecture SSD(Single Shot Detector) en keras par Pierluigi Ferrari, cf https://github.com/pierluigiferrari/ssd_keras)

RCNN ( implémentation de Mask R-CNN par matterport en keras, cf https://github.com/matterport/Mask_RCNN)


Ces modèles peuvent être chargés et utilisés grâce aux configurations. On fournit aux configurations des précisions sur les modèles qui sont contenues dans le dictionnaire 'MODEL'

Tous les paramètres concernant les modèles se trouvent donc dans le dictionnaire MODEL. Ce dictionnaire doit contenir au minimum les paramètres suivants :
MODEL_TYPE : le type de modèle utilisé
WEIGHTS_PATH : le chemin menant aux données
TASK : la tâche que devra effectuer le modèle ; redondant avec TASK_NAME dans le dictionnaire TASK

Le paramètre MODEL_TYPE peut prendre les valeurs suivantes :
  DENSE_MNIST : un modèle dense pour la résolution du dataset MNIST
  RCNN : le modèle de Mask R-CNN tel qu'implémenté par matterport.
  SSD300 : le modèle SSD de taille d"entrée 300x300 tel qu'implémenté par Pierluigi Ferrari.
  CUSTOM : dans le cas d'un modèle importé non intégré dans la plateforme [TODO : à tester ]

Les autres paramètres sont optionnels, mais certains peuvent être requis en fonction des valeurs des paramètres précédents. Ils sont listés ci-desosus :

TASK : la tâche à effectuer. Peux prendre les même valeurs que TASK_NAME dans le dictionnaire TASK.
       Obligatoire si MODEL_TYPE == RCNN
LOGS_PATH : un chemin vers le dossier contenant les logs de l'entrainement à venir.
            OBLIGATOIRE si TASK == TRAIN  et que MODEL_TYPE == RCNN
IMG_SHAPE : tableau décrivant la forme de l'image utilisé en input. PRends la forme suivante : [XX, YY, ZZ]
            OBLIGATOIRE si TASK == SSD300
CLASSES : classes of the dataset the model will work with. Should respect the following template : ["Background","...",...]
          OBLIGATOIRE si MODEL_TYPE == RCNN ou MODEL_TYPE == SSD300
BATCH_SIZE : the batch size for the task to come.
             OBLIGATOIRE si MODEL_TYPE == SSD300
CALLBACKS : a dictionnary that contains all information relative to the callbacks. For more information about this parameter, see the README in the Callbacks folder.
COMPILATION : a dictionnary that contains all information relative to the compilation of the model.
              OBLIGATOIRE si TASK == TRAIN ou TASK == FIND_LR ou MODEL_TYPE == SSD300

              Ce dictionnaire doit contenir trois paramètres :
              LOSS : un dictionnaore contenant des informations sur la loss associée au modèle. Pour plus d'informations, voir le README dans le dosser LOSS
              OPT : un dictionnaire contenant les informations sur l'optimizer associé au modèle. Pour plus d'informations, voir le README dans le dossier Optimizers
              METRICS : un tableau contenant les différentes métriques à suivre lors de l'entrainement du modèle. Doit suivre le template suivant : ["metric1", "metric2",...]

##Templates
Voici quelques templates valides pour un dictionnaire MODEL :

- Pour un modèle préchargé dans keras :
"MODEL" : {
  "MODEL_TYPE" : "DENSE_MNIST",
  "WEIGHTS_PATH" : "KERAS_EASY",
  "TASK" : "TRAIN",
  "COMPILATION" : {
    "LOSS" : {
      "NAME" : "categorical_crossentropy"
    },
    "OPT" : {
      "NAME" : "rmsprop"
    },
    "METRICS" : ["accuracy"]
  },
}

- Pour utiliser un RCNN :
"MODEL" : {
  "LOGS_PATH":"...",
  "WEIGHTS_PATH" : "...",
  "MODEL_TYPE" :"RCNN",
  "TASK": "INFERENCE",
  "CLASSES" : ["Background", "..."],
  "COMPILATION" : {
    "LOSS" : {
      ...
    },
    "OPT" : {
      ...
    },
    "METRICS" : [...]
  },
  "CALLBACKS" : {
    ...
  }
}

- Exemple d'utilisation dans une configuration :
{"configuration": {
  "DATAS": {
    ...
  },
	"TASK": {
    ...
		},
  "MODEL" : {
    "MODEL_TYPE" : "DENSE_MNIST",
    "WEIGHTS_PATH" : "KERAS_EASY",
    "TASK" : "TRAIN",
    "COMPILATION" : {
      "LOSS" : {
        "NAME" : "categorical_crossentropy"
      },
      "OPT" : {
        "NAME" : "rmsprop"
      },
      "METRICS" : ["accuracy"]
    },
  }
}}
