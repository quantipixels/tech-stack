# Kotlin and Spring Boot

Use `java-spring.md` for Spring Boot and Spring Modulith. This file adds only the
Kotlin differences.

### detekt — required (main Kotlin linter)
setting: `buildUponDefaultConfig = true`; a baseline only for old code
verified: 2026-10-06 · https://detekt.dev

### ktlint through Spotless — required
setting: `kotlin { ktlint() }`; `spotlessCheck` in the gate
verified: 2026-10-06 · https://pinterest.github.io/ktlint/

### SpotBugs — optional
why: works on bytecode, so it sees Kotlin, but Kotlin-generated code adds noise
verified: 2026-10-06 · https://spotbugs.github.io

### PMD, Checkstyle, Error Prone — required for Java sources only
why: Checkstyle and Error Prone read Java source only; PMD has few Kotlin rules. Keep them for Java files in mixed projects; detekt covers Kotlin
verified: 2026-10-06 · https://pmd.github.io
