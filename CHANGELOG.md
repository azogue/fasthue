# Changelog

## [v1.2.1](https://github.com/azogue/fasthue/tree/v1.2.1) (2021-05-09)

[Full Changelog](https://github.com/azogue/fasthue/compare/v1.2.0...v1.2.1)

**Changes:**

- Add "iot_class" to integration manifest

## [v1.2.0](https://github.com/azogue/fasthue/tree/v1.2.0) (2021-03-08)

[Full Changelog](https://github.com/azogue/fasthue/compare/v1.1.1...v1.2.0)

**Changes:**

- Implement "Options" menu to change update interval globally anytime
- Modified scan intervals by calling the `fasthue.set_update_interval` service won't persist a HA restart, going back to the global value stored in the integration config (BREAKING CHANGE)
- Add Norwegian (from @hwikene), update README (from @huubeikens), remove some warning log messages

## [v1.1.1](https://github.com/azogue/fasthue/tree/v1.1.1) (2020-05-10)

[Full Changelog](https://github.com/azogue/fasthue/compare/v1.1.0...v1.1.1)

**Changes:**

- Add Italian (from @sagitt), Polish (from @nepozs) and Spanish translations

## [v1.1.0](https://github.com/azogue/fasthue/tree/v1.1.0) (2020-04-28)

[Full Changelog](https://github.com/azogue/fasthue/compare/v1.0.0...v1.1.0)

**Changes:**

- Rename translations folder to follow HA Core changes for HA >= v0.109.
- Add Github Action to validate for HACS
- Add Github Action to validate for HA Core (with `hassfest`)

## [v1.0.0](https://github.com/azogue/fasthue/tree/v1.0.0) (2020-04-17)

**Initial version**
