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
