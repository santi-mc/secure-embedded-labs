# Fundamentos de seguridad firmware

## Índice

- [Activos](#activos)
- [Superficie de ataque](#superficie-de-ataque)
- [Secretos](#secretos)
- [Logs](#logs)
- [Configuración](#configuración)
- [Actualización](#actualización)

## Activos

- Firmware.
- Claves y credenciales.
- Configuración.
- Identidad de dispositivo.
- Datos de sensores.

## Superficie de ataque

- UART/USB/JTAG.
- Interfaces de red.
- OTA.
- Configuración remota.
- Almacenamiento externo.

## Secretos

Los secretos no deben imprimirse ni persistirse sin protección.

## Logs

Los logs son una API de auditoría y no deben contener secretos.

## Configuración

Toda configuración debe validarse antes de aplicarse.

## Actualización

Las actualizaciones deben ser autenticadas, recuperables y trazables.
