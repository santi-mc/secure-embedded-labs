# LAB 03 — Plan de pruebas

## Índice

- [Objetivo](#objetivo)
- [Pruebas de fase 03A](#pruebas-de-fase-03a)
- [Pruebas pendientes](#pruebas-pendientes)
- [Criterio de cierre](#criterio-de-cierre)

## Objetivo

Validar primero el baseline MQTT sin TLS y dejar trazada la matriz completa para fases posteriores.

## Pruebas de fase 03A

| ID | Prueba | Estado esperado | Estado actual |
| --- | --- | --- | --- |
| T03A-001 | `help` | Lista comandos. | CUMPLE |
| T03A-002 | `scenario_list` | Lista los once escenarios. | CUMPLE |
| T03A-003 | `select_scenario M03-1883` | Selecciona baseline sin TLS. | CUMPLE |
| T03A-004 | `scenario_status` | Muestra host, puerto 1883 y `tls_enabled=false`. | CUMPLE |
| T03A-005 | `mqtt_connect_dry_run` | Emite clasificación de seguridad insegura esperada. | CUMPLE |
| T03A-006 | `mqtt_publish_dry_run` | Emite publicación simulada sin broker real. | CUMPLE |
| T03A-007 | Checker de logs | Acepta el baseline inseguro como evidencia didáctica. | CUMPLE |
| T03A-008 | Gates estáticos | Gate global y gate LAB 03 en PASS. | CUMPLE |

## Pruebas pendientes

- LAB 03B: autenticación 1884 sin TLS.
- Conexión real a 1883.
- TLS 8883/8886/8885.
- mTLS 8884.
- Certificado expirado 8887.
- WebSockets 8080/8081/8090/8091.

## Criterio de cierre

LAB 03A queda cerrado como dry-run contractual cuando el firmware compila, arranca en ESP32-S3, captura evidencia de `M03-1883` y pasan gates estáticos.

Las fases de conexión real quedan `NO VALIDADO` hasta que existan evidencias contra broker y documentación de disponibilidad/timeout.
