#pragma once

#include "app_config/app_config.hpp"
#include "board_hal/esp_system_clock.hpp"
#include "board_hal/stdio_console.hpp"
#include "command_console/command_console.hpp"
#include "lab01_domain/security_profile.hpp"
#include "secure_log/json_log.hpp"
#include "security_status/security_status.hpp"
#include "sensor_sim/sensor_sim.hpp"

namespace secure_lab {

class Application final {
public:
    Application();

    [[noreturn]] void run();

private:
    EspSystemClock clock_;
    JsonLog log_;
    StdioConsoleInput console_;
    AppConfigService config_;
    SensorSimulator sensor_;
    SecurityStatusService security_status_;
    CommandConsole command_console_;

    static SecurityProfile activeProfile() noexcept;
};

}  // namespace secure_lab
