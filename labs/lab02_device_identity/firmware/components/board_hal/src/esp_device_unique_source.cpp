#include "board_hal/esp_device_unique_source.hpp"

#include "esp_mac.h"

namespace secure_lab {

HardwareUniqueId EspDeviceUniqueSource::readHardwareUniqueId() const noexcept
{
    HardwareUniqueId mac{};
    const esp_err_t err = esp_efuse_mac_get_default(mac.data());
    if (err != ESP_OK) {
        mac.fill(0U);
    }
    return mac;
}

}  // namespace secure_lab
