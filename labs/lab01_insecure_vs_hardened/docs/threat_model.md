# LAB 01 — Threat model

## Índice

- [Objetivo](#objetivo)
- [Activos](#activos)
- [Suposiciones](#suposiciones)
- [Superficie de ataque](#superficie-de-ataque)
- [Amenazas](#amenazas)
- [Fuera de alcance](#fuera-de-alcance)
- [Estado](#estado)

## Objetivo

Modelar amenazas locales de consola/logs para introducir seguridad embebida sin red.

## Activos

| Activo | Sensibilidad |
|---|---|
| `mqtt_password` de laboratorio | Secreto didáctico. |
| Configuración operativa | Integridad. |
| Logs | Evidencia y canal de fuga. |
| Comandos de consola | Superficie local. |

## Suposiciones

- El atacante tiene acceso a la consola local USB/UART del dispositivo de laboratorio.
- No hay conectividad de red en este laboratorio.
- Los secretos son ficticios; no deben usarse credenciales reales.

## Superficie de ataque

```text
USB Serial/JTAG console
logs del monitor serie
comandos de configuración
factory_reset
```

## Amenazas

| ID | Amenaza | Mitigación HARDENED |
|---|---|---|
| T-001 | Lectura de secretos mediante `get_config`. | Redacción. |
| T-002 | Fuga por logging de comandos. | Redacción de argumentos sensibles. |
| T-003 | Configuración inválida por parser débil. | Parser estricto y rango. |
| T-004 | Reset destructivo no autorizado. | Bloqueo por política. |

## Fuera de alcance

- Ataques remotos.
- TLS/MQTT.
- OTA.
- Secure Boot como mitigación activa.
- Flash Encryption como mitigación activa.

## Estado

```text
CUMPLE:
- Threat model local definido.

NO VALIDADO:
- Evidencia de explotación/mitigación pendiente.
```
