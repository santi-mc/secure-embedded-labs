# Capítulo 01 — Firmware inseguro vs firmware endurecido

## Índice

- [Objetivo](#objetivo)
- [Idea central](#idea-central)
- [Qué se demuestra](#qué-se-demuestra)
- [Relación con el laboratorio](#relación-con-el-laboratorio)
- [Estado](#estado)

## Objetivo

Introducir la primera práctica de ciberseguridad embebida: comparar un firmware vulnerable de laboratorio con una variante endurecida que corrige las mismas debilidades.

## Idea central

Un microcontrolador no necesita estar conectado a Internet para tener superficie de ataque. Una consola local, logs verbosos, comandos de configuración y secretos mal tratados son suficientes para crear vulnerabilidades reales.

## Qué se demuestra

- Fuga de secretos por `get_config`.
- Fuga de secretos por logs de comandos brutos.
- Configuración inválida por parser débil.
- Reset destructivo sin autorización.
- Redacción y validación como mitigaciones básicas.

## Relación con el laboratorio

El firmware y las evidencias se encuentran en:

```text
labs/lab01_insecure_vs_hardened/
```

LAB 01 está cerrado para el alcance actual con evidencias automáticas de consola, scanner de secretos y gates estáticos.

## Estado

```text
CUMPLE:
- Capítulo inicial alineado con LAB 01.
- Evidencias del laboratorio incorporadas al estado del repositorio.

NO VALIDADO:
- Revisión editorial completa pendiente.
```
