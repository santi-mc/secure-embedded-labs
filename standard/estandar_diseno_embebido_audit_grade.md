# Estándar permanente de diseño embebido audit-grade

**Versión:** 1.0  
**Ámbito:** firmware embebido, laboratorios, PoC, herramientas auxiliares, proyectos ESP-IDF/ESP32-S3 y proyectos equivalentes sobre microcontroladores.  
**Regla matriz:** un laboratorio puede ser inseguro de forma intencionada; nunca puede ser precario por descuido.

---

## Índice

- [0. Clasificación obligatoria de cada entrega](#0.-clasificación-obligatoria-de-cada-entrega)
- [1. Arquitectura por componentes](#1.-arquitectura-por-componentes)
- [2. OOP/SOLID adaptado a embebidos](#2.-oopsolid-adaptado-a-embebidos)
- [3. FULL HAL / BSP obligatorio](#3.-full-hal--bsp-obligatorio)
- [4. Modelo temporal explícito](#4.-modelo-temporal-explícito)
- [5. Concurrencia, ISR y recursos compartidos](#5.-concurrencia,-isr-y-recursos-compartidos)
- [6. Presupuesto de recursos](#6.-presupuesto-de-recursos)
- [7. Política de memoria dinámica](#7.-política-de-memoria-dinámica)
- [8. Bring-up HW/SW documentado](#8.-bring-up-hwsw-documentado)
- [9. Taxonomía de errores y recuperación](#9.-taxonomía-de-errores-y-recuperación)
- [10. Watchdog con contrato de supervisión](#10.-watchdog-con-contrato-de-supervisión)
- [11. Modos de operación y estados](#11.-modos-de-operación-y-estados)
- [12. Configuración segura y transaccional](#12.-configuración-segura-y-transaccional)
- [13. Logs como API de diagnóstico y auditoría](#13.-logs-como-api-de-diagnóstico-y-auditoría)
- [14. Seguridad desde diseño](#14.-seguridad-desde-diseño)
- [15. Testabilidad por diseño](#15.-testabilidad-por-diseño)
- [16. Trazabilidad completa](#16.-trazabilidad-completa)
- [17. QA gates estrictos](#17.-qa-gates-estrictos)
- [18. Parches y commits](#18.-parches-y-commits)
- [19. Release trazable](#19.-release-trazable)
- [20. Documentación audit-grade](#20.-documentación-audit-grade)
- [21. Fabricación, provisioning y vida en campo](#21.-fabricación,-provisioning-y-vida-en-campo)
- [22. Actualización tecnológica y fuentes verificadas](#22.-actualización-tecnológica-y-fuentes-verificadas)
- [23. Norma específica para laboratorios](#23.-norma-específica-para-laboratorios)
- [P0 — Bloquea entrega](#p0-bloquea-entrega)
- [P1 — Bloquea cierre de laboratorio/proyecto](#p1-bloquea-cierre-de-laboratorioproyecto)
- [P2 — Deuda aceptable solo si se declara](#p2-deuda-aceptable-solo-si-se-declara)

## 0. Clasificación obligatoria de cada entrega

Toda entrega debe indicar explícitamente:

```text
CUMPLE
NO CUMPLE
NO VALIDADO
PENDIENTE
```

No se puede afirmar “compila”, “funciona”, “está listo”, “es seguro”, “es producción” o “queda cerrado” si no hay evidencia real.

Formato obligatorio de cierre:

```text
CUMPLE:
- ...

NO CUMPLE:
- ...

NO VALIDADO:
- ...

PENDIENTE:
- ...
```

---

## 1. Arquitectura por componentes

Todo proyecto debe tener arquitectura explícita y documentada.

Debe separar, como mínimo:

```text
Application
Domain / Use Cases
Services
HAL / Drivers
Board Support Package
Platform / RTOS Adapter
Configuration
Logging / Diagnostics
Security
Tests
Tools
Docs
```

### Criterios

```text
CUMPLE si:
- main no contiene lógica crítica.
- Cada componente tiene una responsabilidad clara.
- Las dependencias son explícitas.
- No hay acoplamiento circular.
- La lógica de dominio no depende directamente de APIs del SDK.

NO CUMPLE si:
- main concentra inicialización, lógica de negocio, hardware y errores.
- Hay llamadas directas a GPIO/UART/I2C/SPI/NVS desde lógica de dominio.
- Hay componentes sin frontera clara.
```

---

## 2. OOP/SOLID adaptado a embebidos

La norma no exige C++ pesado ni sobreingeniería.

Exige:

```text
- encapsulación
- interfaces explícitas
- responsabilidad única
- bajo acoplamiento
- inversión de dependencias
- abstracción de hardware
- testabilidad
```

No exige:

```text
- herencia profunda
- RTTI
- excepciones
- patrones innecesarios
- memoria dinámica sin control
```

La interpretación correcta es: **diseño orientado a interfaces, responsabilidades y encapsulación**, no dogmatismo OO.

### Criterios

```text
CUMPLE si:
- Los componentes dependen de interfaces, no de implementaciones.
- El hardware puede sustituirse por fakes/stubs.
- Las responsabilidades están separadas.
- No hay singletons/globales críticos salvo justificación documentada.

NO CUMPLE si:
- Se usa OOP como dogma.
- Se introducen patrones complejos sin necesidad.
- Se degrada determinismo, RAM, flash o mantenibilidad.
```

---

## 3. FULL HAL / BSP obligatorio

Todo acceso a hardware debe pasar por HAL/BSP.

```text
Domain/Application
        ↓
Interface
        ↓
HAL/BSP
        ↓
SDK / registros / periférico físico
```

### Criterios

```text
CUMPLE si:
- GPIO, UART, I2C, SPI, ADC, NVS, timers y watchdog están encapsulados.
- El pinout está centralizado.
- El dominio no conoce números de GPIO.
- Hay fakes/stubs cuando aplica.

NO CUMPLE si:
- Hay gpio_set_level(), uart_read_bytes(), i2c_master_*, spi_device_* o llamadas equivalentes dispersas fuera de HAL/BSP.
- La lógica de aplicación depende de detalles de placa.
```

---

## 4. Modelo temporal explícito

Todo firmware debe declarar su modelo temporal:

```text
superloop
scheduler cooperativo
time-triggered scheduler
event-driven
RTOS con tareas
híbrido
ISR-driven
```

Cada tarea/actividad debe documentar:

```text
nombre
periodo
deadline
prioridad
WCET estimado o medido
jitter permitido
stack asignado
recursos compartidos
timeout
política de fallo
```

Ejemplo:

```text
task: telemetry_task
period: 60 s
deadline: 5 s
priority: 5
stack: 4096 bytes
shared_resources: mqtt_client, config
timeout: 10 s
failure_policy: log + retry backoff
```

### Criterios

```text
NO CUMPLE si:
- Hay delays fijos no justificados.
- Hay polling infinito sin timeout.
- Hay tareas sin stack budget.
- Hay prioridades sin criterio.
- Hay dependencias temporales implícitas.
```

---

## 5. Concurrencia, ISR y recursos compartidos

Todo recurso compartido debe tener propietario y contrato de acceso.

Debe documentarse:

```text
recurso
propietario
lectores
escritores
contexto: task / ISR / timer / callback
mecanismo de sincronización
timeout
política de fallo
```

Las ISR deben cumplir:

```text
- duración mínima
- no bloqueantes
- sin memoria dinámica
- sin logs pesados
- sin lógica de negocio
- sin acceso no protegido a recursos compartidos
- comunicación mediante cola/evento/flag ISR-safe
```

### Criterios

```text
NO CUMPLE si:
- Una ISR ejecuta lógica de negocio.
- Dos tareas acceden al mismo periférico sin propietario.
- Un mutex puede bloquear indefinidamente.
- Un callback modifica estado global sin contrato.
```

---

## 6. Presupuesto de recursos

Todo firmware debe declarar presupuesto de recursos.

Debe incluir:

```text
flash usada / límite
RAM estática
heap mínimo libre
stack por tarea
uso estimado de CPU
tamaño de buffers
uso de NVS/flash
consumo energético si aplica
```

### Criterios

```text
NO CUMPLE si:
- Se crean tareas sin stack declarado.
- Se usan buffers sin límite.
- Se usa heap en rutas críticas sin justificación.
- No se revisa el map file en entregas relevantes.
- No se mide stack high-water mark cuando aplica.
```

---

## 7. Política de memoria dinámica

La memoria dinámica queda restringida.

Permitida:

```text
- inicialización
- componentes de terceros justificados
- buffers con límites y fallo controlado
```

Prohibida:

```text
- ISR
- rutas hard real-time
- bucles críticos
- asignaciones sin comprobación de error
- reintentos indefinidos de asignación
```

### Criterios

```text
CUMPLE si:
- malloc/new están encapsulados o prohibidos.
- Toda asignación puede fallar de forma controlada.
- Se mide heap mínimo libre.
- Hay RESOURCE_EXHAUSTED documentado.

NO CUMPLE si:
- Se ignora malloc == nullptr.
- Se asigna memoria en cada ciclo periódico.
- Se usa std::string/std::vector sin política en firmware crítico.
```

---

## 8. Bring-up HW/SW documentado

Todo proyecto firmware debe tener:

```text
docs/bringup_checklist.md
```

Debe incluir:

```text
alimentaciones
reset
reloj
pinout
boot mode
UART/USB/JTAG
I2C scan
SPI sanity test
periféricos críticos
estado de LEDs
medidas eléctricas relevantes
riesgos de daño hardware
limitaciones instrumentales
```

### Criterios

```text
NO CUMPLE si:
- No se sabe qué puerto es consola.
- No se documenta pinout.
- Se prueba firmware sin confirmar alimentación/reset.
- No se documenta la diferencia entre USB, UART, JTAG o bootloader.
```

---

## 9. Taxonomía de errores y recuperación

Todo proyecto debe tener una taxonomía común de errores.

Mínimo:

```text
OK
BAD_PARAMETER
INVALID_STATE
NOT_READY
TIMEOUT
BUS_ERROR
PROTOCOL_ERROR
CONFIG_INVALID
SECURITY_VIOLATION
RESOURCE_EXHAUSTED
UNSUPPORTED
INTERNAL_ERROR
FATAL_ERROR
```

Cada error debe tener:

```text
código estable
severidad
origen
log asociado
acción de recuperación
si permite continuar
si exige modo degradado
si exige reset/fail-safe
```

### Criterios

```text
NO CUMPLE si:
- Una función crítica devuelve bool sin causa.
- Un timeout se ignora.
- Un fallo de periférico queda en silencio.
- Los errores solo existen como strings libres.
```

---

## 10. Watchdog con contrato de supervisión

Todo watchdog debe tener política explícita.

Debe documentarse:

```text
timeout
quién lo alimenta
condición mínima para alimentarlo
subsistemas supervisados
qué fallo impide alimentarlo
acción tras reset
lectura de causa de reset
modo debug
modo producción
```

### Criterios

```text
CUMPLE si:
- El watchdog solo se alimenta si el sistema está sano.
- La causa de reset queda registrada.
- El timeout está justificado por el modelo temporal.

NO CUMPLE si:
- Se alimenta desde una ISR periódica sin comprobar salud.
- Se alimenta desde múltiples puntos arbitrarios.
- Se desactiva en producción sin justificación.
```

---

## 11. Modos de operación y estados

Todo firmware debe declarar sus modos de operación.

Mínimos recomendados:

```text
BOOT
SELF_TEST
NORMAL
DEGRADED
RECOVERY
FACTORY
MAINTENANCE
PRODUCTION
FATAL
```

Cada transición debe tener:

```text
estado origen
evento
precondición
acción
estado destino
log
timeout
recuperación
```

### Criterios

```text
NO CUMPLE si:
- El firmware tiene estados implícitos no documentados.
- Un error grave sigue ejecutando como NORMAL.
- No existe modo degradado o fatal cuando el producto lo necesita.
```

---

## 12. Configuración segura y transaccional

Toda configuración debe estar validada, tipada y trazada.

Debe incluir:

```text
schema
tipo
rango
default seguro
persistencia
validación
aplicación transaccional
rollback si aplica
redacción de secretos
versión de configuración
migración si aplica
```

### Criterios

```text
CUMPLE si:
- Un valor inválido no altera el estado.
- Los defaults son seguros.
- La configuración sensible es write-only.
- La configuración persistida tiene versión.

NO CUMPLE si:
- set_period 0 es aceptado.
- Un valor fuera de rango se persiste.
- get_config imprime password/token en perfil endurecido.
```

---

## 13. Logs como API de diagnóstico y auditoría

Los logs son contrato, no texto libre.

Deben ser:

```text
estables
parseables
nombrados por evento
sin secretos
con severidad
con razón de error
con uptime/timestamp
con estado/modo
con código de error cuando aplique
```

Ejemplo válido:

```json
{"event":"config_update_rejected","severity":"warning","status":"rejected","reason":"out_of_range","uptime_ms":12345}
```

Ejemplo no válido:

```json
{"event":"uart_command_received","raw":"set_mqtt_password MiPassword123"}
```

### Criterios

```text
NO CUMPLE si:
- Se loguean passwords, tokens, claves privadas o comandos sensibles completos.
- Hay logs no parseables en rutas críticas.
- Los errores no tienen razón.
```

---

## 14. Seguridad desde diseño

Todo proyecto IoT/embebido debe incorporar seguridad desde diseño.

Mínimos obligatorios:

```text
threat model
activos protegidos
superficie de ataque
interfaces físicas
interfaces lógicas
gestión de secretos
logs sin secretos
configuración validada
perfiles DEV/FACTORY/PRODUCTION
política de actualización
riesgo residual
```

Para ESP32-S3/ESP-IDF deben considerarse según fase:

```text
Secure Boot
Flash Encryption
NVS Encryption
OTA firmada
anti-rollback
debug/JTAG/UART lockdown
TLS
identidad de dispositivo
SBOM
gestión de vulnerabilidades
```

### Criterios

```text
NO CUMPLE si:
- Hay secretos hardcodeados sin marcar como laboratorio inseguro.
- Hay secretos en logs.
- No hay threat model.
- No hay distinción DEV/FACTORY/PRODUCTION.
```

---

## 15. Testabilidad por diseño

Todo componente debe poder probarse razonablemente.

Debe existir separación entre:

```text
lógica pura
HAL
tiempo
transporte
persistencia
aleatoriedad
seguridad
```

Requisitos:

```text
tests unitarios cuando sea posible
fakes/stubs para hardware
tests manuales documentados si no hay automatización
tests de regresión para cada bug
casos positivos y negativos
logs de evidencia
```

### Criterios

```text
NO CUMPLE si:
- Una regla de negocio solo puede probarse flasheando hardware.
- No hay forma de simular errores de HAL.
- No hay test de regresión para un bug corregido.
```

---

## 16. Trazabilidad completa

Todo requisito debe poder seguirse así:

```text
requisito → diseño → implementación → test → evidencia
```

Cada requisito debe tener:

```text
ID
descripción
tipo: funcional / seguridad / temporal / hardware / calidad
justificación
componente responsable
test asociado
evidencia
estado
```

Ejemplo:

```text
SR-LOG-001
Los logs del perfil HARDENED no deben exponer secretos.

Diseño:
secure_log + command_console redaction policy

Implementación:
CommandConsole::logCommandSafely()

Test:
tools/check_no_secrets_in_logs.py --profile hardened

Evidencia:
docs/audit_evidence.md
```

---

## 17. QA gates estrictos

Cada entrega debe pasar gates objetivos.

Gates mínimos para ESP-IDF:

```text
git status revisado
target correcto
idf.py set-target esp32s3
idf.py build
0 errores
0 warnings
0 deprecated APIs
dependencias CMake explícitas
sin build/ en paquete fuente
sin sdkconfig salvo decisión documentada
static checks OK
tests unitarios si existen
scripts QA OK
documentación actualizada
commit message incluido
```

### Criterios

```text
NO CUMPLE si:
- Hay warnings.
- No se ha ejecutado build y se afirma que compila.
- Hay dependencias implícitas.
- No hay evidencia de pruebas.
```

---

## 18. Parches y commits

Todo parche debe ser atómico, aplicable y trazable.

Obligatorio:

```text
patch contra árbol real
git apply --check OK
alcance definido
causa
cambio
impacto
validación
limitaciones
mensaje de commit
```

Formato:

```text
tipo(scope): resumen
```

Ejemplos:

```text
fix(lab01): eliminar fuga de secretos en consola endurecida
feat(hal): añadir abstracción de consola USB Serial-JTAG
test(config): cubrir validación estricta de sample_period_s
docs(audit): documentar evidencias del LAB 01
```

### Criterios

```text
NO CUMPLE si:
- El patch no aplica contra el árbol real.
- No incluye commit message.
- Mezcla varias correcciones no relacionadas.
- Toca documentación/código sin justificación.
```

---

## 19. Release trazable

Toda entrega debe ser reproducible y trazable.

Debe incluir:

```text
versión
target
toolchain
ESP-IDF version
commit
perfil de build
hash de artefactos si aplica
changelog
limitaciones conocidas
estado de gates
```

### Criterios

```text
NO CUMPLE si:
- README dice una versión y firmware imprime otra.
- Se entrega ZIP con build/ contaminando la fuente.
- No hay changelog.
- No hay manifest de release cuando aplica.
```

---

## 20. Documentación audit-grade

Todo proyecto debe tener documentación suficiente para auditarlo y mantenerlo.

Documentos mínimos:

```text
README.md
CHANGELOG.md
docs/architecture.md
docs/requirements.md
docs/security_requirements.md
docs/threat_model.md
docs/temporal_model.md
docs/concurrency_model.md
docs/resource_budget.md
docs/bringup_checklist.md
docs/test_plan.md
docs/audit_evidence.md
docs/known_limitations.md
docs/risk_register.md
```

Según fase:

```text
docs/security_architecture.md
docs/ota_policy.md
docs/provisioning_policy.md
docs/watchdog_policy.md
docs/release_process.md
SECURITY.md
```

---

## 21. Fabricación, provisioning y vida en campo

En proyectos que evolucionen hacia producto debe existir política de fabricación y operación.

Debe contemplar:

```text
perfil DEV
perfil FACTORY
perfil PRODUCTION
provisioning de identidad
provisioning de secretos
bloqueo post-fabricación
factory reset controlado
decommissioning
diagnóstico de campo
causa de reset
contador de boots
último error fatal
versión activa
estado de seguridad
```

---

## 22. Actualización tecnológica y fuentes verificadas

El estándar no queda limitado a una bibliografía fija.

Se admiten nuevas tendencias solo si están justificadas por fuentes verificables.

Jerarquía de fuentes:

```text
A — Norma oficial / organismo regulador.
B — Estándar industrial reconocido.
C — Guía oficial de fabricante o autoridad técnica.
D — Artículo académico revisado o preprint técnico con metodología clara.
E — Tendencia industrial razonable, aceptada solo si no contradice A-D.
```

Cada decisión nueva debe indicar:

```text
fuente base
por qué aplica
criterio de aceptación
cómo se verifica
limitaciones
```

Tendencias aceptables si están justificadas:

```text
Secure by Design
DevSecOps embebido
SBOM/VEX
SLSA/provenance
firmware signing
reproducible builds
fuzzing de parsers/protocolos
contract-based verification
Rust embebido donde aporte
model-based design cuando reduzca riesgo
continuous compliance
```

---

## 23. Norma específica para laboratorios

Un laboratorio puede tener vulnerabilidades o simplificaciones intencionadas, pero deben estar controladas.

Permitido:

```text
vulnerabilidades intencionadas
stubs
simuladores
alcance reducido
no producción
perfiles inseguros didácticos
```

No permitido:

```text
warnings
parches no validados
arquitectura accidentalmente monolítica
dependencias implícitas
documentación falsa
afirmar build no validado
fugas de secretos no intencionadas
```

### Criterio

```text
CUMPLE como laboratorio si:
- el objetivo didáctico está declarado
- las vulnerabilidades intencionadas están documentadas
- las mitigaciones están probadas
- hay evidencia
- hay gates
- hay limitaciones claras

NO CUMPLE si:
- “es un laboratorio” se usa para justificar mala ingeniería.
```

---

# Severidad de incumplimientos

## P0 — Bloquea entrega

```text
No compila.
Hay warnings.
Hay API deprecada.
No hay target validado.
Hay fuga de secretos.
No hay HAL para hardware crítico.
No hay patch aplicable.
No hay commit message.
Se afirma algo no validado.
Hay riesgo de dañar hardware no documentado.
```

## P1 — Bloquea cierre de laboratorio/proyecto

```text
Falta arquitectura.
Falta modelo temporal.
Falta política de errores.
Falta resource budget.
Falta bring-up checklist.
Falta test plan.
Falta evidencia.
Falta trazabilidad.
```

## P2 — Deuda aceptable solo si se declara

```text
Faltan tests automatizados no críticos.
Falta segunda placa.
Falta profiling completo.
Falta SBOM completo en fase inicial.
Falta fuzzing en parsers no expuestos todavía.
```

---

# Resumen final del estándar

Todo proyecto embebido debe cumplir:

```text
1. Clasificación CUMPLE / NO CUMPLE / NO VALIDADO.
2. Arquitectura por componentes.
3. OOP/SOLID adaptado a embebidos.
4. FULL HAL/BSP.
5. Modelo temporal explícito.
6. Política de concurrencia, ISR y recursos compartidos.
7. Presupuesto de recursos.
8. Política de memoria dinámica.
9. Bring-up HW/SW documentado.
10. Taxonomía de errores y recuperación.
11. Watchdog con contrato.
12. Modos de operación y transiciones.
13. Configuración segura y transaccional.
14. Logs como API sin secretos.
15. Seguridad desde diseño.
16. Testabilidad por diseño.
17. Trazabilidad requisito → diseño → implementación → test → evidencia.
18. QA gates estrictos.
19. Parches contra árbol real con commit message.
20. Release trazable.
21. Documentación audit-grade.
22. Fabricación/provisioning/vida en campo cuando aplique.
23. Actualización tecnológica basada en fuentes verificadas.
24. Laboratorios rigurosos, aunque sean didácticos.
```

---

# Fuentes base recomendadas

Este estándar se debe mantener alineado con:

```text
- Bibliografía clásica y moderna de sistemas embebidos.
- Normas industriales reconocidas.
- Guías oficiales de ciberseguridad.
- Documentación oficial de fabricantes.
- Evidencia académica o técnica verificable.
```

Fuentes de referencia:

```text
- Elecia White — Making Embedded Systems.
- Michael J. Pont — Patterns for Time-Triggered Embedded Systems.
- IEC 62443.
- ETSI EN 303 645.
- NIST SSDF SP 800-218.
- CISA Secure by Design.
- CRA / RED europeos.
- MISRA C/C++.
- CERT C/C++.
- BARR-C.
- NASA/JPL Power of Ten.
- CycloneDX / SPDX.
- SLSA / OpenSSF.
```
