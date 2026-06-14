#pragma once

#include "lab02_domain/interfaces.hpp"

#include <cstddef>
#include <string>

namespace secure_lab {

class StdioConsoleInput final : public IConsoleInput {
public:
    explicit StdioConsoleInput(std::size_t max_line_length) noexcept;

    ConsoleReadStatus readLine(std::string& line) override;

private:
    std::size_t max_line_length_;
    std::string pending_line_;
    bool overflow_active_ = false;
    bool swallow_next_lf_ = false;

    ConsoleReadStatus completeLine(std::string& line) noexcept;
    static bool isLineTerminator(int character) noexcept;
};

}  // namespace secure_lab
