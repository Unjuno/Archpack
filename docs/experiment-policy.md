# Archpack experiment policy

## 0. Purpose

Archpack should stay small and reviewable.

The main repository can contain the core, reviewed plugins, examples, tests, and documentation.

---

## 1. Core policy

The core remains:

```text
pack directory → file tree → explicit repair
```

New behavior should not enter the core unless it clearly belongs there.

---

## 2. Experiment rule

The default rule is:

```text
one problem → one small experiment → one review → keep, revise, or drop
```

Each experiment should focus on one feature or one problem.

---

## 3. Repository role

Use one repository for now.

The repository may contain:

- the core,
- reviewed plugins,
- plugin examples,
- plugin documentation,
- tests,
- small experiments under review.

A separate release repository or release fork is not needed unless this workflow becomes unmanageable.

---

## 4. Review questions

Before keeping an experiment, answer:

1. What concrete problem does it solve?
2. Can it be shown with a small example?
3. Does it preserve the core loop?
4. Does it add hidden complexity?
5. Does it have tests or clear manual checks?
6. Can it be documented briefly?
7. Can it be dropped later without damaging the core?

---

## 5. Keep criteria

A feature or plugin may remain only if:

- it solves a concrete problem,
- it is small enough to review,
- it has tests or clear checks,
- it does not make the core harder to explain,
- it does not force unrelated format changes,
- it can be documented briefly,
- it can be ignored or dropped later.

---

## 6. Future management tools

Possible future tools:

```text
archpack plugin list
archpack plugin disable <name>
archpack plugin remove <name>
archpack plugin doctor <name>
```

These are not core commands.

They should be added only after there are multiple reviewed plugins to manage.
