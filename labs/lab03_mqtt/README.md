# LAB 03 — Familia MQTT contra test.mosquitto.org

**Versión:** 0.2.0
**Estado:** EN CURSO
**Modelo:** familia de sublaboratorios independientes


## Ãndice

- [Índice](#indice)
- [Objetivo](#objetivo)
- [Objetivos de aprendizaje](#objetivos-de-aprendizaje)
- [Prerrequisitos](#prerrequisitos)
- [Hardware requerido](#hardware-requerido)
- [Alcance](#alcance)
- [Fuera de alcance](#fuera-de-alcance)
- [Estructura](#estructura)
- [Matriz contractual](#matriz-contractual)
- [Arquitectura](#arquitectura)
- [Cómo trabajar](#como-trabajar)
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
- [Matriz contractual](#matriz-contractual)
- [Arquitectura](#arquitectura)
- [Cómo trabajar](#como-trabajar)
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

Agrupar una matriz reproducible de escenarios MQTT contra `test.mosquitto.org`, separando cada puerto/propiedad de seguridad en sublaboratorios auditables.

LAB 03 no es un único firmware monolítico ni un laboratorio exclusivamente TLS. Es una familia de pruebas MQTT que cubre MQTT plano, autenticación sin TLS, TLS, TLS con credenciales, mTLS, rechazo de certificado expirado y MQTT over WebSockets.

## Objetivos de aprendizaje

- Distinguir conectividad funcional de diseño seguro.
- Comparar MQTT plano, MQTT autenticado, MQTT sobre TLS, mTLS y MQTT over WebSockets.
- Evidenciar que usuario/password sin TLS no protege credenciales.
- Evidenciar que una conexión TLS solo es aceptable si valida correctamente el certificado del servidor.
- Mantener trazabilidad escenario → diseño → firmware → test → evidencia.

## Prerrequisitos

- ESP32-S3 compatible con ESP-IDF.
- Consola USB Serial/JTAG operativa para los sublaboratorios dry-run.
- Python 3 para herramientas de captura y gates.
- Acceso de red a `test.mosquitto.org` solo cuando se introduzcan conexiones reales.
- Ningún secreto real debe usarse en el broker público.

## Hardware requerido

La familia `lab03_mqtt` actúa como contenedor documental y contractual. Los requisitos ejecutables se declaran en cada sublaboratorio.

Mínimo común previsto:

- ESP32-S3 compatible con ESP-IDF.
- Consola USB Serial/JTAG operativa para fases dry-run.
- Cable USB de datos.
- Conectividad Wi-Fi solo en fases de conexión real.
- Broker público `test.mosquitto.org` solo para validaciones reales, nunca para secretos reales.

## Alcance

Esta carpeta define el contrato común de la familia LAB 03 y contiene sublaboratorios independientes:

```text
lab03_mqtt/
├── README.md
├── CHANGELOG.md
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

## Fuera de alcance

- Mezclar todos los escenarios en un único laboratorio ejecutable.
- Tratar `lab03_mqtt/` como firmware final único.
- Versionar secretos reales, claves privadas reales o credenciales operativas.
- Declarar conexión real validada cuando solo exista dry-run.

## Estructura

- `docs/`: contrato común, matriz, política de broker, certificados, riesgos y evidencias agregadas.
- `evidence/`: evidencias agregadas de la familia, especialmente gates estáticos.
- `tools/`: gates y herramientas agregadas de la familia.
- `common/`: componentes reutilizables, helpers y contratos compartidos.
- `lab03a...lab03g/`: sublaboratorios con README, CHANGELOG, docs, evidence, firmware, test y tools propios.

## Matriz contractual

| Sublab | Escenario | Puerto | TLS | Auth | Estado |
| --- | --- | ---: | --- | --- | --- |
| LAB 03A | M03-1883 | 1883 | No | No | CUMPLE dry-run |
| LAB 03B | M03-1884 | 1884 | No | Usuario/password | PENDIENTE |
| LAB 03C | M03-8883 / M03-8886 | 8883 / 8886 | Sí | No | PENDIENTE |
| LAB 03D | M03-8885 | 8885 | Sí | Usuario/password | PENDIENTE |
| LAB 03E | M03-8884 | 8884 | Sí | Certificado cliente | PENDIENTE |
| LAB 03F | M03-8887 | 8887 | Sí, expirado | No | PENDIENTE |
| LAB 03G | M03-8080/8081/8090/8091 | 8080/8081/8090/8091 | Mixto | Mixto | PENDIENTE |

## Arquitectura

La arquitectura se divide en dos niveles:

```text
Familia LAB 03
├── contrato común MQTT
├── matriz de escenarios
├── política de broker público
├── gates agregados
└── sublaboratorios independientes

Sublaboratorio LAB 03x
├── firmware propio o reutilización explícita
├── herramientas propias
├── test manual/automático
├── evidencia propia
└── estado CUMPLE/NO CUMPLE/NO VALIDADO/PENDIENTE
```

## Cómo trabajar

No continuar con un sublaboratorio si el anterior no tiene documentación, evidencias y gates alineados.

Para LAB 03A:

```powershell
cd labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/firmware
idf.py set-target esp32s3
idf.py build
```

Para gates agregados:

```powershell
python labs/lab03_mqtt/tools/run_static_gates.py
python labs/lab03_mqtt/tools/capture_static_gates.py
```

## Evidencias

- Evidencia agregada de familia: `evidence/lab03_static_gates.txt`.
- Evidencia LAB 03A: `lab03a_m03_1883_plain_no_auth/evidence/lab03_m03_1883_console.log`.
- Cada sublaboratorio futuro debe tener evidencia propia.

## Estado

```text
CUMPLE:
- LAB 03 queda modelado como familia MQTT, no como único laboratorio TLS.
- LAB 03A conserva la evidencia dry-run de M03-1883.
- La matriz completa queda trazada por sublaboratorios independientes.

NO CUMPLE:
- Los escenarios sin TLS no son diseños seguros para credenciales ni payloads sensibles.

NO VALIDADO:
- Conexión real contra test.mosquitto.org.
- TLS/mTLS/WebSockets reales.
- Build formal cero warnings con stdout completo si no se aporta evidencia específica.

PENDIENTE:
- Implementar LAB 03B en su propio subdirectorio.
- Completar TLS, mTLS, certificado expirado y WebSockets en sublaboratorios separados.
```

## Software requerido

- Git.
- Python 3.
- ESP-IDF compatible con el target ESP32-S3.
- PowerShell o terminal equivalente.
- Herramientas del repositorio bajo `tools/` y `labs/lab03_mqtt/tools/`.

## EjecuciÃ³n

Desde la raÃ­z del repositorio:

```powershell
python tools
epo_quality_gates
un_static_repo_gates.py
python labs\lab03_mqtt	ools
un_static_gates.py
python labs\lab03_mqtt	ools\capture_static_gates.py
```

Para compilar LAB 03A tras la migraciÃ³n:

```powershell
cd labs\lab03_mqtt\lab03a_m03_1883_plain_no_auth
irmware
idf.py set-target esp32s3
idf.py build
cd ..\..\..\..
```

## Limitaciones conocidas

- El broker `test.mosquitto.org` es pÃºblico y puede no estar disponible permanentemente.
- No deben publicarse secretos reales.
- Las fases dry-run validan contrato local, no conectividad real.

## Arquitectura prevista

LAB 03 se estructura como familia MQTT:

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
