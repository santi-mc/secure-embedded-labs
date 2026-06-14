#pragma once

#include "board_hal/esp_device_unique_source.hpp"
#include "board_hal/esp_system_clock.hpp"
#include "board_hal/stdio_console.hpp"
#include "command_console/command_console.hpp"
#include "identity_service/identity_service.hpp"
#include "lab02_domain/security_profile.hpp"
#include "secure_log/json_log.hpp"
#include "security_status/security_status.hpp"

namespace secure_lab {

class Application final {
public:
    Application();

    [[noreturn]] void run();

private:
    EspSystemClock clock_;
    JsonLog log_;
    StdioConsoleInput console_;
    EspDeviceUniqueSource unique_source_;
    IdentityService identity_;
    SecurityStatusService security_status_;
    CommandConsole command_console_;

    static SecurityProfile activeProfile() noexcept;
};

}  // namespace secure_lab
