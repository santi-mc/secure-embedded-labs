#pragma once

#include "lab02_domain/interfaces.hpp"

namespace secure_lab {

class EspSystemClock final : public IClock {
public:
    std::uint64_t uptimeMs() const noexcept override;
};

}  // namespace secure_lab
