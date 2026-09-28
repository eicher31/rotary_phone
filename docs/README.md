# Documentation

- [`hardware.md`](hardware.md) — modifications à apporter au téléphone, brochage GPIO, câblage.
- [`bom.md`](bom.md) — liste de matériel et coûts estimés, par poste et pour 6 postes.
- [`software-architecture.md`](software-architecture.md) — vue d'ensemble logicielle, topics MQTT, choix techniques.
- [`setup.md`](setup.md) — guide d'installation pas à pas (image SD → Ansible → Asterisk → test).

## État du projet — ce qui est validé

Ce dépôt a été écrit dans un environnement sans accès au matériel réel
(pas de Raspberry Pi, pas de téléphone, pas de serveur Asterisk
disponible). Pour ne pas laisser croire à une validation qui n'a pas eu
lieu, voici précisément ce qui est vérifié et ce qui ne l'est pas :

| Composant | État |
|---|---|
| Décodage des impulsions du cadran (`gpio_daemon/dial_decoder.py`) | ✅ Couvert par des tests unitaires (`gpio-daemon/tests/`), logique indépendante du matériel |
| Anti-rebond (`gpio_daemon/debounce.py`) | ✅ Couvert par des tests unitaires |
| Cadence de sonnerie (`gpio_daemon/ringer.py`) | ✅ Couvert par des tests unitaires |
| Abstraction GPIO (`gpio_daemon/gpio_backend.py`) | ⚠️ Le backend réel (`GpiozeroBackend`) n'a pas pu être testé sur un vrai Pi/GPIO — à valider en premier lors du montage du premier prototype |
| Client `baresip ctrl_tcp` (`gpio_daemon/baresip_client.py`) | ⚠️ Écrit de façon prudente (parsing tolérant), mais le format exact des événements JSON dépend de la version de baresip installée — **à vérifier sur le matériel réel** avant de s'y fier |
| Configuration Asterisk/PJSIP (`pbx/`) | ⚠️ Syntaxiquement correcte, non testée faute de serveur Asterisk disponible ici |
| Playbook Ansible (`ansible/`) | ⚠️ Structure complète, non exécutée faute de Raspberry Pi disponible ici |
| Dimensionnement électrique (micro électret, ampli, moteur/solénoïde de sonnerie) | ⚠️ Choix de composants raisonnables mais **à valider à la mesure** (impédance de l'écouteur d'origine, force nécessaire pour frapper les timbres, etc.) — voir `hardware.md` |
| Carte audio IQaudio Codec Zero : entrée micro externe | ✅ Documentée officiellement (prise jack 3.5mm mono dédiée, désactive le micro embarqué automatiquement, overlay mainline `dtoverlay=rpi-codeczero`) — voir `hardware.md` et [pinout.xyz/pinout/codec_zero](https://pinout.xyz/pinout/codec_zero) |

**Premier jalon recommandé avant de répliquer sur 6 postes** : monter un
seul prototype complet, valider chaque point ⚠️ ci-dessus dessus, ajuster
le code/la config en conséquence, *puis* dupliquer via Ansible sur les 5
autres.
