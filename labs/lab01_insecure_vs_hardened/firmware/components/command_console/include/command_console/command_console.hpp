#pragma once

#include "app_config/app_config.hpp"
#include "lab01_domain/interfaces.hpp"
#include "lab01_domain/security_profile.hpp"
#include "secure_log/json_log.hpp"
#include "security_status/security_status.hpp"
#include "sensor_sim/sensor_sim.hpp"

#include <cstdint>
#include <string>
#include <vector>

namespace secure_lab {

class CommandConsole final {
public:
    CommandConsole(IConsoleInput& console,
                   JsonLog& log,
                   AppConfigService& config,
                   SensorSimulator& sensor,
                   SecurityStatusService& security_status,
                   SecurityProfile profile) noexcept;

    [[noreturn]] void runForever();

private:
    IConsoleInput& console_;
    JsonLog& log_;
    AppConfigService& config_;
    SensorSimulator& sensor_;
    SecurityStatusService& security_status_;
    SecurityProfile profile_;

    void dispatch(const std::string& line);
    void logCommandReceived(const std::string& line,
                            const std::vector<std::string>& tokens) const;
    void handleHelp() const;
    void handleStatus() const;
    void handleSample();
    void handleGetConfig() const;
    void handleSetPeriod(const std::vector<std::string>& tokens);
    void handleSetMqttPassword(const std::vector<std::string>& tokens);
    void handleFactoryReset();
    void rejectCommand(const char* command, const char* reason) const;

    static std::vector<std::string> tokenize(const std::string& line);
    static bool isSensitiveCommand(const std::string& command) noexcept;
    static bool parseStrictUint32(const std::string& text, std::uint32_t& value) noexcept;
    static std::uint32_t parseInsecureUint32(const std::string& text) noexcept;
};

}  // namespace secure_lab
