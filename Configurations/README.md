#Configurations

L'intérêt de cette plateforme est de rendre le code transparent pour l'utilisateur.
Ainsi, tout interaction entre l'utilisateur et le code a lieu au travers d'une configuration.
Ces fichiers de configuration possèdent des paramètres obligatoires et d'autres optionnels - seule une combinaison valide de ces paramètres permettra d'utiliser correctement cette plateforme.

Les paramètres sont organisés dans un fichier json, contenant un dictionnaires nommé 'configuration'. Chaque fichier de configuration est au moins composé des éléments suivants :


DATAS - element comprenant les informations relatives aux données
TASK - element comprenant les informations relatives à la tâche effectuee
MODEL - elemnet comprenant les informations relatives au modèle utilisé

Ces paramètres contiennent des dictionnaires, qui possèdent eux aussi des clés obligatoires:

Dans DATAS :
  DATA_FORMAT - information concernant le format des données
  DATA_PATH - information sur le chemin menant aux données
  DATA_FEED - information sur la manière de charger les données
  DATA_TYPE - information sur le type de données

Dans TASK :
  TASK_NAME - le nom de la tâche à effectuer
  TASK_SPEC - informations spécifiques à la tâche

Dans MODEL :
  MODEL_TYPE - information sur le type de modèle utilisé
  WEIGHTS_PATH - information sur le chemin menant aux données


Un fichier de configuration minimal aura donc cette allure :

{"configuration": {
	"DATAS": {
		"DATA_FORMAT" : "...",
		"DATA_FEED" : "...",
		"DATA_PATH" : "...",
		"DATA_TYPE" : "...",
	},
	"TASK": {
		"TASK_NAME" : "...",
		"TASK_SPEC" : {...}
	},
	"MODEL" : {
		"MODEL_TYPE" : "...",
		"WEIGHTS_PATH" : "...",
  }
}}

Les valeurs des paramètres doivent être adaptés à ces derniers ; pour plus d''information, vous pouvez suivre les tutoriels et exemples (TODO) ou bien lire les README des sections respectives (cf Instances/README.md).

En fonction des options choisies, on devra rajouter des composantes (nouveaux paramètres)
dans les dictionnaires adaptés. Pour connaitre ces choix, vous pouvez suivre les tutoriels et exemples (TODO) ou bien lire les README des sections respectives (cf Instances/README.md).
