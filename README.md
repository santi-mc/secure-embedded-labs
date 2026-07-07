# Secure Embedded Labs

**Estado:** EN CURSO
**Objetivo:** laboratorios reproducibles de ciberseguridad embebida para ESP32-S3.

## Índice

- [Objetivo](#objetivo)
- [Estado de laboratorios](#estado-de-laboratorios)
- [Árbol principal](#arbol-principal)
- [Criterio de cierre](#criterio-de-cierre)
- [Gates mínimos](#gates-minimos)

## Objetivo

`secure-embedded-labs` es un repositorio-libro de laboratorios de ciberseguridad embebida.
Cada laboratorio debe mantener firmware, documentación, evidencias, herramientas y gates alineados.

## Estado de laboratorios

| Lab | Tema | Estado |
| --- | --- | --- |
| LAB 01 | Firmware inseguro vs endurecido | CUMPLE |
| LAB 02 | Identidad única de dispositivo | CUMPLE |
| LAB 03 | Familia MQTT contra `test.mosquitto.org` | EN CURSO |
| LAB 04...LAB 10 | Fases futuras | PENDIENTE |

## Árbol principal

```text
secure-embedded-labs/
├── book/
├── docs/
├── labs/
│   ├── lab01_insecure_vs_hardened/
│   ├── lab02_device_identity/
│   └── lab03_mqtt/
├── standard/
└── tools/
```

## Criterio de cierre

Un laboratorio solo puede declararse `CUMPLE` cuando existen implementación, documentación, evidencias y gates en PASS.
Las fases dry-run deben diferenciarse explícitamente de las conexiones reales.

## Gates mínimos

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
```
