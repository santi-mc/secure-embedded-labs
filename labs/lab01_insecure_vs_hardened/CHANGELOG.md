# LAB 01 — Changelog

## Índice

- [Unreleased](#unreleased)
- [0.1.0](#010)

## Unreleased

- Añadida captura automática de evidencias de consola para `INSECURE` y `HARDENED`.
- Añadida validación automática de perfil observado en logs capturados.
- Añadida captura automática de gates estáticos.
- Añadida captura automática del scanner de secretos.
- Actualizada documentación de evidencias, test plan y trazabilidad.
- Corregido el buffer de línea de la consola para no tratar cada carácter USB Serial/JTAG como comando independiente.
- Corregido spam de `console_warning` cuando `stdin` no entrega una línea disponible todavía.

## 0.1.0

- Añadido firmware ESP-IDF para ESP32-S3.
- Añadidos perfiles `INSECURE` y `HARDENED`.
- Añadida consola USB Serial/JTAG por stdio.
- Añadidas vulnerabilidades intencionadas y mitigaciones.
- Añadidos documentos audit-grade del laboratorio.
- Añadidos gates estáticos y scanner de logs.
