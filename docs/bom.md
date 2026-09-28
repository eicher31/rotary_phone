# Liste de matériel (BOM)

Prix indicatifs (commande en ligne, quantités unitaires) — à affiner selon
fournisseurs réels (Digikey/Mouser/AliExpress/Pihut/Distrelec).

## Par poste (× 6)

| Élément | Rôle | Prix indicatif |
|---|---|---|
| Raspberry Pi Zero W | cerveau du poste (Wi-Fi intégré) — choisi pour sa disponibilité, voir `hardware.md` | ~15 € |
| Carte microSD 16-32 Go (classe A1/A2) | OS | ~6 € |
| Carte audio **IQaudio Codec Zero** (HAT I2S, officielle Raspberry Pi) | interface audio recommandée — remplace carte son USB + ampli, se branche directement sur le connecteur 40 broches (pas besoin d'adaptateur OTG), prise jack 3.5mm mono pour micro externe + ampli mono 8Ω intégrés, voir `hardware.md` | ~18-23 € |
| Capsule micro électret | câblée sur la prise jack micro externe de la carte Codec Zero, remplace le micro carbone d'origine | ~1 € |
| Petit haut-parleur 8 Ω (si l'écouteur d'origine n'est pas réutilisable) | câblé sur la sortie ampli mono de la carte Codec Zero | ~2 € |
| Module MOSFET (IRLZ44N + diode de roue libre, voir références ci-dessous) | pilote le frappeur de timbres — un module relais a été écarté, trop volumineux pour le boîtier, voir `hardware.md` | ~2 € |
| Petit moteur vibrant ou solénoïde 5V | frappe les timbres d'origine | ~3-6 € |
| Alimentation 5V/2.5A micro-USB *ou* splitter PoE | alimentation | ~8-12 € |
| Divers : fils, dominos/wago, entretoises, connecteurs Dupont, gaine thermo | câblage | ~5 € |

**Total électronique par poste : ~60-72 €** (hors téléphone lui-même).

## Références précises (fournisseurs vérifiés)

| Élément | Référence / lien |
|---|---|
| Carte audio IQaudio Codec Zero | [The Pi Hut](https://thepihut.com/products/iqaudio-codec-zero) (~£16) ou [Kiwi Electronics](https://www.kiwi-electronics.com/en/iqaudio-codec-zero-10833) (~€20.62 HT), livrent en Suisse |
| Capsule micro électret | [RS PRO Microphone Element](https://www.distrelec.ch/en/microphone-element-electret-condenser-omni-directional-44-db-50hz-16khz-rs-pro-7800784/p/30404884) — Distrelec |
| Haut-parleur 8 Ω | [RS PRO Miniature Speaker 22.5mm 8Ω](https://www.distrelec.ch/en/miniature-speaker-22-5mm-80mw-8ohm-73db-rs-pro-7243100/p/30404817) — Distrelec |
| MOSFET N logic-level (IRLZ44N, TO-220) | [Infineon IRLZ44NPBF](https://www.distrelec.ch/fr/mosfet-kanal-55v-47a-to-220-infineon-irlz44npbf/p/30341412) — Distrelec réf. **30341412** |
| Diode de roue libre | [Diotec 1N4007, DO-41](https://www.distrelec.ch/fr/diode-de-redressement-1kv-1a-do-41-diotec-1n4007/p/11052628) — Distrelec réf. **11052628** |
| Solénoïde 5V | [SparkFun Push Solenoid 5V (ROB-11015)](https://www.distrelec.ch/en/push-solenoid-5v-sparkfun-electronics-rob-11015/p/30145495) — Distrelec |
| Alimentation officielle micro-USB 5.1V/2.5A | [Raspberry Pi T5989DV](https://www.distrelec.ch/en/usb-power-supply-for-raspberry-pi-240vac-500ma-13w-euro-type-cee-16-plug-us-plug-uk-type-bs1363-plug-au-plug-usb-micro-plug-raspberry-pi-t5989dv/p/30134465) — Distrelec |
| Carte microSD 32 Go A1 | [SanDisk Ultra 32GB microSDHC A1](https://www.galaxus.ch/de/s1/product/sandisk-ultra-32-gb-microsdhc-u1-uhs-i-speicherkarte-15663866) — Galaxus (pas trouvé chez Distrelec) |
| Fils Dupont / gaine thermorétractable | Catégories [DuPont](https://www.distrelec.ch/en/manufacturer/dupont/man_dpn) et [gaines thermorétractables](https://www.galaxus.ch/fr/s4/producttype/gaine-thermoretractable-3652) |

Résistances (220 Ω série + 10 kΩ pull-down pour la grille du MOSFET) :
composants génériques, n'importe quel assortiment de résistances 1/4W
convient — pas de référence dédiée nécessaire.

### Optionnel : réseau filaire

| Élément | Rôle | Prix indicatif |
|---|---|---|
| Adaptateur USB-Ethernet | fiabilité audio/réseau si le Wi-Fi est saturé, voir `software-architecture.md` | ~8 € |
| Adaptateur micro-USB OTG simple (USB-A → micro-USB) | pour brancher l'adaptateur Ethernet — un simple adaptateur suffit maintenant (plus besoin de hub multi-ports, la carte audio n'utilise plus le port USB) | ~6-10 € |

## Pour 6 postes

- Électronique : **~360-432 €**
- Téléphones à acquérir (l'utilisateur en possède déjà un) : brocante,
  Ricardo.ch, eBay — typiquement **15-40 CHF/pièce** en Suisse pour ce
  type de modèle PTT, donc **~75-200 CHF** pour les 4-5 restants.

## Serveur central (Asterisk + Mosquitto + Node-RED)

- Réutilisation d'un Raspberry Pi 4 (4 Go) ou mini-PC déjà disponible :
  **0 €**.
- Sinon, Raspberry Pi 4 4 Go dédié + alimentation + carte SD :
  **~60-70 €**.

## Total estimé du projet

| Poste de dépense | Montant |
|---|---|
| Électronique (6 postes) | ~360-432 € |
| Téléphones supplémentaires (4-5) | ~75-200 CHF |
| Serveur central (si à acheter) | ~60-70 € |
| **Total** | **~495-700 €/CHF** selon options retenues |
