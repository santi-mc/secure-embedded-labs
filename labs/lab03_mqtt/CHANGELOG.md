# Changelog — LAB 03 MQTT

## Índice

- [Unreleased](#unreleased)

## Unreleased

### Changed

- LAB 03 deja de representarse como `lab03_mqtt` y pasa a `lab03_mqtt`.
- La matriz MQTT se reorganiza como familia de sublaboratorios independientes.
- LAB 03A conserva la evidencia dry-run de M03-1883 en su propio subdirectorio.

### Added

- Estructura `lab03a` a `lab03g` para cubrir todos los escenarios MQTT del broker de pruebas.
- Directorio `common/` para contratos y reutilización explícita entre sublaboratorios.

### Status

```text
CUMPLE:
- Reorganización estructural de LAB 03 como familia MQTT.
- LAB 03A queda aislado como sublaboratorio.

NO VALIDADO:
- Gates locales tras aplicar la migración, hasta ejecutar las herramientas.
```
