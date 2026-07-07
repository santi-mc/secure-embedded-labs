# Capítulo 03 — Matriz MQTT y transporte seguro

## Índice

- [Objetivo](#objetivo)
- [Idea central](#idea-central)
- [Qué se demuestra](#qué-se-demuestra)
- [Matriz didáctica](#matriz-didáctica)
- [Relación con el laboratorio](#relación-con-el-laboratorio)
- [Estado](#estado)

## Objetivo

Introducir la seguridad de transporte en MQTT mediante una matriz progresiva de escenarios contra `test.mosquitto.org`.

## Idea central

Una conexión MQTT funcional no implica seguridad. El laboratorio separa conectividad, autenticación, confidencialidad, validación de certificado y autenticación mutua.

## Qué se demuestra

- MQTT TCP plano sin TLS como baseline inseguro.
- Autenticación sin TLS como mejora insuficiente.
- TLS como mitigación de confidencialidad e integridad de canal.
- Validación de certificado servidor como requisito de seguridad.
- Rechazo de certificados expirados como comportamiento correcto.
- mTLS y WebSockets como fases posteriores.

## Matriz didáctica

```text
LAB 03A — M03-1883: MQTT TCP sin TLS y sin autenticación.
LAB 03B — M03-1884: MQTT TCP sin TLS con usuario/password.
LAB 03C — M03-8883/M03-8886: Matriz MQTT sin autenticación.
LAB 03D — M03-8885: Matriz MQTT con usuario/password.
LAB 03E — M03-8884: MQTT mTLS.
LAB 03F — M03-8887: certificado expirado, rechazo obligatorio.
LAB 03G — MQTT over WebSockets.
```

## Relación con el laboratorio

El firmware y las evidencias se encuentran en:

```text
labs/lab03_mqtt/
```

LAB 03A está cerrado como dry-run contractual: selecciona `M03-1883`, emite logs NDJSON, clasifica el escenario como funcional pero `NO CUMPLE` seguridad y dispone de evidencia de consola y gates.

## Estado

```text
CUMPLE:
- Capítulo técnico inicial creado.
- LAB 03A/M03-1883 alineado con evidencias y gates.

NO CUMPLE:
- Los escenarios sin TLS son inseguros por diseño y se mantienen solo como baseline didáctico.

NO VALIDADO:
- Conexión real MQTT contra broker público.
- TLS/mTLS/WebSockets reales.
- Revisión editorial completa pendiente.

PENDIENTE:
- LAB 03B y fases posteriores.
```


## Estructura por sublaboratorios

LAB 03 se organiza como familia `labs/lab03_mqtt/` con sublaboratorios independientes LAB 03A–LAB 03G. Esta estructura evita presentar como TLS escenarios que son deliberadamente MQTT plano.
