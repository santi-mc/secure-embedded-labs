# Roadmap

## Índice

- [Visión](#visión)
- [Fase 0 — Fundación](#fase-0--fundación)
- [Fase 1 — Laboratorios base](#fase-1--laboratorios-base)
- [Fase 2 — Seguridad conectada](#fase-2--seguridad-conectada)
- [Fase 3 — Plataforma segura](#fase-3--plataforma-segura)
- [Fase 4 — Publicación y libro](#fase-4--publicación-y-libro)
- [Criterio de cierre](#criterio-de-cierre)

## Visión

Crear una ruta abierta para aprender ciberseguridad embebida con laboratorios reproducibles, auditables y orientados a evidencia.

## Fase 0 — Fundación

- [x] Estructura base del repositorio.
- [x] Estándar audit-grade incorporado.
- [x] Plantilla de laboratorio con README e índice.
- [x] Política de contribución.
- [x] Política de seguridad.
- [x] Licencias separadas para código y documentación.

## Fase 1 — Laboratorios base

- [x] LAB 01 — Firmware inseguro vs firmware endurecido.
- [x] LAB 02 — Identidad única de dispositivo.

Estado de cierre:

```text
LAB 01: CUMPLE con evidencias automáticas de consola, secret scan y gates.
LAB 02: CUMPLE con evidencias automáticas de consola, validadores de identidad y gates.
```

## Fase 2 — Seguridad conectada

- [ ] LAB 03 — MQTT seguro con TLS.
- [ ] LAB 04 — OTA firmada con rollback.
- [ ] LAB 05 — Configuración remota segura.

## Fase 3 — Plataforma segura

- [ ] LAB 06 — Hardening de interfaces físicas.
- [ ] LAB 07 — SBOM y trazabilidad de release.
- [ ] LAB 08 — Secure Boot + Flash Encryption.
- [ ] LAB 09 — Gateway seguro multi-interfaz.

## Fase 4 — Publicación y libro

- [ ] Normalizar capítulos en `book/`.
- [ ] Revisar licencia documental.
- [ ] Preparar versión publicable.

## Criterio de cierre

Un laboratorio solo se marca como cerrado cuando dispone de:

- firmware o artefacto técnico versionado;
- documentación con índice;
- plan de pruebas;
- evidencias reales o declaración explícita `NO VALIDADO`;
- gates ejecutados y documentados;
- commit trazable.
