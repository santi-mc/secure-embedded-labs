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
