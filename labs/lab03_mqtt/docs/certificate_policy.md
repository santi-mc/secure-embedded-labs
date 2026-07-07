# LAB 03 — Política de certificados

## Índice

- [Objetivo](#objetivo)
- [Reglas](#reglas)
- [Material permitido](#material-permitido)
- [Material prohibido](#material-prohibido)

## Objetivo

Definir cómo se incorporarán certificados en las fases TLS del LAB 03.

## Reglas

- Las CA públicas o de Mosquitto pueden versionarse si su licencia lo permite y son públicas.
- Los certificados privados de cliente no deben versionarse.
- Las claves privadas deben generarse localmente y quedar fuera de Git.
- El puerto 8887 debe fallar por certificado expirado.

## Material permitido

- CA pública en PEM/DER.
- Certificados de ejemplo sin clave privada.
- Instrucciones reproducibles para generar certificados cliente.

## Material prohibido

- Claves privadas reales.
- Tokens reales.
- Certificados de infraestructura privada.
