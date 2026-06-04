#pragma once

#include "lab01_domain/config_contract.hpp"
#include "lab01_domain/security_profile.hpp"
#include "secure_log/json_log.hpp"

#include <cstdint>
#include <string>

namespace secure_lab {

struct AppConfigData final {
    std::string device_id;
    std::uint32_t sample_period_s;
    std::string mqtt_host;
    std::uint16_t mqtt_port;
    std::string mqtt_username;
    std::string mqtt_password;
};

enum class ConfigUpdateStatus : std::uint8_t {
    Accepted = 0,
    RejectedOutOfRange,
    RejectedByPolicy,
};

class AppConfigService final {
public:
    AppConfigService();

    const AppConfigData& current() const noexcept;

    ConfigUpdateStatus setSamplePeriod(std::uint32_t seconds,
                                       SecurityProfile profile) noexcept;
    void setMqttPassword(const std::string& password);
    ConfigUpdateStatus factoryReset(SecurityProfile profile);

    void logConfig(const JsonLog& log, SecurityProfile profile) const;

private:
    AppConfigData config_;
};

const char* toString(ConfigUpdateStatus status) noexcept;

}  // namespace secure_lab
