import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Exemple avec des données fictives
df = pd.read_excel( "etf_data.xlsx" )  # Remplacez par le vrai fichier
columns = [
    #"ISIN",
    "Perf 1 month",
    "Perf 3 months",
    "Perf 6 months",
    "Perf 1 year",
    "Perf 3 years",
    "Perf 5 years",
]

# Optionnel : Supprimer les colonnes non numériques ou inutiles
df = df[ columns ]

# Centrage et réduction (obligatoire pour l'ACP)
X = StandardScaler().fit_transform( df )

# Initialisation de l'ACP
pca = PCA( n_components = 2 )  # Choisissez le nombre de composantes à garder

# Appliquer l'ACP
X_pca = pca.fit_transform( X )

print( X_pca )

# Convertir le résultat en DataFrame
#df_pca = pd.DataFrame( X_pca, columns = [ 'PC1', 'PC2' ] )

# Nuage de points des deux premières composantes
# sns.scatterplot(data=df_pca, x='PC1', y='PC2')
# plt.title( 'Projection des données sur les 2 premières composantes principales' )
# plt.xlabel( 'PC1' )
# plt.ylabel( 'PC2' )
# plt.show()

# Variance expliquée par composante
# plt.figure( figsize = ( 8, 4 ) )
# plt.plot( np.cumsum( pca.explained_variance_ratio_ ), marker = "o" )
# plt.xlabel( "Nombre de composantes" )
# plt.ylabel( "Variance expliquée cumulée" )
# plt.title( "Variance expliquée par l'ACP" )
# plt.grid( True )
# plt.show()

# Afficher les poids (loadings) des variables originales sur les composantes principales
# loadings = pd.DataFrame(
#     pca.components_.T,
#     columns = ['PC1', 'PC2'],
#     index   = df.columns
# )
# print(loadings)