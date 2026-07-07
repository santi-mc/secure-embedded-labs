#!/usr/bin/env python3
"""Align repository-level documentation with the current audit-grade project state.

This maintenance script is intentionally idempotent.  It does not advance any
laboratory implementation.  It only repairs the cross-repository documentation
surface that must move together with LAB 01, LAB 02 and LAB 03A.
"""
from __future__ import annotations

from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[2]


def normalize(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def write_text(relpath: str, content: str) -> None:
    path = ROOT / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(normalize(content), encoding="utf-8", newline="\n")
    print(f"updated: {relpath}")


def main() -> int:
    write_text(
        "README.md",
        r"""
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
        ├── lab03_mqtt_tls/
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
        - `book/chapters/03_matriz_mqtt_tls.md`

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
        """,
    )

    write_text(
        "ROADMAP.md",
        r"""
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
        """,
    )

    write_text(
        "CHANGELOG.md",
        r"""
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
        """,
    )

    write_text(
        "labs/README.md",
        r"""
        # Laboratorios

        ## Índice

        - [Regla común](#regla-común)
        - [Lista de laboratorios](#lista-de-laboratorios)
        - [Estados actuales](#estados-actuales)
        - [Plantilla](#plantilla)
        - [Regla de cierre](#regla-de-cierre)

        ## Regla común

        Cada laboratorio debe tener un `README.md` con índice y estructura didáctica completa.

        Cada avance debe actualizar también los artefactos transversales del repositorio: README raíz, ROADMAP, CHANGELOG, libro, docs, evidencias e índices cuando aplique.

        ## Lista de laboratorios

        | Lab | Carpeta | Tema | Estado |
        | ---: | --- | --- | --- |
        | 01 | `lab01_insecure_vs_hardened` | Firmware inseguro vs firmware endurecido | CUMPLE |
        | 02 | `lab02_device_identity` | Identidad única de dispositivo | CUMPLE |
        | 03 | `lab03_mqtt_tls` | Matriz MQTT contra test.mosquitto.org | EN CURSO: 03A CUMPLE |
        | 04 | `lab04_signed_ota` | OTA firmada con rollback | PENDIENTE |
        | 05 | `lab05_secure_remote_config` | Configuración remota segura | PENDIENTE |
        | 06 | `lab06_physical_interface_hardening` | Hardening de interfaces físicas | PENDIENTE |
        | 07 | `lab07_sbom_release_traceability` | SBOM y trazabilidad de release | PENDIENTE |
        | 08 | `lab08_secure_boot_flash_encryption` | Secure Boot + Flash Encryption | PENDIENTE |
        | 09 | `lab09_secure_multi_interface_gateway` | Gateway seguro multi-interfaz | PENDIENTE |
        | 10 | `lab10_mini_psirt` | Mini PSIRT de producto | PENDIENTE |

        ## Estados actuales

        ```text
        CUMPLE:
        - LAB 01 con evidencias de consola, secret scan y gates.
        - LAB 02 con evidencias de identidad INSECURE/HARDENED y gates.
        - LAB 03A/M03-1883 como dry-run MQTT plano sin TLS con evidencia de consola y gates.

        NO VALIDADO:
        - Builds formales con stdout completo y cero warnings para todos los laboratorios.
        - Conexiones reales MQTT contra broker público.
        - TLS/mTLS/WebSockets de LAB 03.

        PENDIENTE:
        - LAB 03B/M03-1884.
        - LAB 04 a LAB 10.
        ```

        ## Plantilla

        La plantilla está en:

        ```text
        labs/_template/README.md
        ```

        ## Regla de cierre

        No se marca un laboratorio como cerrado si no están alineados:

        - README del laboratorio;
        - documentación interna del laboratorio;
        - evidencias;
        - gates;
        - README raíz;
        - ROADMAP;
        - CHANGELOG global;
        - libro o capítulo correspondiente;
        - índices de navegación.
        """,
    )

    write_text(
        "docs/index.md",
        r"""
        # Documentación general

        ## Índice

        - [Ruta de aprendizaje](learning_path.md)
        - [Glosario](glossary.md)
        - [Bibliografía](bibliography.md)
        - [Secure by Design](secure_by_design.md)
        - [Threat Modeling](threat_modeling.md)
        - [Fundamentos de seguridad firmware](firmware_security_basics.md)
        - [Modelo de publicación](publishing_model.md)
        - [Libro abierto](../book/README.md)
        - [Estándar audit-grade](../standard/estandar_diseno_embebido_audit_grade.md)

        Este índice recoge la documentación transversal. Los detalles ejecutables, evidencias y gates viven dentro de cada laboratorio.
        """,
    )

    write_text(
        "docs/learning_path.md",
        r"""
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
        """,
    )

    write_text(
        "docs/publishing_model.md",
        r"""
        # Modelo de publicación

        ## Índice

        - [Repositorio](#repositorio)
        - [Libro](#libro)
        - [Licencias](#licencias)
        - [Versionado](#versionado)
        - [Cierre transversal](#cierre-transversal)

        ## Repositorio

        El repositorio contiene código, documentación, laboratorios, scripts, evidencias y capítulos en desarrollo.

        La unidad de entrega no es solo el firmware de un laboratorio. Una entrega audit-grade debe alinear también documentación, evidencias, libro, roadmap y changelog.

        ## Libro

        El directorio `book/` evoluciona hacia un libro con licencia abierta. Cada laboratorio validado o en curso debe tener una entrada de libro proporcional a su madurez.

        Capítulos actuales:

        - Capítulo 01 — LAB 01.
        - Capítulo 02 — LAB 02.
        - Capítulo 03 — LAB 03A y matriz MQTT.

        ## Licencias

        - Código: Apache-2.0.
        - Documentación: CC BY-SA 4.0.

        ## Versionado

        Cada release público debe indicar estado, alcance y limitaciones.

        El changelog global debe registrar los hitos transversales y no limitarse a cambios de firmware.

        ## Cierre transversal

        Antes de declarar cerrado un laboratorio o subfase se revisan:

        ```text
        README.md
        ROADMAP.md
        CHANGELOG.md
        labs/README.md
        book/README.md
        book/chapters/*
        docs/index.md
        docs/learning_path.md
        labs/<lab>/README.md
        labs/<lab>/CHANGELOG.md
        labs/<lab>/docs/*
        labs/<lab>/evidence/README.md
        ```
        """,
    )

    write_text(
        "book/README.md",
        r"""
        # Libro abierto

        ## Índice

        - [Objetivo](#objetivo)
        - [Estructura](#estructura)
        - [Capítulos](#capítulos)
        - [Licencia](#licencia)
        - [Estado](#estado)
        - [Criterio editorial](#criterio-editorial)

        ## Objetivo

        Este directorio evoluciona hacia un libro práctico con licencia abierta sobre ciberseguridad aplicada a firmware embebido y microcontroladores.

        El libro no sustituye a los laboratorios: los interpreta, ordena y explica con narrativa didáctica.

        ## Estructura

        ```text
        book/
        ├── chapters/
        │   ├── 01_firmware_inseguro_vs_endurecido.md
        │   ├── 02_identidad_dispositivo.md
        │   └── 03_matriz_mqtt_tls.md
        ├── figures/
        └── references/
        ```

        ## Capítulos

        | Capítulo | Laboratorio | Estado |
        | --- | --- | --- |
        | 01 — Firmware inseguro vs firmware endurecido | LAB 01 | CUMPLE como capítulo técnico inicial |
        | 02 — Identidad única de dispositivo | LAB 02 | CUMPLE como capítulo técnico inicial |
        | 03 — Matriz MQTT y transporte seguro | LAB 03A | CUMPLE como capítulo técnico inicial de baseline dry-run |

        ## Licencia

        El material propio de documentación se publica bajo CC BY-SA 4.0 salvo indicación distinta.

        ## Estado

        ```text
        CUMPLE:
        - Estructura inicial creada.
        - Capítulos 01, 02 y 03 alineados con el estado técnico actual.

        NO VALIDADO:
        - Revisión editorial completa no realizada.
        - Figuras definitivas no incorporadas.
        - Referencias bibliográficas del libro no normalizadas.

        PENDIENTE:
        - Convertir capítulos técnicos en narrativa editorial completa.
        - Añadir figuras y diagramas.
        - Preparar versión publicable.
        ```

        ## Criterio editorial

        Un capítulo puede estar en estado técnico inicial si enlaza con evidencias reales y declara sus limitaciones. No puede afirmar una validación que el laboratorio no tenga.
        """,
    )

    write_text(
        "book/chapters/01_firmware_inseguro_vs_endurecido.md",
        r"""
        # Capítulo 01 — Firmware inseguro vs firmware endurecido

        ## Índice

        - [Objetivo](#objetivo)
        - [Idea central](#idea-central)
        - [Qué se demuestra](#qué-se-demuestra)
        - [Relación con el laboratorio](#relación-con-el-laboratorio)
        - [Estado](#estado)

        ## Objetivo

        Introducir la primera práctica de ciberseguridad embebida: comparar un firmware vulnerable de laboratorio con una variante endurecida que corrige las mismas debilidades.

        ## Idea central

        Un microcontrolador no necesita estar conectado a Internet para tener superficie de ataque. Una consola local, logs verbosos, comandos de configuración y secretos mal tratados son suficientes para crear vulnerabilidades reales.

        ## Qué se demuestra

        - Fuga de secretos por `get_config`.
        - Fuga de secretos por logs de comandos brutos.
        - Configuración inválida por parser débil.
        - Reset destructivo sin autorización.
        - Redacción y validación como mitigaciones básicas.

        ## Relación con el laboratorio

        El firmware y las evidencias se encuentran en:

        ```text
        labs/lab01_insecure_vs_hardened/
        ```

        LAB 01 está cerrado para el alcance actual con evidencias automáticas de consola, scanner de secretos y gates estáticos.

        ## Estado

        ```text
        CUMPLE:
        - Capítulo inicial alineado con LAB 01.
        - Evidencias del laboratorio incorporadas al estado del repositorio.

        NO VALIDADO:
        - Revisión editorial completa pendiente.
        ```
        """,
    )

    write_text(
        "book/chapters/02_identidad_dispositivo.md",
        r"""
        # Capítulo 02 — Identidad única de dispositivo

        ## Índice

        - [Objetivo](#objetivo)
        - [Idea central](#idea-central)
        - [Qué se demuestra](#qué-se-demuestra)
        - [Relación con el laboratorio](#relación-con-el-laboratorio)
        - [Estado](#estado)

        ## Objetivo

        Explicar por qué una identidad hardcoded o mutable no sirve como base de seguridad en un dispositivo embebido.

        ## Idea central

        Identificar un dispositivo no equivale a autenticarlo. Una identidad clonable permite suplantación aunque el firmware parezca funcional.

        ## Qué se demuestra

        - Identidad hardcoded y clonable en perfil INSECURE.
        - Exposición de `raw_hardware_id` en perfil INSECURE.
        - Mutación de identidad mediante consola insegura.
        - Identidad derivada de eFuse MAC y hash en perfil HARDENED.
        - Redacción de identificadores crudos y rechazo de mutación en perfil HARDENED.

        ## Relación con el laboratorio

        El firmware y las evidencias se encuentran en:

        ```text
        labs/lab02_device_identity/
        ```

        LAB 02 está cerrado para el alcance actual con evidencias INSECURE/HARDENED y gates estáticos.

        ## Estado

        ```text
        CUMPLE:
        - Capítulo técnico inicial creado.
        - Estado alineado con LAB 02.

        NO VALIDADO:
        - Revisión editorial completa pendiente.
        ```
        """,
    )

    write_text(
        "book/chapters/03_matriz_mqtt_tls.md",
        r"""
        # Capítulo 03 — Matriz MQTT y transporte seguro

        ## Índice

        - [Objetivo](#objetivo)
        - [Idea central](#idea-central)
        - [Qué se demuestra](#qué-se-demuestra)
        - [Matriz didáctica](#matriz-didáctica)
        - [Relación con el laboratorio](#relación-con-el-laboratorio)
        - [Estado](#estado)

        ## Objetivo

        Introducir la seguridad de transporte en MQTT mediante una matriz progresiva de escenarios contra `test.mosquitto.org`.

        ## Idea central

        Una conexión MQTT funcional no implica seguridad. El laboratorio separa conectividad, autenticación, confidencialidad, validación de certificado y autenticación mutua.

        ## Qué se demuestra

        - MQTT TCP plano sin TLS como baseline inseguro.
        - Autenticación sin TLS como mejora insuficiente.
        - TLS como mitigación de confidencialidad e integridad de canal.
        - Validación de certificado servidor como requisito de seguridad.
        - Rechazo de certificados expirados como comportamiento correcto.
        - mTLS y WebSockets como fases posteriores.

        ## Matriz didáctica

        ```text
        LAB 03A — M03-1883: MQTT TCP sin TLS y sin autenticación.
        LAB 03B — M03-1884: MQTT TCP sin TLS con usuario/password.
        LAB 03C — M03-8883/M03-8886: MQTT TLS sin autenticación.
        LAB 03D — M03-8885: MQTT TLS con usuario/password.
        LAB 03E — M03-8884: MQTT mTLS.
        LAB 03F — M03-8887: certificado expirado, rechazo obligatorio.
        LAB 03G — MQTT over WebSockets.
        ```

        ## Relación con el laboratorio

        El firmware y las evidencias se encuentran en:

        ```text
        labs/lab03_mqtt_tls/
        ```

        LAB 03A está cerrado como dry-run contractual: selecciona `M03-1883`, emite logs NDJSON, clasifica el escenario como funcional pero `NO CUMPLE` seguridad y dispone de evidencia de consola y gates.

        ## Estado

        ```text
        CUMPLE:
        - Capítulo técnico inicial creado.
        - LAB 03A/M03-1883 alineado con evidencias y gates.

        NO CUMPLE:
        - Los escenarios sin TLS son inseguros por diseño y se mantienen solo como baseline didáctico.

        NO VALIDADO:
        - Conexión real MQTT contra broker público.
        - TLS/mTLS/WebSockets reales.
        - Revisión editorial completa pendiente.

        PENDIENTE:
        - LAB 03B y fases posteriores.
        ```
        """,
    )

    write_text(
        "labs/lab03_mqtt_tls/docs/audit_evidence.md",
        r"""
        # LAB 03 — Evidencias de auditoría

        ## Índice

        - [Estado](#estado)
        - [Evidencias actuales](#evidencias-actuales)
        - [Pendientes](#pendientes)

        ## Estado

        ```text
        CUMPLE:
        - Evidencia de consola LAB 03A/M03-1883 capturada y verificada.
        - Evidencia de gates estáticos LAB 03 capturada y verificada.

        NO VALIDADO:
        - Build real con stdout completo y cero warnings versionado.
        - Conexión real al broker.
        - Validación TLS/mTLS/WebSockets.
        ```

        ## Evidencias actuales

        | Evidencia | Estado | Descripción |
        | --- | --- | --- |
        | `evidence/lab03_m03_1883_console.log` | CUMPLE | Baseline MQTT 1883 sin TLS, dry-run contractual. |
        | `evidence/lab03_static_gates.txt` | CUMPLE | Gates globales y gate específico LAB 03. |

        ## Pendientes

        - Capturar stdout completo de `idf.py build` cuando se cierre release firmware formal.
        - Añadir evidencias de conexión real al broker en fases posteriores.
        - Añadir evidencias TLS/certificados en fases posteriores.
        - Añadir evidencia LAB 03B/M03-1884 antes de marcar esa fase como cerrada.
        """,
    )

    write_text(
        "labs/lab03_mqtt_tls/docs/test_plan.md",
        r"""
        # LAB 03 — Plan de pruebas

        ## Índice

        - [Objetivo](#objetivo)
        - [Pruebas de fase 03A](#pruebas-de-fase-03a)
        - [Pruebas pendientes](#pruebas-pendientes)
        - [Criterio de cierre](#criterio-de-cierre)

        ## Objetivo

        Validar primero el baseline MQTT sin TLS y dejar trazada la matriz completa para fases posteriores.

        ## Pruebas de fase 03A

        | ID | Prueba | Estado esperado | Estado actual |
        | --- | --- | --- | --- |
        | T03A-001 | `help` | Lista comandos. | CUMPLE |
        | T03A-002 | `scenario_list` | Lista los once escenarios. | CUMPLE |
        | T03A-003 | `select_scenario M03-1883` | Selecciona baseline sin TLS. | CUMPLE |
        | T03A-004 | `scenario_status` | Muestra host, puerto 1883 y `tls_enabled=false`. | CUMPLE |
        | T03A-005 | `mqtt_connect_dry_run` | Emite clasificación de seguridad insegura esperada. | CUMPLE |
        | T03A-006 | `mqtt_publish_dry_run` | Emite publicación simulada sin broker real. | CUMPLE |
        | T03A-007 | Checker de logs | Acepta el baseline inseguro como evidencia didáctica. | CUMPLE |
        | T03A-008 | Gates estáticos | Gate global y gate LAB 03 en PASS. | CUMPLE |

        ## Pruebas pendientes

        - LAB 03B: autenticación 1884 sin TLS.
        - Conexión real a 1883.
        - TLS 8883/8886/8885.
        - mTLS 8884.
        - Certificado expirado 8887.
        - WebSockets 8080/8081/8090/8091.

        ## Criterio de cierre

        LAB 03A queda cerrado como dry-run contractual cuando el firmware compila, arranca en ESP32-S3, captura evidencia de `M03-1883` y pasan gates estáticos.

        Las fases de conexión real quedan `NO VALIDADO` hasta que existan evidencias contra broker y documentación de disponibilidad/timeout.
        """,
    )

    write_text(
        "labs/lab03_mqtt_tls/CHANGELOG.md",
        r"""
        # CHANGELOG LAB 03

        ## Índice

        - [Unreleased](#unreleased)
        - [Estado actual](#estado-actual)
        - [Historial](#historial)

        ## Unreleased

        - Alineada documentación audit-grade tras cierre de LAB 03A.
        - Actualizados documentos de evidencias y plan de pruebas para reflejar `CUMPLE` en M03-1883 dry-run.
        - Registrada necesidad de mantener README raíz, ROADMAP, CHANGELOG global y libro sincronizados antes de LAB 03B.

        ## Estado actual

        - LAB 03A / M03-1883: `CUMPLE` como baseline MQTT TCP sin TLS con evidencia de consola capturada y gates estáticos.
        - Matriz completa test.mosquitto.org: definida contractualmente y pendiente de ejecución real por fases.
        - Siguiente fase: LAB 03B / M03-1884.

        ## Historial

        - Inicio de LAB 03A como matriz MQTT contra test.mosquitto.org.
        - Añadido baseline MQTT 1883 sin TLS como escenario inseguro controlado.
        - Añadidos firmware dry-run, documentación, gates y herramientas de evidencia.
        """,
    )

    write_text(
        "labs/lab03_mqtt_tls/evidence/README.md",
        r"""
        # Evidencias LAB 03

        ## Índice

        - [Propósito](#propósito)
        - [Evidencias de fase 03A](#evidencias-de-fase-03a)
        - [Pendientes](#pendientes)

        ## Propósito

        Este directorio almacena evidencias de ejecución del LAB 03. No se deben versionar credenciales reales, certificados privados ni payloads sensibles.

        ## Evidencias de fase 03A

        | Fichero | Estado | Descripción |
        | --- | --- | --- |
        | `lab03_m03_1883_console.log` | CUMPLE | Baseline MQTT 1883 sin TLS, dry-run contractual. |
        | `lab03_static_gates.txt` | CUMPLE | Gates estáticos globales y específicos LAB 03. |

        ## Pendientes

        | Evidencia | Estado |
        | --- | --- |
        | `lab03_m03_1884_console.log` | PENDIENTE |
        | `lab03_build_esp32s3.txt` | PENDIENTE |
        | `lab03_real_broker_matrix.txt` | PENDIENTE |
        | `lab03_tls_certificate_validation.txt` | PENDIENTE |
        """,
    )

    print("alignment complete: repository documentation is consistent with LAB 01, LAB 02 and LAB 03A state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
