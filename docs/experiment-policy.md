# Archpack experiment policy

## 0. Purpose

Archpack should avoid growing into a large unclear tool.

The project does not need a separate release repository or release fork at this stage.

The main repository can contain the MVP, reviewed plugins, experiments, examples, and documentation, as long as accepted behavior remains reviewable and removable.

The purpose is:

```text
try small features → review them → keep useful ones → remove bad or unnecessary ones
```

---

## 1. Core policy

Archpack should grow through reviewed changes, not through uncontrolled feature accumulation.

The default rule is:

```text
one problem → one experiment → one review → keep, revise, or remove
```

A plugin or feature may enter the repository only after review.

A plugin or feature may also be removed later if it becomes unnecessary, too complex, unsafe, or out of scope.

---

## 2. Repository role

Use one repository for now.

The repository is used to:

- prove the core loop,
- keep validation files and examples,
- test candidate plugins,
- collect user-story-map problems,
- review plugin experiments,
- keep accepted plugins,
- remove features that should not remain.

A separate release repository or release fork is not needed unless the single-repository workflow becomes unmanageable.

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
concrete problem from user story map
→ one-feature branch or small experiment
→ implementation with tests
→ review behavior and complexity
→ keep, revise, or remove
```

A fork is optional.

A separate repository is optional.

The important requirement is that the experiment remains small enough to review.

---

## 5. Keep criteria

A feature or plugin may remain in the repository only if:

- it solves a repeated or important user problem,
- it has a small example,
- it has tests or clear manual verification steps,
- it does not force unrelated schema changes,
- it does not make the core workflow harder to explain,
- it can be documented briefly,
- it can be disabled, ignored, or removed when no longer needed.

If these are not true, the feature should be revised or removed.

---

## 6. Review questions

Before keeping an experiment, answer:

1. What concrete problem does it solve?
2. Can the problem be reproduced with a small example?
3. Does the feature keep the pack format understandable?
4. Does it preserve the small core loop?
5. Does it introduce hidden complexity?
6. Can it be tested?
7. Can it be documented briefly?
8. Can it be removed without damaging the core?
9. Should this be kept, revised, or removed?

---

## 7. Removal is allowed

Removing a feature is not a failure.

Removal is useful when it reveals:

- the feature is too complex,
- the problem is not Archpack's responsibility,
- the idea needs a different design,
- the feature should stay external,
- the feature is useful only for a narrow project type,
- the feature increases maintenance cost more than user value.

---

## 8. Future removal tooling

Archpack may later include tools that make removal safer.

Possible future tools:

```text
archpack plugin list
archpack plugin disable <name>
archpack plugin remove <name>
archpack plugin doctor <name>
```

These are not core MVP commands.

They should be added only after there are real reviewed plugins to manage.

---

## 9. Relationship to user story mapping

The user story map identifies concrete problems.

This experiment policy defines how candidate solutions are tested, reviewed, kept, or removed.

```text
user story map
→ problem issue
→ one-feature experiment
→ review
→ keep, revise, or remove
```

---

## 10. First rule

Do not expand the core before the core MVP remains stable.

The core MVP remains:

```text
pack directory → file tree → explicit repair
```

After that, plugin experiments may be generated in quantity, but they must remain reviewable and removable.
