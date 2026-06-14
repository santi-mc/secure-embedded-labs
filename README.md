# Secure Embedded Labs

Repositorio público de laboratorios auditables para aprender ciberseguridad aplicada a microcontroladores, firmware embebido e IoT.

El proyecto combina dos objetivos:

1. **Aprendizaje técnico**: comprender seguridad en firmware mediante laboratorios reproducibles sobre microcontroladores reales.
2. **Conocimiento abierto**: construir una base pública reutilizable que pueda evolucionar hacia documentación extensa o un libro con licencia abierta.

> Un laboratorio puede ser inseguro de forma intencionada; nunca puede ser precario por descuido.

## Índice

- [Objetivo](#objetivo)
- [Principios del proyecto](#principios-del-proyecto)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Roadmap de laboratorios](#roadmap-de-laboratorios)
- [Evidencias y gates](#evidencias-y-gates)
- [Estándar de diseño embebido](#estándar-de-diseño-embebido)
- [Licencias](#licencias)
- [Estado actual](#estado-actual)
- [Cómo contribuir](#cómo-contribuir)

## Objetivo

Crear una ruta pública, rigurosa y práctica para estudiar ciberseguridad embebida desde firmware real, evidencias reproducibles y documentación audit-grade.

El repositorio está diseñado para enseñar con contraste controlado:

- comportamiento inseguro intencionado;
- mitigación endurecida;
- trazabilidad requisito → diseño → implementación → test → evidencia;
- gates de calidad ejecutables por cualquier persona.

## Principios del proyecto

- Arquitectura por componentes.
- HAL/BSP explícito cuando aplica.
- Logs tratados como API de diagnóstico.
- Evidencias pequeñas, versionables y sin secretos reales.
- Perfiles inseguros solo para docencia y nunca por descuido.
- Estados explícitos: `CUMPLE`, `NO CUMPLE`, `NO VALIDADO`, `PENDIENTE`.

## Estructura del repositorio

```text
.github/       Workflows y automatización.
book/          Material destinado a capítulos o libro abierto.
docs/          Documentación transversal.
labs/          Laboratorios prácticos.
standard/      Estándar audit-grade del proyecto.
tools/         Gates y utilidades globales.
```

## Roadmap de laboratorios

| Laboratorio | Estado | Resumen |
| --- | --- | --- |
| LAB 01 — Firmware inseguro vs firmware endurecido | CUMPLE | Validado en ESP32-S3 con evidencias automáticas de consola, secret scan y gates. |
| LAB 02 — Identidad única de dispositivo | CUMPLE | Validado en ESP32-S3 con evidencias automáticas de identidad INSECURE/HARDENED y gates. |
| LAB 03 — MQTT seguro con TLS | PENDIENTE | No implementado todavía. |
| LAB 04 — OTA firmada con rollback | PENDIENTE | No implementado todavía. |
| LAB 05 — Configuración remota segura | PENDIENTE | No implementado todavía. |
| LAB 06 — Hardening de interfaces físicas | PENDIENTE | No implementado todavía. |
| LAB 07 — SBOM y trazabilidad de release | PENDIENTE | No implementado todavía. |
| LAB 08 — Secure Boot + Flash Encryption | PENDIENTE | No implementado todavía. |
| LAB 09 — Gateway seguro multi-interfaz | PENDIENTE | No implementado todavía. |
| LAB 10 — Mini PSIRT de producto | PENDIENTE | No implementado todavía. |

## Evidencias y gates

Cada laboratorio debe incluir, como mínimo:

- README con índice obligatorio;
- documentación técnica audit-grade;
- plan de pruebas;
- evidencias de consola o test cuando aplique;
- gates estáticos propios;
- estado explícito de validación.

Los gates globales se ejecutan con:

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
```

## Estándar de diseño embebido

El estándar del proyecto está en:

```text
standard/estandar_diseno_embebido_audit_grade.md
```

Ese documento define el criterio de arquitectura, testabilidad, trazabilidad, evidencias, logs, configuración, seguridad y transparencia del repositorio.

## Licencias

El código fuente, scripts, firmware y herramientas se publican bajo Apache License 2.0. Ver `LICENSE`.

La documentación, material didáctico, guías y capítulos se publican bajo Creative Commons Attribution-ShareAlike 4.0 International. Ver `LICENSE-DOCS`.

## Estado actual

```text
CUMPLE:
- Estructura pública inicial.
- Estándar audit-grade incorporado.
- LAB 01 implementado y validado localmente en ESP32-S3.
- LAB 02 implementado y validado localmente en ESP32-S3.
- Evidencias automáticas de consola/gates para LAB 01 y LAB 02.
- Gates estáticos globales y por laboratorio.

NO VALIDADO:
- Build completo con stdout versionado y cero warnings para todos los laboratorios.
- CI de build real en hardware o contenedor ESP-IDF para todos los laboratorios.

PENDIENTE:
- Implementar LAB 03.
- Capturar evidencias completas de build cuando proceda.
```

## Cómo contribuir

Ver `CONTRIBUTING.md` y `SECURITY.md`.
