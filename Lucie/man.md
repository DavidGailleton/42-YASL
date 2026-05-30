# 📚 YASL — Cheat Sheet

> **YASL** *(Yasl is an Accounting Stack Language)* — Langage interprété basé sur un paradigme de **piles multiples inversées**.

---

## 🗂️ Table des matières

1. [Concept fondamental](#concept-fondamental)
2. [Sélecteur de pile](#sélecteur-de-pile)
3. [Modificateurs d'opération](#modificateurs-dopération)
4. [Push — Pousser des données](#push--pousser-des-données)
5. [Opérateurs](#opérateurs)
6. [Sous-ensembles & Fonctions](#sous-ensembles--fonctions)
7. [Structures de contrôle](#structures-de-contrôle)
8. [Bibliothèque standard](#bibliothèque-standard)
9. [Exemple complet](#exemple-complet)

---

## Concept fondamental

- Le runtime dispose de **10 piles** par défaut (numérotées `0` à `9`).
- Chaque pile est **inversée** : elle grandit vers le haut, et les opérations push/pop se font **par la base**.
- Les piles acceptent 4 types : `integer`, `string`, `float`, `list`.
- Les piles d'entrée et de sortie par défaut sont **toutes les deux `0`** au démarrage.

```
"Hello"   ← sommet
"World"
17
1.0
------    ← base (pop/push ici)
```

> ⚠️ Les opérations cross-type sont parfois permises (le type du premier élément prime). Si l'opération n'a pas de sens, le programme s'arrête avec une erreur.

---

## Sélecteur de pile

Syntaxe pour préciser les piles d'entrée et/ou de sortie :

```
<pile_entrée>::<opération>::<pile_sortie>
```

| Syntaxe | Signification |
|---|---|
| `2::+::3` | Prend depuis la pile 2, pousse le résultat sur la pile 3 |
| `::+::3` | Pile d'entrée courante → résultat sur la pile 3 |
| `2::+::` | Prend depuis la pile 2 → pile de sortie courante |
| `$$2::op::$$3` | Dépile la pile 2 pour obtenir le numéro de pile d'entrée ; idem pour la sortie |

> 📌 Un sélecteur sur un sous-ensemble ou une fonction s'applique à **toutes** les opérations à l'intérieur.

---

## Modificateurs d'opération

Ils se placent **avant** l'opération : `<modificateur><opération>`

| Modificateur | Syntaxe | Effet |
|---|---|---|
| Répétition | `#` | Dépile un entier strictement positif N, répète l'opération suivante N fois |
| Conservation | `%` | Garde les paramètres sur la pile au lieu de les dépiler |

> ⚠️ `%` n'affecte pas le modificateur `#`, ni les sélecteurs `$$`.

---

## Push — Pousser des données

Pousser une valeur = écrire la valeur seule sur une ligne.

| Type | Exemple | Remarque |
|---|---|---|
| Entier | `42` | Syntaxe style C disponible |
| Chaîne | `"hello"` | Entre guillemets doubles |
| Flottant | `3.14` | Séparé par un point |
| Liste | *(indirect)* | Impossible directement, utiliser `[]` |

---

## Opérateurs

### Arithmétique

| Op | Effet | Args |
|---|---|---|
| `+` | Addition | 2 |
| `-` | Soustraction | 2 |
| `*` | Multiplication | 2 |
| `/` | Division | 2 |
| `%` | Modulo | 2 |

### Pile

| Op | Effet | Args |
|---|---|---|
| `#` | **count** — pousse le nombre d'éléments de la pile d'entrée | 0 |
| `!` | **drop** — supprime le premier élément | 1 |
| `=` | **dup** — duplique le premier élément | 1 |
| `^` | **roll** — dépile N, puis fait tourner les N éléments suivants d'une position | 1+N |
| `!^` | **unroll** — inverse du roll | 1+N |

### Comparaison

| Op | Signification |
|---|---|
| `<` | Inférieur à |
| `>` | Supérieur à |
| `<=` | Inférieur ou égal |
| `>=` | Supérieur ou égal |
| `==` | Égal |
| `!=` | Différent |

> Ces opérateurs consomment **2 arguments** sur la pile.

### Logique (booléen)

| Op | Effet | Args |
|---|---|---|
| `&&` | AND logique | 2 |
| `\|\|` | OR logique | 2 |
| `~~` | NOT logique | 1 |

### Binaire (bit à bit)

| Op | Effet | Args |
|---|---|---|
| `&` | AND binaire | 2 |
| `\|` | OR binaire | 2 |
| `~` | NOT binaire | 1 |
| `<<` | Décalage gauche (2e arg décalé de 1er arg fois) | 2 |
| `>>` | Décalage droit | 2 |

### Listes

| Op | Effet | Args |
|---|---|---|
| `[]` | **list** — crée une liste avec les N éléments suivants (N = premier arg) | 1+N |
| `][` | **unlist** — explose une liste sur la pile, pousse le nombre d'éléments créés | 1 |
| `[#]` | **list count** — pousse le nombre d'éléments dans la liste (premier arg) | 1 |
| `]#[` | **get item** — extrait l'élément à l'index (1er arg) dans la liste (2e arg) | 2 |

---

## Sous-ensembles & Fonctions

### Sous-ensemble *(subset)*

```yasl
( <opération> [<opération> ...] )
```

Groupe d'opérations formant une seule opération dans leur portée.

### Fonction

```yasl
{ <opération> [<opération> ...] } nom_fonction
```

Définit une fonction réutilisable. On l'appelle ensuite simplement par son nom :

```yasl
nom_fonction
```

> 📌 Une fonction ne peut être appelée que dans la même portée (*scope*) où elle est définie.

---

## Structures de contrôle

### Condition — `?`

```yasl
? <opération>
? <opération> : <opération>
```

- Dépile le premier argument (booléen).
- Si **vrai** → exécute la 1re opération.
- Si **faux** et que `:` est présent → exécute la 2e opération.

### Boucle — `@`

```yasl
@ <opération>
```

Répète l'opération **tant que** le premier argument sur la pile est **vrai** (non-faux).

---

## Bibliothèque standard

| Fonction | Effet |
|---|---|
| `print` | Affiche le premier élément de la pile |
| `read` | Lit une ligne depuis l'entrée standard *(ne fonctionne pas en mode interactif)* |
| `eval` | Parse et exécute le premier argument (string) comme du code YASL |
| `exit` | Termine le programme, le premier argument est le code de retour shell |

---

## Exemple complet

```yasl
#!yasl

#!                // Supprime les arguments de ligne de commande (drop répété)

"YASL\n"
"my name is "
"Hello, "
#                 // Compte les éléments sur la pile (→ 3)
#print            // Répète print 3 fois → affiche les 3 chaînes
```

**Exécution pas à pas :**

| Étape | Pile (bas → sommet) |
|---|---|
| Après les 3 push | `"YASL\n"` / `"my name is "` / `"Hello, "` |
| `#` (count) | Pousse `3` |
| `#print` | Affiche `"Hello, "`, puis `"my name is "`, puis `"YASL\n"` |

---

## 🔧 Invocation

```bash
yasl mon_script.yasl
# ou shebang dans le fichier :
#!/usr/bin/env yasl
```

---

*Cheat sheet basée sur le manuel BSD — YASL, March 4, 2022.*