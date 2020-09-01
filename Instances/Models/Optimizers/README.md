#Optimizers

L'intérêt de cette plateforme est de rendre le code transparent pour l'utilisateur.
Ainsi, tout interaction entre l'utilisateur et le code a lieu au travers d'une configuration.
Ces fichiers de configuration possèdent des paramètres obligatoires et d'autres optionnels - seule une combinaison valide de ces paramètres permettra d'utiliser correctement cette plateforme.

## L'optimizer
L'optimizer est l'algorithme qui sera utilisé pour mettre à jour les poids des neurones du réseau lors de l'entrainement. Il en existe des spécifiques à des modèles et des généraux dont l'utilisation est répandue. Keras héberge de manière native certains des optimizers généraux ; voici une liste des optimizers natifs de keras utilisable via cette plateforme :

         ['sgd',
				  'rmsprop',
				  'adagrad',
				  'adadelta',
				  'adam',
				  'adamax',
				  'nadam'
				  ]

Pour en savoir plus sur ces optimizers, rendez-vous sur la documentation de keras : https://keras.io/api/optimizers/


Les paramètres concernant les optimizers se trouvent dans le dictionnaire OPT, qui est lui-même élément du dictionnaire COMPILATION, élément du dictionnaire MODEL.
Toutes les informations concernant la loss doivent être contenus dans le dictionnaire nommé OPT.

Ce dictionnaire est composé de la clé NAME , qui peut prendre les valeurs de la liste ci-dessus, ou les valeurs suivantes :
- RCNN : optimizer associée au modèle RCNN
- SGD : optimizer associée au modèle SSD300.

Dans le cas de l'utilisation du paramètres SGD, les paramètres supplémentaires suivants sont requis :

TODO.

##Templates

- Le template d'ajout de l'optimizer' est le suivant :

"OPT" : {
  "NAME" : ...,
  ...
}

- Template valide utilisant le dictionnaire MODEL :

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
