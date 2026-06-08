# Secure Embedded Labs

Repositorio público de laboratorios auditables para aprender ciberseguridad aplicada a microcontroladores, firmware embebido e IoT.

El proyecto combina dos objetivos:

1. **Aprendizaje técnico:** comprender seguridad en firmware mediante laboratorios reproducibles sobre microcontroladores reales.
2. **Conocimiento abierto:** construir una base pública reutilizable que pueda evolucionar hacia documentación extensa o un libro con licencia abierta.

> Un laboratorio puede ser inseguro de forma intencionada; nunca puede ser precario por descuido.

## Índice

- [Objetivo](#objetivo)
- [Principios del proyecto](#principios-del-proyecto)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Roadmap de laboratorios](#roadmap-de-laboratorios)
- [Estándar de diseño embebido](#estándar-de-diseño-embebido)
- [Licencias](#licencias)
- [Estado actual](#estado-actual)
- [Cómo contribuir](#cómo-contribuir)

## Objetivo

Crear una ruta pública, rigurosa y práctica para aprender desarrollo seguro en sistemas embebidos, con foco inicial en **ESP32-S3 / ESP-IDF**.

Cada laboratorio debe permitir:

```text
clonar → leer → compilar → flashear → reproducir → auditar → aprender
```

## Principios del proyecto

Todo laboratorio debe cumplir el estándar permanente de diseño embebido audit-grade:

- arquitectura por componentes;
- FULL HAL/BSP;
- diseño orientado a interfaces y encapsulación;
- modelo temporal explícito;
- política de concurrencia, ISR y recursos compartidos;
- presupuesto de recursos;
- configuración validada;
- logs como API sin secretos;
- seguridad desde diseño;
- trazabilidad requisito → diseño → implementación → test → evidencia;
- QA gates estrictos;
- cero warnings;
- documentación audit-grade;
- transparencia `CUMPLE / NO CUMPLE / NO VALIDADO / PENDIENTE`.

El estándar completo está en:

```text
standard/estandar_diseno_embebido_audit_grade.md
```

## Estructura del repositorio

```text
secure-embedded-labs/
├── standard/
├── docs/
├── labs/
├── book/
├── tools/
└── .github/
```

## Roadmap de laboratorios

| Lab | Tema | Estado |
|---:|---|---|
| 01 | Firmware inseguro vs firmware endurecido | Validado localmente en ESP32-S3 |
| 02 | Identidad única de dispositivo | Pendiente |
| 03 | MQTT seguro con TLS | Pendiente |
| 04 | OTA firmada con rollback | Pendiente |
| 05 | Configuración remota segura | Pendiente |
| 06 | Hardening de interfaces físicas | Pendiente |
| 07 | SBOM y trazabilidad de release | Pendiente |
| 08 | Secure Boot + Flash Encryption | Pendiente |
| 09 | Gateway seguro multi-interfaz | Pendiente |
| 10 | Mini PSIRT de producto | Pendiente |

## Estándar de diseño embebido

Este repositorio no acepta laboratorios precarios. Cada entrega debe clasificarse explícitamente:

```text
CUMPLE:
- ...

NO CUMPLE:
- ...

NO VALIDADO:
- ...

PENDIENTE:
- ...
```

## Licencias

- Código fuente, scripts y firmware: **Apache-2.0**. Véase `LICENSE-CODE` y `LICENSE`.
- Documentación, texto educativo, figuras propias y futuro material de libro: **CC BY-SA 4.0**. Véase `LICENSE-DOCS`.

Los datasheets, normas, libros, artículos y documentos de terceros no se redistribuirán salvo permiso explícito. Se citarán o enlazarán según corresponda.

## Estado actual

```text
CUMPLE:
- Repositorio público estructurado.
- Estándar audit-grade incluido.
- Readme principal con índice.
- Gates estáticos de estructura incluidos.
- LAB 01 implementado con firmware ESP-IDF para ESP32-S3.
- LAB 01 validado localmente en hardware en perfiles INSECURE y HARDENED.
- Evidencias funcionales de consola añadidas para LAB 01.

NO CUMPLE:
- No contiene todavía capítulos completos de libro.
- Los laboratorios posteriores al LAB 01 aún no están implementados.

NO VALIDADO:
- Build completo con cero warnings no queda cerrado hasta versionar stdout completo de `idf.py build`.
- CI real en GitHub queda pendiente de revisar tras cada push.

PENDIENTE:
- Capturar evidencia formal de build ESP-IDF completo.
- Capturar evidencia formal del scanner de secretos.
- Implementar LAB 02.
```

## Cómo contribuir

Lee `CONTRIBUTING.md` antes de abrir un Pull Request.
