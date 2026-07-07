# LAB 03A — M03-1883 / MQTT TCP plano sin autenticación

**Estado:** CUMPLE dry-run
**Escenario:** M03-1883
**Puerto:** 1883


## Ãndice

- [Índice](#indice)
- [Objetivo](#objetivo)
- [Objetivos de aprendizaje](#objetivos-de-aprendizaje)
- [Prerrequisitos](#prerrequisitos)
- [Hardware requerido](#hardware-requerido)
- [Alcance](#alcance)
- [Fuera de alcance](#fuera-de-alcance)
- [Estructura](#estructura)
- [Evidencias](#evidencias)
- [Estado](#estado)
- [Software requerido](#software-requerido)
- [EjecuciÃ³n](#ejecucia3n)
- [Limitaciones conocidas](#limitaciones-conocidas)

## Índice

- [Ãndice](#andice)
- [Objetivo](#objetivo)
- [Objetivos de aprendizaje](#objetivos-de-aprendizaje)
- [Prerrequisitos](#prerrequisitos)
- [Hardware requerido](#hardware-requerido)
- [Alcance](#alcance)
- [Fuera de alcance](#fuera-de-alcance)
- [Estructura](#estructura)
- [Evidencias](#evidencias)
- [Estado](#estado)
- [Software requerido](#software-requerido)
- [EjecuciÃ³n](#ejecucia3n)
- [Limitaciones conocidas](#limitaciones-conocidas)
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

## Objetivo

Demostrar el baseline MQTT TCP plano sin TLS y sin autenticación.

## Objetivos de aprendizaje

- Separar comportamiento funcional de clasificación de seguridad.
- Mantener logs parseables y sin secretos reales.
- Generar evidencias reproducibles del escenario.
- Conservar trazabilidad con la matriz contractual de `../docs/scenario_matrix.md`.

## Prerrequisitos

- Revisar el README de la familia `../README.md`.
- Mantener limpio el árbol de artefactos generados.
- No usar secretos reales contra `test.mosquitto.org`.

## Hardware requerido

- ESP32-S3 compatible con ESP-IDF.
- Consola USB Serial/JTAG operativa.
- Cable USB de datos.
- No requiere conectividad Wi-Fi ni broker real en la fase dry-run.

## Alcance

Este directorio contiene el contrato, la implementación y las evidencias propias del escenario `M03-1883`.

## Fuera de alcance

- Reutilizar evidencias de otro sublaboratorio como si fueran propias.
- Mezclar firmware o herramientas de escenarios distintos sin declaración explícita en `../common/`.
- Declarar conexión real validada si solo existe dry-run.

## Estructura

```text
lab03a_m03_1883_plain_no_auth/
├── README.md
├── CHANGELOG.md
├── docs/
├── evidence/
├── firmware/
├── test/
└── tools/
```

## Evidencias

Las evidencias de este sublaboratorio deben residir en `evidence/`.

## Estado

```text
CUMPLE:
- Firmware dry-run y evidencia de consola M03-1883 migrados desde la estructura anterior.
- El escenario queda aislado como sublaboratorio independiente.

NO CUMPLE:
- MQTT TCP plano sin TLS no es seguro para datos sensibles.

NO VALIDADO:
- Conexión real al broker.
- Build formal cero warnings si no existe evidencia adicional.

PENDIENTE:
- Mantener gates y documentación alineados tras la migración.
```

## Software requerido

- Git.
- Python 3.
- ESP-IDF compatible con el target ESP32-S3.
- PowerShell o terminal equivalente.
- Herramientas del repositorio bajo `tools/` y `labs/lab03_mqtt/tools/`.

## EjecuciÃ³n

Ejecutar siempre desde la raÃ­z del repositorio salvo que el comando indique otra ruta.

```powershell
python tools
epo_quality_gates
un_static_repo_gates.py
python labs\lab03_mqtt	ools
un_static_gates.py
```

## Limitaciones conocidas

- El broker `test.mosquitto.org` es pÃºblico y puede no estar disponible permanentemente.
- No deben publicarse secretos reales.
- Las fases dry-run validan contrato local, no conectividad real.

## Arquitectura prevista

La arquitectura prevista separa documentación, firmware, pruebas, herramientas y evidencias.

En LAB 03, `lab03_mqtt/` actúa como familia MQTT y cada sublaboratorio `lab03a`...`lab03g` debe cerrarse de forma independiente.

## Modelo temporal

Las fases dry-run usan interacción por consola y no ejecutan tareas de red reales.

Cuando se introduzca conexión real, cada tarea, timeout, retry y deadline deberá quedar documentado en el sublaboratorio correspondiente.

## Threat model

El threat model mínimo considera:

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
- Separación clara entre dry-run y conexión real.
- Estado explícito `CUMPLE`, `NO CUMPLE`, `NO VALIDADO` y `PENDIENTE`.

## Cómo compilar

Cuando el sublaboratorio incluya firmware:

```powershell
cd labs\lab03_mqtt\lab03a_m03_1883_plain_no_auth\firmware
idf.py set-target esp32s3
idf.py build
```

La ruta debe ajustarse al sublaboratorio correspondiente.

## Cómo flashear

Cuando el sublaboratorio incluya firmware:

```powershell
idf.py -p COMx flash monitor
```

Debe sustituirse `COMx` por el puerto real.

## Cómo probar

Ejecutar primero gates directos:

```powershell
python tools\repo_quality_gates\run_static_repo_gates.py
python labs\lab03_mqtt\tools\run_static_gates.py
```

Después capturar evidencia estática cuando aplique.

## Evidencias esperadas

- Evidencia de consola cuando aplique.
- Evidencia de gates estáticos.
- Evidencia de build si se declara compilación validada.
- Evidencia de conexión real solo cuando exista prueba de red documentada.

## Errores comunes

- Confundir autenticación con confidencialidad.
- Declarar seguro un escenario sin TLS.
- Versionar `build/`, `sdkconfig` o `sdkconfig.old`.
- Reutilizar evidencias de otro laboratorio.
- Mantener rutas legacy tras una migración.

## Ejercicios

- Identificar qué activo protege cada mitigación.
- Clasificar el escenario como funcional, inseguro, mitigado o no validado.
- Revisar si los logs contienen secretos.

## Preguntas de repaso

- ¿Qué diferencia hay entre autenticación y cifrado?
- ¿Qué evidencia demuestra que el escenario fue probado?
- ¿Qué condición impide declarar `CUMPLE`?
- ¿Qué parte queda fuera de alcance en dry-run?

## Fuentes

- Documentación del repositorio.
- Documentación oficial de ESP-IDF cuando aplique.
- Documentación pública de `test.mosquitto.org` para LAB 03.
- Estándar interno audit-grade del proyecto.
