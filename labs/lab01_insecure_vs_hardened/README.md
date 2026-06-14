# LAB 01 — Firmware inseguro vs firmware endurecido

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

Demostrar, de forma controlada y reproducible, cómo un firmware embebido puede exponer secretos y aceptar configuración inválida por una consola local, y cómo mitigar esos fallos mediante un perfil endurecido.

## Objetivos de aprendizaje

- Entender que una consola local también es superficie de ataque.
- Observar cómo `get_config` y los logs pueden filtrar secretos.
- Comparar parsing débil frente a parsing estricto.
- Aplicar redacción de secretos en logs.
- Diferenciar vulnerabilidad intencionada de precariedad accidental.
- Practicar evidencias `INSECURE` vs `HARDENED`.

## Prerrequisitos

- ESP-IDF instalado.
- Python 3 con `pyserial` para captura automática.
- Conocimientos básicos de C++ embebido.
- Lectura del estándar `standard/estandar_diseno_embebido_audit_grade.md`.
- Hardware ESP32-S3 con USB Serial/JTAG operativo.

## Alcance

Este laboratorio cubre seguridad local de consola, logs, secretos ficticios y validación de configuración en RAM.

## Fuera de alcance

```text
- MQTT/TLS
- OTA
- Secure Boot activo
- Flash Encryption activa
- NVS segura
- Ataques remotos
- Producción
```

## Hardware requerido

- ESP32-S3 DevKit o equivalente.
- Cable USB de datos conectado al puerto USB nativo.

## Software requerido

- ESP-IDF compatible con ESP32-S3.
- Python 3.
- `pyserial` para `tools/capture_console_evidence.py`.
- Git.

## Arquitectura prevista

El firmware está en `firmware/` y usa arquitectura por componentes:

```text
main → app_core → command_console/app_config/sensor_sim/security_status/secure_log/board_hal
```

La documentación detallada está en `docs/architecture.md`.

## Modelo temporal

Modelo event-driven cooperativo por consola bloqueante. No hay tareas periódicas propias ni ISR de aplicación.

Ver `docs/temporal_model.md` y `docs/concurrency_model.md`.

## Threat model

Amenaza principal: usuario local con acceso a consola/monitor serie capaz de leer logs y ejecutar comandos.

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
Secure IoT LAB 01 → Active security profile
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
get_config
set_period 0
set_period 10abc
set_mqtt_password LAB01_TEST_PASSWORD
get_config
factory_reset
security_status
```

Secuencia completa en `test/manual_lab01_commands.txt`.

## Captura automática de evidencias

Instala `pyserial` si no está disponible:

```powershell
python -m pip install pyserial
```

Con el firmware `INSECURE` ya compilado y flasheado:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py `
  --port COMx `
  --profile insecure `
  --output labs\lab01_insecure_vs_hardened\evidence\lab01_insecure_console.log
```

Con el firmware `HARDENED` ya compilado y flasheado:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py `
  --port COMx `
  --profile hardened `
  --output labs\lab01_insecure_vs_hardened\evidence\lab01_hardened_console.log
```

Captura de gates estáticos:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_static_gates.py
```

Captura del scanner de secretos:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_secret_scan.py
```

## Evidencias esperadas

Evidencias automatizadas versionables:

```text
evidence/lab01_insecure_console.log
evidence/lab01_hardened_console.log
evidence/lab01_static_gates.txt
evidence/lab01_secret_scan.txt
```

Evidencia aún pendiente para cierre audit-grade completo:

```text
evidence/lab01_build_esp32s3.txt
```

Validación manual equivalente de logs:

```powershell
python labs\lab01_insecure_vs_hardened\tools\check_no_secrets_in_logs.py labs\lab01_insecure_vs_hardened\evidence\lab01_insecure_console.log --profile insecure
python labs\lab01_insecure_vs_hardened\tools\check_no_secrets_in_logs.py labs\lab01_insecure_vs_hardened\evidence\lab01_hardened_console.log --profile hardened
```

## Errores comunes

- Usar el puerto UART externo en vez del USB Serial/JTAG nativo.
- Probar solo un perfil y considerar cerrado el laboratorio.
- Usar una contraseña real en `set_mqtt_password`.
- Guardar metadatos de captura con comandos sensibles en claro.
- No validar que el perfil observado coincide con el perfil solicitado.
- Confundir `INSECURE` didáctico con firmware válido para producción.
- Ignorar avisos de checksum mismatch entre imagen compilada y flasheada.
- Usar un HUB USB inestable durante la validación.

## Ejercicios

1. Captura la fuga de `mqtt_password` en perfil `INSECURE`.
2. Demuestra que `set_period 25s` queda aceptado en `INSECURE` por parsing débil.
3. Demuestra que `set_period 25s` queda rechazado en `HARDENED`.
4. Demuestra que `set_period 0` queda rechazado en `HARDENED`.
5. Demuestra que `set_mqtt_password` no aparece en bruto en logs `HARDENED`.
6. Regenera las evidencias con `capture_console_evidence.py` y valida que ambas tienen `capture_validation result=PASS`.

## Preguntas de repaso

1. ¿Por qué `get_config` puede ser una fuga de información?
2. ¿Por qué loguear comandos brutos es peligroso?
3. ¿Qué diferencia hay entre validar sintaxis y validar rango?
4. ¿Por qué `factory_reset` debe tener política de autorización?
5. ¿Por qué una evidencia debe validar el perfil real observado y no solo el nombre del fichero?

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
- Perfil INSECURE validado en hardware como demostración vulnerable.
- Perfil HARDENED validado en hardware como mitigación.
- Logs HARDENED redactan secretos.
- factory_reset queda bloqueado en HARDENED.
- Captura automática de evidencias añadida.

NO CUMPLE:
- No es firmware de producción.
- No implementa red, TLS, OTA, Secure Boot ni Flash Encryption activa.

NO VALIDADO:
- Build completo con cero warnings pendiente de evidencia stdout versionada.

PENDIENTE:
- Regenerar evidencias con scripts automáticos.
- Capturar `idf.py build` completo en `evidence/lab01_build_esp32s3.txt`.
- Revisar CI tras push.
```
