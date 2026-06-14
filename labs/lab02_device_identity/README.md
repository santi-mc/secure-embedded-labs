# LAB 02 — Identidad única de dispositivo

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
- [Captura automática de evidencias](#captura-automática-de-evidencias)
- [Evidencias esperadas](#evidencias-esperadas)
- [Errores comunes](#errores-comunes)
- [Ejercicios](#ejercicios)
- [Preguntas de repaso](#preguntas-de-repaso)
- [Fuentes](#fuentes)
- [Estado](#estado)

## Objetivo

Demostrar por qué la identidad de dispositivo no debe ser un identificador hardcodeado, clonado o editable por consola, y cómo generar una identidad pública estable a partir de una fuente de identidad hardware sin exponer datos sensibles ni confundir identidad con autenticación.

## Objetivos de aprendizaje

- Diferenciar identidad pública, autenticación y secretos.
- Detectar el riesgo de usar IDs hardcodeados o compartidos entre dispositivos.
- Detectar el riesgo de exponer MAC/eFuse en logs operativos.
- Comparar identidad clonable `INSECURE` frente a identidad derivada `HARDENED`.
- Diseñar logs de identidad sin secretos y con trazabilidad.
- Validar evidencias de consola y gates estáticos.
- Automatizar la captura de evidencias sin editar logs manualmente.

## Prerrequisitos

- ESP-IDF instalado.
- Conocimientos básicos de C++ embebido.
- Lectura del estándar `standard/estandar_diseno_embebido_audit_grade.md`.
- Haber completado o leído el LAB 01.

## Alcance

Este laboratorio cubre identidad local de dispositivo en ESP32-S3 usando consola USB Serial/JTAG, eFuse MAC como fuente hardware no secreta y derivación local de un `device_id` público estable.

## Fuera de alcance

```text
- Provisioning PKI real
- Certificados cliente TLS
- Secure Element
- NVS cifrada
- Attestation remota real
- Alta de dispositivos en backend
- Producción
```

## Hardware requerido

- ESP32-S3 DevKit o equivalente.
- Cable USB de datos conectado al puerto USB nativo.

## Software requerido

- ESP-IDF compatible con ESP32-S3.
- Python 3.
- Git.
- `pyserial` para captura automática de consola:

```powershell
python -m pip install pyserial
```

## Arquitectura prevista

El firmware está en `firmware/` y usa arquitectura por componentes:

```text
main → app_core → command_console/identity_service/security_status/secure_log/board_hal
```

Componentes principales:

```text
lab02_domain      → contratos, perfiles, interfaces y versión
board_hal         → reloj, consola stdio y fuente de identidad hardware
identity_service  → política de identidad INSECURE/HARDENED
command_console   → comandos de laboratorio
secure_log        → logs JSON/NDJSON sin secretos en HARDENED
security_status   → estado de seguridad del target
app_core          → composición de aplicación
```

Ver `docs/architecture.md`.

## Modelo temporal

Modelo event-driven cooperativo por consola bloqueante con backoff cuando no hay datos. No hay tareas periódicas propias ni ISR de aplicación.

Ver `docs/temporal_model.md` y `docs/concurrency_model.md`.

## Threat model

Amenaza principal: operador local o atacante con acceso a consola capaz de leer identidad, copiar claims, modificar IDs o recopilar identificadores hardware.

Ver `docs/threat_model.md`.

## Requisitos

Los requisitos están en:

```text
docs/requirements.md
docs/security_requirements.md
```

## Cómo compilar

Desde la raíz del laboratorio:

```powershell
python tools/run_static_gates.py
cd firmware
idf.py set-target esp32s3
idf.py build
```

Para seleccionar perfil:

```powershell
idf.py menuconfig
```

Ruta de configuración:

```text
Secure IoT LAB 02 → Active identity profile
```

## Cómo flashear

Desde `firmware/`:

```powershell
idf.py -p COMx flash monitor
```

Sustituye `COMx` por el puerto USB Serial/JTAG detectado.

## Cómo probar

Dentro del monitor:

```text
help
identity_status
get_identity
get_claim
set_device_id LAB02-CLONED-ID
security_status
```

Secuencia completa en `test/manual_lab02_commands.txt`.

## Captura automática de evidencias

La captura automática se hace con `tools/capture_console_evidence.py`. El script no cambia el perfil, no compila y no flashea: primero hay que cargar el firmware con el perfil correspondiente.

### Capturar INSECURE

1. Selecciona `INSECURE` en `idf.py menuconfig`.
2. Compila y flashea.
3. Ejecuta desde la raíz del repo:

```powershell
python labs/lab02_device_identity/tools/capture_console_evidence.py `
  --port COMx `
  --profile insecure `
  --output labs/lab02_device_identity/evidence/lab02_insecure_console.log
```

### Capturar HARDENED

1. Selecciona `HARDENED` en `idf.py menuconfig`.
2. Compila y flashea.
3. Ejecuta desde la raíz del repo:

```powershell
python labs/lab02_device_identity/tools/capture_console_evidence.py `
  --port COMx `
  --profile hardened `
  --output labs/lab02_device_identity/evidence/lab02_hardened_console.log
```

### Wrapper PowerShell

También se puede usar:

```powershell
labs/lab02_device_identity/tools/capture_console_evidence.ps1 `
  -Port COMx `
  -Profile insecure

labs/lab02_device_identity/tools/capture_console_evidence.ps1 `
  -Port COMx `
  -Profile hardened
```

### Capturar gates estáticos

```powershell
python labs/lab02_device_identity/tools/capture_static_gates.py
```

Esto genera:

```text
labs/lab02_device_identity/evidence/lab02_static_gates.txt
```

## Evidencias esperadas

Evidencias a capturar:

```text
evidence/lab02_insecure_console.log
evidence/lab02_hardened_console.log
evidence/lab02_static_gates.txt
evidence/lab02_build_esp32s3.txt
```

Validación esperada:

```powershell
python labs/lab02_device_identity/tools/check_lab02_identity_logs.py labs/lab02_device_identity/evidence/lab02_insecure_console.log --profile insecure
python labs/lab02_device_identity/tools/check_lab02_identity_logs.py labs/lab02_device_identity/evidence/lab02_hardened_console.log --profile hardened
```

## Errores comunes

- Confundir identidad pública con secreto de autenticación.
- Usar el mismo `device_id` hardcodeado en todos los dispositivos.
- Exponer MAC/eFuse sin necesidad operativa.
- Permitir que una consola local cambie el identificador estable en HARDENED.
- Considerar una identidad derivada como sustituto de certificados o claves privadas.
- Ignorar avisos de checksum mismatch entre imagen compilada y flasheada.
- Capturar logs con un perfil distinto al indicado por el nombre del fichero.
- Editar manualmente logs para que pasen el scanner.

## Ejercicios

1. Demuestra que el perfil `INSECURE` arranca con un `device_id` clonable.
2. Demuestra que `set_device_id LAB02-CLONED-ID` es aceptado en `INSECURE`.
3. Demuestra que `get_claim` en `INSECURE` expone un token compartido de laboratorio.
4. Demuestra que `HARDENED` deriva un `device_id` estable y no editable.
5. Demuestra que `HARDENED` no expone MAC ni token de autenticación.
6. Ejecuta el scanner de logs y guarda la evidencia.
7. Genera logs automáticamente y compáralos contra la captura manual.

## Preguntas de repaso

1. ¿Por qué un `device_id` hardcodeado es clonable?
2. ¿Por qué identidad no equivale a autenticación?
3. ¿Cuándo puede ser aceptable derivar una identidad pública desde un identificador hardware?
4. ¿Por qué no deben aparecer secretos en claims ni logs?
5. ¿Qué evidencias mínimas cierran el LAB 02?
6. ¿Por qué la captura automatizada reduce errores de auditoría?

## Fuentes

Ver `docs/references.md` y la bibliografía global del repositorio.

## Estado

```text
CUMPLE:
- README con índice obligatorio.
- Firmware ESP-IDF para ESP32-S3 añadido.
- Documentación audit-grade inicial añadida.
- Gates estáticos del laboratorio añadidos.
- Script de captura automática de consola añadido.
- Script de captura de gates estáticos añadido.
- Build y flash validados por el operador tras corregir toString(profile).
- Perfil INSECURE validado funcionalmente por el operador.
- Perfil HARDENED validado funcionalmente por el operador.

NO CUMPLE:
- No es firmware de producción.
- No implementa PKI, TLS cliente, Secure Element ni attestation remota real.

NO VALIDADO:
- Evidencias generadas automáticamente pendientes de commit.
- Build completo con cero warnings pendiente de evidencia stdout versionada.

PENDIENTE:
- Ejecutar captura automática INSECURE.
- Ejecutar captura automática HARDENED.
- Ejecutar captura automática de gates.
- Capturar `idf.py build` completo en `evidence/lab02_build_esp32s3.txt`.
- Revisar CI tras push.
```
