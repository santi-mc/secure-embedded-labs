#pragma once

#include <cstdint>
#include <string>

namespace secure_lab {

class IClock {
public:
    virtual ~IClock() = default;
    virtual std::uint64_t uptimeMs() const noexcept = 0;
};

enum class ConsoleReadStatus : std::uint8_t {
    Ok = 0,
    EndOfFile,
    LineTooLong,
};

class IConsoleInput {
public:
    virtual ~IConsoleInput() = default;
    virtual ConsoleReadStatus readLine(std::string& line) = 0;
};

}  // namespace secure_lab
