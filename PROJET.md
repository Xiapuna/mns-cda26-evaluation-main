<p align="center">
<img src="docs/logo.png" alt="logo">
</p>

## Brief fonctionnel

### 1. Contexte et objectif

Une entreprise de taille moyenne souhaite se doter d'un **outil interne** permettant de centraliser les **idées d'évènements à organiser en interne** : conférences, ateliers, team building, sorties d'équipe, afterworks, etc.

Aujourd'hui, on peut imaginer que ces informations circulent par e-mail ou via différents outils non centralisés. L'objectif est donc de disposer d'une **application web interne légère**, accessible via un navigateur, permettant de :

- consulter les évènements proposés
- proposer facilement une idée d'évènement via un formulaire
- exposer une petite information synthétique au format JSON pour une future intégration (intranet, écran d'accueil, outil RH)

### 2. Périmètre spécifique à l'évaluation

Dans le cadre de cette éval, l'application ne gèrera **que les évènements**.
Il n'y a **pas de gestion des utilisateurs**, pas d'authentification, pas de notion d'inscription ou de participation.

### 3. Fonctionnalités

#### 3.1 Consultation des évènements

L'utilisateur doit pouvoir consulter la liste des évènements proposés.

Chaque évènement est caractérisé par :

- un titre (exemple _Repas de fin d'année_)
- un type d'évènement (conférence, team building, sortie, repas d'équipe, autre) (exemple _repas d'équipe_)
- la date proposée pour l'évènement (exemple _20 décembre 2026_)
- le lieu proposé (exemple _le 124_)
- une description courte (exemple _un repas de fin d'année pour déguster un dernier riz crousty ensemble !_)
- la date à laquelle la proposition a été soumise (exemple _2 février 2026_)

Les évènements doivent être affichés sous forme de liste claire et lisible.

#### 3.2 Proposition d'un évènement

L'utilisateur doit pouvoir proposer un nouvel évènement via une page dédiée.
La création d'un évènement se fait à l'aide d'un **formulaire HTML** comportant au minimum :

- un titre
- un type d'évènement (liste prédéfinie, voir ci-dessus)
- la date proposée
- un lieu
- une description

Les règles suivantes doivent être respectées :

- tous les champs sont obligatoires
- si un champ est manquant ou invalide, un message d'erreur clair est affiché
- en cas de succès, l'évènement est enregistré en base et l'utilisateur est redirigé vers la liste des évènements

#### 3.3 Pages de l'application

L'application doit proposer au minimum les pages suivantes :

- **Page d'accueil**
  Affichage de tous les évènements stockés en base de données, avec possibilité de les supprimer un par un.

- **Page d'ajout d'un évènement**
  Formulaire de création d'un nouvel évènement.

Toutes les pages doivent être rendues à l'aide de **templates Jinja2**.

### 4. Données et persistance

Les données doivent être stockées dans une **base de données SQLite** créée au premier lancement.

### 5. API REST/JSON

⚠️ Les contraintes mentionnées dans cette section, notamment sur les normes API REST s'appliquent **uniquement** pour la route définie dans ce paragraphe. Les autres routes ci-dessus (interface HTML) restent standard et ne sont pas concernées.

L'application doit exposer **une route sous la forme d'une API/REST** destinée à un usage futur (intranet, affichage automatique, statistiques simples).

Cette route doit :

- respecter la norme REST
- retourner une réponse JSON valide
- utiliser un code HTTP approprié
- retourner des données lisibles et structurées

L'objectif de la route est d'exposer les **5 prochains évènements** (selon la date proposée).

### 6. Contraintes techniques

- Framework : Flask
- Base de données : SQLite
- ORM : SQLAlchemy
- Lancement simple de l'application (commande claire)
- Structure de projet lisible et cohérente

### 7. Hors périmètre explicite

Dans le cadre de l'éval, les éléments suivants sont volontairement exclus :

- gestion des utilisateurs ou des rôles
- système d'inscription ou de participation
- notifications, e-mails, calendrier externe
- logique complexe de planning
