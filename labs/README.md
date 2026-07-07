# Laboratorios

## Índice

- [Propósito](#proposito)
- [Árbol](#arbol)
- [Estado](#estado)

## Propósito

Agrupar laboratorios reproducibles de ciberseguridad embebida con evidencias auditables.

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
- LAB 01 cerrado para el alcance actual.
- LAB 02 cerrado para el alcance actual.
- LAB 03A cerrado como dry-run dentro de la familia MQTT.

PENDIENTE:
- LAB 03B y siguientes sublaboratorios MQTT.
- LAB 04–LAB 10.
```
