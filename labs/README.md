# Laboratorios

## Índice

- [Regla común](#regla-común)
- [Lista de laboratorios](#lista-de-laboratorios)
- [Estados actuales](#estados-actuales)
- [Plantilla](#plantilla)
- [Regla de cierre](#regla-de-cierre)

## Regla común

Cada laboratorio debe tener un `README.md` con índice y estructura didáctica completa.

Cada avance debe actualizar también los artefactos transversales del repositorio: README raíz, ROADMAP, CHANGELOG, libro, docs, evidencias e índices cuando aplique.

## Lista de laboratorios

| Lab | Carpeta | Tema | Estado |
| ---: | --- | --- | --- |
| 01 | `lab01_insecure_vs_hardened` | Firmware inseguro vs firmware endurecido | CUMPLE |
| 02 | `lab02_device_identity` | Identidad única de dispositivo | CUMPLE |
| 03 | `lab03_mqtt_tls` | Matriz MQTT contra test.mosquitto.org | EN CURSO: 03A CUMPLE |
| 04 | `lab04_signed_ota` | OTA firmada con rollback | PENDIENTE |
| 05 | `lab05_secure_remote_config` | Configuración remota segura | PENDIENTE |
| 06 | `lab06_physical_interface_hardening` | Hardening de interfaces físicas | PENDIENTE |
| 07 | `lab07_sbom_release_traceability` | SBOM y trazabilidad de release | PENDIENTE |
| 08 | `lab08_secure_boot_flash_encryption` | Secure Boot + Flash Encryption | PENDIENTE |
| 09 | `lab09_secure_multi_interface_gateway` | Gateway seguro multi-interfaz | PENDIENTE |
| 10 | `lab10_mini_psirt` | Mini PSIRT de producto | PENDIENTE |

## Estados actuales

```text
CUMPLE:
- LAB 01 con evidencias de consola, secret scan y gates.
- LAB 02 con evidencias de identidad INSECURE/HARDENED y gates.
- LAB 03A/M03-1883 como dry-run MQTT plano sin TLS con evidencia de consola y gates.

NO VALIDADO:
- Builds formales con stdout completo y cero warnings para todos los laboratorios.
- Conexiones reales MQTT contra broker público.
- TLS/mTLS/WebSockets de LAB 03.

PENDIENTE:
- LAB 03B/M03-1884.
- LAB 04 a LAB 10.
```

## Plantilla

La plantilla está en:

```text
labs/_template/README.md
```

## Regla de cierre

No se marca un laboratorio como cerrado si no están alineados:

- README del laboratorio;
- documentación interna del laboratorio;
- evidencias;
- gates;
- README raíz;
- ROADMAP;
- CHANGELOG global;
- libro o capítulo correspondiente;
- índices de navegación.
