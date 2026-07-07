# Changelog

## Índice

- [Unreleased](#unreleased)
- [0.1.0](#010)

## Unreleased

- Corregida la alineación transversal del repositorio tras cierre de LAB 03A.
- Actualizado README raíz con árbol real de directorios, estado LAB 03A y regla de actualización transversal.
- Actualizado ROADMAP con subfases LAB 03A–LAB 03G.
- Actualizado `labs/README.md` con estados por laboratorio y rutas reales.
- Actualizado `book/README.md` y añadidos capítulos 02 y 03.
- Actualizados `docs/index.md`, `docs/learning_path.md` y `docs/publishing_model.md` para reflejar repositorio-libro.
- Alineadas evidencias documentales de LAB 03A con `lab03_m03_1883_console.log` y `lab03_static_gates.txt`.
- Añadido LAB 03A como matriz MQTT contra `test.mosquitto.org`, con baseline M03-1883 sin TLS.
- Añadido LAB 02 de identidad única de dispositivo con evidencias INSECURE/HARDENED.
- Añadido LAB 01 inicial: firmware inseguro/endurecido para ESP32-S3, documentación audit-grade y gates estáticos.

## 0.1.0

- Estructura inicial del repositorio público.
- Estándar audit-grade incorporado.
- Plantillas de laboratorios con README e índice.
- Licencias separadas para código y documentación.
- Gates estáticos iniciales.

## LAB 03 MQTT family restructure

### Changed

- `labs/lab03_mqtt` pasa a `labs/lab03_mqtt`.
- LAB 03 queda organizado como familia de sublaboratorios LAB 03A–LAB 03G.
- LAB 03A conserva la evidencia dry-run M03-1883 en su propio subdirectorio.

### Status

```text
CUMPLE:
- Estructura corregida antes de continuar con LAB 03B.
```
