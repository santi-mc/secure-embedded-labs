# LAB 03 — Familia MQTT contra test.mosquitto.org

**Versión:** 0.2.0
**Estado:** EN CURSO
**Modelo:** familia de sublaboratorios independientes

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

Organizar una matriz MQTT reproducible contra `test.mosquitto.org`, separando cada escenario en un sublaboratorio auditable.

## Objetivos de aprendizaje

- Diferenciar conectividad funcional de diseño seguro.
- Separar autenticación, confidencialidad, validación de certificados y mTLS.
- Evidenciar que MQTT plano no protege credenciales ni payloads sensibles.
- Mantener trazabilidad escenario → diseño → firmware → test → evidencia.

## Prerrequisitos

- Repositorio limpio de artefactos generados.
- Python 3 para herramientas y gates.
- ESP-IDF cuando se compile firmware.
- No usar secretos reales contra brokers públicos.

## Alcance

Esta familia cubre los escenarios MQTT publicados por `test.mosquitto.org` mediante sublaboratorios independientes.

## Fuera de alcance

- Declarar conexión real si solo existe dry-run.
- Versionar secretos, claves privadas reales o credenciales operativas.
- Tratar LAB 03 como un único firmware monolítico.

## Hardware requerido

- ESP32-S3 compatible.
- Cable USB de datos.
- Consola USB Serial/JTAG para fases dry-run.
- Conectividad Wi-Fi solo cuando el sublaboratorio declare conexión real.

## Software requerido

- Git.
- Python 3.
- ESP-IDF compatible con ESP32-S3.
- PowerShell o terminal equivalente.

## Arquitectura prevista

```text
lab03_mqtt/
├── common/
├── docs/
├── evidence/
├── tools/
├── lab03a_m03_1883_plain_no_auth/
├── lab03b_m03_1884_plain_auth/
├── lab03c_m03_8883_8886_tls_server_auth/
├── lab03d_m03_8885_tls_userpass/
├── lab03e_m03_8884_mtls_client_cert/
├── lab03f_m03_8887_expired_cert_rejection/
└── lab03g_m03_websockets/
```

La carpeta superior contiene contrato común, documentación de matriz, gates agregados y evidencias transversales. Cada sublaboratorio mantiene su propio cierre documental y técnico.

## Modelo temporal

Las fases dry-run usan interacción por consola. No hay tareas de red reales ni dependencia temporal externa.
Cuando se introduzca conexión real, el sublaboratorio deberá documentar tareas, timeouts, retry, backoff y deadlines.

## Threat model

Amenazas mínimas:

- exposición de credenciales;
- ausencia de confidencialidad;
- validación incorrecta de certificados;
- uso de broker público;
- publicación accidental de secretos;
- confusión entre autenticación y cifrado.

## Requisitos

- Logs sin secretos.
- Evidencias reproducibles.
- Gates globales y específicos en PASS.
- Separación explícita entre dry-run y conexión real.
- Estados `CUMPLE`, `NO CUMPLE`, `NO VALIDADO` y `PENDIENTE`.

## Cómo compilar

Para LAB 03A:

```powershell
cd labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/firmware
idf.py set-target esp32s3
idf.py build
```

## Cómo flashear

Para LAB 03A:

```powershell
idf.py -p COMx flash monitor
```

Sustituir `COMx` por el puerto real.

## Cómo probar

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
python labs/lab03_mqtt/tools/run_static_gates.py
python labs/lab03_mqtt/tools/capture_static_gates.py
```

## Evidencias esperadas

- Evidencia agregada de gates: `evidence/lab03_static_gates.txt`.
- Evidencia LAB 03A: `lab03a_m03_1883_plain_no_auth/evidence/lab03_m03_1883_console.log`.
- Evidencias propias para LAB 03B y siguientes cuando se implementen.

## Errores comunes

- Confundir autenticación con confidencialidad.
- Declarar seguro un escenario sin TLS.
- Mantener rutas legacy tras una migración.
- Reutilizar evidencias de otro sublaboratorio.

## Ejercicios

- Clasificar cada escenario como funcional, inseguro, mitigado o no validado.
- Identificar qué activo protege cada mitigación.
- Revisar si los logs contienen secretos.

## Preguntas de repaso

- ¿Por qué usuario/password sin TLS no protege credenciales?
- ¿Qué diferencia hay entre TLS y mTLS?
- ¿Por qué un certificado expirado debe provocar fallo de conexión?

## Fuentes

- Documentación pública de `test.mosquitto.org`.
- Documentación oficial de ESP-IDF.
- Estándar audit-grade interno del proyecto.

## Estado

```text
CUMPLE:
- LAB 03 queda modelado como familia MQTT.
- LAB 03A queda aislado como sublaboratorio para M03-1883.

NO VALIDADO:
- LAB 03B y posteriores no están cerrados.
- Conexión MQTT real todavía no forma parte del cierre dry-run.

PENDIENTE:
- Continuar con LAB 03B después de cerrar gates y evidencia estática.
```
