# L-System
Projet python CPI2 pour l'année 2020 par BRISSET Joachim, HOPSORE Theo, KEMGNE Jules-Antoine
****************

## Description
Le but de ce projet est de creer un programme capable de produire un fichier permettant de dessiner un L-System au niveau desiré

## Exmples
Exemple simple pour Linux
``` bash 
python3 l-system.py -i Exemple/floconKoch3.txt -o floconKoch3.py
```
Exemple avancé pour Linux
``` bash 
 for file in Exemples/*.txt; do echo $file; python3 l-system.py -i $file -o "${file%.*}.py"; done
```

## Syntax
- ``` -i <file> ``` selection le fichier d'entrée
- ``` -o <file> ``` selection le fichier de sortie
- ``` --nodraw ``` ne dessine pas a la fin du programme

## TODO
- verifier que pour chaque symbole [ il y a un ] de même niveau d'imbrication
- verifier que tout les symboles ont une action associé
- ajouter l'argument -f pour forcer et ne pas avoir d'interaction avec l'utilisateur