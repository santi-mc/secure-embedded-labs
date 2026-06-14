# Plan de pruebas LAB 02

## Índice

- [Objetivo](#objetivo)
- [Pruebas INSECURE](#pruebas-insecure)
- [Pruebas HARDENED](#pruebas-hardened)
- [Gates](#gates)
- [Estado](#estado)

## Objetivo

Definir pruebas mínimas para validar el comportamiento didáctico del LAB 02.

## Pruebas INSECURE

```text
[ ] Arranca con profile=INSECURE.
[ ] get_identity muestra device_id clonable.
[ ] get_claim expone token compartido de laboratorio.
[ ] set_device_id acepta un ID arbitrario.
```

## Pruebas HARDENED

```text
[ ] Arranca con profile=HARDENED.
[ ] get_identity muestra device_id derivado.
[ ] raw_mac aparece como <redacted>.
[ ] get_claim no incluye token ni secreto.
[ ] set_device_id queda rechazado por política.
```

## Gates

```text
[ ] python tools/repo_quality_gates/run_static_repo_gates.py
[ ] python labs/lab02_device_identity/tools/run_static_gates.py
[ ] idf.py build sin warnings
```

## Estado

```text
PENDIENTE:
- Ejecutar pruebas reales.
```
