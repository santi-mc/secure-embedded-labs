# LAB 02 — Evidencia de auditoría

## Índice

- [Objetivo](#objetivo)
- [Matriz de evidencias](#matriz-de-evidencias)
- [Validación funcional](#validación-funcional)
- [Limitaciones](#limitaciones)
- [Estado](#estado)

## Objetivo

Registrar la evidencia audit-grade disponible para el LAB 02 y su relación con los requisitos del laboratorio.

## Matriz de evidencias

| Evidencia | Estado | Resultado |
| --- | --- | --- |
| `evidence/lab02_insecure_console.log` | CUMPLE | Perfil INSECURE validado con identidad mutable y claim clonable. |
| `evidence/lab02_hardened_console.log` | CUMPLE | Perfil HARDENED validado con identidad derivada, no mutable y sin exposición de raw hardware ID. |
| `evidence/lab02_static_gates.txt` | CUMPLE | Gates estáticos globales y del LAB 02 capturados con PASS. |
| `evidence/lab02_build_esp32s3.txt` | PENDIENTE | Falta stdout completo de build. |

## Validación funcional

```text
CUMPLE:
- INSECURE: set_device_id acepta CLONED-DEVICE-001.
- INSECURE: get_claim emite insecure_cloneable_claim con token compartido ficticio.
- HARDENED: identity_source=efuse_mac_sha256_truncated.
- HARDENED: raw_hardware_id=<redacted>.
- HARDENED: set_device_id rechazado por política.
- HARDENED: auth_token=not_applicable.
```

## Limitaciones

```text
NO VALIDADO:
- Build completo con cero warnings pendiente de evidencia stdout versionada.
- Secure Boot y Flash Encryption no están activos en este laboratorio.
```

## Estado

```text
CUMPLE:
- Evidencias funcionales y gates disponibles.

PENDIENTE:
- Captura de build completo.
```
