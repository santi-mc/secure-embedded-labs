#pragma once

#include <cstdint>

namespace secure_lab {

enum class SecurityProfile : std::uint8_t {
    Insecure = 0,
    Hardened = 1,
};

inline const char* toString(const SecurityProfile profile) noexcept
{
    switch (profile) {
    case SecurityProfile::Insecure:
        return "INSECURE";
    case SecurityProfile::Hardened:
        return "HARDENED";
    default:
        return "UNKNOWN";
    }
}

}  // namespace secure_lab
