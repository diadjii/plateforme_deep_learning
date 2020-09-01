#Visualization

L'intérêt de cette plateforme est de rendre le code transparent pour l'utilisateur.
Ainsi, tout interaction entre l'utilisateur et le code a lieu au travers d'une configuration.
Ces fichiers de configuration possèdent des paramètres obligatoires et d'autres optionnels - seule une combinaison valide de ces paramètres permettra d'utiliser correctement cette plateforme.

## La visualisation
Les visualisations des métriques lors de l'entrainement ou des résultats lors de l'inférence permettent de constater visuellement de l'efficacité de la tâche effectuée. Ces visualisations sont gérées par l'instance de visualisation. Cette instance utilise les configurations pour identifier les tâches à effectuer et produire les visuels demandés.

Cette instance n'est pas encore bien factorisée et organisée et nécessite un travail de restructuration.
