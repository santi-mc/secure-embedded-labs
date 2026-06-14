#pragma once

#include "identity_service/identity_service.hpp"
#include "lab02_domain/interfaces.hpp"
#include "lab02_domain/security_profile.hpp"
#include "secure_log/json_log.hpp"
#include "security_status/security_status.hpp"

#include <string>
#include <vector>

namespace secure_lab {

class CommandConsole final {
public:
    CommandConsole(IConsoleInput& input,
                   const JsonLog& log,
                   IdentityService& identity,
                   const SecurityStatusService& security_status,
                   SecurityProfile profile) noexcept;

    [[noreturn]] void runForever();

private:
    IConsoleInput& input_;
    const JsonLog& log_;
    IdentityService& identity_;
    const SecurityStatusService& security_status_;
    SecurityProfile profile_;

    void processLine(const std::string& line);
    void handleHelp() const;
    void handleSetDeviceId(const std::vector<std::string>& tokens);
    void rejectCommand(const std::string& command, const char* reason) const;
    void logCommandReceived(const std::string& line, const std::vector<std::string>& tokens) const;

    static std::vector<std::string> tokenize(const std::string& line);
};

}  // namespace secure_lab
