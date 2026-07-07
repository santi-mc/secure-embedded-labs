# Ruta de aprendizaje

## Índice

- [Nivel 1 — Fundamentos](#nivel-1--fundamentos)
- [Nivel 2 — Seguridad conectada](#nivel-2--seguridad-conectada)
- [Nivel 3 — Plataforma segura](#nivel-3--plataforma-segura)
- [Nivel 4 — Producto y comunidad](#nivel-4--producto-y-comunidad)
- [Estados](#estados)

## Nivel 1 — Fundamentos

- LAB 01 — Firmware inseguro vs firmware endurecido. Estado: `CUMPLE`.
- LAB 02 — Identidad única de dispositivo. Estado: `CUMPLE`.

## Nivel 2 — Seguridad conectada

- LAB 03 — Matriz MQTT contra `test.mosquitto.org`.
  - LAB 03A — M03-1883 sin TLS y sin autenticación. Estado: `CUMPLE` como dry-run.
  - LAB 03B — M03-1884 con usuario/password sin TLS. Estado: `PENDIENTE`.
  - LAB 03C–03G — TLS, mTLS, certificado expirado y WebSockets. Estado: `PENDIENTE`.
- LAB 04 — OTA firmada con rollback. Estado: `PENDIENTE`.
- LAB 05 — Configuración remota segura. Estado: `PENDIENTE`.

## Nivel 3 — Plataforma segura

- LAB 06 — Hardening de interfaces físicas.
- LAB 07 — SBOM y trazabilidad de release.
- LAB 08 — Secure Boot + Flash Encryption.
- LAB 09 — Gateway seguro multi-interfaz.

## Nivel 4 — Producto y comunidad

- LAB 10 — Mini PSIRT de producto.
- Capítulos públicos.
- Publicación de releases educativas.

## Estados

```text
CUMPLE:
- LAB 01.
- LAB 02.
- LAB 03A dry-run.

NO VALIDADO:
- LAB 03 conexión real MQTT.
- LAB 03 TLS/mTLS/WebSockets.

PENDIENTE:
- LAB 03B en adelante.
- LAB 04 a LAB 10.
```
