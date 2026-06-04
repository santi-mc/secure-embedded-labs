#include "sensor_sim/sensor_sim.hpp"

#include <cstdlib>

namespace secure_lab {

SensorSimulator::SensorSimulator() noexcept : counter_(0U) {}

SensorSample SensorSimulator::read() noexcept
{
    ++counter_;
    const std::int32_t temp_delta = static_cast<std::int32_t>(counter_ % 25U);
    const std::int32_t hum_delta = static_cast<std::int32_t>((counter_ * 3U) % 40U);
    return SensorSample{2300 + temp_delta, 5000 + hum_delta};
}

std::string SensorSimulator::fixed2(const std::int32_t value_x100)
{
    const std::int32_t integer = value_x100 / 100;
    const std::int32_t fraction = std::abs(value_x100 % 100);
    std::string out = std::to_string(integer);
    out += ".";
    if (fraction < 10) {
        out += "0";
    }
    out += std::to_string(fraction);
    return out;
}

}  // namespace secure_lab
