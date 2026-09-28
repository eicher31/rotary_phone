# Guide d'installation

## 0. Prototype unique d'abord

Avant de dupliquer sur 6 postes, montez et validez **un seul** prototype
complet (voir la checklist dans `README.md` → "État du projet"). Les
étapes ci-dessous s'appliquent aussi bien au prototype qu'au déploiement
final via Ansible.

## 1. Serveur central

1. Installer Raspberry Pi OS (ou toute Debian/Ubuntu) sur le serveur
   central (Pi 4 conseillé, ou réutiliser une machine existante).
2. Installer Asterisk et Mosquitto :
   ```bash
   sudo apt update
   sudo apt install -y asterisk mosquitto mosquitto-clients
   ```
3. Déployer la configuration de ce dépôt :
   ```bash
   sudo cp pbx/asterisk/pjsip.conf /etc/asterisk/pjsip.conf
   sudo cp pbx/asterisk/extensions.conf /etc/asterisk/extensions.conf
   sudo cp pbx/mosquitto/mosquitto.conf /etc/mosquitto/conf.d/rotary-phones.conf
   ```
4. **Changer tous les mots de passe** `changeme-*` dans `pjsip.conf` avant
   toute mise en production, et créer les comptes Mosquitto :
   ```bash
   sudo mosquitto_passwd -c /etc/mosquitto/passwd nodered
   sudo mosquitto_passwd /etc/mosquitto/passwd phone01
   # ... répéter pour phone02..phone06
   ```
5. Redémarrer les services :
   ```bash
   sudo systemctl restart asterisk mosquitto
   ```
6. (Optionnel) Installer Node-RED et importer `node-red/flows.json`.

## 2. Chaque poste (Raspberry Pi Zero 2 W)

### 2.1 Image de base

1. Flasher Raspberry Pi OS Lite (64-bit) sur la carte microSD avec
   Raspberry Pi Imager, en activant SSH + Wi-Fi dans les options avancées
   (identifiants propres à chaque poste si vous n'utilisez pas encore
   Ansible pour ça).
2. Démonter la carte microSD, l'insérer dans le Pi Zero 2 W, câbler le
   matériel selon `hardware.md`, démarrer.

### 2.2 Déploiement automatisé (Ansible, recommandé pour 6 postes)

1. Éditer `ansible/inventory/hosts.yml` : IP, `phone_id`, `sip_extension`
   et brochage GPIO de chacun des 6 postes.
2. Éditer `ansible/group_vars/all.yml` : adresse du broker MQTT et du
   registrar SIP (le serveur central).
3. Lancer le playbook :
   ```bash
   cd ansible
   ansible-playbook site.yml
   ```
   Cela installe et configure baresip, le daemon GPIO
   (`rotary-phone-daemon.service`) et l'audio sur les 6 postes en une
   commande.

### 2.3 Déploiement manuel (pour un prototype rapide, sans Ansible)

```bash
sudo apt install -y baresip baresip-mod-ctrl-tcp python3-venv

cd gpio-daemon
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

cp config.example.yaml /etc/rotary-phone-config.yaml
# éditer /etc/rotary-phone-config.yaml : phone_id, sip_extension, mqtt_host, pins...

sudo .venv/bin/python -m gpio_daemon --config /etc/rotary-phone-config.yaml
```

## 3. Vérifications de bout en bout

1. **Audio** : `aplay -l` et `arecord -l` doivent lister la carte son USB ;
   tester avec `speaker-test` et `arecord -d 5 test.wav && aplay test.wav`.
2. **baresip** : `telnet 127.0.0.1 4444` (ou `nc`) doit se connecter au
   port `ctrl_tcp` ; envoyer `/dial 100` doit déclencher un appel.
3. **Daemon GPIO** : `sudo journalctl -u rotary-phone-daemon -f` en
   décrochant/raccrochant et en composant un chiffre doit montrer les
   changements d'état.
4. **MQTT** : sur le serveur central,
   `mosquitto_sub -t 'phone/#' -v` doit afficher les événements en
   temps réel pendant qu'on manipule un poste.
5. **Appel réel** : décrocher le poste 1, composer `101` → le poste 2
   doit sonner (timbres mécaniques via le frappeur).
6. **Déclenchement de jeu** : composer un code sur un poste, vérifier
   dans Node-RED (ou `mosquitto_sub`) que chaque chiffre arrive bien sur
   `phone/<id>/digit`.
