#Losses

L'intérêt de cette plateforme est de rendre le code transparent pour l'utilisateur.
Ainsi, tout interaction entre l'utilisateur et le code a lieu au travers d'une configuration.
Ces fichiers de configuration possèdent des paramètres obligatoires et d'autres optionnels - seule une combinaison valide de ces paramètres permettra d'utiliser correctement cette plateforme.

## La loss (fonction de perte)
Lors de l'entrainement d'un modèle, nous utilisons une fonction de perte (ou loss function) pour mesurer la distance entre les labels fournis par le réseaude neurones et ceux attendus (dans le cas d'un entraînement supervisé). Ces fonctions permettent de calculer la perte, qu'un modèle doit chercher à minimiser durant son entraînement.

Il existe plusieurs fonctions de pertes utilisées, certaines spécifiques à des modèles, d'autres plus générales. Keras héberge de manière native certaines des fonctions générales ; voici une liste des fonctions de pertes natives de keras utilisable via cette plateforme :

       ['categorical_crossentropy',
				'mean_squared_error',
				'mean_absolute_error',
				'mean_absolute_percentage_error',
				'mean_squared_percentage_error',
				'mean_squared_logarithmic_error',
				'squared_hinge',
				'hinge',
				'categorical_hinge',
				'logcosh',
				'huber_loss',
				'categorical_crossentropy',
				'sparse_categorical_crossentropy',
				'binary_crossentropy',
				'kullback_leibler_divergence',
				'poisson',
				'cosine_proximity',
				'is_categorical_crossentropy',
				]
Pour en savoir plus sur ces fonctions de perte, rendez-vous sur la documentation de keras : https://keras.io/api/losses/


Les paramètres concernant la loss se trouvent dans le dictionnaire LOSS, qui est lui-même élément du dictionnaire COMPILATION, élément du dictionnaire MODEL.
Toutes les informations concernant la loss doivent être contenus dans le dictionnaire nommé LOSS.

Ce dictionnaire est composé de la clé NAME , qui peut prendre les valeurs de la liste ci-dessus, ou les valeurs suivantes :
- RCNN_LOSS : fonction de perte associée au modèle RCNN
- SSD_LOSS : fonction de perte associée au modèle SSD300.

Dans le cas de l'utilisation du paramètres SSD_LOSS, les paramètres supplémentaires suivants sotn requis :

TODO.

##Templates

- Le template d'ajout de la loss est le suivant :

"LOSS" : {
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
