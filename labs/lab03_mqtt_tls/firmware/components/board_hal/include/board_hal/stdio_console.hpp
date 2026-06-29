#pragma once
#include "lab03_domain/types.hpp"
namespace secure_lab {
class StdioConsole {
public:
    ConsoleReadStatus readLine(ConsoleLine& out_line) noexcept;
private:
    char buffer_[sizeof(ConsoleLine::value)]{};
    std::size_t length_{0};
    bool previous_was_cr_{false};
};
}  // namespace secure_lab
