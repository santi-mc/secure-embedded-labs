# LAB 03 — Matriz MQTT contra test.mosquitto.org

**Version:** 0.1.0

## Índice

- [Objetivo](#objetivo)
- [Alcance](#alcance)
- [Roadmap interno](#roadmap-interno)
- [Broker de pruebas](#broker-de-pruebas)
- [Matriz contractual](#matriz-contractual)
- [Arquitectura](#arquitectura)
- [Firmware](#firmware)
- [Comandos de consola](#comandos-de-consola)
- [Cómo compilar](#cómo-compilar)
- [Cómo probar](#cómo-probar)
- [Evidencias esperadas](#evidencias-esperadas)
- [Estado](#estado)

## Objetivo

Construir una matriz reproducible de escenarios MQTT usando el broker público `test.mosquitto.org`.

El primer objetivo ejecutable es demostrar el baseline inseguro `1883` sin TLS. El laboratorio queda preparado desde el primer commit para cubrir los once escenarios publicados por el broker: MQTT plano, MQTT con autenticación, MQTT sobre TLS, mTLS, certificado expirado y MQTT over WebSockets.

## Alcance

Esta fase crea el contrato de matriz y un firmware didáctico inicial que ejecuta comprobaciones dry-run de política MQTT. No establece todavía conexión real con el broker.

## Roadmap interno

```text
LAB 03A — MQTT TCP 1883 sin TLS, baseline inseguro.
LAB 03B — MQTT TCP 1884 con autenticación sin TLS.
LAB 03C — MQTT TCP 8883/8886 con TLS y validación de servidor.
LAB 03D — MQTT TCP 8885 con TLS y autenticación usuario/password.
LAB 03E — MQTT TCP 8884 con certificado cliente.
LAB 03F — MQTT TCP 8887 con certificado servidor expirado, rechazo esperado.
LAB 03G — MQTT over WebSockets 8080/8081/8090/8091.
```

## Broker de pruebas

Broker contractual: `test.mosquitto.org`.

No se deben enviar secretos reales. Los usuarios, passwords, topics y payloads del laboratorio son ficticios y deben tratarse como material didáctico.

## Matriz contractual

Ver `docs/scenario_matrix.md`.

## Arquitectura

```text
main
├── command_console
├── mqtt_scenario
├── secure_log
├── board_hal
└── lab03_domain
```

La implementación inicial es intencionadamente dry-run para separar política de seguridad, trazabilidad de escenarios y contrato de evidencias antes de introducir Wi-Fi, ESP-MQTT, certificados y broker real.

## Firmware

El firmware arranca sobre ESP32-S3 y consola USB Serial/JTAG. La selección de escenarios se hace en runtime desde consola.

## Comandos de consola

```text
help
scenario_list
select_scenario <id>
scenario_status
mqtt_connect_dry_run
mqtt_publish_dry_run
security_status
```

Escenario por defecto: `M03-1883`.

## Cómo compilar

```powershell
cd labs\lab03_mqtt_tls\firmware
idf.py set-target esp32s3
idf.py build
```

## Cómo probar

```powershell
python labs\lab03_mqtt_tls\tools\capture_console_evidence.py `
  --port COM5 `
  --scenario M03-1883 `
  --output labs\lab03_mqtt_tls\evidence\lab03_m03_1883_console.log

python labs\lab03_mqtt_tls\tools\check_mqtt_scenario_logs.py `
  labs\lab03_mqtt_tls\evidence\lab03_m03_1883_console.log `
  --scenario M03-1883
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

## Estado

```text
CUMPLE:
- Matriz contractual completa de test.mosquitto.org documentada.
- Firmware inicial dry-run para ESP32-S3 añadido.
- Baseline 1883 sin TLS modelado como NO CUMPLE de seguridad esperado.
- Gates y herramientas de evidencia añadidos.

NO CUMPLE:
- 1883/1884/8080/8090 no son diseños seguros porque no usan TLS.
- Esta fase no implementa conexión real al broker.

NO VALIDADO:
- Build real ESP-IDF pendiente.
- Flash en ESP32-S3 pendiente.
- Evidencia real pendiente.

PENDIENTE:
- Integrar ESP-MQTT como dependencia gestionada.
- Añadir Wi-Fi/provisioning de red.
- Ejecutar matriz real contra test.mosquitto.org.
- Introducir TLS, CA, mTLS y WebSockets en fases posteriores.
```
