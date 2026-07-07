# Libro abierto

## Índice

- [Objetivo](#objetivo)
- [Estructura](#estructura)
- [Capítulos](#capítulos)
- [Licencia](#licencia)
- [Estado](#estado)
- [Criterio editorial](#criterio-editorial)

## Objetivo

Este directorio evoluciona hacia un libro práctico con licencia abierta sobre ciberseguridad aplicada a firmware embebido y microcontroladores.

El libro no sustituye a los laboratorios: los interpreta, ordena y explica con narrativa didáctica.

## Estructura

```text
book/
├── chapters/
│   ├── 01_firmware_inseguro_vs_endurecido.md
│   ├── 02_identidad_dispositivo.md
│   └── 03_matriz_mqtt_tls.md
├── figures/
└── references/
```

## Capítulos

| Capítulo | Laboratorio | Estado |
| --- | --- | --- |
| 01 — Firmware inseguro vs firmware endurecido | LAB 01 | CUMPLE como capítulo técnico inicial |
| 02 — Identidad única de dispositivo | LAB 02 | CUMPLE como capítulo técnico inicial |
| 03 — Matriz MQTT y transporte seguro | LAB 03A | CUMPLE como capítulo técnico inicial de baseline dry-run |

## Licencia

El material propio de documentación se publica bajo CC BY-SA 4.0 salvo indicación distinta.

## Estado

```text
CUMPLE:
- Estructura inicial creada.
- Capítulos 01, 02 y 03 alineados con el estado técnico actual.

NO VALIDADO:
- Revisión editorial completa no realizada.
- Figuras definitivas no incorporadas.
- Referencias bibliográficas del libro no normalizadas.

PENDIENTE:
- Convertir capítulos técnicos en narrativa editorial completa.
- Añadir figuras y diagramas.
- Preparar versión publicable.
```

## Criterio editorial

Un capítulo puede estar en estado técnico inicial si enlaza con evidencias reales y declara sus limitaciones. No puede afirmar una validación que el laboratorio no tenga.
