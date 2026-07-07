# Modelo de publicación del repositorio

## Índice

- [Objetivo](#objetivo)
- [Regla de publicación](#regla-de-publicacion)
- [Artefactos afectados](#artefactos-afectados)
- [Estado](#estado)

## Objetivo

Definir cómo se publica una entrega audit-grade en `secure-embedded-labs`.

## Regla de publicación

Una entrega no es solo firmware. Una entrega puede afectar código, documentación, laboratorios, evidencias, libro, changelog y gates.

No se declara cierre si el estado queda inconsistente entre documentación y evidencia.

## Artefactos afectados

Cada cambio de laboratorio debe revisar, cuando aplique:

```text
README.md
ROADMAP.md
CHANGELOG.md
labs/README.md
book/README.md
book/chapters/*
docs/index.md
docs/learning_path.md
docs/publishing_model.md
tools/repo_quality_gates/*
labs/<lab>/README.md
labs/<lab>/CHANGELOG.md
labs/<lab>/docs/*
labs/<lab>/evidence/README.md
```

## Estado

```text
CUMPLE:
- Criterio transversal documentado.

PENDIENTE:
- Automatizar comprobaciones adicionales si el repositorio crece.
```
