#pragma once

#include "lab01_domain/security_profile.hpp"
#include "secure_log/json_log.hpp"

namespace secure_lab {

class SecurityStatusService final {
public:
    void logStatus(const JsonLog& log, SecurityProfile profile) const;
};

}  // namespace secure_lab
