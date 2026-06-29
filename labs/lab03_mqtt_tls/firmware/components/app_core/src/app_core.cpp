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
