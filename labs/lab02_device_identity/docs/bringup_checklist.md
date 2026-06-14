# Bring-up checklist LAB 02

## Índice

- [Objetivo](#objetivo)
- [Checklist](#checklist)
- [Criterio de parada](#criterio-de-parada)
- [Estado](#estado)

## Objetivo

Definir los pasos mínimos para arrancar y validar el LAB 02 en ESP32-S3.

## Checklist

```text
[ ] Confirmar rama limpia.
[ ] Ejecutar gates estáticos.
[ ] Configurar target esp32s3.
[ ] Compilar perfil INSECURE.
[ ] Flashear perfil INSECURE.
[ ] Capturar evidencia de identidad clonable.
[ ] Compilar perfil HARDENED.
[ ] Flashear perfil HARDENED.
[ ] Capturar evidencia de identidad derivada y no editable.
[ ] Ejecutar scanner de logs.
[ ] Limpiar build/sdkconfig antes de commit.
```

## Criterio de parada

Cualquier checksum mismatch, warning de build o fallo de gate bloquea el commit de cierre.

## Estado

```text
PENDIENTE:
- Ejecutar en hardware.
```
