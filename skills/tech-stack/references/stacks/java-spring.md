# Java and Spring Boot

### Spring Boot — default
verified: 2026-10-06 · https://spring.io/projects/spring-boot

### Spring Modulith — default for module boundaries
setting: one test that calls `ApplicationModules.of(App.class).verify()`
why: the Spring equivalent of Elixir Boundary; fails on reaches into another module's internals
verified: 2026-10-06 · https://spring.io/projects/spring-modulith

### Spotless with google-java-format, AOSP style — required
setting: `googleJavaFormat().aosp()`; `spotlessCheck` in the gate
why: preferred style (4-space AOSP)
verified: 2026-10-06 · https://github.com/diffplug/spotless

### Error Prone — required
setting: chosen checks raised with `-Xep:<Check>:ERROR`
verified: 2026-10-06 · https://errorprone.info/docs/flags

### SpotBugs with FindSecBugs — required
setting: exclude filter only for reviewed false positives, each with a reason
verified: 2026-10-06 · https://spotbugs.github.io

### PMD — required
setting: bug rules plus `CyclomaticComplexity` and `CognitiveComplexity`
verified: 2026-10-06 · https://pmd.github.io

### Checkstyle — required
setting: fails the build on findings; rules that Spotless already formats are off
verified: 2026-10-06 · https://checkstyle.org

### Spring Boot scheduler capacity and shutdown — default (over the one-thread pool)
setting: for Boot's auto-configured `ThreadPoolTaskScheduler`, set `spring.task.scheduling.pool.size` to at least the number of independent scheduled jobs sharing it; set `spring.task.scheduling.thread-name-prefix=scheduled-jobs-`, `spring.task.scheduling.shutdown.await-termination=true` and `spring.task.scheduling.shutdown.await-termination-period` to the project's shutdown budget (for example `60s`).
why: five scheduled jobs in a Spring Boot backend shared one thread, so a slow job delayed the others; explicit capacity and bounded shutdown waiting avoid that configuration.
verified: 2026-10-24 · https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html · https://docs.spring.io/spring-boot/appendix/application-properties/index.html#application-properties.core.spring.task.scheduling.pool.size · https://docs.spring.io/spring-framework/reference/integration/scheduling.html#scheduling-annotation-support-scheduled

This is a conservative project sizing rule, not a framework requirement. Revisit capacity and downstream limits whenever jobs are added; a test can count `@Scheduled` methods assigned to this scheduler and require the pool size to cover them (account for repeatable schedules and dynamic registrations separately). Boot's platform-thread scheduler defaults to one thread. With virtual threads enabled, Boot uses `SimpleAsyncTaskScheduler`, which ignores pooling properties; assess that scheduler separately.

### Spring Security account-status checks — default (over exceptions from user lookup)
setting: return `UserDetails` from `loadUserByUsername` with accurate `isAccountNonLocked`, `isEnabled`, `isAccountNonExpired` and `isCredentialsNonExpired` flags. For custom pre-authentication rules, configure a `UserDetailsChecker` through `setPreAuthenticationChecks`; preserve the standard status checks when replacing that checker.
why: throwing `LockedException` during lookup made a backend unwrap `InternalAuthenticationServiceException` and prevented its provider pre-check from running.
verified: 2026-10-24 · https://github.com/spring-projects/spring-security/blob/6.5.x/core/src/main/java/org/springframework/security/authentication/dao/DaoAuthenticationProvider.java#L106-L128 · https://github.com/spring-projects/spring-security/blob/6.5.x/core/src/main/java/org/springframework/security/authentication/dao/AbstractUserDetailsAuthenticationProvider.java

In Spring Security 6.5.x, `retrieveUser` rethrows `UsernameNotFoundException` and `InternalAuthenticationServiceException` and wraps other `Exception`s. Pre-checks run after retrieval, outside that wrapper: locked, disabled and expired accounts produce their status exceptions directly. Credential expiry is checked after credential validation. Map suspended/deleted states to flags according to the project's account policy; lookup should not throw account-status exceptions.

Java and Kotlin entries are a starting list from QP's stack. Add settings
from the first real project; do not invent them ahead of use.
