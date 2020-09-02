#Train

L'intérêt de cette plateforme est de rendre le code transparent pour l'utilisateur.
Ainsi, tout interaction entre l'utilisateur et le code a lieu au travers d'une configuration.
Ces fichiers de configuration possèdent des paramètres obligatoires et d'autres optionnels - seule une combinaison valide de ces paramètres permettra d'utiliser correctement cette plateforme.

## L'entrainement
L'entrainement est la phase qui permet au modèle de devenir performant sur les données fournies, si le dataset et le modèle sont adéquats.

C'est la phase la plus importante dans un projet. De l'entrainement dépendra les performances du modèle entrainé, et donc les performances dans les applications futures.

Toutes les informations relatives à l'entrainelent se trouvent dans le dictionnaire 'TASK'. Ce dictionnaire doit contenir au minimum les paramètres suivants :

TASK_NAME : indique le nom de la tâche à effectuer. Dans le cas d'une inference, ce paramètre aura forcément pour valeur TRAIN
TASK_SPEC : un dictionnaire contenant les informations spécifiques à la tâche à effectuer.

Dans le cas de l'entrainement, on pourra trouver toutes les informations nécessaires à l'execution de la tâche dans le dictionnaire TASK_SPEC. Ce dernier devra forcément contenir les paramètres suivants :

EPOCHS : Nombre d'epochs que devra durer l'entraînement
BATCH_SIZE : Taille du batch de données lors de l'entrainement

Des paramètres supplémentaires sont nécessaires dans le cas de l'utilisation du modèle SSD300. (TODO : ajout de ses paramètres)
