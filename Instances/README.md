#Instances

Ce dossier regroupe des instances qui se chargent de charger les différents éléments (modèles, données, ...) et d'effectuer les tâches décrites dans la configuration.

Ces instances sont réparties comme suit :
- Datas : contient une instance qui se charge de charger les données et de les mettre en forme. C'est là que seront traitées toutes les informations concernant le dataset.
- Inference: contient une instance qui se charge d'exécuter le workflow d'inférence en faisant appels aux autres instances de manière appropriée.
- Models : contient une instance qui se charge de charger les modèles et tous les éléments associés. C'est là que seront traitées toutes les informations concernant les modèles.
- Training : contient une instance qui se charge d'éxecuter le workflow d'entrainement en faisant appels auxautres instances de manière appropriée.
- Visualization : contient une instance qui se charge des visualisations et de la production des outputs.

Cette répartition permet de facilement intégrer dde nouvelles fonctionnalités sans avoir à modifier une grosse partie du code ; de plus, elle permet au développeur expérimenter de facilement identifier les parties du code concernées par les différentes étapes du workflow et ainsi d'explorer le code plus facilement.

Ces instances sont documentées avec des README dans leurs dossiers respectifs
