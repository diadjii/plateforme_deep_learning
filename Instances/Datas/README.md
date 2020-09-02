# Datas

L'intérêt de cette plateforme est de rendre le code transparent pour l'utilisateur.
Ainsi, tout interaction entre l'utilisateur et le code a lieu au travers d'une configuration.
Ces fichiers de configuration possèdent des paramètres obligatoires et d'autres optionnels - seule une combinaison valide de ces paramètres permettra d'utiliser correctement cette plateforme.

## Les Datas
Les données sont une partie intrinsèques des algorithmes de Deep Learning. Elles sont utilisées pour entraîner les modèles et sont les sujets des applications de ces mêmes modèles. Elles revêtent une importance particulière.

Cette plateforme suppose que les données fournies sont mises en forme et prête à l'utilisation. On fournit aux configurations des précisions sur les données qui sont contenues dans le dictionnaire 'DATAS'.

Tous les paramètres concernant les données se trouvent donc dans le dictionnaire DATAS. Ce dictionnaire doit contenir au minimum les paramètres suivants :

DATA_FORMAT - information concernant le format des données

DATA_PATH - information sur le chemin menant aux données

DATA_FEED - information sur la manière de charger les données

DATA_TYPE - information sur le type de données


Ces paramètres doivent correspondre aux valeurs suivantes :

Pour DATA_FORMAT :

  GEN si le format des données utilise une génération par dossiers

  VOC si le format des données respecte la norme PascalVOC

  KERAS si les données sont un des datasets préchargés dans keras.


Pour DATA_FEED :

  GENERATOR si les données seront chargées par un générateur

  IMG si les données images seront chargées directement en mémoire

  KERAS_DATASET si les données sont un des datasets préchargés dans keras.


Pour DATA_TYPE :

  IMG si les données sont des données image


Pour DATA_PATH :

  Le nom d'un dataset inclus dans keras si les données sont un des datasets préchargés dans keras (exemple : MNIST)

  Un chemin valide vers la racine du dataset sinon.


Les autres paramètres sont optionnels, mais certains peuvent être requis en fonction des valeurs des paramètres précédents. Ils sont listés ci-dessous :

RESHAPE : indique qu'on doit transformer le dataset pour le rendre exploitable

          OBLIGATOIRE si DATA_FEED == KERAS_DATASET

LABEL_FORMAT : indique le format du label.

              Valeurs possibles :

                VIA_JSON : les labels sont annotés dans un fichier json respectant la norme VIA

              OBLIGATOIRE si DATA_FORMAT == GEN et DATA_TYPE == IMG

LABEL_NAME : indique le nom du fichier contenant les labels

             OBLIGATOIRE si DATA_FORMAT == GEN et DATA_TYPE == IMG

CLASSES : indique les classes correspondant au dataset utilisé, comme suit : ["background", " ...", ...]

          OBLIGATOIRE si DATA_FORMAT == GEN ou DATA_FORMAT == VOC

GENERATOR : un dictionnaire qui donne des informations sur le générateur à utiliser

            OBLIGATOIRE si DATA_FORMAT == VOC

## Templates :
Voici quelques templates valides pour un dictionnaire DATAS :

- Utilisant un dataset préchargé dans keras :

"DATAS": {

  "DATA_FORMAT" : "KERAS",

  "DATA_FEED" : "KERAS_DATASET",

  "DATA_PATH" : "MNIST",

  "DATA_TYPE" : "IMG",

  "RESHAPE" : "True"

}

- Utilisant un generateur et le format VIA_JSON :

"DATAS": {

  "DATA_FORMAT" : "GEN",

  "DATA_FEED" : "GENERATOR",

  "DATA_PATH" : "...",

  "DATA_TYPE" : "IMG",

  "LABEL_FORMAT": "VIA_JSON",

  "LABEL_NAME" : "via_region_data.json",

  "CLASSES" : ["Background", "...",...]

}


- Exemple d'utilisation dans une configuration :

{"configuration": {

  "DATAS": {

    "DATA_FORMAT" : "KERAS",

    "DATA_FEED" : "KERAS_DATASET",

    "DATA_PATH" : "MNIST",

    "DATA_TYPE" : "IMG",

    "RESHAPE" : "True"

  },

"TASK": {

    ...

		},

"MODEL" : {

    ...

	}

}}
