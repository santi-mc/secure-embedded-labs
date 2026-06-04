#include "board_hal/stdio_console.hpp"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include <cstdio>

namespace secure_lab {

namespace {

inline constexpr TickType_t kNoDataBackoffTicks = pdMS_TO_TICKS(50U);

}  // namespace

StdioConsoleInput::StdioConsoleInput(const std::size_t max_line_length) noexcept
    : max_line_length_(max_line_length)
{
    pending_line_.reserve(max_line_length_);
}

bool StdioConsoleInput::isLineTerminator(const int character) noexcept
{
    return (character == '\n') || (character == '\r');
}

ConsoleReadStatus StdioConsoleInput::completeLine(std::string& line) noexcept
{
    if (overflow_active_) {
        overflow_active_ = false;
        pending_line_.clear();
        line.clear();
        return ConsoleReadStatus::LineTooLong;
    }

    line = pending_line_;
    pending_line_.clear();
    return ConsoleReadStatus::Ok;
}

ConsoleReadStatus StdioConsoleInput::readLine(std::string& line)
{
    line.clear();

    for (;;) {
        const int character = std::getchar();
        if (character == EOF) {
            clearerr(stdin);
            vTaskDelay(kNoDataBackoffTicks);
            return ConsoleReadStatus::NoData;
        }

        if ((character == '\n') && swallow_next_lf_) {
            swallow_next_lf_ = false;
            continue;
        }

        if (isLineTerminator(character)) {
            swallow_next_lf_ = (character == '\r');
            return completeLine(line);
        }

        swallow_next_lf_ = false;

        if (overflow_active_) {
            continue;
        }

        if (pending_line_.size() >= max_line_length_) {
            pending_line_.clear();
            overflow_active_ = true;
            continue;
        }

        pending_line_.push_back(static_cast<char>(character));
    }
}

}  // namespace secure_lab
