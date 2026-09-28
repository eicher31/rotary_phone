# gpio-daemon

Service Python (un par poste) qui relie le matériel du téléphone
(crochet, cadran, frappeur de timbres) à baresip (appels SIP) et à MQTT
(événements/commandes pour la régie de jeu).

Voir [`../docs/software-architecture.md`](../docs/software-architecture.md)
pour le fonctionnement d'ensemble.

## Modules

- `debounce.py` — anti-rebond logiciel générique.
- `dial_decoder.py` — décodage des impulsions du cadran en chiffres
  (deux stratégies : contacts hors-repos + impulsion, ou temporisation).
- `ringer.py` — cadence de sonnerie pour le frappeur de timbres.
- `gpio_backend.py` — abstraction GPIO (backend réel `gpiozero` + backend
  `FakeBackend` pour les tests).
- `baresip_client.py` — client pour le module `ctrl_tcp` de baresip.
- `mqtt_client.py` — fine couche autour de `paho-mqtt`.
- `config.py` — chargement de la configuration YAML par poste.
- `service.py` — assemble le tout (`PhoneDaemon`), point d'entrée `main()`.

## Tests

Les modules `debounce`, `dial_decoder`, `ringer` et `gpio_backend`
(backend factice) sont testés sans aucun matériel :

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

## Lancer le daemon

```bash
python -m gpio_daemon --config /etc/rotary-phone/config.yaml
```

Voir `config.example.yaml` pour le format de configuration, et
`rotary-phone-daemon.service` pour l'unité systemd (déployée
automatiquement par le rôle Ansible `gpio-daemon`).
