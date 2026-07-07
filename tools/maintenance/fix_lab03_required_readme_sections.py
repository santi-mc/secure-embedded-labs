#!/usr/bin/env python3
"""
Make LAB 03 README comply with the repository-wide lab README contract.

The repository gate validates a fixed list of section headers for every lab.
This script is idempotent and writes a complete LAB 03 README containing all
required sections while preserving the LAB 03A Mosquitto baseline scope.
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "labs" / "lab03_mqtt_tls"
README = LAB / "README.md"
GENERATOR = ROOT / "tools" / "maintenance" / "apply_lab03_mosquitto_matrix.py"

LAB03_README = r"""
# LAB 03 — Matriz MQTT contra test.mosquitto.org

**Versión:** 0.1.0

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
- [Cómo compilar](#cómo-compilar)
- [Cómo flashear](#cómo-flashear)
- [Cómo probar](#cómo-probar)
- [Evidencias esperadas](#evidencias-esperadas)
- [Errores comunes](#errores-comunes)
- [Ejercicios](#ejercicios)
- [Preguntas de repaso](#preguntas-de-repaso)
- [Fuentes](#fuentes)
- [Estado](#estado)

## Objetivo

Construir una matriz reproducible de escenarios MQTT usando el broker público `test.mosquitto.org`.

El primer objetivo ejecutable es demostrar el baseline inseguro `M03-1883`: MQTT TCP plano, puerto 1883, sin TLS y sin autenticación. El laboratorio queda preparado desde el primer commit para cubrir los once escenarios publicados por el broker: MQTT plano, MQTT con autenticación, MQTT sobre TLS, mTLS, certificado expirado y MQTT over WebSockets.

## Objetivos de aprendizaje

- Entender la diferencia entre MQTT plano, MQTT autenticado, MQTT sobre TLS y MQTT sobre WebSockets.
- Evidenciar por qué MQTT sin TLS no debe considerarse seguro aunque permita conexión funcional.
- Comparar los escenarios publicados por `test.mosquitto.org` en puertos 1883, 1884, 8883, 8884, 8885, 8886, 8887, 8080, 8081, 8090 y 8091.
- Aprender a clasificar cada escenario como `CUMPLE`, `NO CUMPLE`, `NO VALIDADO` o `PENDIENTE` según transporte, autenticación y validación de certificados.
- Generar evidencias reproducibles mediante consola, logs NDJSON y gates estáticos.

## Prerrequisitos

- Placa ESP32-S3 con consola USB Serial/JTAG operativa.
- ESP-IDF v6.0.x configurado para target `esp32s3`.
- Python 3 disponible dentro del entorno ESP-IDF.
- Puerto serie identificado, por ejemplo `COM5` en Windows.
- Para LAB 03A no se requieren credenciales reales, certificados privados ni conexión real al broker.
- Para fases posteriores será necesario acceso de red hacia `test.mosquitto.org` y material criptográfico de prueba cuando aplique.

## Alcance

Esta fase crea el contrato de matriz y un firmware didáctico inicial que ejecuta comprobaciones dry-run de política MQTT. No establece todavía conexión real con el broker.

LAB 03A cubre:

```text
M03-1883 — MQTT TCP 1883 sin TLS y sin autenticación.
```

El resto de escenarios queda documentado y trazado para fases posteriores.

## Fuera de alcance

- Conexión real Wi-Fi/Ethernet al broker público.
- Integración real de ESP-MQTT.
- Validación real de certificados X.509.
- mTLS con certificado cliente.
- MQTT over WebSockets real.
- Gestión de secretos reales.

## Hardware requerido

- ESP32-S3 compatible con ESP-IDF v6.0.x.
- Cable USB de datos para alimentación, flasheo y consola USB Serial/JTAG.
- Equipo host con acceso a puerto serie.

## Software requerido

- ESP-IDF v6.0.x.
- Python del entorno ESP-IDF.
- `pyserial` para captura de evidencias desde consola.
- Git para versionado y revisión de gates.

## Arquitectura prevista

```text
main
├── board_hal
├── command_console
├── lab03_domain
├── mqtt_scenario
└── secure_log
```

La implementación inicial es intencionadamente dry-run para separar política de seguridad, trazabilidad de escenarios y contrato de evidencias antes de introducir red, ESP-MQTT, certificados y broker real.

## Modelo temporal

- Arranque del firmware y emisión de evento `boot`.
- Inicio de consola y emisión de evento `console_start`.
- Lectura interactiva línea a línea desde USB Serial/JTAG.
- Ejecución síncrona de comandos de escenario.
- Emisión de logs NDJSON con `uptime_ms` para cada evento.
- Captura automática con tiempos acotados desde script Python.

No hay todavía timeouts de red, DNS, TLS handshake ni reconexión MQTT real en LAB 03A.

## Threat model

Activos protegidos futuros:

- Credenciales MQTT.
- Identidad del dispositivo.
- Topics y payloads operativos.
- Material criptográfico de cliente.
- Integridad del canal broker-dispositivo.

Amenazas modeladas desde LAB 03A:

- Escucha pasiva de tráfico MQTT plano.
- Exposición de credenciales si se usa autenticación sin TLS.
- Confusión entre conectividad funcional y seguridad del canal.
- Aceptación indebida de certificados expirados o no confiables en fases TLS.

## Requisitos

| ID | Requisito | Estado |
| --- | --- | --- |
| LAB03-RQ-001 | Definir matriz completa `test.mosquitto.org`. | CUMPLE |
| LAB03-RQ-002 | Implementar baseline `M03-1883` sin TLS. | CUMPLE |
| LAB03-RQ-003 | Clasificar `M03-1883` como funcional pero `NO CUMPLE` seguridad. | CUMPLE |
| LAB03-RQ-004 | Emitir logs NDJSON reproducibles. | CUMPLE |
| LAB03-RQ-005 | Capturar y verificar evidencia de consola. | CUMPLE |
| LAB03-RQ-006 | Ejecutar conexión real a broker. | PENDIENTE |
| LAB03-RQ-007 | Validar TLS, CA, mTLS y certificado expirado. | PENDIENTE |

## Cómo compilar

```powershell
cd labs\lab03_mqtt_tls\firmware
idf.py set-target esp32s3
idf.py build
```

El directorio `build/`, `sdkconfig` y `sdkconfig.old` son artefactos generados y no deben versionarse.

## Cómo flashear

```powershell
cd labs\lab03_mqtt_tls\firmware
idf.py -p COM5 flash monitor
```

Sustituir `COM5` por el puerto real del ESP32-S3.

## Cómo probar

Prueba manual mínima en monitor:

```text
help
scenario_list
select_scenario M03-1883
scenario_status
mqtt_connect_dry_run
mqtt_publish_dry_run
security_status
```

Captura automática:

```powershell
python labs\lab03_mqtt_tls\tools\capture_console_evidence.py `
  --port COM5 `
  --scenario M03-1883 `
  --output labs\lab03_mqtt_tls\evidence\lab03_m03_1883_console.log

python labs\lab03_mqtt_tls\tools\check_mqtt_scenario_logs.py `
  labs\lab03_mqtt_tls\evidence\lab03_m03_1883_console.log `
  --scenario M03-1883
```

Gates:

```powershell
python labs\lab03_mqtt_tls\tools\capture_static_gates.py
python tools\repo_quality_gates\run_static_repo_gates.py
python labs\lab03_mqtt_tls\tools\run_static_gates.py
```

## Evidencias esperadas

```text
evidence/lab03_m03_1883_console.log
evidence/lab03_static_gates.txt
```

Evidencias pendientes para cierre completo futuro:

```text
evidence/lab03_build_esp32s3.txt
evidence/lab03_real_broker_matrix.txt
evidence/lab03_tls_certificate_validation.txt
```

## Errores comunes

- Capturar el puerto mientras `idf.py monitor` sigue abierto.
- Flashear otra carpeta de laboratorio y obtener eventos de `LAB02`.
- Dejar `firmware/build`, `sdkconfig` o `sdkconfig.old` dentro del árbol antes de ejecutar gates.
- Confundir `M03-1883` funcional con un diseño seguro.
- Usar credenciales reales contra un broker público.

## Ejercicios

- Identificar qué escenarios de la matriz son funcionales pero `NO CUMPLE` desde el punto de vista de seguridad.
- Comparar 1883 frente a 1884 y explicar por qué autenticación sin TLS no protege credenciales.
- Preparar la extensión de LAB 03B para `M03-1884` manteniendo evidencias NDJSON.
- Diseñar los criterios de rechazo esperados para `M03-8887` con certificado expirado.

## Preguntas de repaso

- ¿Por qué MQTT sin TLS no debe transportar credenciales reales?
- ¿Qué diferencia hay entre autenticación de cliente y cifrado del canal?
- ¿Qué evidencia mínima demuestra que `M03-1883` es solo un baseline inseguro?
- ¿Por qué un certificado expirado debe producir rechazo en un cliente endurecido?

## Fuentes

- Documentación pública de `test.mosquitto.org`.
- Documentación ESP-IDF de consola USB Serial/JTAG.
- Documentación ESP-MQTT para fases posteriores.
- Estándar interno `standard/estandar_diseno_embebido_audit_grade.md`.

## Estado

```text
CUMPLE:
- Matriz contractual completa de test.mosquitto.org documentada.
- Firmware inicial dry-run para ESP32-S3 añadido.
- Baseline 1883 sin TLS modelado como NO CUMPLE de seguridad esperado.
- Consola interactiva USB Serial/JTAG validada.
- Captura de evidencia M03-1883 generada y verificada.
- Gates y herramientas de evidencia añadidos.

NO CUMPLE:
- 1883/1884/8080/8090 no son diseños seguros porque no usan TLS.
- Esta fase no implementa conexión real al broker.

NO VALIDADO:
- Build real ESP-IDF con stdout completo y cero warnings versionado.
- Matriz real contra broker público.
- Validación real de certificados TLS.

PENDIENTE:
- LAB 03B: MQTT 1884 autenticado sin TLS.
- Integrar ESP-MQTT como dependencia gestionada.
- Añadir Wi-Fi/provisioning de red.
- Ejecutar matriz real contra test.mosquitto.org.
- Introducir TLS, CA, mTLS y WebSockets en fases posteriores.
```
"""


def clean(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean(content), encoding="utf-8", newline="\n")


def update_lab_readme() -> None:
    if not README.exists():
        raise FileNotFoundError(f"missing LAB 03 README: {README}")
    write(README, LAB03_README)


def update_generator_template() -> None:
    if not GENERATOR.exists():
        return

    text = GENERATOR.read_text(encoding="utf-8", errors="replace")
    marker = '    write("labs/lab03_mqtt_tls/README.md", r\'\'\'\n'
    start = text.find(marker)
    if start < 0:
        return

    body_start = start + len(marker)
    end_match = re.search(r"\n    '''\)", text[body_start:])
    if not end_match:
        return

    body_end = body_start + end_match.start()
    replacement_body = textwrap.indent(clean(LAB03_README), "        ").rstrip()
    new_text = text[:body_start] + replacement_body + text[body_end:]
    GENERATOR.write_text(new_text.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    update_lab_readme()
    update_generator_template()
    print("PASS: LAB 03 README required sections aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
