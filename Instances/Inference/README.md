#Inference

L'intérêt de cette plateforme est de rendre le code transparent pour l'utilisateur.
Ainsi, tout interaction entre l'utilisateur et le code a lieu au travers d'une configuration.
Ces fichiers de configuration possèdent des paramètres obligatoires et d'autres optionnels - seule une combinaison valide de ces paramètres permettra d'utiliser correctement cette plateforme.

## L'inférence
L'inférence permet d'appliquer un modèle sur des données afin d'utiliser les ouputs à des fins multiples. Tous les paramètres relatifs à l'inférence se trouvent dans le dictionnaire 'TASK'. Ce dictionnaire doit contenir au minimum les paramètres suivants :

TASK_NAME : indique le nom de la tâche à effectuer. Dans le cas d'une inference, ce paramètre aura forcément pour valeur INFERENCE
TASK_SPEC : un dictionnaire contenant les informations spécifiques à la tâche à effectuer.

Dans le cas de l'inférence, on pourra trouver toutes les informations nécessaires à l'execution de la tâche dans le dictionnaire TASK_SPEC. Ce dernier devra forcément contenir les paramètres suivants :

TODO
