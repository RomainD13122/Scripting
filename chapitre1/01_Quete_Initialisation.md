# Quête 1 : Mise en place de l'environnement de travail

## Objectifs de la quête
- [x] Assurer un environnement de virtualisation fonctionnel.
- [x] Vérifier la présence de Python et l'installer si nécessaire.

---

## 1. Environnement de Virtualisation

Pour réaliser les laboratoires sans risquer d'endommager le système d'exploitation principal (l'hôte), nous utilisons un **Hyperviseur de Type 2**. Cela permet de faire tourner des machines virtuelles (VM) isolées.

### Architecture retenue
Nous avons opté pour la configuration suivante :
* **Hyperviseur :** Oracle VM VirtualBox (Gratuit et Open Source).
* **Machine Virtuelle (Guest) :** Ubuntu Server (ou Debian) pour sa légèreté et sa compatibilité avec Python.



### Procédure d'installation

1.  **Téléchargement de l'hyperviseur :**
    * Se rendre sur le site officiel de [VirtualBox](https://www.virtualbox.org/).
    * Télécharger la version correspondant au système hôte (Windows, macOS ou Linux).
2.  **Installation :**
    * Lancer l'exécutable et suivre les instructions par défaut.
    * *Note :* Sous Windows, il peut être nécessaire d'activer la virtualisation (VT-x/AMD-V) dans le BIOS si ce n'est pas déjà fait.
3.  **Création de la première VM :**
    * Cliquer sur "Nouvelle".
    * Nom : `Quest-Machine-01`.
    * ISO : Sélectionner l'image disque Linux téléchargée (ex: `ubuntu-22.04-live-server.iso`).
    * Ressources : Allouer au minimum 2 vCPU et 4 Go de RAM pour assurer la fluidité.

**Validation :**
La machine virtuelle démarre et arrive sur l'écran de login. L'environnement est considéré comme fonctionnel.

---

## 2. Vérification et Installation de Python

Python est un langage de script essentiel pour l'automatisation des tâches à venir. Une fois connecté sur la machine virtuelle (via le terminal), nous devons vérifier sa présence.

### Étape A : Vérification de l'installation

Dans le terminal de la machine virtuelle, exécutez la commande suivante :

```bash
python3 --version