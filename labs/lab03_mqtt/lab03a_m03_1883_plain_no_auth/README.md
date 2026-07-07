# LAB 03A — M03-1883 / MQTT TCP plano sin autenticación

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

Demostrar el baseline MQTT TCP plano sin TLS y sin autenticación.

## Objetivos de aprendizaje

- Separar comportamiento funcional de clasificación de seguridad.
- Mantener logs parseables y sin secretos reales.
- Generar evidencias reproducibles del escenario.
- Conservar trazabilidad con la matriz contractual de LAB 03.

## Prerrequisitos

- Repositorio limpio de artefactos generados.
- Python 3 disponible.
- ESP-IDF disponible cuando el sublaboratorio incluya firmware.
- Lectura previa de `README.md`, `ROADMAP.md` y `labs/README.md`.

## Alcance

Este sublaboratorio cubre `M03-1883` sobre `test.mosquitto.org`, puerto `1883`, TLS `false` y autenticación `false`.

## Fuera de alcance

- Uso de secretos reales.
- Producción.
- Mezclar el resultado con otros escenarios MQTT.
- Declarar conexión real sin evidencia específica.

## Hardware requerido

- ESP32-S3 compatible con ESP-IDF para los sublaboratorios con firmware.
- Cable USB de datos para alimentación, flasheo y consola.
- Para fases dry-run no se requiere conectividad Wi-Fi real.
- Para conexión real se documentará red, broker, timeout y limitaciones.

## Software requerido

- Git.
- Python 3.
- ESP-IDF compatible con ESP32-S3.
- PowerShell o terminal equivalente.
- Herramientas del repositorio bajo `tools/` y `labs/lab03_mqtt/tools/`.

## Arquitectura prevista

El sublaboratorio mantiene documentación, firmware, herramientas, pruebas y evidencias propias. La familia `lab03_mqtt/` aporta matriz común y gates agregados.

## Modelo temporal

Las fases dry-run usan interacción por consola y no ejecutan tareas de red reales. Cuando exista conexión real, los timeouts, retries, callbacks y deadlines deberán documentarse aquí.

## Threat model

- Exposición de credenciales o payloads.
- Ausencia o mala configuración de TLS.
- Confusión entre autenticación y confidencialidad.
- Uso de broker público de pruebas.
- Logs con información sensible.

## Requisitos

- No registrar secretos reales.
- Distinguir `CUMPLE`, `NO CUMPLE`, `NO VALIDADO` y `PENDIENTE`.
- Mantener evidencia propia del sublaboratorio.
- Pasar gate global y gate LAB 03 antes de cierre.

## Cómo compilar

```powershell
cd labs\lab03_mqtt\lab03a_m03_1883_plain_no_auth\firmware
idf.py set-target esp32s3
idf.py build
```

## Cómo flashear

```powershell
cd labs\lab03_mqtt\lab03a_m03_1883_plain_no_auth\firmware
idf.py -p COMx flash monitor
```

## Cómo probar

```powershell
python labs\lab03_mqtt\lab03a_m03_1883_plain_no_auth\tools\check_mqtt_scenario_logs.py labs\lab03_mqtt\lab03a_m03_1883_plain_no_auth\evidence\lab03_m03_1883_console.log --scenario M03-1883
```

## Evidencias esperadas

- `evidence/lab03_m03_1883_console.log`.
- `../../evidence/lab03_static_gates.txt`.

## Errores comunes

- Confundir autenticación con confidencialidad.
- Declarar seguro un escenario sin TLS.
- Declarar conexión real validada cuando solo existe dry-run.
- Versionar `build/`, `sdkconfig`, `sdkconfig.old`, `managed_components` o `__pycache__`.
- Reutilizar evidencias de otro laboratorio.

## Ejercicios

- Clasificar el escenario como funcional, inseguro, mitigado o no validado.
- Identificar qué activo protege cada mitigación.
- Revisar si los logs contienen secretos.
- Relacionar cada evidencia con el requisito que valida.

## Preguntas de repaso

- ¿Qué diferencia hay entre conectividad funcional y cumplimiento de seguridad?
- ¿Qué evidencia demuestra que el escenario fue probado?
- ¿Qué condición impide declarar `CUMPLE`?
- ¿Qué queda fuera de alcance en dry-run?

## Fuentes

- Documentación del repositorio.
- Estándar audit-grade del proyecto.
- Documentación oficial de ESP-IDF cuando aplique.
- Documentación pública de `test.mosquitto.org` para LAB 03.

## Estado

```text
CUMPLE:
- Dry-run de M03-1883 validado.
- Evidencia de consola disponible.
- Clasificación de seguridad: funcional, pero NO CUMPLE como diseño seguro.

NO VALIDADO:
- Conexión real MQTT.

PENDIENTE:
- Mantener evidencia tras cualquier cambio estructural.
```
