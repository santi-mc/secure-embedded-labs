# Secure Embedded Labs

Repositorio público de laboratorios auditables para aprender ciberseguridad aplicada a microcontroladores, firmware embebido e IoT.

El proyecto combina dos objetivos:

1. Aprendizaje técnico: comprender seguridad en firmware mediante laboratorios reproducibles sobre microcontroladores reales.
2. Conocimiento abierto: construir una base pública reutilizable que evoluciona hacia documentación extensa y libro con licencia abierta.

> Un laboratorio puede ser inseguro de forma intencionada; nunca puede ser precario por descuido.

## Índice

- [Objetivo](#objetivo)
- [Principios del proyecto](#principios-del-proyecto)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Roadmap de laboratorios](#roadmap-de-laboratorios)
- [Evidencias y gates](#evidencias-y-gates)
- [Libro abierto](#libro-abierto)
- [Regla de actualización transversal](#regla-de-actualización-transversal)
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
- gates de calidad ejecutables por cualquier persona;
- capítulos y documentación navegable alineados con cada laboratorio.

## Principios del proyecto

- Arquitectura por componentes.
- HAL/BSP explícito cuando aplica.
- Logs tratados como API de diagnóstico.
- Evidencias pequeñas, versionables y sin secretos reales.
- Perfiles inseguros solo para docencia y nunca por descuido.
- Estados explícitos: `CUMPLE`, `NO CUMPLE`, `NO VALIDADO`, `PENDIENTE`.
- Nada se declara cerrado si README, roadmap, changelog, libro, evidencias y gates no están alineados.

## Estructura del repositorio

```text
.github/       Workflows y automatización.
book/          Material destinado a capítulos o libro abierto.
├── chapters/  Capítulos didácticos alineados con laboratorios.
├── figures/   Figuras y recursos gráficos del libro.
└── references/Referencias del libro.
docs/          Documentación transversal.
labs/          Laboratorios prácticos.
├── _template/
├── lab01_insecure_vs_hardened/
├── lab02_device_identity/
├── lab03_mqtt/
├── lab04_signed_ota/
├── lab05_secure_remote_config/
├── lab06_physical_interface_hardening/
├── lab07_sbom_release_traceability/
├── lab08_secure_boot_flash_encryption/
├── lab09_secure_multi_interface_gateway/
└── lab10_mini_psirt/
standard/      Estándar audit-grade del proyecto.
tools/         Gates y utilidades globales.
```

## Roadmap de laboratorios

| Laboratorio | Estado | Resumen |
| --- | --- | --- |
| LAB 01 — Firmware inseguro vs firmware endurecido | CUMPLE | Validado en ESP32-S3 con evidencias automáticas de consola, secret scan y gates. |
| LAB 02 — Identidad única de dispositivo | CUMPLE | Validado en ESP32-S3 con evidencias automáticas de identidad INSECURE/HARDENED y gates. |
| LAB 03 — Matriz MQTT contra test.mosquitto.org | EN CURSO | LAB 03A/M03-1883 CUMPLE en dry-run con evidencia de consola y gates. Siguiente: LAB 03B/M03-1884. |
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
- estado explícito de validación;
- actualización de documentación transversal cuando cambie el estado del laboratorio.

Los gates globales se ejecutan con:

```powershell
python tools\repo_quality_gates\run_static_repo_gates.py
```

Los artefactos generados no deben quedar en el árbol antes de ejecutar gates:

```text
firmware/build
firmware/sdkconfig
firmware/sdkconfig.old
managed_components
dependencies.lock
```

## Libro abierto

El directorio `book/` contiene el material que evoluciona hacia libro abierto. Cada laboratorio cerrado o en curso debe tener su capítulo o, como mínimo, una entrada explícita de continuidad.

Capítulos actuales:

- `book/chapters/01_firmware_inseguro_vs_endurecido.md`
- `book/chapters/02_identidad_dispositivo.md`
- `book/chapters/03_matriz_mqtt.md`

## Regla de actualización transversal

Cada parche que cambie estado de laboratorio debe revisar y actualizar, cuando aplique:

```text
README.md
ROADMAP.md
CHANGELOG.md
labs/README.md
book/README.md
book/chapters/*
docs/index.md
docs/learning_path.md
docs/publishing_model.md
labs/<lab>/README.md
labs/<lab>/CHANGELOG.md
labs/<lab>/docs/*
labs/<lab>/evidence/README.md
tools/repo_quality_gates/*
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
- LAB 03A/M03-1883 validado como dry-run MQTT sin TLS.
- Evidencias automáticas de consola/gates para LAB 01, LAB 02 y LAB 03A.
- Gates estáticos globales y por laboratorio.
- Libro abierto iniciado con capítulos 01, 02 y 03.

NO CUMPLE:
- Los escenarios MQTT sin TLS de LAB 03 son inseguros por diseño y se mantienen solo como baseline didáctico.

NO VALIDADO:
- Build completo con stdout versionado y cero warnings para todos los laboratorios.
- CI de build real en hardware o contenedor ESP-IDF para todos los laboratorios.
- Conexión MQTT real contra test.mosquitto.org.
- Validación real TLS/mTLS/certificados en LAB 03.

PENDIENTE:
- LAB 03B — M03-1884 MQTT TCP autenticado sin TLS.
- Capturar evidencias completas de build cuando proceda.
- Evolucionar capítulos del libro desde borrador técnico a texto editorial.
```

## Cómo contribuir

Ver `CONTRIBUTING.md` y `SECURITY.md`.
