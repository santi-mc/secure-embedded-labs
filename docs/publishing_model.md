# Modelo de publicación

## Índice

- [Repositorio](#repositorio)
- [Libro](#libro)
- [Licencias](#licencias)
- [Versionado](#versionado)
- [Cierre transversal](#cierre-transversal)

## Repositorio

El repositorio contiene código, documentación, laboratorios, scripts, evidencias y capítulos en desarrollo.

La unidad de entrega no es solo el firmware de un laboratorio. Una entrega audit-grade debe alinear también documentación, evidencias, libro, roadmap y changelog.

## Libro

El directorio `book/` evoluciona hacia un libro con licencia abierta. Cada laboratorio validado o en curso debe tener una entrada de libro proporcional a su madurez.

Capítulos actuales:

- Capítulo 01 — LAB 01.
- Capítulo 02 — LAB 02.
- Capítulo 03 — LAB 03A y matriz MQTT.

## Licencias

- Código: Apache-2.0.
- Documentación: CC BY-SA 4.0.

## Versionado

Cada release público debe indicar estado, alcance y limitaciones.

El changelog global debe registrar los hitos transversales y no limitarse a cambios de firmware.

## Cierre transversal

Antes de declarar cerrado un laboratorio o subfase se revisan:

```text
README.md
ROADMAP.md
CHANGELOG.md
labs/README.md
book/README.md
book/chapters/*
docs/index.md
docs/learning_path.md
labs/<lab>/README.md
labs/<lab>/CHANGELOG.md
labs/<lab>/docs/*
labs/<lab>/evidence/README.md
```

## Cierre transversal LAB 03 MQTT

Cada sublaboratorio de `labs/lab03_mqtt/` debe actualizar, como mínimo, su README, CHANGELOG, evidencias, documentación del libro, ROADMAP y changelog global antes de considerarse cerrado.
