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
- [Evidencias esperadas](#evidencias-esperadas)
- [Errores comunes](#errores-comunes)
- [Ejercicios](#ejercicios)
- [Preguntas de repaso](#preguntas-de-repaso)
- [Fuentes](#fuentes)
- [Estado](#estado)

## Objetivo

Demostrar por qué una identidad de dispositivo no debe ser hardcoded, clonable ni mutable por consola, y cómo derivar un identificador estable desde material de hardware sin exponer identificadores brutos.

## Objetivos de aprendizaje

- Diferenciar identificador público, identidad local y autenticación.
- Observar el riesgo de identidades clonables.
- Observar el riesgo de comandos `set_device_id` sin política.
- Comparar identidad hardcoded frente a identidad derivada de eFuse MAC + SHA-256 truncado.
- Entender que un identificador no es un secreto ni sustituye autenticación.
- Capturar evidencias INSECURE/HARDENED automatizadas.

## Prerrequisitos

- ESP-IDF instalado.
- ESP32-S3 con USB Serial/JTAG operativo.
- Python 3 con `pyserial` para captura automática.
- Lectura del estándar `standard/estandar_diseno_embebido_audit_grade.md`.

## Alcance

Este laboratorio cubre identidad local de dispositivo, exposición de identificadores, mutabilidad por consola y claims didácticos.

## Fuera de alcance

```text
- Certificados X.509 reales.
- Secure element.
- TLS mutuo.
- Provisioning industrial.
- NVS segura.
- Secure Boot activo.
- Flash Encryption activa.
- Producción.
```

## Hardware requerido

- ESP32-S3 DevKit o equivalente.
- Cable USB de datos conectado al puerto USB nativo.

## Software requerido

- ESP-IDF compatible con ESP32-S3.
- Python 3.
- pyserial.
- Git.

## Arquitectura prevista

El firmware está en `firmware/` y usa arquitectura por componentes:

```text
main → app_core → command_console/identity_service/security_status/secure_log/board_hal
```

La documentación detallada está en `docs/architecture.md`.

## Modelo temporal

Modelo event-driven cooperativo por consola. No hay tareas periódicas propias ni ISR de aplicación.

Ver `docs/temporal_model.md` y `docs/concurrency_model.md`.

## Threat model

Amenaza principal: usuario local con acceso a consola capaz de leer identidad, clonar identificadores o intentar modificar el `device_id`.

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

Comandos disponibles:

```text
help
identity_status
get_identity
get_claim
set_device_id CLONED-DEVICE-001
security_status
```

Captura automática desde la raíz del repo:

```powershell
python labs\lab02_device_identity\tools\capture_console_evidence.py --port COMx --profile insecure --output labs\lab02_device_identity\evidence\lab02_insecure_console.log
python labs\lab02_device_identity\tools\capture_console_evidence.py --port COMx --profile hardened --output labs\lab02_device_identity\evidence\lab02_hardened_console.log
python labs\lab02_device_identity\tools\capture_static_gates.py
```

Validación de logs:

```powershell
python labs\lab02_device_identity\tools\check_lab02_identity_logs.py labs\lab02_device_identity\evidence\lab02_insecure_console.log --profile insecure
python labs\lab02_device_identity\tools\check_lab02_identity_logs.py labs\lab02_device_identity\evidence\lab02_hardened_console.log --profile hardened
```

## Evidencias esperadas

Evidencias versionadas:

```text
evidence/lab02_insecure_console.log
evidence/lab02_hardened_console.log
evidence/lab02_static_gates.txt
```

Evidencias pendientes para cierre completo audit-grade:

```text
evidence/lab02_build_esp32s3.txt
```

## Errores comunes

- Capturar `INSECURE` con firmware `HARDENED` cargado.
- Ignorar un mismatch de perfil detectado por el script de captura.
- Confundir identidad pública con autenticación.
- Exponer raw MAC en HARDENED.
- Versionar logs con tokens reales.
- Flashear con target incorrecto (`esp32` en vez de `esp32s3`).

## Ejercicios

1. Demuestra que `INSECURE` permite cambiar `device_id` desde consola.
2. Demuestra que `INSECURE` genera un claim clonable con token compartido ficticio.
3. Demuestra que `HARDENED` rechaza `set_device_id`.
4. Demuestra que `HARDENED` redacta `raw_hardware_id`.
5. Explica por qué `auth_token="not_applicable"` no equivale a autenticación.

## Preguntas de repaso

1. ¿Por qué una identidad hardcoded es clonable?
2. ¿Por qué una identidad no debe ser mutable por consola en campo?
3. ¿Qué aporta derivar un identificador de eFuse MAC con hash?
4. ¿Por qué raw MAC puede considerarse dato sensible de inventario?
5. ¿Qué diferencia hay entre identidad y autenticación?

## Fuentes

Ver `docs/references.md` y la bibliografía global del repositorio.

## Estado

```text
CUMPLE:
- README con índice obligatorio.
- Firmware ESP-IDF para ESP32-S3 añadido.
- Documentación audit-grade del laboratorio añadida.
- Gates estáticos del laboratorio añadidos.
- Consola USB Serial/JTAG validada en hardware.
- Perfil INSECURE validado con evidencia automática.
- Perfil HARDENED validado con evidencia automática.
- Logs HARDENED redactan raw_hardware_id.
- set_device_id queda bloqueado en HARDENED.
- Gates estáticos capturados con PASS.

NO CUMPLE:
- No es firmware de producción.
- No implementa certificados, TLS mutuo, Secure Boot ni Flash Encryption activa.

NO VALIDADO:
- Build completo con cero warnings pendiente de evidencia stdout versionada.

PENDIENTE:
- Capturar `idf.py build` completo en `evidence/lab02_build_esp32s3.txt`.
- Revisar CI tras push.
```
