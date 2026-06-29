# LAB 03 — Threat model

## Índice

- [Activos](#activos)
- [Atacantes](#atacantes)
- [Amenazas](#amenazas)
- [Mitigaciones previstas](#mitigaciones-previstas)

## Activos

- Identidad lógica MQTT.
- Usuario/password ficticio de laboratorio.
- Payloads publicados.
- Certificados CA y certificados cliente futuros.
- Logs de diagnóstico.

## Atacantes

- Observador pasivo de red.
- Intermediario activo capaz de MITM.
- Usuario local con acceso a consola.
- Cliente MQTT externo suscrito al broker público.

## Amenazas

| Amenaza | Escenario | Estado |
| --- | --- | --- |
| Lectura de payload en claro | 1883, 1884, 8080, 8090 | CUMPLE como vulnerabilidad didáctica. |
| Robo de credenciales | 1884, 8090 | CUMPLE como vulnerabilidad didáctica. |
| MITM TLS si no se valida CA | 8883, 8885, 8886, 8081, 8091 | PENDIENTE de fases TLS. |
| Aceptación de certificado expirado | 8887 | Debe rechazarse. |
| Exposición de secretos en logs | Todos | Debe bloquearse en perfiles endurecidos. |

## Mitigaciones previstas

- TLS con validación de certificado servidor.
- Rechazo de certificados expirados.
- Redacción de credenciales en logs.
- mTLS para puerto 8884.
- Separación de escenarios inseguros y endurecidos.
