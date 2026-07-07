# Estructura de la familia LAB 03 MQTT

## Índice

- [Propósito](#propósito)
- [Árbol contractual](#árbol-contractual)
- [Reglas](#reglas)
- [Estado](#estado)

## Propósito

Documentar la decisión arquitectónica de convertir LAB 03 en una familia MQTT con sublaboratorios independientes.

## Árbol contractual

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

## Reglas

- Cada sublaboratorio tiene `README.md`, `CHANGELOG.md`, `docs/`, `evidence/`, `firmware/`, `test/` y `tools/`.
- La familia mantiene matriz, políticas y gates agregados.
- Los sublaboratorios mantienen evidencias propias.

## Estado

```text
CUMPLE:
- Estructura contractual definida.
```
