# LAB 01 — Registro de riesgos

## Índice

- [Objetivo](#objetivo)
- [Riesgos](#riesgos)
- [Estado](#estado)

## Objetivo

Registrar riesgos técnicos y didácticos del laboratorio.

## Riesgos

| ID | Riesgo | Severidad | Mitigación |
|---|---|---|---|
| R-001 | Confundir perfil INSECURE con producción. | Alta | README, disclaimer y logs de boot. |
| R-002 | Usar secretos reales durante pruebas. | Alta | Documentación y scanner de logs. |
| R-003 | Consola no accesible por puerto incorrecto. | Media | Bring-up checklist USB Serial/JTAG. |
| R-004 | Build no validado en IDF real. | Alta | Gate obligatorio antes de cierre. |

## Estado

```text
CUMPLE:
- Riesgos iniciales declarados.
```
