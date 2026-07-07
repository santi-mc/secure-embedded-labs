# Capítulo 02 — Identidad única de dispositivo

## Índice

- [Objetivo](#objetivo)
- [Idea central](#idea-central)
- [Qué se demuestra](#qué-se-demuestra)
- [Relación con el laboratorio](#relación-con-el-laboratorio)
- [Estado](#estado)

## Objetivo

Explicar por qué una identidad hardcoded o mutable no sirve como base de seguridad en un dispositivo embebido.

## Idea central

Identificar un dispositivo no equivale a autenticarlo. Una identidad clonable permite suplantación aunque el firmware parezca funcional.

## Qué se demuestra

- Identidad hardcoded y clonable en perfil INSECURE.
- Exposición de `raw_hardware_id` en perfil INSECURE.
- Mutación de identidad mediante consola insegura.
- Identidad derivada de eFuse MAC y hash en perfil HARDENED.
- Redacción de identificadores crudos y rechazo de mutación en perfil HARDENED.

## Relación con el laboratorio

El firmware y las evidencias se encuentran en:

```text
labs/lab02_device_identity/
```

LAB 02 está cerrado para el alcance actual con evidencias INSECURE/HARDENED y gates estáticos.

## Estado

```text
CUMPLE:
- Capítulo técnico inicial creado.
- Estado alineado con LAB 02.

NO VALIDADO:
- Revisión editorial completa pendiente.
```
