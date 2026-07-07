# LAB 03 — Evidencias de auditoría

## Índice

- [Estado](#estado)
- [Evidencias actuales](#evidencias-actuales)
- [Pendientes](#pendientes)

## Estado

```text
CUMPLE:
- Evidencia de consola LAB 03A/M03-1883 capturada y verificada.
- Evidencia de gates estáticos LAB 03 capturada y verificada.

NO VALIDADO:
- Build real con stdout completo y cero warnings versionado.
- Conexión real al broker.
- Validación TLS/mTLS/WebSockets.
```

## Evidencias actuales

| Evidencia | Estado | Descripción |
| --- | --- | --- |
| `evidence/lab03_m03_1883_console.log` | CUMPLE | Baseline MQTT 1883 sin TLS, dry-run contractual. |
| `evidence/lab03_static_gates.txt` | CUMPLE | Gates globales y gate específico LAB 03. |

## Pendientes

- Capturar stdout completo de `idf.py build` cuando se cierre release firmware formal.
- Añadir evidencias de conexión real al broker en fases posteriores.
- Añadir evidencias TLS/certificados en fases posteriores.
- Añadir evidencia LAB 03B/M03-1884 antes de marcar esa fase como cerrada.
