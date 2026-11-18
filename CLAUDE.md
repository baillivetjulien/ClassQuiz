# ClassQuiz — version de l'Agence

Fork de [mawoka-myblock/ClassQuiz](https://github.com/mawoka-myblock/ClassQuiz), refondu pour l'Agence régionale de l'orientation et des métiers de Normandie. Il sert aux quiz en direct des ateliers des conseillères et remplace Kahoot.

Le pilotage (issues, décisions, usage réel de Kahoot) est dans le dépôt privé `baillivetjulien/leohoot`, cloné sur le serveur dans `~/Leohoot`. Avant un ticket, lire sa spec (#33), `~/Leohoot/docs/usage-kahoot.md`, `~/Leohoot/GLOSSARY.md` et les ADR de `~/Leohoot/docs/adr/`.

## Règles

- **Dépôt public** (licence MPL 2.0) : aucun secret, aucun contenu de l'Agence (quiz, données, identifiants).
- **Branches** : `agence` est notre version et la branche par défaut ; `master` reste le miroir de l'amont, sans aucun commit à nous.
- **Changements localisés**, pour que les mises à jour amont restent faciles à reporter :
  - champs optionnels dans le JSON des questions ou des joueurs plutôt que des migrations de base ;
  - thème par les variables Tailwind 4 et les utilitaires globaux avant de modifier les composants ;
  - nouveaux composants plutôt que réécriture des existants quand c'est possible.
- **Code et commentaires en anglais**, comme l'amont ; tous les textes d'interface passent par l'i18n, et le français est la langue par défaut. Messages de commit en français, qui citent le ticket : `baillivetjulien/leohoot#<n>`.
- **Corrections d'intérêt général** (bugs de l'amont) : à faire dans un commit séparé, puis à proposer en PR à `mawoka-myblock/ClassQuiz`.

## Construire et déployer

- Un push sur `agence` construit les images (`.github/workflows/build_*.yml`, x86 uniquement) et les publie sur `ghcr.io/baillivetjulien/classquiz-{frontend,backend,caddy}:agence`. Chaque workflow ne se déclenche que si ses fichiers changent ; sinon, `gh workflow run build_frontend.yml --ref agence`.
- L'instance d'essai (`~/classquiz-essai`, `classquiz.orientation-normandie.fr`) utilise ces images : `docker compose pull && docker compose up -d`.
- Tests backend : `run_tests.sh` (pytest) ; frontend : `pnpm lint` et `pnpm check` dans `frontend/`. Captures d'écran avec Playwright et Chromium, disponibles via `~/espaceoim/node_modules` (`nvm use 22`).

## Reporter une mise à jour de l'amont

```bash
git fetch amont
git switch master && git merge --ff-only amont/master && git push origin master
git switch agence && git merge master   # résoudre les conflits, tester, puis pousser
git push origin agence
```

## Agent skills

### Issue tracker

Issues GitHub du dépôt privé `baillivetjulien/leohoot` (toujours `gh ... -R baillivetjulien/leohoot`), un jalon « Refonte » par étape, blocages en dépendances natives. Voir `~/Leohoot/docs/agents/issue-tracker.md`.

### Triage labels

`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. Voir `~/Leohoot/docs/agents/triage-labels.md`.

### Domain docs

Contexte unique, dans le dépôt de pilotage : `~/Leohoot/GLOSSARY.md` et `~/Leohoot/docs/adr/`. Voir `~/Leohoot/docs/agents/domain.md`.
