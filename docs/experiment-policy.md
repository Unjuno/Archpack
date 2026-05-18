# Archpack experiment policy

## 0. Purpose

Archpack should avoid growing into a large unclear tool.

After the MVP, new ideas should be explored as small isolated experiments before they are considered for the main project.

The default rule is:

```text
one problem → one experiment → one review → accept, revise, or reject
```

---

## 1. Principle

Do not add a feature to the main project just because it sounds useful.

A feature must first prove that it solves a concrete problem without making Archpack harder to understand.

Main should stay small.
Experiments can be many.

---

## 2. Experiment unit

Each experiment should focus on exactly one feature or one problem.

Good examples:

- Try generated-file drift checks only.
- Try clean-up of generated `AGENTS.md` only.
- Try a simple reference check only.
- Try a static network-call detector only.

Bad examples:

- Add drift checks, repair, clean-up, and network checks together.
- Redesign the pack format while adding a new feature.
- Add a feature without a concrete observed problem.

---

## 3. Recommended workflow

```text
MVP main branch
→ create issue from a concrete problem
→ create one-feature fork or branch
→ implement the smallest experiment
→ review generated behavior and complexity
→ decide whether to merge, revise, or discard
```

The experiment can live in a fork or a separate branch.

The important point is that it must remain isolated from main until reviewed.

---

## 4. Review questions

Before merging an experiment, answer:

1. What concrete problem does it solve?
2. Can the problem be reproduced with a small example?
3. Does the feature keep the pack format understandable?
4. Does it preserve the small MVP loop?
5. Does it introduce hidden complexity?
6. Can it be tested in CI?
7. Can it be documented briefly?
8. Should this be merged, revised, or rejected?

---

## 5. Merge criteria

An experiment may be merged only if:

- it solves a repeated or important user problem,
- it has a small example,
- it has tests or clear manual verification steps,
- it does not force unrelated schema changes,
- it does not make the core workflow harder to explain.

If these are not true, the experiment should remain outside main.

---

## 6. Rejection is allowed

Rejecting an experiment is not a failure.

Rejected experiments are useful when they reveal:

- the feature is too complex,
- the problem is not Archpack's responsibility,
- the idea needs a different design,
- the feature should stay as an external add-on.

---

## 7. Relationship to user story mapping

The user story map identifies concrete problems.

This experiment policy defines how candidate solutions are tested.

```text
user story map → problem issue → one-feature experiment → review → main or reject
```

---

## 8. First rule

Do not expand Archpack before the MVP works.

The MVP remains:

```text
pack → file tree → local AGENTS.md → effective AGENTS.md
```
