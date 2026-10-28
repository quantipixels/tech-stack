# Spring Boot layout (Java and Kotlin)

```
apps/<service>/
  src/main/<lang>/<base>/
    <module>/                Spring Modulith application module, package-by-feature
      <Module>Api.<ext>      the module's public API (others call only this package level)
      internal/              entities, repositories, services private to the module
      web/                   controllers and DTOs for this module
    Application.<ext>
  src/main/resources/db/migration/   Flyway, forward-only
  src/test/<lang>/<base>/<module>/   module tests (@ApplicationModuleTest)
  src/test/<lang>/<base>/ModularityTest.<ext>   ApplicationModules.verify()
```

## Rules
- Package by feature, not by layer (no top-level `controllers/`, `services/`, `repositories/`).
- Other modules use only a module's top-level package; `internal` stays private (Spring Modulith verifies this).
- Cross-module side effects inside one transaction go through the owner's API; asynchronous ones through Spring Modulith events with the event publication registry.
- Flyway for migrations by default; confirm it on the first Spring project.
