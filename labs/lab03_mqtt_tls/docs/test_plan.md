# LAB 03 — Plan de pruebas

## Índice

- [Objetivo](#objetivo)
- [Pruebas de fase 03A](#pruebas-de-fase-03a)
- [Pruebas pendientes](#pruebas-pendientes)
- [Criterio de cierre](#criterio-de-cierre)

## Objetivo

Validar primero el baseline MQTT sin TLS y dejar trazada la matriz completa para fases posteriores.

## Pruebas de fase 03A

| ID | Prueba | Estado esperado |
| --- | --- | --- |
| T03A-001 | `help` | Lista comandos. |
| T03A-002 | `scenario_list` | Lista los once escenarios. |
| T03A-003 | `select_scenario M03-1883` | Selecciona baseline sin TLS. |
| T03A-004 | `scenario_status` | Muestra host, puerto 1883 y `tls_enabled=false`. |
| T03A-005 | `mqtt_connect_dry_run` | Emite `security_result=NO_CUMPLE_EXPECTED`. |
| T03A-006 | `mqtt_publish_dry_run` | Emite publicación simulada sin broker real. |
| T03A-007 | checker de logs | Debe aceptar el baseline inseguro como evidencia didáctica. |

## Pruebas pendientes

- Conexión real a 1883.
- Autenticación 1884.
- TLS 8883/8886/8885.
- mTLS 8884.
- Certificado expirado 8887.
- WebSockets 8080/8081/8090/8091.

## Criterio de cierre

La fase 03A se cierra cuando el firmware compile, arranque en ESP32-S3, capture evidencia de `M03-1883` y pasen gates estáticos.
