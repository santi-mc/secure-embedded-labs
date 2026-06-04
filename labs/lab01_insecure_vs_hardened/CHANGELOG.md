# LAB 01 — Changelog

## Índice

- [Unreleased](#unreleased)
- [0.1.0](#010)

## Unreleased

- Corregido el buffer de línea de la consola para no tratar cada carácter USB Serial/JTAG como comando independiente.
- Corregido spam de `console_warning` cuando `stdin` no entrega una línea disponible todavía.
- Pendiente capturar evidencia real en hardware ESP32-S3.

## 0.1.0

- Añadido firmware ESP-IDF para ESP32-S3.
- Añadidos perfiles `INSECURE` y `HARDENED`.
- Añadida consola USB Serial/JTAG por stdio.
- Añadidas vulnerabilidades intencionadas y mitigaciones.
- Añadidos documentos audit-grade del laboratorio.
- Añadidos gates estáticos y scanner de logs.
