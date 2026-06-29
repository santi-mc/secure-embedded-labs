# LAB 03 — Registro de riesgos

## Índice

- [Riesgos](#riesgos)
- [Tratamiento](#tratamiento)

## Riesgos

| Riesgo | Impacto | Tratamiento |
| --- | --- | --- |
| Broker público no disponible | Evidencia temporalmente no reproducible | Marcar NO VALIDADO TEMPORAL. |
| Puertos TLS/WebSockets deshabilitados temporalmente | Falsos negativos | Registrar fecha, hora y error. |
| Exposición de credenciales ficticias | Confusión con secretos reales | Usar solo valores de laboratorio. |
| Certificados cambiados por el servicio | Fallo de pinning rígido | Usar validación de CA, no fingerprint fijo salvo prueba explícita. |
| MQTT component externo en ESP-IDF 6 | Build no reproducible si no se fija dependencia | Usar `idf_component.yml` en fase real. |

## Tratamiento

Cada evidencia debe indicar si el fallo procede del firmware, del broker público o de disponibilidad externa.
