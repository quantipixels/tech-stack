# Java and Spring Boot

### Spring Boot — default
verified: pending · https://spring.io/projects/spring-boot

### Spring Modulith — default for module boundaries
setting: one test that calls `ApplicationModules.of(App.class).verify()`
why: the Spring equivalent of Elixir Boundary; fails on reaches into another module's internals
verified: pending · https://spring.io/projects/spring-modulith

### Spotless with google-java-format, AOSP style — required
setting: `googleJavaFormat().aosp()`; `spotlessCheck` in the gate
why: preferred style (4-space AOSP)
verified: pending · https://github.com/diffplug/spotless

### Error Prone — required
setting: chosen checks raised with `-Xep:<Check>:ERROR`
verified: pending · https://errorprone.info/docs/flags

### SpotBugs with FindSecBugs — required
setting: exclude filter only for reviewed false positives, each with a reason
verified: pending · https://spotbugs.github.io

### PMD — required
setting: bug rules plus `CyclomaticComplexity` and `CognitiveComplexity`
verified: pending · https://pmd.github.io

### Checkstyle — required
setting: fails the build on findings; rules that Spotless already formats are off
verified: pending · https://checkstyle.org

Java and Kotlin entries are a starting list from QP's stack. Add settings
from the first real project; do not invent them ahead of use.
