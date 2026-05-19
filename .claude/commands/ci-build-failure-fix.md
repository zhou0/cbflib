---
name: ci-build-failure-fix
description: Workflow command scaffold for ci-build-failure-fix in cbflib.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /ci-build-failure-fix

Use this workflow when working on **ci-build-failure-fix** in `cbflib`.

## Goal

Fixes CI build failures by updating build scripts, resolving deprecations, and addressing platform/toolchain issues.

## Common Files

- `CMakeLists.txt`
- `examples/convert_image.c`
- `.github/workflows/cmake-multi-platform.yml`
- `Makefile_old`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Identify cause of CI build failure (e.g., deprecated function, missing library, optional toolchain component).
- Update source code to replace deprecated or problematic functions (e.g., mktemp → mkstemp in examples/convert_image.c).
- Modify CMakeLists.txt to adjust build options, add or remove dependencies, and make components optional as needed.
- Explicitly link required libraries (e.g., libm) in CMakeLists.txt to resolve linkage errors.
- Update CI workflow files (e.g., .github/workflows/cmake-multi-platform.yml) to ensure required tools are installed on all platforms.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.