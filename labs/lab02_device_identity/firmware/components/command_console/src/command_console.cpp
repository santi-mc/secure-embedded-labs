#include "command_console/command_console.hpp"

#include <utility>

namespace secure_lab {

CommandConsole::CommandConsole(IConsoleInput& input,
                               const JsonLog& log,
                               IdentityService& identity,
                               const SecurityStatusService& security_status,
                               const SecurityProfile profile) noexcept
    : input_(input),
      log_(log),
      identity_(identity),
      security_status_(security_status),
      profile_(profile)
{
}

[[noreturn]] void CommandConsole::runForever()
{
    log_.event("console_start",
               {{"profile", toString(profile_)},
                {"transport", "usb_serial_jtag_stdio"},
                {"line_policy", "max_length_enforced"}});

    std::string line;
    for (;;) {
        const ConsoleReadStatus status = input_.readLine(line);
        switch (status) {
        case ConsoleReadStatus::Ok:
            processLine(line);
            break;
        case ConsoleReadStatus::NoData:
            break;
        case ConsoleReadStatus::LineTooLong:
            log_.event("command_rejected",
                       {{"profile", toString(profile_)},
                        {"cmd", "<line>"},
                        {"reason", "line_too_long"}});
            break;
        case ConsoleReadStatus::EndOfFile:
            log_.event("console_warning",
                       {{"profile", toString(profile_)}, {"reason", "stdin_eof"}});
            break;
        default:
            log_.event("console_warning",
                       {{"profile", toString(profile_)}, {"reason", "unknown_read_status"}});
            break;
        }
    }
}

void CommandConsole::processLine(const std::string& line)
{
    const std::vector<std::string> tokens = tokenize(line);
    logCommandReceived(line, tokens);

    if (tokens.empty()) {
        return;
    }

    const std::string& command = tokens.front();
    if (command == "help") {
        handleHelp();
    } else if (command == "identity_status") {
        identity_.logIdentityStatus(log_, profile_);
    } else if (command == "get_identity") {
        identity_.logIdentity(log_, profile_);
    } else if (command == "get_claim") {
        identity_.logClaim(log_, profile_);
    } else if (command == "set_device_id") {
        handleSetDeviceId(tokens);
    } else if (command == "security_status") {
        security_status_.logStatus(log_, profile_);
    } else {
        rejectCommand(command, "unknown_command");
    }
}

void CommandConsole::handleHelp() const
{
    log_.event("help",
               {{"profile", toString(profile_)},
                {"commands", "help,identity_status,get_identity,get_claim,set_device_id <id>,security_status"}});
}

void CommandConsole::handleSetDeviceId(const std::vector<std::string>& tokens)
{
    if (tokens.size() != 2U) {
        rejectCommand("set_device_id", "invalid_argument_count");
        return;
    }

    const IdentityUpdateStatus status = identity_.setDeviceId(tokens[1U], profile_);
    if (status == IdentityUpdateStatus::Accepted) {
        const IdentityView view = identity_.current(profile_);
        log_.event("identity_update_accepted",
                   {{"profile", toString(profile_)},
                    {"field", "device_id"},
                    {"value", view.device_id}});
        return;
    }

    log_.event("identity_update_rejected",
               {{"profile", toString(profile_)},
                {"field", "device_id"},
                {"reason", IdentityService::toString(status)}});
}

void CommandConsole::rejectCommand(const std::string& command, const char* reason) const
{
    log_.event("command_rejected",
               {{"profile", toString(profile_)}, {"cmd", command}, {"reason", reason}});
}

void CommandConsole::logCommandReceived(const std::string& line,
                                        const std::vector<std::string>& tokens) const
{
    if (profile_ == SecurityProfile::Insecure) {
        log_.event("command_received", {{"profile", toString(profile_)}, {"raw", line}});
        return;
    }

    if (tokens.empty()) {
        log_.event("command_received", {{"profile", toString(profile_)}, {"cmd", ""}});
        return;
    }

    if (tokens.front() == "set_device_id") {
        log_.event("command_received",
                   {{"profile", toString(profile_)},
                    {"cmd", tokens.front()},
                    {"args", "<redacted>"}});
        return;
    }

    log_.event("command_received", {{"profile", toString(profile_)}, {"cmd", tokens.front()}});
}

std::vector<std::string> CommandConsole::tokenize(const std::string& line)
{
    std::vector<std::string> tokens;
    std::string current;

    for (const char c : line) {
        if ((c == ' ') || (c == '\t')) {
            if (!current.empty()) {
                tokens.push_back(std::move(current));
                current.clear();
            }
            continue;
        }
        current.push_back(c);
    }

    if (!current.empty()) {
        tokens.push_back(std::move(current));
    }

    return tokens;
}

}  // namespace secure_lab
