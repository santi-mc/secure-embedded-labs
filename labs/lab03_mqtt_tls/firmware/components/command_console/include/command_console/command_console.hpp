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
