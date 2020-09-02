#Callbacks

L'intérêt de cette plateforme est de rendre le code transparent pour l'utilisateur.
Ainsi, tout interaction entre l'utilisateur et le code a lieu au travers d'une configuration.
Ces fichiers de configuration possèdent des paramètres obligatoires et d'autres optionnels - seule une combinaison valide de ces paramètres permettra d'utiliser correctement cette plateforme.

## Les Callbacks
Les callbacks sont des objets prenant effet à différentes étapes de l'entrainement (i.e au début ou à la fin d'une epoch, ou d'un batch, etc..)
cf https://keras.io/api/callbacks/


Les paramètres concernant les callbacks se trouvent dans le dictionnaire MODEL.
Toutes les informations concernant les callbacks doivent être contenus dans un dictionnaire nommé CALLBACKS. Pour chaque callback ajouté au modèle, on trouvera un dictionnaire rapportant les informations liés à ce callback.


Le template d'ajout de callbacks est le suivant :

"CALLBACKS" : {
  "CALLBACK_1" : {
    "PARAM1" : X,
    "PARAM2" : Y,
    ...
  },
  "CALLBACK_2":  {
    "PARAM1" : X,
    "PARAM2" : Y,
    ...
  },
  ...
}


Les valeurs CALLBACK_1 et CALLBACK_2 dans le template ci-dessus ne peuvent être arbitraires ; elles doivent correspondre à un callback connu (géré par la plateforme). Ces valeurs peuvent être les suivantes :
CHECKPOINT (https://keras.io/api/callbacks/model_checkpoint/)
EARLY_STOPPING (https://keras.io/api/callbacks/early_stopping/)
LR_SCHEDULER (https://keras.io/api/callbacks/learning_rate_scheduler/)
TERMINATE_NAN (https://keras.io/api/callbacks/terminate_on_nan/)
REDUCE_LR_ON_PLATEAU (https://keras.io/api/callbacks/reduce_lr_on_plateau/)
CSV_LOGGER (https://keras.io/api/callbacks/csv_logger/)

TODO : ajouter tous les callback keras

Ces callbacks ont chacun des paramètres qui doivent être ajoutés dans le dictionnaire approprié. Ces paramètres sont listés ci-dessous pour chaque callback.

CHECKPOINT :
  PATH
  VB
  MONITOR
  BEST_ONLY
  WEIGHTS_ONLY
  MODE
  PERIOD

Description des paramètres : https://keras.io/api/callbacks/model_checkpoint/

EARLY_STOPPING :
  MONITOR
  MIN_DELTA
  PATIENCE
  VB

Description des paramètres : https://keras.io/api/callbacks/early_stopping/

TERMINATE_NAN :
Pas de paramètres ; simplement lui donner la valeur "True" si on souhaite utiliser ce callback.

REDUCE_LR_ON_PLATEAU :
  MONITOR
  FACTOR
  PATIENCE
  MIN_LR

Descritpion des paramètres : https://keras.io/api/callbacks/reduce_lr_on_plateau/

CSV_LOGGER :
  FILENAME
  SEP
  APPEND

Description des paramètres : https://keras.io/api/callbacks/csv_logger/

Dans le cas du LR_SCHEDULER, plusieurs algorithmes permettant de générer un planificateur pour la learning rate ont été implémentés. Le choix de cet algorithme se fait grâce aux paramètre obligatoires SCHEDULE et TYPE, qui peuvent prendre les valeurs suivants :

TYPE : le type de scheduler.
  CYCLIC_LR : une planification cyclique du learning rate.
  LR_DECAY : une planification strictement décroissante du learning rate

SCHEDULE : le type de scheduler dans le cas où TYPE==LR_DECAY
  ssd_schedule : le planificateur pour la learning rate tel qu'implémenté par Pierluigi Ferrari dans son implémentation du SSD en keras, cf https://github.com/pierluigiferrari/
  STEP : pour une learning rate décroissante step by step
  LINEAR : pour une learning rate décroissante de manière linéaire
  POLY : pour une learning rate décroissante de manière polynomiale
  NONE : dans le cas où le schedule n'est pas de type decay.

En plus du paramètre SCHEDULE et TYPE, en fonction des valeurs de ses paramètres, on pourra avoir besoin d'ajouter d'autres paramètres à la configuration :

- si TYPE == CYCLIC_LR et SCHEDULE == NONE :
BASE_LR : la valeur de départ pour la learning rate
MAX_LR : valeur laximale pour la learning rate
STEP_SIZE : nombre d'itérations pour atteindre la moitié du cycle
MODE : le mode de modification de la learning rate. Peut prendre l'une des trois valeurs suivantes : 'triangular','triangular2','exp_range'

- si SCHEDULE == ssd_schedule :
VB : valeur pour le verbose mode.

- si TYPE == LR_DECAY et SCHEDULE == STEP :
INIT_ALPHA : valeur de départ pour la learning rate
FACTOR : facteur de décroissance, float entre 0 et 1
DROP_EVERY : nombre d'epochs entre chaque décroissance.


- si TYPE == LR_DECAY et SCHEDULE == LINEAR :
INIT_ALPHA : valeur de départ pour la learning rate
MAX_EPOCHS : maximum d'epochs pendant lequel la learning rate va décroitre

- si TYPE == LR_DECAY et SCHEDULE == POLY :
INIT_ALPHA : valeur de départ pour la learning rate
MAX_EPOCHS : maximum d'epochs pendant lequel la learning rate va décroitre
POWER : puissance pour la décroissance de la learning rate

----------------------------
Exemple d'utilisation de Callbacks :


{"configuration": {
	"DATAS": {
    ...
	},
	"TASK": {
    ...
		}
	},
	"MODEL" : {
    ...
    "CALLBACKS" : {
      "CHECKPOINT" : {
        "PATH" : "path_to_checkoint\\checpoint.h5",
        "VB" : 1,
        "MONITOR" : "val_loss",
        "BEST_ONLY" : "False",
        "WEIGHTS_ONLY" : "True",
        "MODE" : "auto",
        "PERIOD" : 2
      },
      "EARLY_STOPPING" : {
        "MONITOR" : "val_loss",
        "MIN_DELTA" : 0.1,
        "PATIENCE" : 5,
        "VB" : 1
      },
      "LR_SCHEDULER":{
				"TYPE" : "LR_DECAY",
				"SCHEDULE" : "POLY",
				"INIT_ALPHA" : 0.01,
				"MAX_EPOCHS" : 12,
        "POWER" : 5,
        "VB" : 0
			},
      "TERMINATE_NAN" : "True",
      "REDUCE_LR_ON_PLATEAU":{
        "MONITOR" : "val_loss",
        "FACTOR" : 0.1,
        "PATIENCE" : 5,
        "MIN_LR" : 0.0001
      },
      "CSV_LOGGER":{
        "FILENAME" : "csv_logger_default_",
        "SEP" : ",",
        "APPEND" : "True"
      }
    }
	}
}}
