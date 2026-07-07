# Laboratorios

## Índice

- [Resumen](#resumen)
- [Tabla de laboratorios](#tabla-de-laboratorios)
- [Árbol](#arbol)
- [Estado](#estado)

## Resumen

Los laboratorios están organizados como unidades auditables. Cada uno debe mantener documentación, firmware, herramientas, test y evidencias.

## Tabla de laboratorios

| Lab | Directorio | Tema | Estado |
| --- | --- | --- | --- |
| LAB 01 | `lab01_insecure_vs_hardened` | Firmware inseguro vs endurecido | CUMPLE |
| LAB 02 | `lab02_device_identity` | Identidad única de dispositivo | CUMPLE |
| LAB 03 | `lab03_mqtt` | Familia MQTT contra `test.mosquitto.org` | EN CURSO |
| LAB 04...LAB 10 | placeholders | Fases futuras | PENDIENTE |

## Árbol

```text
labs/
├── _template/
├── lab01_insecure_vs_hardened/
├── lab02_device_identity/
├── lab03_mqtt/
│   ├── common/
│   ├── docs/
│   ├── evidence/
│   ├── tools/
│   ├── lab03a_m03_1883_plain_no_auth/
│   ├── lab03b_m03_1884_plain_auth/
│   ├── lab03c_m03_8883_8886_tls_server_auth/
│   ├── lab03d_m03_8885_tls_userpass/
│   ├── lab03e_m03_8884_mtls_client_cert/
│   ├── lab03f_m03_8887_expired_cert_rejection/
│   └── lab03g_m03_websockets/
└── lab04...lab10/
```

## Estado

```text
CUMPLE:
- LAB 01 y LAB 02 cerrados para el alcance actual.
- LAB 03A cerrado como dry-run dentro de la familia MQTT.

PENDIENTE:
- LAB 03B y siguientes.
```
