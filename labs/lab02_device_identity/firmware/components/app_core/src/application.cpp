#include "app_core/application.hpp"

#include "lab02_domain/version.hpp"
#include "sdkconfig.h"

namespace secure_lab {

SecurityProfile Application::activeProfile() noexcept
{
#if CONFIG_LAB02_PROFILE_HARDENED
    return SecurityProfile::Hardened;
#else
    return SecurityProfile::Insecure;
#endif
}

Application::Application()
    : clock_(),
      log_(clock_),
      console_(CONFIG_LAB02_CONSOLE_LINE_MAX),
      unique_source_(),
      identity_(unique_source_),
      security_status_(),
      command_console_(console_, log_, identity_, security_status_, activeProfile())
{
}

[[noreturn]] void Application::run()
{
    log_.event("boot",
               {{"project", kProjectName},
                {"fw_version", kFirmwareVersion},
                {"lab", kLabId},
                {"profile", toString(activeProfile())},
                {"target", "esp32s3"},
                {"console_transport", "usb_serial_jtag_stdio"},
                {"build_gate", "not_executed_by_generator"}});

    command_console_.runForever();
}

}  // namespace secure_lab
