# rotary_phone

Conversion de vieux téléphones muraux à cadran (mécaniques, ~années 1950-60,
type PTT suisse à deux timbres) en postes **VoIP fonctionnels** doublés
d'**accessoires de jeu** (escape game / jeu de piste), pilotés par un
Raspberry Pi Zero 2 W par téléphone. Objectif : 5-6 unités identiques.

## Ce que fait chaque poste

- **Appels réels** : décrocher/raccrocher et composer un numéro sur le
  cadran d'origine passe un vrai appel SIP vers un autre poste (ou
  l'extérieur), via un petit standard Asterisk central.
- **Événements de jeu** : chaque impulsion du cadran et chaque
  décroché/raccroché est aussi publié sur un bus MQTT, pour qu'une régie
  de jeu (ex. Node-RED) puisse réagir à un code composé, déclencher un
  indice, faire sonner un poste à distance, etc.
- L'aspect du téléphone reste inchangé : boîtier, combiné, cadran et
  timbres d'origine sont conservés ; seuls le micro, le haut-parleur et
  l'électronique interne sont remplacés/ajoutés.

## Structure du dépôt

| Dossier | Contenu |
|---|---|
| [`docs/`](docs/README.md) | Vue d'ensemble, modifications matérielles, BOM, architecture logicielle, guide d'installation |
| [`gpio-daemon/`](gpio-daemon/README.md) | Service Python (un par poste) : décodage cadran, crochet, sonnerie, MQTT, pilotage de baresip |
| [`ansible/`](ansible) | Playbook de déploiement reproductible sur les 6 Raspberry Pi |
| [`pbx/`](pbx) | Configuration Asterisk (PJSIP + dialplan) et Mosquitto pour le serveur central |
| [`node-red/`](node-red) | Flow d'exemple pour le tableau de bord de régie |

## État du projet

Voir [`docs/README.md`](docs/README.md#état-du-projet--ce-qui-est-validé) pour
le détail de ce qui est testé (logique de décodage du cadran, anti-rebond,
cadence de sonnerie — couvert par des tests unitaires, sans matériel) par
rapport à ce qui reste à valider sur le matériel réel (audio, protocole
exact de `baresip ctrl_tcp`, dimensionnement du frappeur de timbres, etc.).

## Démarrage rapide

```bash
cd gpio-daemon
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Pour la suite (câblage, déploiement Ansible, configuration Asterisk),
voir [`docs/setup.md`](docs/setup.md).
