# Árbol contractual del repositorio

## Índice

- [Propósito](#propósito)
- [Árbol principal](#árbol-principal)
- [Detalle LAB 03](#detalle-lab-03)
- [Estado](#estado)

## Propósito

Este documento fija el árbol documental mínimo del repositorio. El árbol no es decorativo: forma parte del contrato audit-grade del proyecto.

## Árbol principal

```text
secure-embedded-labs/
├── .github/
├── book/
│   ├── chapters/
│   ├── figures/
│   └── references/
├── docs/
├── labs/
│   ├── _template/
│   ├── lab01_insecure_vs_hardened/
│   ├── lab02_device_identity/
│   ├── lab03_mqtt/
│   └── lab04...lab10/
├── standard/
└── tools/
```

## Detalle LAB 03

```text
labs/lab03_mqtt/
├── README.md
├── CHANGELOG.md
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

## Estado

```text
CUMPLE:
- LAB 03 se representa como familia MQTT con sublaboratorios independientes.

PENDIENTE:
- Mantener este árbol actualizado en cada parche estructural.
```
