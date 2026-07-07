# LAB 03C — M03-8883 / M03-8886 / MQTT TLS con validación de servidor

**Estado:** PENDIENTE
**Escenario:** M03-8883 / M03-8886
**Puerto:** 8883 / 8886

## Índice

- [Objetivo](#objetivo)
- [Objetivos de aprendizaje](#objetivos-de-aprendizaje)
- [Prerrequisitos](#prerrequisitos)
- [Alcance](#alcance)
- [Fuera de alcance](#fuera-de-alcance)
- [Hardware requerido](#hardware-requerido)
- [Software requerido](#software-requerido)
- [Arquitectura prevista](#arquitectura-prevista)
- [Modelo temporal](#modelo-temporal)
- [Threat model](#threat-model)
- [Requisitos](#requisitos)
- [Cómo compilar](#como-compilar)
- [Cómo flashear](#como-flashear)
- [Cómo probar](#como-probar)
- [Evidencias esperadas](#evidencias-esperadas)
- [Errores comunes](#errores-comunes)
- [Ejercicios](#ejercicios)
- [Preguntas de repaso](#preguntas-de-repaso)
- [Fuentes](#fuentes)
- [Estado](#estado)

## Objetivo

Validar el escenario `M03-8883 / M03-8886` dentro de la familia LAB 03 MQTT.

## Objetivos de aprendizaje

- Separar comportamiento funcional de cumplimiento de seguridad.
- Identificar el efecto de TLS, autenticación y validación de certificados.
- Mantener evidencia propia del sublaboratorio.

## Prerrequisitos

- Revisar `../README.md`.
- Mantener limpio el árbol de artefactos generados.
- No usar secretos reales contra brokers públicos.

## Alcance

Este sublaboratorio cubre `M03-8883 / M03-8886`: MQTT TLS con validación de servidor.

## Fuera de alcance

- Reutilizar evidencias de otro sublaboratorio.
- Declarar conexión real si solo existe dry-run.
- Introducir credenciales reales en firmware, logs o documentación.

## Hardware requerido

- ESP32-S3 compatible.
- Cable USB de datos.
- Consola USB Serial/JTAG para fases dry-run.

## Software requerido

- Git.
- Python 3.
- ESP-IDF compatible con ESP32-S3 cuando exista firmware.
- PowerShell o terminal equivalente.

## Arquitectura prevista

```text
lab03c_m03_8883_8886_tls_server_auth/
├── README.md
├── CHANGELOG.md
├── docs/
├── evidence/
├── firmware/
├── test/
└── tools/
```

## Modelo temporal

La fase dry-run usa interacción por consola. Las conexiones reales deberán declarar timeouts, retry y política de fallo.

## Threat model

Propiedades del escenario:

```text
TLS: Sí
Auth: No
Broker: test.mosquitto.org
```

## Requisitos

- Logs sin secretos.
- Evidencia propia del escenario.
- Separación explícita entre dry-run y conexión real.
- Gates en PASS antes de declarar cierre.

## Cómo compilar

Este sublaboratorio todavía no tiene firmware propio validado.

## Cómo flashear

No aplica hasta que exista firmware propio validado.

## Cómo probar

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
python labs/lab03_mqtt/tools/run_static_gates.py
```

## Evidencias esperadas

- Evidencia de consola propia cuando se implemente.
- Evidencia de gates tras integrar el sublaboratorio.

## Errores comunes

- Confundir autenticación con confidencialidad.
- Publicar secretos reales.
- Dar por validada una conexión no probada.

## Ejercicios

- Clasificar el escenario como seguro, inseguro o no validado.
- Identificar qué propiedades de seguridad faltan.
- Revisar si la evidencia disponible justifica el estado declarado.

## Preguntas de repaso

- ¿Qué protege TLS en este escenario?
- ¿Qué protege la autenticación?
- ¿Qué evidencia permite declarar `CUMPLE`?

## Fuentes

- Documentación pública de `test.mosquitto.org`.
- Documentación oficial de ESP-IDF.
- Estándar audit-grade interno del proyecto.

## Estado

```text
PENDIENTE
```
