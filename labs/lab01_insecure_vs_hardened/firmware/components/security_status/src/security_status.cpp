#include "security_status/security_status.hpp"

#include "lab01_domain/version.hpp"

#include "esp_efuse.h"
#include "esp_secure_boot.h"

namespace secure_lab {

void SecurityStatusService::logStatus(const JsonLog& log, const SecurityProfile profile) const
{
    log.event("security_status",
              {{"project", kProjectName},
               {"fw_version", kFirmwareVersion},
               {"lab", kLabId},
               {"profile", toString(profile)},
               {"target", "esp32s3"},
               {"console_transport", "usb_serial_jtag_stdio"},
               {"secure_boot", esp_secure_boot_enabled() ? "true" : "false"},
               {"flash_encryption", esp_efuse_is_flash_encryption_enabled() ? "true" : "false"}});
}

}  // namespace secure_lab
