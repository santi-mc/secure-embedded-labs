# Arquitectura LAB 02

## Índice

- [Objetivo](#objetivo)
- [Componentes](#componentes)
- [Flujo de dependencias](#flujo-de-dependencias)
- [Contratos](#contratos)
- [Política de encapsulación](#política-de-encapsulación)
- [Estado](#estado)

## Objetivo

Definir una arquitectura por componentes para demostrar identidad clonable frente a identidad derivada de hardware sin exponer secretos.

## Componentes

| Componente | Responsabilidad |
| --- | --- |
| `lab02_domain` | Tipos, contratos, perfiles, constantes y versión. |
| `board_hal` | Reloj, consola stdio y fuente de identidad hardware ESP32-S3. |
| `identity_service` | Política de identidad para perfiles `INSECURE` y `HARDENED`. |
| `command_console` | Parser de comandos y orquestación de casos de laboratorio. |
| `secure_log` | Emisión de eventos JSON/NDJSON. |
| `security_status` | Consulta de Secure Boot y Flash Encryption. |
| `app_core` | Composición de dependencias y ciclo principal. |

## Flujo de dependencias

```text
app_core
├── command_console
│   ├── identity_service
│   ├── security_status
│   └── secure_log
├── board_hal
└── lab02_domain
```

## Contratos

Las interfaces principales están en `lab02_domain/interfaces.hpp`:

```text
IClock              → uptime monotónico en ms
IConsoleInput       → lectura de línea con estado explícito
IDeviceUniqueSource → lectura de identificador hardware no secreto
```

## Política de encapsulación

El firmware no accede directamente a eFuse/MAC desde lógica de aplicación. La lectura queda encapsulada en HAL y la política de exposición queda en `identity_service`.

## Estado

```text
CUMPLE:
- Separación por componentes.
- HAL para fuente de identidad hardware.
- Identidad y logs separados.

NO VALIDADO:
- Build real pendiente.
```
