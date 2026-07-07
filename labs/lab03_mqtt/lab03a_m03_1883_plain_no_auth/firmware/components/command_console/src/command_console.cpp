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
