#include "app_config/app_config.hpp"

namespace secure_lab {

AppConfigService::AppConfigService()
    : config_{"LAB01-UNPROVISIONED",
              kSamplePeriodDefaultS,
              "mqtt.example.invalid",
              kMqttPortDefault,
              "lab_user",
              kLabDefaultPassword}
{
}

const AppConfigData& AppConfigService::current() const noexcept
{
    return config_;
}

ConfigUpdateStatus AppConfigService::setSamplePeriod(const std::uint32_t seconds,
                                                     const SecurityProfile profile) noexcept
{
    if (profile == SecurityProfile::Insecure) {
        // Intentional LAB 01 vulnerability V-002: insecure profile accepts any value.
        config_.sample_period_s = seconds;
        return ConfigUpdateStatus::Accepted;
    }

    if ((seconds < kSamplePeriodMinS) || (seconds > kSamplePeriodMaxS)) {
        return ConfigUpdateStatus::RejectedOutOfRange;
    }

    config_.sample_period_s = seconds;
    return ConfigUpdateStatus::Accepted;
}

void AppConfigService::setMqttPassword(const std::string& password)
{
    config_.mqtt_password = password;
}

ConfigUpdateStatus AppConfigService::factoryReset(const SecurityProfile profile)
{
    if (profile != SecurityProfile::Insecure) {
        return ConfigUpdateStatus::RejectedByPolicy;
    }

    config_ = AppConfigData{"LAB01-UNPROVISIONED",
                            kSamplePeriodDefaultS,
                            "mqtt.example.invalid",
                            kMqttPortDefault,
                            "lab_user",
                            kLabDefaultPassword};
    return ConfigUpdateStatus::Accepted;
}

void AppConfigService::logConfig(const JsonLog& log, const SecurityProfile profile) const
{
    const char* password_view = (profile == SecurityProfile::Insecure)
                                    ? config_.mqtt_password.c_str()
                                    : kRedactedSecret;

    log.event("config_dump",
              {{"profile", toString(profile)},
               {"device_id", config_.device_id},
               {"sample_period_s", std::to_string(config_.sample_period_s)},
               {"mqtt_host", config_.mqtt_host},
               {"mqtt_port", std::to_string(config_.mqtt_port)},
               {"mqtt_username", config_.mqtt_username},
               {"mqtt_password", password_view}});
}

const char* toString(const ConfigUpdateStatus status) noexcept
{
    switch (status) {
    case ConfigUpdateStatus::Accepted:
        return "accepted";
    case ConfigUpdateStatus::RejectedOutOfRange:
        return "out_of_range";
    case ConfigUpdateStatus::RejectedByPolicy:
        return "rejected_by_policy";
    default:
        return "unknown";
    }
}

}  // namespace secure_lab
