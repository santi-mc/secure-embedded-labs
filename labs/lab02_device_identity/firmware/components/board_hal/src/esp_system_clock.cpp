#include "board_hal/esp_system_clock.hpp"

#include "esp_timer.h"

namespace secure_lab {

std::uint64_t EspSystemClock::uptimeMs() const noexcept
{
    return static_cast<std::uint64_t>(esp_timer_get_time() / 1000LL);
}

}  // namespace secure_lab
