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
