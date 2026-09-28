# Liste de matériel (BOM)

Prix indicatifs (commande en ligne, quantités unitaires) — à affiner selon
fournisseurs réels (Digikey/Mouser/AliExpress/Pihut/Distrelec).

## Par poste (× 6)

| Élément | Rôle | Prix indicatif |
|---|---|---|
| Raspberry Pi Zero W | cerveau du poste (Wi-Fi intégré) — choisi pour sa disponibilité, voir `hardware.md` | ~15 € |
| Carte microSD 16-32 Go (classe A1/A2) | OS | ~6 € |
| Adaptateur son USB jack 3.5mm *ou* HAT I2S (ex. ReSpeaker 2-Mic) | interface audio | ~3-20 € |
| Adaptateur micro-USB OTG (USB-A → micro-USB) *ou* hub OTG multi-ports si Ethernet USB aussi utilisé | **indispensable si carte son USB** — le Zero W n'a pas de port USB-A, voir `hardware.md`. Inutile si vous prenez l'option HAT I2S (se branche directement sur le connecteur 40 broches). | ~6-15 € |
| Ampli classe D PAM8403 | pilote le haut-parleur d'écouteur | ~1.5 € |
| Capsule micro électret | remplace le micro carbone d'origine | ~1 € |
| Petit haut-parleur 8 Ω (si l'écouteur d'origine n'est pas réutilisable) | audio sortant | ~2 € |
| Module MOSFET (ex. IRLZ44N + driver) | pilote le frappeur de timbres | ~2 € |
| Petit moteur vibrant ou solénoïde 5V | frappe les timbres d'origine | ~3-6 € |
| Alimentation 5V/2.5A micro-USB *ou* splitter PoE | alimentation | ~8-12 € |
| Adaptateur USB-Ethernet (optionnel, recommandé si Wi-Fi saturé) | fiabilité audio/réseau — nécessite alors un hub OTG multi-ports (ligne ci-dessus) plutôt qu'un simple adaptateur, puisqu'il se cumule avec la carte son | ~8 € |
| Divers : fils, dominos/wago, entretoises, connecteurs Dupont, gaine thermo | câblage | ~5 € |

**Total électronique par poste : ~60-95 €** (hors téléphone lui-même).

## Pour 6 postes

- Électronique : **~360-570 €**
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
| Électronique (6 postes) | ~360-570 € |
| Téléphones supplémentaires (4-5) | ~75-200 CHF |
| Serveur central (si à acheter) | ~60-70 € |
| **Total** | **~495-840 €/CHF** selon options retenues |
