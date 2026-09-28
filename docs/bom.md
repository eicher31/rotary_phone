# Liste de matériel (BOM)

Prix indicatifs (commande en ligne, quantités unitaires) — à affiner selon
fournisseurs réels (Digikey/Mouser/AliExpress/Pihut/Distrelec).

## Par poste (× 6)

| Élément | Rôle | Prix indicatif |
|---|---|---|
| Raspberry Pi Zero W | cerveau du poste (Wi-Fi intégré) — choisi pour sa disponibilité, voir `hardware.md` | ~15 € |
| Carte microSD 16-32 Go (classe A1/A2) | OS | ~6 € |
| Carte audio **Waveshare DA7212 Audio Board (A)** (HAT I2S) | interface audio recommandée — remplace carte son USB + ampli, se branche directement sur le connecteur 40 broches (pas besoin d'adaptateur OTG), entrée micro externe + ampli mono intégrés, voir `hardware.md` | ~22-25 € |
| Capsule micro électret | câblée sur l'entrée micro externe de la carte DA7212, remplace le micro carbone d'origine | ~1 € |
| Petit haut-parleur 8 Ω (si l'écouteur d'origine n'est pas réutilisable) | câblé sur la sortie ampli mono de la carte DA7212 | ~2 € |
| Module MOSFET (ex. IRLZ44N + driver) | pilote le frappeur de timbres | ~2 € |
| Petit moteur vibrant ou solénoïde 5V | frappe les timbres d'origine | ~3-6 € |
| Alimentation 5V/2.5A micro-USB *ou* splitter PoE | alimentation | ~8-12 € |
| Divers : fils, dominos/wago, entretoises, connecteurs Dupont, gaine thermo | câblage | ~5 € |

**Total électronique par poste : ~64-74 €** (hors téléphone lui-même).

### Optionnel : réseau filaire

| Élément | Rôle | Prix indicatif |
|---|---|---|
| Adaptateur USB-Ethernet | fiabilité audio/réseau si le Wi-Fi est saturé, voir `software-architecture.md` | ~8 € |
| Adaptateur micro-USB OTG simple (USB-A → micro-USB) | pour brancher l'adaptateur Ethernet — un simple adaptateur suffit maintenant (plus besoin de hub multi-ports, la carte audio n'utilise plus le port USB) | ~6-10 € |

## Pour 6 postes

- Électronique : **~384-444 €**
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
| Électronique (6 postes) | ~384-444 € |
| Téléphones supplémentaires (4-5) | ~75-200 CHF |
| Serveur central (si à acheter) | ~60-70 € |
| **Total** | **~520-715 €/CHF** selon options retenues |
