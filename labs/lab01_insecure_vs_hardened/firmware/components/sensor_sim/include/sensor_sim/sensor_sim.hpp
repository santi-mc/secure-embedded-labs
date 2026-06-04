#pragma once

#include <cstdint>
#include <string>

namespace secure_lab {

struct SensorSample final {
    std::int32_t temperature_c_x100;
    std::int32_t humidity_rh_x100;
};

class SensorSimulator final {
public:
    SensorSimulator() noexcept;

    SensorSample read() noexcept;

    static std::string fixed2(std::int32_t value_x100);

private:
    std::uint32_t counter_;
};

}  // namespace secure_lab
