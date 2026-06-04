# LAB 01 — Bring-up HW/SW

## Índice

- [Objetivo](#objetivo)
- [Hardware](#hardware)
- [Checklist](#checklist)
- [Puertos](#puertos)
- [Estado](#estado)

## Objetivo

Evitar ambigüedad de consola, target y conexión durante pruebas.

## Hardware

- ESP32-S3 DevKit o board equivalente con USB nativo operativo.
- Cable USB de datos.
- PC con ESP-IDF instalado.

## Checklist

```text
[ ] Confirmar board ESP32-S3.
[ ] Confirmar cable USB de datos.
[ ] Confirmar puerto COM con VID/PID Espressif si se usa USB Serial/JTAG.
[ ] Ejecutar python -m serial.tools.list_ports -v.
[ ] Ejecutar idf.py set-target esp32s3.
[ ] Ejecutar idf.py build.
[ ] Ejecutar idf.py -p <COMx> flash monitor.
[ ] Confirmar evento boot.
[ ] Confirmar help responde.
```

## Puertos

El LAB 01 usa consola por USB Serial/JTAG mediante stdio. No depende del conversor USB-UART externo de la placa.

## Estado

```text
CUMPLE:
- Checklist inicial definida.

NO VALIDADO:
- Puerto y placa reales pendientes en cada entorno.
```
