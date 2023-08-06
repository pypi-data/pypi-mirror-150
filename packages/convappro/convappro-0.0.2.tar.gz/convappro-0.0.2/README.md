# Bienvenue sur le guide de convappro! (sujet 31)
Convappro a pour objectif de donner avec la plus grande précision la valeur approximative du sinus de tout nombre réel (angle en radians modulo 2pi).

Cette précision théorique est de l'ordre de 10<sup>-100</sup> et utilise les formules de Taylor-Lagrange pour les développements limités et les suites de Cauchy pour en certifier la convergence (la stabilité et la précision).

Ce module a été réalisé par Henri MACEDO GONÇALVES, Alexandre RAMDOO, NOVERRAZ Marion et HAGHVIRDILOO Mostafa comme but scolaire.

## Consignes d'utilisation

### 1. Installation
```shell script
pip install convappro
``` 
ou encore
```shell script
python3 -m pip install convappro
```

### 2. Utilisation
Soit vous utilisez le main à disposition:

- Dans le terminal, allez sur le répertoire qui contient code.py et tapez:
```
  ./code.py
```

Soit en l'utilisant manuellement:
```
python3
from code import *
valeur = calculs(x)
```

- La variable x est la valeur que vous souhaitez calculer.

### 3. Les fonctions

Vous avez à votre disposition les fonctions suivantes:

Certificat de convergence d'une suite (r(n)<sub>n</sub>) de l'ordre k du calcul conv(k):
```
resultat = valeur.conv(k)
```

r(n) calcule n-ième élément:
```
valeur.r(n)
```

Affiche les n premiers éléments de la suite:
```
valeur.suiteR(n)
```

Preuve de Cauchy:
```
valeur.preuveCauchy(epsilon)
```

Affiche à partir de quel r(n) l'ordre est atteinte:
```
valeur.ordreAtteinte(epsilon)
```

Tronque x ( ex: valeur.r(valeur.preuveCauchy(epsilon)) ) à 10<sup>-p</sup> près:
```
a = valeur.tronque(x,p)
```

## DISCLAIMER
Ce module n'a pas vocation à remplacer le module de base math. Il est réalisé à titre scolaire et les auteurs ne sauraient en aucun cas être tenus responsables de sa mauvaise utilisation.
