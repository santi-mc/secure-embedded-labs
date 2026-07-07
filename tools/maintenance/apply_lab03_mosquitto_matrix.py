#!/usr/bin/env python3
"""
Generate LAB 03 as a Mosquitto public-broker scenario matrix.

This maintenance tool intentionally writes the LAB 03 tree from templates so the
patch can be add-only and robust against Markdown context drift.
"""

from __future__ import annotations

from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "labs" / "lab03_mqtt_tls"


def clean(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def write(relative: str, content: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean(content), encoding="utf-8", newline="\n")


def remove_gitkeep(relative_dir: str) -> None:
    marker = ROOT / relative_dir / ".gitkeep"
    if marker.exists():
        marker.unlink()


def update_if_present(path: Path, replacements: list[tuple[str, str]]) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def generate_docs() -> None:
    write("labs/lab03_mqtt_tls/README.md", r'''
        # LAB 03 — Matriz MQTT contra test.mosquitto.org

        **Versión:** 0.1.0

        ## Índice

        - [Objetivo](#objetivo)
        - [Objetivos de aprendizaje](#objetivos-de-aprendizaje)
        - [Prerrequisitos](#prerrequisitos)
        - [Alcance](#alcance)
        - [Fuera de alcance](#fuera-de-alcance)
        - [Hardware requerido](#hardware-requerido)
        - [Software requerido](#software-requerido)
        - [Arquitectura prevista](#arquitectura-prevista)
        - [Modelo temporal](#modelo-temporal)
        - [Threat model](#threat-model)
        - [Requisitos](#requisitos)
        - [Cómo compilar](#cómo-compilar)
        - [Cómo flashear](#cómo-flashear)
        - [Cómo probar](#cómo-probar)
        - [Evidencias esperadas](#evidencias-esperadas)
        - [Errores comunes](#errores-comunes)
        - [Ejercicios](#ejercicios)
        - [Preguntas de repaso](#preguntas-de-repaso)
        - [Fuentes](#fuentes)
        - [Estado](#estado)

        ## Objetivo

        Construir una matriz reproducible de escenarios MQTT usando el broker público `test.mosquitto.org`.

        El primer objetivo ejecutable es demostrar el baseline inseguro `M03-1883`: MQTT TCP plano, puerto 1883, sin TLS y sin autenticación. El laboratorio queda preparado desde el primer commit para cubrir los once escenarios publicados por el broker: MQTT plano, MQTT con autenticación, MQTT sobre TLS, mTLS, certificado expirado y MQTT over WebSockets.

        ## Objetivos de aprendizaje

        - Entender la diferencia entre MQTT plano, MQTT autenticado, MQTT sobre TLS y MQTT sobre WebSockets.
        - Evidenciar por qué MQTT sin TLS no debe considerarse seguro aunque permita conexión funcional.
        - Comparar los escenarios publicados por `test.mosquitto.org` en puertos 1883, 1884, 8883, 8884, 8885, 8886, 8887, 8080, 8081, 8090 y 8091.
        - Aprender a clasificar cada escenario como `CUMPLE`, `NO CUMPLE`, `NO VALIDADO` o `PENDIENTE` según transporte, autenticación y validación de certificados.
        - Generar evidencias reproducibles mediante consola, logs NDJSON y gates estáticos.

        ## Prerrequisitos

        - Placa ESP32-S3 con consola USB Serial/JTAG operativa.
        - ESP-IDF v6.0.x configurado para target `esp32s3`.
        - Python 3 disponible dentro del entorno ESP-IDF.
        - Puerto serie identificado, por ejemplo `COM5` en Windows.
        - Para LAB 03A no se requieren credenciales reales, certificados privados ni conexión real al broker.
        - Para fases posteriores será necesario acceso de red hacia `test.mosquitto.org` y material criptográfico de prueba cuando aplique.

        ## Alcance

        Esta fase crea el contrato de matriz y un firmware didáctico inicial que ejecuta comprobaciones dry-run de política MQTT. No establece todavía conexión real con el broker.

        LAB 03A cubre:

        ```text
        M03-1883 — MQTT TCP 1883 sin TLS y sin autenticación.
        ```

        El resto de escenarios queda documentado y trazado para fases posteriores.

        ## Fuera de alcance

        - Conexión real Wi-Fi/Ethernet al broker público.
        - Integración real de ESP-MQTT.
        - Validación real de certificados X.509.
        - mTLS con certificado cliente.
        - MQTT over WebSockets real.
        - Gestión de secretos reales.

        ## Hardware requerido

        - ESP32-S3 compatible con ESP-IDF v6.0.x.
        - Cable USB de datos para alimentación, flasheo y consola USB Serial/JTAG.
        - Equipo host con acceso a puerto serie.

        ## Software requerido

        - ESP-IDF v6.0.x.
        - Python del entorno ESP-IDF.
        - `pyserial` para captura de evidencias desde consola.
        - Git para versionado y revisión de gates.

        ## Arquitectura prevista

        ```text
        main
        ├── board_hal
        ├── command_console
        ├── lab03_domain
        ├── mqtt_scenario
        └── secure_log
        ```

        La implementación inicial es intencionadamente dry-run para separar política de seguridad, trazabilidad de escenarios y contrato de evidencias antes de introducir red, ESP-MQTT, certificados y broker real.

        ## Modelo temporal

        - Arranque del firmware y emisión de evento `boot`.
        - Inicio de consola y emisión de evento `console_start`.
        - Lectura interactiva línea a línea desde USB Serial/JTAG.
        - Ejecución síncrona de comandos de escenario.
        - Emisión de logs NDJSON con `uptime_ms` para cada evento.
        - Captura automática con tiempos acotados desde script Python.

        No hay todavía timeouts de red, DNS, TLS handshake ni reconexión MQTT real en LAB 03A.

        ## Threat model

        Activos protegidos futuros:

        - Credenciales MQTT.
        - Identidad del dispositivo.
        - Topics y payloads operativos.
        - Material criptográfico de cliente.
        - Integridad del canal broker-dispositivo.

        Amenazas modeladas desde LAB 03A:

        - Escucha pasiva de tráfico MQTT plano.
        - Exposición de credenciales si se usa autenticación sin TLS.
        - Confusión entre conectividad funcional y seguridad del canal.
        - Aceptación indebida de certificados expirados o no confiables en fases TLS.

        ## Requisitos

        | ID | Requisito | Estado |
        | --- | --- | --- |
        | LAB03-RQ-001 | Definir matriz completa `test.mosquitto.org`. | CUMPLE |
        | LAB03-RQ-002 | Implementar baseline `M03-1883` sin TLS. | CUMPLE |
        | LAB03-RQ-003 | Clasificar `M03-1883` como funcional pero `NO CUMPLE` seguridad. | CUMPLE |
        | LAB03-RQ-004 | Emitir logs NDJSON reproducibles. | CUMPLE |
        | LAB03-RQ-005 | Capturar y verificar evidencia de consola. | CUMPLE |
        | LAB03-RQ-006 | Ejecutar conexión real a broker. | PENDIENTE |
        | LAB03-RQ-007 | Validar TLS, CA, mTLS y certificado expirado. | PENDIENTE |

        ## Cómo compilar

        ```powershell
        cd labs\lab03_mqtt_tls\firmware
        idf.py set-target esp32s3
        idf.py build
        ```

        El directorio `build/`, `sdkconfig` y `sdkconfig.old` son artefactos generados y no deben versionarse.

        ## Cómo flashear

        ```powershell
        cd labs\lab03_mqtt_tls\firmware
        idf.py -p COM5 flash monitor
        ```

        Sustituir `COM5` por el puerto real del ESP32-S3.

        ## Cómo probar

        Prueba manual mínima en monitor:

        ```text
        help
        scenario_list
        select_scenario M03-1883
        scenario_status
        mqtt_connect_dry_run
        mqtt_publish_dry_run
        security_status
        ```

        Captura automática:

        ```powershell
        python labs\lab03_mqtt_tls\tools\capture_console_evidence.py `
          --port COM5 `
          --scenario M03-1883 `
          --output labs\lab03_mqtt_tls\evidence\lab03_m03_1883_console.log

        python labs\lab03_mqtt_tls\tools\check_mqtt_scenario_logs.py `
          labs\lab03_mqtt_tls\evidence\lab03_m03_1883_console.log `
          --scenario M03-1883
        ```

        Gates:

        ```powershell
        python labs\lab03_mqtt_tls\tools\capture_static_gates.py
        python tools\repo_quality_gates\run_static_repo_gates.py
        python labs\lab03_mqtt_tls\tools\run_static_gates.py
        ```

        ## Evidencias esperadas

        ```text
        evidence/lab03_m03_1883_console.log
        evidence/lab03_static_gates.txt
        ```

        Evidencias pendientes para cierre completo futuro:

        ```text
        evidence/lab03_build_esp32s3.txt
        evidence/lab03_real_broker_matrix.txt
        evidence/lab03_tls_certificate_validation.txt
        ```

        ## Errores comunes

        - Capturar el puerto mientras `idf.py monitor` sigue abierto.
        - Flashear otra carpeta de laboratorio y obtener eventos de `LAB02`.
        - Dejar `firmware/build`, `sdkconfig` o `sdkconfig.old` dentro del árbol antes de ejecutar gates.
        - Confundir `M03-1883` funcional con un diseño seguro.
        - Usar credenciales reales contra un broker público.

        ## Ejercicios

        - Identificar qué escenarios de la matriz son funcionales pero `NO CUMPLE` desde el punto de vista de seguridad.
        - Comparar 1883 frente a 1884 y explicar por qué autenticación sin TLS no protege credenciales.
        - Preparar la extensión de LAB 03B para `M03-1884` manteniendo evidencias NDJSON.
        - Diseñar los criterios de rechazo esperados para `M03-8887` con certificado expirado.

        ## Preguntas de repaso

        - ¿Por qué MQTT sin TLS no debe transportar credenciales reales?
        - ¿Qué diferencia hay entre autenticación de cliente y cifrado del canal?
        - ¿Qué evidencia mínima demuestra que `M03-1883` es solo un baseline inseguro?
        - ¿Por qué un certificado expirado debe producir rechazo en un cliente endurecido?

        ## Fuentes

        - Documentación pública de `test.mosquitto.org`.
        - Documentación ESP-IDF de consola USB Serial/JTAG.
        - Documentación ESP-MQTT para fases posteriores.
        - Estándar interno `standard/estandar_diseno_embebido_audit_grade.md`.

        ## Estado

        ```text
        CUMPLE:
        - Matriz contractual completa de test.mosquitto.org documentada.
        - Firmware inicial dry-run para ESP32-S3 añadido.
        - Baseline 1883 sin TLS modelado como NO CUMPLE de seguridad esperado.
        - Consola interactiva USB Serial/JTAG validada.
        - Captura de evidencia M03-1883 generada y verificada.
        - Gates y herramientas de evidencia añadidos.

        NO CUMPLE:
        - 1883/1884/8080/8090 no son diseños seguros porque no usan TLS.
        - Esta fase no implementa conexión real al broker.

        NO VALIDADO:
        - Build real ESP-IDF con stdout completo y cero warnings versionado.
        - Matriz real contra broker público.
        - Validación real de certificados TLS.

        PENDIENTE:
        - LAB 03B: MQTT 1884 autenticado sin TLS.
        - Integrar ESP-MQTT como dependencia gestionada.
        - Añadir Wi-Fi/provisioning de red.
        - Ejecutar matriz real contra test.mosquitto.org.
        - Introducir TLS, CA, mTLS y WebSockets en fases posteriores.
        ```
    ''')

    write("labs/lab03_mqtt_tls/docs/scenario_matrix.md", r'''
        # LAB 03 — Matriz de escenarios MQTT

        ## Índice

        - [Objetivo](#objetivo)
        - [Matriz](#matriz)
        - [Criterios de seguridad](#criterios-de-seguridad)
        - [Notas de certificados](#notas-de-certificados)

        ## Objetivo

        Definir la matriz contractual completa de escenarios que se probarán contra `test.mosquitto.org`.

        ## Matriz

        | ID | Puerto | Transporte | TLS | Autenticación | Estado esperado |
        | --- | ---: | --- | --- | --- | --- |
        | M03-1883 | 1883 | MQTT TCP | No | No | Conecta en fase real, pero NO CUMPLE seguridad. |
        | M03-1884 | 1884 | MQTT TCP | No | Usuario/password | Conecta en fase real, pero credenciales sin TLS. |
        | M03-8883 | 8883 | MQTT TCP | Sí | No | Debe validar certificado servidor con CA Mosquitto. |
        | M03-8884 | 8884 | MQTT TCP | Sí | Certificado cliente | Debe exigir certificado cliente. |
        | M03-8885 | 8885 | MQTT TCP | Sí | Usuario/password | Debe validar TLS y autenticación. |
        | M03-8886 | 8886 | MQTT TCP | Sí | No | Debe validar certificado de cadena pública. |
        | M03-8887 | 8887 | MQTT TCP | Sí expirado | No | Debe rechazar certificado expirado. |
        | M03-8080 | 8080 | MQTT WebSocket | No | No | Conecta en fase real, pero NO CUMPLE seguridad. |
        | M03-8081 | 8081 | MQTT WebSocket | Sí | No | Debe validar WSS. |
        | M03-8090 | 8090 | MQTT WebSocket | No | Usuario/password | Conecta en fase real, pero credenciales sin TLS. |
        | M03-8091 | 8091 | MQTT WebSocket | Sí | Usuario/password | Debe validar WSS + autenticación. |

        ## Criterios de seguridad

        ```text
        CUMPLE:
        - TLS habilitado cuando hay autenticación o datos sensibles.
        - Certificado servidor validado.
        - Certificado expirado rechazado.
        - Certificado cliente requerido cuando el escenario lo exige.

        NO CUMPLE:
        - MQTT sin TLS como diseño final.
        - Usuario/password sobre transporte no cifrado.
        - Aceptar certificados expirados.
        - Desactivar verificación de certificado en escenarios TLS.
        ```

        ## Notas de certificados

        Las fases TLS deben incorporar CA de Mosquitto o CA pública aplicable según el puerto. No se deben almacenar certificados privados reales en el repositorio.
    ''')

    write("labs/lab03_mqtt_tls/docs/threat_model.md", r'''
        # LAB 03 — Threat model

        ## Índice

        - [Activos](#activos)
        - [Atacantes](#atacantes)
        - [Amenazas](#amenazas)
        - [Mitigaciones previstas](#mitigaciones-previstas)

        ## Activos

        - Identidad lógica MQTT.
        - Usuario/password ficticio de laboratorio.
        - Payloads publicados.
        - Certificados CA y certificados cliente futuros.
        - Logs de diagnóstico.

        ## Atacantes

        - Observador pasivo de red.
        - Intermediario activo capaz de MITM.
        - Usuario local con acceso a consola.
        - Cliente MQTT externo suscrito al broker público.

        ## Amenazas

        | Amenaza | Escenario | Estado |
        | --- | --- | --- |
        | Lectura de payload en claro | 1883, 1884, 8080, 8090 | CUMPLE como vulnerabilidad didáctica. |
        | Robo de credenciales | 1884, 8090 | CUMPLE como vulnerabilidad didáctica. |
        | MITM TLS si no se valida CA | 8883, 8885, 8886, 8081, 8091 | PENDIENTE de fases TLS. |
        | Aceptación de certificado expirado | 8887 | Debe rechazarse. |
        | Exposición de secretos en logs | Todos | Debe bloquearse en perfiles endurecidos. |

        ## Mitigaciones previstas

        - TLS con validación de certificado servidor.
        - Rechazo de certificados expirados.
        - Redacción de credenciales en logs.
        - mTLS para puerto 8884.
        - Separación de escenarios inseguros y endurecidos.
    ''')

    write("labs/lab03_mqtt_tls/docs/test_plan.md", r'''
        # LAB 03 — Plan de pruebas

        ## Índice

        - [Objetivo](#objetivo)
        - [Pruebas de fase 03A](#pruebas-de-fase-03a)
        - [Pruebas pendientes](#pruebas-pendientes)
        - [Criterio de cierre](#criterio-de-cierre)

        ## Objetivo

        Validar primero el baseline MQTT sin TLS y dejar trazada la matriz completa para fases posteriores.

        ## Pruebas de fase 03A

        | ID | Prueba | Estado esperado |
        | --- | --- | --- |
        | T03A-001 | `help` | Lista comandos. |
        | T03A-002 | `scenario_list` | Lista los once escenarios. |
        | T03A-003 | `select_scenario M03-1883` | Selecciona baseline sin TLS. |
        | T03A-004 | `scenario_status` | Muestra host, puerto 1883 y `tls_enabled=false`. |
        | T03A-005 | `mqtt_connect_dry_run` | Emite `security_result=NO_CUMPLE_EXPECTED`. |
        | T03A-006 | `mqtt_publish_dry_run` | Emite publicación simulada sin broker real. |
        | T03A-007 | checker de logs | Debe aceptar el baseline inseguro como evidencia didáctica. |

        ## Pruebas pendientes

        - Conexión real a 1883.
        - Autenticación 1884.
        - TLS 8883/8886/8885.
        - mTLS 8884.
        - Certificado expirado 8887.
        - WebSockets 8080/8081/8090/8091.

        ## Criterio de cierre

        La fase 03A se cierra cuando el firmware compile, arranque en ESP32-S3, capture evidencia de `M03-1883` y pasen gates estáticos.
    ''')

    write("labs/lab03_mqtt_tls/docs/audit_evidence.md", r'''
        # LAB 03 — Evidencias de auditoría

        ## Índice

        - [Estado](#estado)
        - [Evidencias esperadas](#evidencias-esperadas)
        - [Pendientes](#pendientes)

        ## Estado

        ```text
        NO VALIDADO:
        - Build real pendiente.
        - Flash en hardware pendiente.
        - Captura de consola pendiente.
        ```

        ## Evidencias esperadas

        | Evidencia | Estado | Descripción |
        | --- | --- | --- |
        | `evidence/lab03_m03_1883_console.log` | PENDIENTE | Baseline MQTT 1883 sin TLS. |
        | `evidence/lab03_static_gates.txt` | PENDIENTE | Gates globales y LAB 03. |

        ## Pendientes

        - Capturar stdout completo de `idf.py build`.
        - Añadir evidencias de conexión real al broker en fases posteriores.
        - Añadir evidencias TLS/certificados en fases posteriores.
    ''')

    write("labs/lab03_mqtt_tls/docs/certificate_policy.md", r'''
        # LAB 03 — Política de certificados

        ## Índice

        - [Objetivo](#objetivo)
        - [Reglas](#reglas)
        - [Material permitido](#material-permitido)
        - [Material prohibido](#material-prohibido)

        ## Objetivo

        Definir cómo se incorporarán certificados en las fases TLS del LAB 03.

        ## Reglas

        - Las CA públicas o de Mosquitto pueden versionarse si su licencia lo permite y son públicas.
        - Los certificados privados de cliente no deben versionarse.
        - Las claves privadas deben generarse localmente y quedar fuera de Git.
        - El puerto 8887 debe fallar por certificado expirado.

        ## Material permitido

        - CA pública en PEM/DER.
        - Certificados de ejemplo sin clave privada.
        - Instrucciones reproducibles para generar certificados cliente.

        ## Material prohibido

        - Claves privadas reales.
        - Tokens reales.
        - Certificados de infraestructura privada.
    ''')

    write("labs/lab03_mqtt_tls/docs/risk_register.md", r'''
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
    ''')

    write("labs/lab03_mqtt_tls/docs/references.md", r'''
        # LAB 03 — Fuentes

        ## Índice

        - [Fuentes principales](#fuentes-principales)

        ## Fuentes principales

        - Mosquitto public test broker: `test.mosquitto.org`.
        - ESP-MQTT official documentation.
        - ESP-IDF programming guide.
        - MQTT 3.1.1 / MQTT 5.0 specifications.
    ''')

    write("labs/lab03_mqtt_tls/evidence/README.md", r'''
        # Evidencias LAB 03

        ## Índice

        - [Propósito](#propósito)
        - [Evidencias de fase 03A](#evidencias-de-fase-03a)
        - [Pendientes](#pendientes)

        ## Propósito

        Este directorio almacena evidencias de ejecución del LAB 03.

        No se deben versionar credenciales reales, certificados privados ni payloads sensibles.

        ## Evidencias de fase 03A

        | Fichero | Estado | Descripción |
        | --- | --- | --- |
        | `lab03_m03_1883_console.log` | PENDIENTE | Baseline MQTT 1883 sin TLS. |
        | `lab03_static_gates.txt` | PENDIENTE | Gates estáticos. |

        ## Pendientes

        | Evidencia | Estado |
        | --- | --- |
        | `lab03_build_esp32s3.txt` | PENDIENTE |
        | `lab03_real_broker_matrix.txt` | PENDIENTE |
        | `lab03_tls_certificate_validation.txt` | PENDIENTE |
    ''')

    write("labs/lab03_mqtt_tls/test/manual_lab03_commands.txt", r'''
        help
        scenario_list
        select_scenario M03-1883
        scenario_status
        mqtt_connect_dry_run
        mqtt_publish_dry_run
        security_status
    ''')

    write("labs/lab03_mqtt_tls/CHANGELOG.md", r'''
        # CHANGELOG LAB 03

        ## Unreleased

        - Añadido LAB 03A como matriz MQTT contra test.mosquitto.org.
        - Añadido baseline MQTT 1883 sin TLS como escenario inseguro controlado.
        - Añadidos firmware dry-run, documentación, gates y herramientas de evidencia.
    ''')

    write("labs/lab03_mqtt_tls/COMMIT_MESSAGE.txt", r'''
        feat(lab03): añadir matriz MQTT con baseline sin TLS
    ''')

# Firmware generation omitted in this compact patch body? No, continue below.

def generate_firmware() -> None:
    write("labs/lab03_mqtt_tls/firmware/CMakeLists.txt", r'''
        cmake_minimum_required(VERSION 3.20)
        include($ENV{IDF_PATH}/tools/cmake/project.cmake)
        project(secure_embedded_labs_lab03)
    ''')

    write("labs/lab03_mqtt_tls/firmware/sdkconfig.defaults", r'''
        CONFIG_IDF_TARGET="esp32s3"
        CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y
        CONFIG_COMPILER_CXX_EXCEPTIONS=n
    ''')

    write("labs/lab03_mqtt_tls/firmware/main/CMakeLists.txt", 'idf_component_register(SRCS "main.cpp" REQUIRES app_core)\n')
    write("labs/lab03_mqtt_tls/firmware/main/main.cpp", r'''
        #include "app_core/app_core.hpp"

        extern "C" void app_main(void) {
            secure_lab::runLab03App();
        }
    ''')

    write("labs/lab03_mqtt_tls/firmware/components/lab03_domain/CMakeLists.txt", 'idf_component_register(SRCS "src/types.cpp" INCLUDE_DIRS "include")\n')
    write("labs/lab03_mqtt_tls/firmware/components/lab03_domain/include/lab03_domain/types.hpp", r'''
        #pragma once

        #include <cstddef>
        #include <cstdint>
        #include <string_view>

        namespace secure_lab {
        enum class TransportKind : std::uint8_t { MqttTcp, MqttWebSocket };
        struct MqttScenario {
            std::string_view id;
            std::string_view host;
            std::uint16_t port;
            TransportKind transport;
            bool tls_enabled;
            bool uses_username_password;
            bool requires_client_certificate;
            bool certificate_expired;
            std::string_view security_result;
            std::string_view notes;
        };
        struct ConsoleLine { char value[160]{}; std::size_t length{0}; };
        enum class ConsoleReadStatus : std::uint8_t { Ok, NoData, LineTooLong };
        inline constexpr std::string_view kProjectName = "secure_embedded_labs_lab03";
        inline constexpr std::string_view kFirmwareVersion = "0.1.0";
        inline constexpr std::string_view kLabId = "LAB03";
        inline constexpr std::string_view kTarget = "esp32s3";
        inline constexpr std::string_view kConsoleTransport = "usb_serial_jtag_stdio";
        const char* toString(TransportKind value) noexcept;
        }  // namespace secure_lab
    ''')
    write("labs/lab03_mqtt_tls/firmware/components/lab03_domain/src/types.cpp", r'''
        #include "lab03_domain/types.hpp"
        namespace secure_lab {
        const char* toString(TransportKind value) noexcept {
            switch (value) {
                case TransportKind::MqttTcp: return "mqtt_tcp";
                case TransportKind::MqttWebSocket: return "mqtt_websocket";
            }
            return "unknown";
        }
        }  // namespace secure_lab
    ''')

    write("labs/lab03_mqtt_tls/firmware/components/secure_log/CMakeLists.txt", r'''
        idf_component_register(SRCS "src/json_log.cpp" INCLUDE_DIRS "include" REQUIRES esp_timer lab03_domain)
    ''')
    write("labs/lab03_mqtt_tls/firmware/components/secure_log/include/secure_log/json_log.hpp", r'''
        #pragma once
        #include <initializer_list>
        #include <string_view>
        namespace secure_lab {
        struct JsonField { std::string_view key; std::string_view value; };
        class JsonLog { public: void event(std::string_view name, std::initializer_list<JsonField> fields = {}) const; };
        }  // namespace secure_lab
    ''')
    write("labs/lab03_mqtt_tls/firmware/components/secure_log/src/json_log.cpp", r'''
        #include "secure_log/json_log.hpp"
        #include "esp_timer.h"
        #include <cstdio>
        namespace secure_lab {
        namespace {
        void printEscaped(std::string_view value) {
            for (const char ch : value) {
                if (ch == '"') { std::printf("\\\""); }
                else if (ch == '\\') { std::printf("\\\\"); }
                else { std::printf("%c", ch); }
            }
        }
        }
        void JsonLog::event(std::string_view name, std::initializer_list<JsonField> fields) const {
            const auto uptime_ms = static_cast<long long>(esp_timer_get_time() / 1000LL);
            std::printf("{\"event\":\"");
            printEscaped(name);
            std::printf("\",\"schema_version\":1,\"uptime_ms\":%lld", uptime_ms);
            for (const auto& field : fields) {
                std::printf(",\"");
                printEscaped(field.key);
                std::printf("\":\"");
                printEscaped(field.value);
                std::printf("\"");
            }
            std::printf("}\n");
            std::fflush(stdout);
        }
        }  // namespace secure_lab
    ''')

    write("labs/lab03_mqtt_tls/firmware/components/board_hal/CMakeLists.txt", 'idf_component_register(SRCS "src/stdio_console.cpp" INCLUDE_DIRS "include" REQUIRES freertos lab03_domain)\n')
    write("labs/lab03_mqtt_tls/firmware/components/board_hal/include/board_hal/stdio_console.hpp", r'''
        #pragma once
        #include "lab03_domain/types.hpp"
        namespace secure_lab {
        class StdioConsole {
        public:
            ConsoleReadStatus readLine(ConsoleLine& out_line) noexcept;
        private:
            char buffer_[sizeof(ConsoleLine::value)]{};
            std::size_t length_{0};
            bool previous_was_cr_{false};
        };
        }  // namespace secure_lab
    ''')
    write("labs/lab03_mqtt_tls/firmware/components/board_hal/src/stdio_console.cpp", r'''
        #include "board_hal/stdio_console.hpp"
        #include "freertos/FreeRTOS.h"
        #include "freertos/task.h"
        #include <cstdio>
        #include <cstring>
        namespace secure_lab {
        namespace { inline constexpr TickType_t kNoDataDelay = pdMS_TO_TICKS(20U); }
        ConsoleReadStatus StdioConsole::readLine(ConsoleLine& out_line) noexcept {
            out_line = ConsoleLine{};
            while (true) {
                const int value = std::getchar();
                if (value == EOF) { clearerr(stdin); vTaskDelay(kNoDataDelay); return ConsoleReadStatus::NoData; }
                const char ch = static_cast<char>(value);
                if (ch == '\r' || ch == '\n') {
                    if (ch == '\n' && previous_was_cr_) { previous_was_cr_ = false; continue; }
                    previous_was_cr_ = (ch == '\r');
                    std::memcpy(out_line.value, buffer_, length_);
                    out_line.value[length_] = '\0';
                    out_line.length = length_;
                    length_ = 0;
                    return ConsoleReadStatus::Ok;
                }
                previous_was_cr_ = false;
                if (length_ + 1U >= sizeof(buffer_)) { length_ = 0; return ConsoleReadStatus::LineTooLong; }
                buffer_[length_++] = ch;
            }
        }
        }  // namespace secure_lab
    ''')

    write("labs/lab03_mqtt_tls/firmware/components/mqtt_scenario/CMakeLists.txt", 'idf_component_register(SRCS "src/mqtt_scenario.cpp" INCLUDE_DIRS "include" REQUIRES lab03_domain secure_log)\n')
    write("labs/lab03_mqtt_tls/firmware/components/mqtt_scenario/include/mqtt_scenario/mqtt_scenario.hpp", r'''
        #pragma once
        #include "lab03_domain/types.hpp"
        #include "secure_log/json_log.hpp"
        #include <cstddef>
        #include <string_view>
        namespace secure_lab {
        class MqttScenarioService {
        public:
            const MqttScenario& selected() const noexcept;
            bool select(std::string_view id) noexcept;
            void logList(const JsonLog& log) const;
            void logStatus(const JsonLog& log) const;
            void logConnectDryRun(const JsonLog& log) const;
            void logPublishDryRun(const JsonLog& log) const;
        private:
            std::size_t selected_index_{0};
        };
        }  // namespace secure_lab
    ''')
    write("labs/lab03_mqtt_tls/firmware/components/mqtt_scenario/src/mqtt_scenario.cpp", r'''
        #include "mqtt_scenario/mqtt_scenario.hpp"
        #include <array>
        namespace secure_lab {
        namespace {
        constexpr std::array<MqttScenario, 11> kScenarios{{
            {"M03-1883", "test.mosquitto.org", 1883, TransportKind::MqttTcp, false, false, false, false, "NO_CUMPLE_EXPECTED", "plain_unauthenticated_baseline"},
            {"M03-1884", "test.mosquitto.org", 1884, TransportKind::MqttTcp, false, true, false, false, "NO_CUMPLE_EXPECTED", "plain_authenticated_credentials_exposed"},
            {"M03-8883", "test.mosquitto.org", 8883, TransportKind::MqttTcp, true, false, false, false, "PENDIENTE_TLS", "mosquitto_ca_required"},
            {"M03-8884", "test.mosquitto.org", 8884, TransportKind::MqttTcp, true, false, true, false, "PENDIENTE_MTLS", "client_certificate_required"},
            {"M03-8885", "test.mosquitto.org", 8885, TransportKind::MqttTcp, true, true, false, false, "PENDIENTE_TLS_AUTH", "tls_with_username_password"},
            {"M03-8886", "test.mosquitto.org", 8886, TransportKind::MqttTcp, true, false, false, false, "PENDIENTE_TLS", "public_ca_chain"},
            {"M03-8887", "test.mosquitto.org", 8887, TransportKind::MqttTcp, true, false, false, true, "RECHAZO_ESPERADO", "server_certificate_expired"},
            {"M03-8080", "test.mosquitto.org", 8080, TransportKind::MqttWebSocket, false, false, false, false, "NO_CUMPLE_EXPECTED", "websocket_plain_unauthenticated"},
            {"M03-8081", "test.mosquitto.org", 8081, TransportKind::MqttWebSocket, true, false, false, false, "PENDIENTE_WSS", "websocket_tls_unauthenticated"},
            {"M03-8090", "test.mosquitto.org", 8090, TransportKind::MqttWebSocket, false, true, false, false, "NO_CUMPLE_EXPECTED", "websocket_plain_authenticated"},
            {"M03-8091", "test.mosquitto.org", 8091, TransportKind::MqttWebSocket, true, true, false, false, "PENDIENTE_WSS_AUTH", "websocket_tls_authenticated"},
        }};
        std::string_view boolText(bool value) noexcept { return value ? "true" : "false"; }
        std::string_view portText(std::uint16_t port) noexcept {
            switch (port) {
                case 1883: return "1883"; case 1884: return "1884"; case 8883: return "8883";
                case 8884: return "8884"; case 8885: return "8885"; case 8886: return "8886";
                case 8887: return "8887"; case 8080: return "8080"; case 8081: return "8081";
                case 8090: return "8090"; case 8091: return "8091"; default: return "unknown";
            }
        }
        }
        const MqttScenario& MqttScenarioService::selected() const noexcept { return kScenarios[selected_index_]; }
        bool MqttScenarioService::select(std::string_view id) noexcept {
            for (std::size_t i = 0; i < kScenarios.size(); ++i) { if (kScenarios[i].id == id) { selected_index_ = i; return true; } }
            return false;
        }
        void MqttScenarioService::logList(const JsonLog& log) const { log.event("scenario_list", {{"count", "11"}, {"ids", "M03-1883,M03-1884,M03-8883,M03-8884,M03-8885,M03-8886,M03-8887,M03-8080,M03-8081,M03-8090,M03-8091"}}); }
        void MqttScenarioService::logStatus(const JsonLog& log) const {
            const auto& s = selected();
            log.event("scenario_status", {{"scenario_id", s.id}, {"host", s.host}, {"port", portText(s.port)}, {"transport", toString(s.transport)}, {"tls_enabled", boolText(s.tls_enabled)}, {"auth_username_password", boolText(s.uses_username_password)}, {"client_certificate_required", boolText(s.requires_client_certificate)}, {"certificate_expired", boolText(s.certificate_expired)}, {"security_result", s.security_result}, {"notes", s.notes}});
        }
        void MqttScenarioService::logConnectDryRun(const JsonLog& log) const {
            const auto& s = selected();
            log.event("mqtt_connect_dry_run", {{"scenario_id", s.id}, {"host", s.host}, {"port", portText(s.port)}, {"tls_enabled", boolText(s.tls_enabled)}, {"network_action", "not_executed"}, {"broker", "test.mosquitto.org"}, {"security_result", s.security_result}});
        }
        void MqttScenarioService::logPublishDryRun(const JsonLog& log) const {
            const auto& s = selected();
            log.event("mqtt_publish_dry_run", {{"scenario_id", s.id}, {"topic", "secure-embedded-labs/lab03/dry-run"}, {"payload", "LAB03_DRY_RUN_PAYLOAD"}, {"network_action", "not_executed"}, {"security_result", s.security_result}});
        }
        }  // namespace secure_lab
    ''')

    write("labs/lab03_mqtt_tls/firmware/components/command_console/CMakeLists.txt", 'idf_component_register(SRCS "src/command_console.cpp" INCLUDE_DIRS "include" REQUIRES board_hal mqtt_scenario secure_log lab03_domain)\n')
    write("labs/lab03_mqtt_tls/firmware/components/command_console/include/command_console/command_console.hpp", r'''
        #pragma once
        #include "board_hal/stdio_console.hpp"
        #include "mqtt_scenario/mqtt_scenario.hpp"
        #include "secure_log/json_log.hpp"
        namespace secure_lab {
        class CommandConsole {
        public:
            CommandConsole(StdioConsole& console, MqttScenarioService& scenarios, const JsonLog& log) noexcept;
            void runForever() noexcept;
        private:
            void handleLine(const ConsoleLine& line) noexcept;
            StdioConsole& console_;
            MqttScenarioService& scenarios_;
            const JsonLog& log_;
        };
        }  // namespace secure_lab
    ''')
    write("labs/lab03_mqtt_tls/firmware/components/command_console/src/command_console.cpp", r'''
        #include "command_console/command_console.hpp"
        #include "lab03_domain/types.hpp"
        #include <string_view>
        namespace secure_lab {
        namespace {
        bool startsWith(std::string_view text, std::string_view prefix) noexcept { return text.substr(0, prefix.size()) == prefix; }
        std::string_view argumentAfter(std::string_view text, std::string_view command) noexcept { return text.size() <= command.size() ? std::string_view{} : text.substr(command.size() + 1U); }
        }
        CommandConsole::CommandConsole(StdioConsole& console, MqttScenarioService& scenarios, const JsonLog& log) noexcept : console_(console), scenarios_(scenarios), log_(log) {}
        void CommandConsole::runForever() noexcept {
            ConsoleLine line{};
            while (true) {
                const auto status = console_.readLine(line);
                if (status == ConsoleReadStatus::NoData) { continue; }
                if (status == ConsoleReadStatus::LineTooLong) { log_.event("command_rejected", {{"reason", "line_too_long"}}); continue; }
                handleLine(line);
            }
        }
        void CommandConsole::handleLine(const ConsoleLine& line) noexcept {
            const std::string_view raw(line.value, line.length);
            if (raw.empty()) { return; }
            log_.event("command_received", {{"raw", raw}});
            if (raw == "help") { log_.event("help", {{"commands", "help,scenario_list,select_scenario <id>,scenario_status,mqtt_connect_dry_run,mqtt_publish_dry_run,security_status"}}); return; }
            if (raw == "scenario_list") { scenarios_.logList(log_); return; }
            if (startsWith(raw, "select_scenario ")) {
                const auto id = argumentAfter(raw, "select_scenario");
                if (scenarios_.select(id)) { log_.event("scenario_selected", {{"scenario_id", id}}); }
                else { log_.event("command_rejected", {{"cmd", "select_scenario"}, {"reason", "unknown_scenario"}}); }
                return;
            }
            if (raw == "scenario_status") { scenarios_.logStatus(log_); return; }
            if (raw == "mqtt_connect_dry_run") { scenarios_.logConnectDryRun(log_); return; }
            if (raw == "mqtt_publish_dry_run") { scenarios_.logPublishDryRun(log_); return; }
            if (raw == "security_status") { log_.event("security_status", {{"project", kProjectName}, {"fw_version", kFirmwareVersion}, {"lab", kLabId}, {"target", kTarget}, {"console_transport", kConsoleTransport}, {"mqtt_real_network", "false"}, {"tls_real_validation", "false"}, {"phase", "LAB03A_MATRIX_DRY_RUN"}}); return; }
            log_.event("command_rejected", {{"cmd", raw}, {"reason", "unknown_command"}});
        }
        }  // namespace secure_lab
    ''')

    write("labs/lab03_mqtt_tls/firmware/components/app_core/CMakeLists.txt", 'idf_component_register(SRCS "src/app_core.cpp" INCLUDE_DIRS "include" REQUIRES board_hal command_console mqtt_scenario secure_log lab03_domain)\n')
    write("labs/lab03_mqtt_tls/firmware/components/app_core/include/app_core/app_core.hpp", 'namespace secure_lab { void runLab03App(); }\n')
    write("labs/lab03_mqtt_tls/firmware/components/app_core/src/app_core.cpp", r'''
        #include "app_core/app_core.hpp"
        #include "board_hal/stdio_console.hpp"
        #include "command_console/command_console.hpp"
        #include "lab03_domain/types.hpp"
        #include "mqtt_scenario/mqtt_scenario.hpp"
        #include "secure_log/json_log.hpp"
        namespace secure_lab {
        void runLab03App() {
            JsonLog log{};
            log.event("boot", {{"project", kProjectName}, {"fw_version", kFirmwareVersion}, {"lab", kLabId}, {"target", kTarget}, {"console_transport", kConsoleTransport}, {"phase", "LAB03A_MATRIX_DRY_RUN"}});
            log.event("console_start", {{"transport", kConsoleTransport}, {"line_policy", "max_length_enforced"}});
            StdioConsole console{};
            MqttScenarioService scenarios{};
            CommandConsole command_console(console, scenarios, log);
            command_console.runForever();
        }
        }  // namespace secure_lab
    ''')


def generate_tools() -> None:
    write("labs/lab03_mqtt_tls/tools/run_static_gates.py", r'''
        #!/usr/bin/env python3
        from __future__ import annotations
        from pathlib import Path
        import sys
        ROOT = Path(__file__).resolve().parents[1]
        REQUIRED_FILES = ["README.md", "CHANGELOG.md", "COMMIT_MESSAGE.txt", "docs/scenario_matrix.md", "docs/threat_model.md", "docs/test_plan.md", "docs/audit_evidence.md", "docs/certificate_policy.md", "docs/risk_register.md", "docs/references.md", "evidence/README.md", "test/manual_lab03_commands.txt", "tools/capture_console_evidence.py", "tools/check_mqtt_scenario_logs.py", "tools/capture_static_gates.py", "firmware/CMakeLists.txt", "firmware/sdkconfig.defaults"]
        REQUIRED_README_SECTIONS = ["## Índice", "## Objetivo", "## Objetivos de aprendizaje", "## Matriz contractual", "## Cómo compilar", "## Evidencias esperadas", "## Estado"]
        def fail(message: str) -> int:
            print(f"FAIL: {message}")
            return 1
        def main() -> int:
            if (ROOT / "firmware/build").exists():
                return fail("forbidden generated directory present: firmware/build")
            for filename in REQUIRED_FILES:
                if not (ROOT / filename).exists():
                    return fail(f"missing required file: {filename}")
            readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
            for section in REQUIRED_README_SECTIONS:
                if section not in readme:
                    return fail(f"README.md missing section: {section}")
            matrix = (ROOT / "docs/scenario_matrix.md").read_text(encoding="utf-8", errors="replace")
            for scenario in ["M03-1883", "M03-1884", "M03-8883", "M03-8884", "M03-8885", "M03-8886", "M03-8887", "M03-8080", "M03-8081", "M03-8090", "M03-8091"]:
                if scenario not in matrix:
                    return fail(f"scenario matrix missing {scenario}")
            print("PASS: LAB 03 static gates completed successfully")
            return 0
        if __name__ == "__main__":
            sys.exit(main())
    ''')

    write("labs/lab03_mqtt_tls/tools/capture_console_evidence.py", r'''
        #!/usr/bin/env python3
        from __future__ import annotations
        import argparse
        import sys
        import time
        from pathlib import Path
        import serial
        COMMANDS = ["help", "scenario_list", "select_scenario {scenario}", "scenario_status", "mqtt_connect_dry_run", "mqtt_publish_dry_run", "security_status"]
        def read_available(ser: serial.Serial, duration_s: float) -> list[str]:
            deadline = time.monotonic() + duration_s
            lines: list[str] = []
            while time.monotonic() < deadline:
                raw = ser.readline()
                if not raw:
                    continue
                line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                if line:
                    lines.append(line)
            return lines
        def capture(port: str, baudrate: int, scenario: str, output: Path) -> int:
            output.parent.mkdir(parents=True, exist_ok=True)
            captured: list[str] = [f"# capture_start lab=LAB03 scenario={scenario} port={port} baudrate={baudrate}"]
            with serial.Serial(port=port, baudrate=baudrate, timeout=0.1) as ser:
                ser.dtr = False
                ser.rts = False
                time.sleep(0.5)
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                captured.extend(read_available(ser, 1.5))
                for template in COMMANDS:
                    command = template.format(scenario=scenario)
                    captured.append(f"# tx {command}")
                    ser.write((command + "\n").encode("utf-8"))
                    ser.flush()
                    captured.extend(read_available(ser, 1.0))
            text = "\n".join(captured) + "\n"
            ok = scenario in text and "mqtt_connect_dry_run" in text and "security_status" in text
            text += f"# capture_validation result={'PASS' if ok else 'FAIL'}\n"
            output.write_text(text, encoding="utf-8", newline="\n")
            print(f"{'PASS' if ok else 'FAIL'}: LAB 03 console evidence written to {output}")
            return 0 if ok else 1
        def main() -> int:
            parser = argparse.ArgumentParser()
            parser.add_argument("--port", required=True)
            parser.add_argument("--baudrate", type=int, default=115200)
            parser.add_argument("--scenario", required=True)
            parser.add_argument("--output", required=True, type=Path)
            args = parser.parse_args()
            return capture(args.port, args.baudrate, args.scenario, args.output)
        if __name__ == "__main__":
            sys.exit(main())
    ''')

    write("labs/lab03_mqtt_tls/tools/check_mqtt_scenario_logs.py", r'''
        #!/usr/bin/env python3
        from __future__ import annotations
        import argparse
        import json
        import sys
        from pathlib import Path
        def fail(message: str) -> int:
            print(f"FAIL: {message}")
            return 1
        def main() -> int:
            parser = argparse.ArgumentParser()
            parser.add_argument("log_file", type=Path)
            parser.add_argument("--scenario", required=True)
            args = parser.parse_args()
            if not args.log_file.exists():
                return fail(f"log file does not exist: {args.log_file}")
            saw_scenario = saw_connect = saw_publish = saw_validation = saw_no_cumple = False
            for line in args.log_file.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.strip() == "# capture_validation result=PASS":
                    saw_validation = True
                if not line.startswith("{"):
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("scenario_id") == args.scenario:
                    saw_scenario = True
                if obj.get("event") == "mqtt_connect_dry_run":
                    saw_connect = True
                    if obj.get("security_result") == "NO_CUMPLE_EXPECTED":
                        saw_no_cumple = True
                if obj.get("event") == "mqtt_publish_dry_run":
                    saw_publish = True
            if not saw_validation: return fail("capture validation PASS not found")
            if not saw_scenario: return fail(f"scenario {args.scenario} not found")
            if not saw_connect: return fail("mqtt_connect_dry_run not found")
            if not saw_publish: return fail("mqtt_publish_dry_run not found")
            if args.scenario == "M03-1883" and not saw_no_cumple: return fail("M03-1883 did not report NO_CUMPLE_EXPECTED")
            print(f"PASS: LAB 03 scenario log checks for {args.scenario}")
            return 0
        if __name__ == "__main__":
            sys.exit(main())
    ''')

    write("labs/lab03_mqtt_tls/tools/capture_static_gates.py", r'''
        #!/usr/bin/env python3
        from __future__ import annotations
        import subprocess
        import sys
        from pathlib import Path
        ROOT = Path(__file__).resolve().parents[3]
        OUT = ROOT / "labs" / "lab03_mqtt_tls" / "evidence" / "lab03_static_gates.txt"
        def run(command: list[str]) -> tuple[int, str, str]:
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            return result.returncode, result.stdout, result.stderr
        def main() -> int:
            OUT.parent.mkdir(parents=True, exist_ok=True)
            sections = ["# LAB 03 static gates evidence", ""]
            commands = [[sys.executable, "tools/repo_quality_gates/run_static_repo_gates.py"], [sys.executable, "labs/lab03_mqtt_tls/tools/run_static_gates.py"]]
            ok = True
            for command in commands:
                rc, stdout, stderr = run(command)
                ok = ok and rc == 0
                sections += ["## command", " ".join(command), f"returncode: {rc}", "stdout:", stdout.strip() or "<empty>", "stderr:", stderr.strip() or "<empty>", ""]
            sections.append(f"# capture_validation result={'PASS' if ok else 'FAIL'}")
            OUT.write_text("\n".join(sections) + "\n", encoding="utf-8", newline="\n")
            print(f"{'PASS' if ok else 'FAIL'}: static gates evidence written to {OUT}")
            return 0 if ok else 1
        if __name__ == "__main__":
            sys.exit(main())
    ''')


def update_global_docs() -> None:
    update_if_present(ROOT / "README.md", [("| LAB 03 | MQTT seguro con TLS | PENDIENTE |", "| LAB 03 | Matriz MQTT test.mosquitto.org | EN CURSO |"), ("LAB 03+ permanecen como laboratorios pendientes.", "LAB 03 está en curso con matriz Mosquitto y baseline 1883 sin TLS; LAB 04+ permanecen pendientes.")])
    update_if_present(ROOT / "ROADMAP.md", [("- [ ] LAB 03 — MQTT seguro con TLS.", "- [ ] LAB 03 — Matriz MQTT test.mosquitto.org: 03A baseline 1883 sin TLS en curso.")])


def main() -> int:
    generate_docs()
    generate_firmware()
    generate_tools()
    update_global_docs()
    for directory in ["labs/lab03_mqtt_tls/docs", "labs/lab03_mqtt_tls/evidence", "labs/lab03_mqtt_tls/test", "labs/lab03_mqtt_tls/tools"]:
        remove_gitkeep(directory)
    print("PASS: LAB 03 Mosquitto matrix generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

## Objetivos de aprendizaje

- Entender la diferencia entre MQTT plano, MQTT autenticado, MQTT sobre TLS y MQTT sobre WebSockets.
- Evidenciar por qué MQTT sin TLS no debe considerarse seguro aunque permita conexión funcional.
- Comparar los escenarios publicados por `test.mosquitto.org` en puertos 1883, 1884, 8883, 8884, 8885, 8886, 8887, 8080, 8081, 8090 y 8091.
- Aprender a clasificar cada escenario como `CUMPLE`, `NO CUMPLE`, `NO VALIDADO` o `PENDIENTE` según transporte, autenticación y validación de certificados.
- Generar evidencias reproducibles mediante consola, logs NDJSON y gates estáticos.
