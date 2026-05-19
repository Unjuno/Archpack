# Archpack experiment policy

## 0. Purpose

Archpack should avoid growing into a large unclear tool.

The MVP repository is a validation space. It exists to test the core idea and candidate features.

The release body may live in a separate fork or a separate repository.

The purpose is to allow many experiments without forcing every experiment into the release version.

---

## 1. Core policy

Do not treat the MVP repository as the final product boundary.

Use it as a feature validation environment.

The default rule is:

```text
one problem → one experiment → one review → promote or discard
```

Only features that prove they belong in the release body should be promoted.

---

## 2. Repository roles

### 2.1 MVP repository

The MVP repository is used to:

- prove the core loop,
- keep validation files and examples,
- test candidate plugins,
- collect user-story-map problems,
- compare one-feature experiments.

It may become messy during exploration, as long as the mess is intentional and reviewable.

### 2.2 Release repository or release fork

The release body is used to:

- hold only accepted features,
- stay small and understandable,
- keep the public workflow stable,
- avoid speculative feature growth,
- provide a clean implementation for actual users.

The release body can be a separate fork or a separate repository.
The exact choice is not decided yet.

---

## 3. Experiment unit

Each experiment should focus on exactly one feature or one problem.

Good examples:

- Try `AGENTS.md` generation only.
- Try effective inherited `AGENTS.md` generation only.
- Try generated-file drift checks only.
- Try clean-up of generated files only.
- Try a simple reference check only.
- Try a static network-call detector only.

Bad examples:

- Add AGENTS generation, drift checks, repair changes, clean-up, and network checks together.
- Redesign the pack format while adding a new feature.
- Add a feature without a concrete observed problem.

---

## 4. Recommended workflow

```text
MVP validation repo
→ concrete problem from user story map
→ one-feature fork, branch, or small repo
→ smallest experiment
→ review behavior and complexity
→ promote to release body, revise, or discard
```

The experiment should remain isolated until reviewed.

---

## 5. Promotion criteria

A feature may be promoted to the release body only if:

- it solves a repeated or important user problem,
- it has a small example,
- it has tests or clear manual verification steps,
- it does not force unrelated schema changes,
- it does not make the core workflow harder to explain,
- it can be documented briefly,
- it fits the current release scope.

If these are not true, the experiment should remain outside the release body.

---

## 6. Review questions

Before promoting an experiment, answer:

1. What concrete problem does it solve?
2. Can the problem be reproduced with a small example?
3. Does the feature keep the pack format understandable?
4. Does it preserve the small core loop?
5. Does it introduce hidden complexity?
6. Can it be tested?
7. Can it be documented briefly?
8. Should this be promoted, revised, or discarded?

---

## 7. Discarding is allowed

Discarding an experiment is not a failure.

Discarded experiments are useful when they reveal:

- the feature is too complex,
- the problem is not Archpack's responsibility,
- the idea needs a different design,
- the feature should stay as an external add-on,
- the feature is useful only for a narrow project type.

---

## 8. Relationship to user story mapping

The user story map identifies concrete problems.

This experiment policy defines how candidate solutions are tested and promoted.

```text
user story map
→ problem issue
→ one-feature experiment
→ review
→ release body or discard
```

---

## 9. First rule

Do not expand the release body before the core MVP works.

The core MVP remains:

```text
pack directory → file tree → explicit repair
```

After that, plugin experiments may be generated in quantity, but only reviewed and accepted behavior should enter the release body.
