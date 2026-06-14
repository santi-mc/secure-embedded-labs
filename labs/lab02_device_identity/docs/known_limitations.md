# Limitaciones conocidas LAB 02

## Índice

- [Objetivo](#objetivo)
- [Limitaciones](#limitaciones)
- [Implicación](#implicación)
- [Estado](#estado)

## Objetivo

Evitar sobredeclarar seguridad fuera del alcance real del laboratorio.

## Limitaciones

```text
- La identidad derivada no autentica al dispositivo.
- La MAC/eFuse usada como entrada no es un secreto.
- No hay almacenamiento persistente de provisioning.
- No hay certificados cliente.
- No hay backend de registro.
```

## Implicación

El laboratorio enseña identidad estable y no clonable por configuración, no autenticación fuerte de producto.

## Estado

```text
CUMPLE:
- Limitaciones explícitas.
```
