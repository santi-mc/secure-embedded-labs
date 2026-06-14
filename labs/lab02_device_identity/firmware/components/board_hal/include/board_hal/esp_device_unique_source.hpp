#pragma once

#include "lab02_domain/interfaces.hpp"

namespace secure_lab {

class EspDeviceUniqueSource final : public IDeviceUniqueSource {
public:
    HardwareUniqueId readHardwareUniqueId() const noexcept override;
};

}  // namespace secure_lab
