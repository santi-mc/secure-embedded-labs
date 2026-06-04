#pragma once

#include "lab01_domain/interfaces.hpp"

#include <cstddef>

namespace secure_lab {

class StdioConsoleInput final : public IConsoleInput {
public:
    explicit StdioConsoleInput(std::size_t max_line_length) noexcept;

    ConsoleReadStatus readLine(std::string& line) override;

private:
    std::size_t max_line_length_;

    static void drainUntilLineEnd() noexcept;
};

}  // namespace secure_lab
