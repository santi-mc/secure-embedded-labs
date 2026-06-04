# Contributing

## Índice

- [Regla principal](#regla-principal)
- [Requisitos de Pull Request](#requisitos-de-pull-request)
- [Gates mínimos](#gates-mínimos)
- [Commits](#commits)
- [Documentación](#documentación)
- [Seguridad](#seguridad)

## Regla principal

No se aceptan cambios que degraden el estándar audit-grade del repositorio.

## Requisitos de Pull Request

Cada PR debe indicar:

- laboratorio o área afectada;
- objetivo;
- alcance;
- fuera de alcance;
- pruebas ejecutadas;
- pruebas no ejecutadas;
- estado `CUMPLE / NO CUMPLE / NO VALIDADO`.

## Gates mínimos

Antes de abrir un PR:

```bash
python tools/repo_quality_gates/run_static_repo_gates.py
```

Si el PR añade firmware ESP-IDF, además debe incluir evidencia de:

```bash
idf.py set-target esp32s3
idf.py build
```

con:

```text
0 errores
0 warnings
0 APIs deprecadas
```

## Commits

Formato recomendado:

```text
tipo(scope): resumen
```

Ejemplos:

```text
feat(lab01): añadir consola endurecida por USB Serial-JTAG
fix(lab01): eliminar fuga de secretos en logs
infra(repo): añadir gates estáticos de estructura
docs(standard): actualizar norma de modelo temporal
```

## Documentación

Todo laboratorio debe tener `README.md` con índice y las secciones obligatorias definidas en `labs/_template/README.md`.

## Seguridad

No se aceptan secretos reales, tokens, claves privadas, credenciales de broker, certificados privados ni datos de dispositivos de terceros.
