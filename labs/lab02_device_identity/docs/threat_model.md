# Threat model LAB 02

## Índice

- [Objetivo](#objetivo)
- [Activos](#activos)
- [Adversarios](#adversarios)
- [Amenazas](#amenazas)
- [Mitigaciones](#mitigaciones)
- [Estado](#estado)

## Objetivo

Modelar amenazas relacionadas con identidad técnica de dispositivo.

## Activos

```text
- device_id público estable
- raw MAC/eFuse como dato identificador hardware
- claims de identidad
- logs de consola
```

## Adversarios

```text
- Operador local no confiable
- Integrador que clona firmware/configuración
- Atacante con acceso a logs
```

## Amenazas

| ID | Amenaza | Perfil afectado |
| --- | --- | --- |
| T-001 | Clonado de `device_id` hardcodeado. | INSECURE |
| T-002 | Exposición de token compartido. | INSECURE |
| T-003 | Cambio local de identidad por consola. | INSECURE |
| T-004 | Exposición innecesaria de raw MAC. | INSECURE |

## Mitigaciones

| ID | Mitigación | Perfil |
| --- | --- | --- |
| M-001 | Derivar `device_id` desde fuente hardware. | HARDENED |
| M-002 | Redactar raw MAC. | HARDENED |
| M-003 | No emitir token de autenticación. | HARDENED |
| M-004 | Rechazar cambios de identidad por consola. | HARDENED |

## Estado

```text
CUMPLE:
- Threat model inicial definido.
```
