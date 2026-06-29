# LAB 03 — Matriz de escenarios MQTT

## Índice

- [Objetivo](#objetivo)
- [Matriz](#matriz)
- [Criterios de seguridad](#criterios-de-seguridad)
- [Notas de certificados](#notas-de-certificados)

## Objetivo

Definir la matriz contractual completa de escenarios que se probarán contra `test.mosquitto.org`.

## Matriz

| ID | Puerto | Transporte | TLS | Autenticación | Estado esperado |
| --- | ---: | --- | --- | --- | --- |
| M03-1883 | 1883 | MQTT TCP | No | No | Conecta en fase real, pero NO CUMPLE seguridad. |
| M03-1884 | 1884 | MQTT TCP | No | Usuario/password | Conecta en fase real, pero credenciales sin TLS. |
| M03-8883 | 8883 | MQTT TCP | Sí | No | Debe validar certificado servidor con CA Mosquitto. |
| M03-8884 | 8884 | MQTT TCP | Sí | Certificado cliente | Debe exigir certificado cliente. |
| M03-8885 | 8885 | MQTT TCP | Sí | Usuario/password | Debe validar TLS y autenticación. |
| M03-8886 | 8886 | MQTT TCP | Sí | No | Debe validar certificado de cadena pública. |
| M03-8887 | 8887 | MQTT TCP | Sí expirado | No | Debe rechazar certificado expirado. |
| M03-8080 | 8080 | MQTT WebSocket | No | No | Conecta en fase real, pero NO CUMPLE seguridad. |
| M03-8081 | 8081 | MQTT WebSocket | Sí | No | Debe validar WSS. |
| M03-8090 | 8090 | MQTT WebSocket | No | Usuario/password | Conecta en fase real, pero credenciales sin TLS. |
| M03-8091 | 8091 | MQTT WebSocket | Sí | Usuario/password | Debe validar WSS + autenticación. |

## Criterios de seguridad

```text
CUMPLE:
- TLS habilitado cuando hay autenticación o datos sensibles.
- Certificado servidor validado.
- Certificado expirado rechazado.
- Certificado cliente requerido cuando el escenario lo exige.

NO CUMPLE:
- MQTT sin TLS como diseño final.
- Usuario/password sobre transporte no cifrado.
- Aceptar certificados expirados.
- Desactivar verificación de certificado en escenarios TLS.
```

## Notas de certificados

Las fases TLS deben incorporar CA de Mosquitto o CA pública aplicable según el puerto. No se deben almacenar certificados privados reales en el repositorio.
