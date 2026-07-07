# Roadmap

## Índice

- [Visión](#visión)
- [Fase 0 — Fundación](#fase-0--fundación)
- [Fase 1 — Laboratorios base](#fase-1--laboratorios-base)
- [Fase 2 — Seguridad conectada](#fase-2--seguridad-conectada)
- [Fase 3 — Plataforma segura](#fase-3--plataforma-segura)
- [Fase 4 — Publicación y libro](#fase-4--publicación-y-libro)
- [Criterio de cierre](#criterio-de-cierre)
- [Regla de avance](#regla-de-avance)

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

- [x] LAB 03A — M03-1883 / MQTT TCP sin TLS y sin autenticación, baseline inseguro dry-run.
- [ ] LAB 03B — M03-1884 / MQTT TCP sin TLS con usuario/password.
- [ ] LAB 03C — M03-8883 y M03-8886 / MQTT TLS sin autenticación.
- [ ] LAB 03D — M03-8885 / MQTT TLS con usuario/password.
- [ ] LAB 03E — M03-8884 / MQTT mTLS con certificado cliente.
- [ ] LAB 03F — M03-8887 / certificado expirado, rechazo obligatorio.
- [ ] LAB 03G — MQTT over WebSockets 8080, 8081, 8090 y 8091.
- [ ] LAB 04 — OTA firmada con rollback.
- [ ] LAB 05 — Configuración remota segura.

Estado de cierre parcial:

```text
LAB 03A: CUMPLE como dry-run contractual con evidencia de consola M03-1883 y gates estáticos.
LAB 03 conexión real: NO VALIDADO.
LAB 03 TLS/mTLS/WebSockets: PENDIENTE.
```

## Fase 3 — Plataforma segura

- [ ] LAB 06 — Hardening de interfaces físicas.
- [ ] LAB 07 — SBOM y trazabilidad de release.
- [ ] LAB 08 — Secure Boot + Flash Encryption.
- [ ] LAB 09 — Gateway seguro multi-interfaz.

## Fase 4 — Publicación y libro

- [x] Iniciar estructura `book/`.
- [x] Añadir capítulo 01 alineado con LAB 01.
- [x] Añadir capítulo 02 alineado con LAB 02.
- [x] Añadir capítulo 03 alineado con LAB 03A.
- [ ] Revisar licencia documental.
- [ ] Preparar versión publicable.
- [ ] Revisión editorial completa.

## Criterio de cierre

Un laboratorio solo se marca como cerrado cuando dispone de:

- firmware o artefacto técnico versionado;
- documentación con índice;
- plan de pruebas;
- evidencias reales o declaración explícita `NO VALIDADO`;
- gates ejecutados y documentados;
- actualización de README raíz, roadmap, changelog, libro e índices cuando aplique;
- commit trazable.

## Regla de avance

No se abre una nueva fase de laboratorio si la fase anterior deja incoherencias en documentación transversal, evidencias, gates o libro.
