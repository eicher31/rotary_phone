# node-red

`flows.json` est un flow de départ pour la régie de jeu : il écoute
`phone/+/state`, `phone/+/digit`, `phone/+/call_state`, et montre comment
déclencher une sonnerie à distance sur `phone/<id>/cmd/ring`.

## Import

Dans l'éditeur Node-RED : menu ☰ → *Import* → coller le contenu de
`flows.json` (ou glisser-déposer le fichier), puis dans le nœud
"Broker rotary-phones", ajuster l'adresse du broker MQTT et les
identifiants (créés côté Mosquitto, voir `../docs/setup.md`).

## Pour aller plus loin

- Installer la palette `node-red-dashboard` pour remplacer les nœuds
  `debug` par un vrai tableau de bord visuel (statut de chaque poste,
  boutons de déclenchement, historique des codes composés).
- Ajouter un nœud `exec`/appel HTTP vers l'AMI d'Asterisk pour déclencher
  des appels/annonces automatiquement en réaction à un code composé
  (ex. via le module `node-red-contrib-asterisk-ami` ou un appel HTTP à
  un petit script wrapper autour de l'AMI).
