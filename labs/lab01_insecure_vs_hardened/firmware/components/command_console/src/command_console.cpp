#include "command_console/command_console.hpp"

#include "lab01_domain/config_contract.hpp"

#include <cctype>
#include <cstdlib>
#include <limits>
#include <sstream>

namespace secure_lab {

namespace {

inline constexpr std::size_t kMaxTokens = 3U;

bool isAsciiDigit(const char c) noexcept
{
    return std::isdigit(static_cast<unsigned char>(c)) != 0;
}

}  // namespace

CommandConsole::CommandConsole(IConsoleInput& console,
                               JsonLog& log,
                               AppConfigService& config,
                               SensorSimulator& sensor,
                               SecurityStatusService& security_status,
                               const SecurityProfile profile) noexcept
    : console_(console),
      log_(log),
      config_(config),
      sensor_(sensor),
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
        const ConsoleReadStatus status = console_.readLine(line);
        switch (status) {
        case ConsoleReadStatus::Ok:
            dispatch(line);
            break;
        case ConsoleReadStatus::LineTooLong:
            log_.event("command_rejected",
                       {{"profile", toString(profile_)},
                        {"cmd", "<unknown>"},
                        {"reason", "line_too_long"}});
            break;
        case ConsoleReadStatus::EndOfFile:
            log_.event("console_warning",
                       {{"profile", toString(profile_)},
                        {"reason", "stdin_eof"}});
            break;
        default:
            log_.event("console_warning",
                       {{"profile", toString(profile_)},
                        {"reason", "unknown_console_status"}});
            break;
        }
    }
}

std::vector<std::string> CommandConsole::tokenize(const std::string& line)
{
    std::vector<std::string> tokens;
    tokens.reserve(kMaxTokens);

    std::istringstream stream(line);
    std::string token;
    while (stream >> token) {
        tokens.push_back(token);
        if (tokens.size() > kMaxTokens) {
            break;
        }
    }

    return tokens;
}

bool CommandConsole::isSensitiveCommand(const std::string& command) noexcept
{
    return command == "set_mqtt_password";
}

void CommandConsole::logCommandReceived(const std::string& line,
                                        const std::vector<std::string>& tokens) const
{
    const std::string command = tokens.empty() ? "<empty>" : tokens.front();

    if (profile_ == SecurityProfile::Insecure) {
        // Intentional LAB 01 vulnerability V-004: raw UART/console payload is logged.
        log_.event("command_received",
                   {{"profile", toString(profile_)},
                    {"raw", line}});
        return;
    }

    if (isSensitiveCommand(command)) {
        log_.event("command_received",
                   {{"profile", toString(profile_)},
                    {"cmd", command},
                    {"args", kRedactedSecret}});
        return;
    }

    log_.event("command_received",
               {{"profile", toString(profile_)},
                {"cmd", command}});
}

void CommandConsole::dispatch(const std::string& line)
{
    const std::vector<std::string> tokens = tokenize(line);
    logCommandReceived(line, tokens);

    if (tokens.empty()) {
        rejectCommand("<empty>", "empty_command");
        return;
    }

    if (tokens.size() > kMaxTokens) {
        rejectCommand(tokens.front().c_str(), "too_many_arguments");
        return;
    }

    const std::string& command = tokens.front();
    if (command == "help") {
        handleHelp();
    } else if ((command == "status") || (command == "security_status")) {
        handleStatus();
    } else if (command == "sample") {
        handleSample();
    } else if (command == "get_config") {
        handleGetConfig();
    } else if (command == "set_period") {
        handleSetPeriod(tokens);
    } else if (command == "set_mqtt_password") {
        handleSetMqttPassword(tokens);
    } else if (command == "factory_reset") {
        handleFactoryReset();
    } else {
        rejectCommand(command.c_str(), "unknown_command");
    }
}

void CommandConsole::handleHelp() const
{
    log_.event("help",
               {{"profile", toString(profile_)},
                {"commands", "help,status,security_status,sample,get_config,set_period <s>,set_mqtt_password <value>,factory_reset"}});
}

void CommandConsole::handleStatus() const
{
    security_status_.logStatus(log_, profile_);
}

void CommandConsole::handleSample()
{
    const SensorSample sample = sensor_.read();
    log_.event("sensor_sample",
               {{"profile", toString(profile_)},
                {"temperature_c", SensorSimulator::fixed2(sample.temperature_c_x100)},
                {"humidity_rh", SensorSimulator::fixed2(sample.humidity_rh_x100)}});
}

void CommandConsole::handleGetConfig() const
{
    config_.logConfig(log_, profile_);
}

bool CommandConsole::parseStrictUint32(const std::string& text, std::uint32_t& value) noexcept
{
    if (text.empty()) {
        return false;
    }

    std::uint32_t accumulator = 0U;
    for (const char c : text) {
        if (!isAsciiDigit(c)) {
            return false;
        }

        const std::uint32_t digit = static_cast<std::uint32_t>(c - '0');
        if (accumulator > ((std::numeric_limits<std::uint32_t>::max() - digit) / 10U)) {
            return false;
        }
        accumulator = (accumulator * 10U) + digit;
    }

    value = accumulator;
    return true;
}

std::uint32_t CommandConsole::parseInsecureUint32(const std::string& text) noexcept
{
    // Intentional LAB 01 vulnerability V-002/V-003: weak parser accepts partial or signed input.
    return static_cast<std::uint32_t>(std::strtoul(text.c_str(), nullptr, 10));
}

void CommandConsole::handleSetPeriod(const std::vector<std::string>& tokens)
{
    if (tokens.size() != 2U) {
        rejectCommand("set_period", "invalid_argument_count");
        return;
    }

    std::uint32_t seconds = 0U;
    if (profile_ == SecurityProfile::Insecure) {
        seconds = parseInsecureUint32(tokens[1]);
    } else if (!parseStrictUint32(tokens[1], seconds)) {
        log_.event("config_update_rejected",
                   {{"profile", toString(profile_)},
                    {"field", "sample_period_s"},
                    {"reason", "invalid_uint32"}});
        return;
    } else {
        // Strict parser succeeded. Range validation is delegated to AppConfigService.
    }

    const ConfigUpdateStatus status = config_.setSamplePeriod(seconds, profile_);
    if (status == ConfigUpdateStatus::Accepted) {
        log_.event("config_update_accepted",
                   {{"profile", toString(profile_)},
                    {"field", "sample_period_s"},
                    {"value", std::to_string(seconds)}});
        return;
    }

    log_.event("config_update_rejected",
               {{"profile", toString(profile_)},
                {"field", "sample_period_s"},
                {"value", std::to_string(seconds)},
                {"reason", toString(status)}});
}

void CommandConsole::handleSetMqttPassword(const std::vector<std::string>& tokens)
{
    if (tokens.size() != 2U) {
        rejectCommand("set_mqtt_password", "invalid_argument_count");
        return;
    }

    config_.setMqttPassword(tokens[1]);
    if (profile_ == SecurityProfile::Insecure) {
        // Intentional LAB 01 vulnerability V-005: insecure profile logs secret value.
        log_.event("secret_updated",
                   {{"profile", toString(profile_)},
                    {"field", "mqtt_password"},
                    {"value", tokens[1]}});
        return;
    }

    log_.event("secret_updated",
               {{"profile", toString(profile_)},
                {"field", "mqtt_password"},
                {"value", kRedactedSecret}});
}

void CommandConsole::handleFactoryReset()
{
    const ConfigUpdateStatus status = config_.factoryReset(profile_);
    if (status == ConfigUpdateStatus::Accepted) {
        log_.event("factory_reset",
                   {{"profile", toString(profile_)},
                    {"status", "accepted"}});
        return;
    }

    log_.event("command_rejected",
               {{"profile", toString(profile_)},
                {"cmd", "factory_reset"},
                {"reason", toString(status)}});
}

void CommandConsole::rejectCommand(const char* const command, const char* const reason) const
{
    log_.event("command_rejected",
               {{"profile", toString(profile_)},
                {"cmd", command},
                {"reason", reason}});
}

}  // namespace secure_lab
