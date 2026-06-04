#pragma once

#include <cstdint>

namespace secure_lab {

inline constexpr std::uint32_t kSamplePeriodMinS = 10U;
inline constexpr std::uint32_t kSamplePeriodMaxS = 3600U;
inline constexpr std::uint32_t kSamplePeriodDefaultS = 60U;
inline constexpr std::uint16_t kMqttPortDefault = 8883U;
inline constexpr const char* kRedactedSecret = "<redacted>";
inline constexpr const char* kLabDefaultPassword = "INSECURE_DEFAULT_PASSWORD";

}  // namespace secure_lab
