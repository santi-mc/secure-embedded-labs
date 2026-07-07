from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[2]

README = dedent('''\
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
.github/                         Workflows y automatización.
book/                            Material destinado a capítulos o libro abierto.
docs/                            Documentación transversal del proyecto.
labs/                            Laboratorios prácticos.
├── lab01_insecure_vs_hardened/  Firmware inseguro vs firmware endurecido.
├── lab02_device_identity/       Identidad única de dispositivo.
└── lab03_mqtt_tls/              Matriz MQTT contra test.mosquitto.org.
    ├── docs/                    Documentación específica del laboratorio.
    ├── evidence/                Evidencias versionables de consola y gates.
    ├── firmware/                Firmware ESP32-S3 del laboratorio.
    ├── test/                    Tests auxiliares del laboratorio.
    ├── tools/                   Captura, validación y gates específicos.
    ├── CHANGELOG.md             Historial del laboratorio.
    └── README.md                Contrato documental del laboratorio.
standard/                        Estándar audit-grade del proyecto.
tools/                           Gates y utilidades globales.
├── maintenance/                 Scripts idempotentes de mantenimiento.
└── repo_quality_gates/          Gates estáticos globales del repositorio.
```

## Roadmap de laboratorios

| Laboratorio | Estado | Resumen |
| --- | --- | --- |
| LAB 01 — Firmware inseguro vs firmware endurecido | CUMPLE | Validado en ESP32-S3 con evidencias automáticas de consola, secret scan y gates. |
| LAB 02 — Identidad única de dispositivo | CUMPLE | Validado en ESP32-S3 con evidencias automáticas de identidad INSECURE/HARDENED y gates. |
| LAB 03 — Matriz MQTT contra test.mosquitto.org | EN CURSO | LAB 03A/M03-1883 cerrado como dry-run con evidencias de consola y gates; siguiente fase: M03-1884 autenticado sin TLS. |
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
- LAB 03A/M03-1883 validado como baseline MQTT sin TLS en modo dry-run.
- Evidencias automáticas de consola/gates para LAB 01, LAB 02 y LAB 03A.
- Gates estáticos globales y por laboratorio.

NO VALIDADO:
- Build completo con stdout versionado y cero warnings para todos los laboratorios.
- CI de build real en hardware o contenedor ESP-IDF para todos los laboratorios.
- Conexión MQTT real contra test.mosquitto.org para la matriz completa de LAB 03.

PENDIENTE:
- Implementar LAB 03B/M03-1884 autenticado sin TLS.
- Capturar evidencias completas de build cuando proceda.
```

## Cómo contribuir

Ver `CONTRIBUTING.md` y `SECURITY.md`.
''')

ROADMAP = dedent('''\
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

- [x] LAB 03A — M03-1883 / MQTT TCP sin TLS y sin autenticación, baseline inseguro validado como dry-run.
- [ ] LAB 03B — M03-1884 / MQTT TCP sin TLS con usuario/password.
- [ ] LAB 03C — M03-8883 y M03-8886 / MQTT TLS sin autenticación.
- [ ] LAB 03D — M03-8885 / MQTT TLS con usuario/password.
- [ ] LAB 03E — M03-8884 / MQTT con certificado cliente.
- [ ] LAB 03F — M03-8887 / rechazo de certificado expirado.
- [ ] LAB 03G — MQTT over WebSockets 8080/8081/8090/8091.
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
''')


def write_if_changed(path: Path, content: str) -> bool:
    normalized = content.replace("\r\n", "\n").rstrip() + "\n"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if current == normalized:
        return False
    path.write_text(normalized, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    changed = []
    if write_if_changed(ROOT / "README.md", README):
        changed.append("README.md")
    if write_if_changed(ROOT / "ROADMAP.md", ROADMAP):
        changed.append("ROADMAP.md")

    if changed:
        print("updated: " + ", ".join(changed))
    else:
        print("already aligned: README.md, ROADMAP.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
