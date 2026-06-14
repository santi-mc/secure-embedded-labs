# Política de hardening LAB 02

## Índice

- [Objetivo](#objetivo)
- [Perfil INSECURE](#perfil-insecure)
- [Perfil HARDENED](#perfil-hardened)
- [Criterios](#criterios)
- [Estado](#estado)

## Objetivo

Definir qué vulnerabilidades son intencionadas y qué mitigaciones debe demostrar el perfil endurecido.

## Perfil INSECURE

```text
V-001: device_id hardcodeado y clonable.
V-002: claim expone token compartido de laboratorio.
V-003: consola permite sobrescribir device_id.
V-004: logs exponen raw_mac.
```

## Perfil HARDENED

```text
M-001: device_id derivado desde fuente hardware mediante hash.
M-002: no se exponen tokens ni secretos.
M-003: raw_mac queda redactado en logs.
M-004: set_device_id queda rechazado por política.
```

## Criterios

La identidad endurecida es pública y estable, pero no se presenta como autenticación criptográfica.

## Estado

```text
CUMPLE:
- Vulnerabilidades y mitigaciones declaradas.
```
