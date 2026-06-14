#pragma once

#include "lab02_domain/interfaces.hpp"
#include "lab02_domain/security_profile.hpp"
#include "secure_log/json_log.hpp"

#include <array>
#include <cstdint>
#include <string>

namespace secure_lab {

struct IdentityView final {
    std::string device_id;
    std::string source;
    std::string raw_hardware_id;
    std::string mutable_by_console;
    std::string claim_contains_secret;
};

enum class IdentityUpdateStatus : std::uint8_t {
    Accepted = 0,
    RejectedByPolicy,
    RejectedInvalidValue,
};

class IdentityService final {
public:
    explicit IdentityService(const IDeviceUniqueSource& unique_source);

    IdentityView current(SecurityProfile profile) const;
    IdentityUpdateStatus setDeviceId(const std::string& device_id,
                                     SecurityProfile profile);

    void logIdentityStatus(const JsonLog& log, SecurityProfile profile) const;
    void logIdentity(const JsonLog& log, SecurityProfile profile) const;
    void logClaim(const JsonLog& log, SecurityProfile profile) const;

    static const char* toString(IdentityUpdateStatus status) noexcept;

private:
    const IDeviceUniqueSource& unique_source_;
    std::string insecure_device_id_;

    IdentityView insecureView() const;
    IdentityView hardenedView() const;

    static std::string toHex(const HardwareUniqueId& id);
    static std::string derivePublicDeviceId(const HardwareUniqueId& id);
    static std::string firstHexBytes(const std::array<std::uint8_t, 32>& digest,
                                     std::size_t bytes);
    static bool isValidInsecureDeviceId(const std::string& device_id) noexcept;
};

}  // namespace secure_lab
