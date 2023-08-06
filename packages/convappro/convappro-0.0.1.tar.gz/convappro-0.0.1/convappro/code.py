#!/usr/bin/env python3

"""
Projet d'analyse: Sujet 31
Le projet: Il nous est demandé d'approcher de la valeur de sin(8/5) tout en certifiant nos résultats.
            Gràce à la formule de Taylor appliquée sur R à la preuve de Cauchy et à l'établissement du certificat de
            convergence, on a constaté que l'on peut etendre cette définition sur R et ainsi pouvoir de cette manière
            moduler à un ordre k les N premières décimales du sin de tout réel
            Voici le programme qui traduit les résultats de nos analyses.
"""
"""
Dans la classe calculs, on définit toutes les fonctions nécessaires et demandées dans l'énoncé
"""

class calculs:
    
    def __init__(self, valeur):
        """
        Initialisation de la fonction calculs pour les problèmes menant à sin(:param valeur)
        :param valeur: valeur de type float
        """
        self.valeur = valeur
        pass

    def valeurAbsolue(self,x):
        """
        Fonction retournant la valeur absolue de :param x
        :param x: Valeur négative ou positive
        :return: La valeur absolue de :param x
        """
        return x if x>0 else x * -1

    def factoriel(self,x):
        """
        Fonction retournant le factoriel de :param x
        :param x: Valeur
        :return: Le factoriel de :param x
        """
        return 1 if x<= 1 else x * self.factoriel(x-1)

    def tronque(self, x, p):
        """
        Fonction tronquant :param x à 10**-:param p près
        :param x: Flottant
        :param p: nombre de troncature souhaitée
        :return: :param x à 10**-:param p près
        """
        p = 10 ** p
        print('a = ', (int(x * p))/p)
        return (int(x * p))/p

    def sinusTaylor(self,angle,p):
        """
        Fonction calculant selon la formule de Taylor la valeur de sin(:param angle)
        à l'ordre :param p
        :param angle: flottant
        :param p: l'ordre n du calcul du developpement limité
        :return: sin(:param angle) selon le developpement limité de Taylor à l'odre n = :param p
        """
        valeur = 0.0
        for n in range(p):
            valeur += (((-1) ** n ) * ((angle ** ((2*n) + 1)) / self.factoriel((2*n) + 1 )))
        return valeur

    def r(self, n):
        """
        r(n)
        :param n: entier naturel, l'indice n de la suite
        :return: r(:param n)
        """
        print(f"r({n}) = {self.sinusTaylor(self.valeur, n)}")
        return self.sinusTaylor(self.valeur, n)
    
    def suiteR(self, n):
        """
        Suite (r(n)_n)
        Fonction pour le main qui affiche chaque valeur de r(n)
        """
        print("\n")
        for i in range(0, n+1):
            self.r(i)
        print("\n")
        

    def conv(self, k):
        """
        Certificat de convergence de la suite (r(n))_n
        :param k: entier naturel, l'ordre k du calcul conv(k)
        :return: conv(:param k)
        """
        n = 0
        ordre = 1 / (10 ** (k))
        while True:
            n += 1
            approche = (2 ** (n + 1)) / self.factoriel(n + 1)
            if (approche <= ordre):
                break
        
        print(f"resultat = {n}")
        return n

    def preuveCauchy(self, epsilon):
        """
        Fonction prouvant la stabilité d'un developpement limité de 10 ** -:param epsilon
        :param epsilon: Ordre de precision souhaité
        :return: L'ordre du developpement limité à partir duquel :param valeur est stable
        """
        n = 1
        while True:
            difference = self.sinusTaylor(self.valeur, n) - self.sinusTaylor(self.valeur, n + 1)
            n += 1
            if (self.valeurAbsolue(difference) < epsilon):
                break
        return n - 1
    
    def ordreAtteint(self, epsilon):
        """
        Fonction pour le main qui affiche à partir de quel rang de la suite R, l'ordre epsilon est atteint
        :param epsilon: Ordre de precision souhaité
        """
        print(f"Certificat d'ordre {epsilon} atteinte à partir de r({self.preuveCauchy(epsilon)})")
        
    
"""
Ensuite, le main execute les fonctions et présente les résultats.
"""

valeur = calculs(8/5)

if __name__ == '__main__':
    print('\n\tDebut du programme\n\n')

    resultat = valeur.conv(7)
    
    valeur.suiteR(resultat)
    
    epsilon = 10 ** -6
    valeur.ordreAtteint(epsilon)
    
    a = valeur.tronque(valeur.r(valeur.preuveCauchy(epsilon)), 6)
    
    print('\n\n\tFin du programme')