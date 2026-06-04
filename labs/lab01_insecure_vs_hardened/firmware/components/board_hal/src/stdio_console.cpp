#include "board_hal/stdio_console.hpp"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include <cstdio>
#include <vector>

namespace secure_lab {

namespace {

inline constexpr TickType_t kNoDataBackoffTicks = pdMS_TO_TICKS(50U);

}  // namespace

StdioConsoleInput::StdioConsoleInput(const std::size_t max_line_length) noexcept
    : max_line_length_(max_line_length)
{
}

void StdioConsoleInput::drainUntilLineEnd() noexcept
{
    int character = 0;
    do {
        character = std::getchar();
    } while ((character != '\n') && (character != '\r') && (character != EOF));
}

ConsoleReadStatus StdioConsoleInput::readLine(std::string& line)
{
    line.clear();

    std::vector<char> buffer(max_line_length_ + 2U, '\0');
    if (std::fgets(buffer.data(), static_cast<int>(buffer.size()), stdin) == nullptr) {
        clearerr(stdin);
        vTaskDelay(kNoDataBackoffTicks);
        return ConsoleReadStatus::NoData;
    }

    line.assign(buffer.data());

    const bool has_newline = (!line.empty()) &&
                             ((line.back() == '\n') || (line.back() == '\r'));
    if (!has_newline && (line.size() > max_line_length_)) {
        drainUntilLineEnd();
        line.clear();
        return ConsoleReadStatus::LineTooLong;
    }

    while ((!line.empty()) && ((line.back() == '\n') || (line.back() == '\r'))) {
        line.pop_back();
    }

    if (line.size() > max_line_length_) {
        line.clear();
        return ConsoleReadStatus::LineTooLong;
    }

    return ConsoleReadStatus::Ok;
}

}  // namespace secure_lab
