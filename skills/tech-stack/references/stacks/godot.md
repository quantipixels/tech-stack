# Godot (GDScript)

### Godot via mise — required
setting: `godot = "4.5.1-stable"`; checked on local macOS and `ubuntu-latest` CI in Tomiwa
why: pin the same engine locally and in CI
verified: 2026-10-07 · https://github.com/quantipixels/tomiwa/blob/ori/mise.toml

### gdscript-formatter — required
setting: `"github:GDQuest/godot-gdscript-formatter-tree-sitter" = { version = "0.18.1", exe = "gdscript-formatter" }`; format check with `--check`, lint with `lint`
why: one pinned formatter and linter for GDScript
verified: 2026-10-07 · https://github.com/GDQuest/GDScript-formatter

### Strict GDScript warnings — required
setting: `gdscript/warnings/<rule>=2` in `[debug]`: `untyped_declaration`, `unsafe_property_access`, `unsafe_method_access`, `unsafe_cast`, `unsafe_call_argument`, `return_value_discarded`
why: new and edited code must pass typed access and discarded-return checks; hash-locked legacy exemptions live in the gate
verified: 2026-10-07 · https://github.com/quantipixels/tomiwa/blob/ori/_scripts/check.py

### Headless gate — required (over `--check-only --script`)
setting: `--import`, then a SceneTree runner that defers script loads until autoloads initialize, a headless regression scene, and boot with `--quit-after 120`
why: `--check-only --script` gives false autoload errors; boot alone misses script and regression failures
verified: 2026-10-07 · https://github.com/quantipixels/tomiwa/blob/ori/_scripts/check.py

### Rendered visual proof — required for visual changes
setting: capture with `--write-movie` and `--fixed-fps`; inspect the rendered frames
why: headless checks missed particle and camera defects in Tomiwa
verified: 2026-10-07 · https://docs.godotengine.org/en/4.5/tutorials/animation/creating_movies.html

### Pixel-art display — default
setting: `display/window/stretch/mode="viewport"`, `display/window/stretch/aspect="keep"`, `display/window/stretch/scale_mode="integer"`
why: keep the aspect ratio and whole pixels when resizing
verified: 2026-10-07 · https://docs.godotengine.org/en/4.5/tutorials/rendering/multiple_resolutions.html

### Fullscreen keys — default
setting: bind F11, Alt+Enter, and Cmd+Ctrl+F; macOS takes F11 for a system action
why: give macOS players a fullscreen key the OS does not take
verified: pending · https://docs.godotengine.org/en/4.5/tutorials/inputs/inputevent.html

## Reference implementation
Private `quantipixels/tomiwa`: `mise.toml`, `_scripts/check.py`, `lefthook.yml`, `.github/workflows/quality.yml`. Hooks and CI call `mise run check`; read these files before copying settings.
