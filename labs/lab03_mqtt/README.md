# LAB 03 — Familia MQTT contra test.mosquitto.org

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

Organizar una matriz reproducible de escenarios MQTT contra `test.mosquitto.org`, separando MQTT plano, autenticación, TLS, mTLS, certificado expirado y WebSockets en sublaboratorios auditables.

## Objetivos de aprendizaje

- Distinguir conectividad funcional de diseño seguro.
- Separar autenticación, confidencialidad y validación de certificados.
- Evitar que un escenario TLS o mTLS oculte los riesgos de MQTT plano.
- Mantener trazabilidad escenario → diseño → firmware → test → evidencia.

## Prerrequisitos

- Repositorio limpio de artefactos generados.
- Python 3 disponible.
- ESP-IDF disponible cuando el sublaboratorio incluya firmware.
- Lectura previa de `README.md`, `ROADMAP.md` y `labs/README.md`.

## Alcance

La carpeta `lab03_mqtt/` define la familia MQTT, la matriz contractual, los gates agregados y la navegación de sublaboratorios LAB 03A–LAB 03G.

## Fuera de alcance

- Tratar `lab03_mqtt/` como firmware final único.
- Mezclar todos los escenarios en un único laboratorio monolítico.
- Usar secretos reales en un broker público.
- Declarar conexión real cuando solo existe dry-run.

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


## Matriz contractual

| Sublab | Escenario | Puerto | TLS | Auth | Estado |
| --- | --- | ---: | --- | --- | --- |
| LAB 03A | M03-1883 | 1883 | No | No | CUMPLE dry-run |
| LAB 03B | M03-1884 | 1884 | No | Usuario/password | PENDIENTE |
| LAB 03C | M03-8883 / M03-8886 | 8883 / 8886 | Sí | No | PENDIENTE |
| LAB 03D | M03-8885 | 8885 | Sí | Usuario/password | PENDIENTE |
| LAB 03E | M03-8884 | 8884 | Sí | Certificado cliente | PENDIENTE |
| LAB 03F | M03-8887 | 8887 | Sí, expirado | No | PENDIENTE |
| LAB 03G | M03-8080/8081/8090/8091 | Mixto | Mixto | Mixto | PENDIENTE |

## Arquitectura prevista

LAB 03 se estructura en una carpeta de familia con documentación común, gates agregados y sublaboratorios independientes. `common/` queda reservado para reutilización explícita. `lab03a`...`lab03g` mantienen cierre documental y técnico propio.

## Modelo temporal

LAB 03A está validado como dry-run por consola. Las fases de conexión real deberán documentar tareas, timeouts, retries, callbacks y deadlines antes de declararse validadas.

## Threat model

- Exposición de credenciales en transporte plano.
- Publicación accidental de secretos en broker público.
- Aceptación de certificados inválidos o expirados.
- Confusión entre autenticación y cifrado.
- Logs que filtren usuario, password, token, certificados privados o payloads sensibles.

## Requisitos

- Cada sublaboratorio debe tener README, CHANGELOG, evidencias y estado explícito.
- Los logs deben ser parseables y no contener secretos reales.
- Los gates globales y LAB 03 deben pasar antes de declarar cierre.
- La documentación transversal debe actualizarse con cada cambio de estado.

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
python tools\repo_quality_gates\run_static_repo_gates.py
python labs\lab03_mqtt\tools\run_static_gates.py
python labs\lab03_mqtt\tools\capture_static_gates.py
```

## Evidencias esperadas

- `labs/lab03_mqtt/evidence/lab03_static_gates.txt`.
- Evidencia específica en cada sublaboratorio.
- `lab03a_m03_1883_plain_no_auth/evidence/lab03_m03_1883_console.log` para LAB 03A.

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
- LAB 03 queda modelado como familia MQTT.
- LAB 03A queda aislado como sublaboratorio para M03-1883.
- Gates agregados disponibles en `labs/lab03_mqtt/tools/`.

NO CUMPLE:
- Los escenarios MQTT sin TLS no son seguros para secretos ni payloads sensibles.

NO VALIDADO:
- Conexión MQTT real contra `test.mosquitto.org`.
- TLS, mTLS y WebSockets reales.

PENDIENTE:
- Implementar LAB 03B en su propio subdirectorio.
- Regenerar evidencias cada vez que cambien gates o documentación.
```
