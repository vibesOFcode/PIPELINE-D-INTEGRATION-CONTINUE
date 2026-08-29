# 🚀 Pipeline d’Intégration Continue — CI/CD

Projet de mise en place d’une **pipeline d’intégration continue** permettant d’automatiser le build, les tests et les contrôles qualité d’un projet.

## 🎯 Objectifs

* Automatiser les tests et validations
* Détecter rapidement les erreurs
* Mettre en pratique les principes **CI/CD & DevOps**
* Garantir une intégration fiable du code

## 🛠️ Technologies

`Git` · `GitLab CI/CD` · `YAML` · `Bash` · `Tests automatisés`

## 📁 Structure

```text
ci-td/
├── .gitlab-ci.yml
├── src/
├── tests/
└── README.md
```

## 🚀 Installation

```bash
git clone https://devops.telecomste.fr/aziz.aya/ci-td.git
cd ci-td
```

Installer ensuite les dépendances selon la technologie utilisée.

## 🧪 Tests

Exécuter les tests localement avant de pousser les modifications :

```bash
# Exemple
npm test
```

La pipeline exécute automatiquement les étapes définies dans `.gitlab-ci.yml`.

## 🔄 Pipeline

```text
Push → Build → Test → Quality → Deploy
```

## 🌿 Workflow Git

```bash
git checkout -b feature/ma-feature
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin feature/ma-feature
```

Créer ensuite une **Merge Request** pour intégrer les changements.

## 📈 Évolutions

* [ ] Analyse qualité du code
* [ ] Docker
* [ ] Déploiement automatisé
* [ ] DevSecOps

## 👤 Auteur

**Aziz Aya** — Projet orienté **DevOps / CI/CD / Automation**.
