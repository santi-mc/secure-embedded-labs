#include "board_hal/stdio_console.hpp"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <cstdio>
#include <cstring>
namespace secure_lab {
namespace { inline constexpr TickType_t kNoDataDelay = pdMS_TO_TICKS(20U); }
ConsoleReadStatus StdioConsole::readLine(ConsoleLine& out_line) noexcept {
    out_line = ConsoleLine{};
    while (true) {
        const int value = std::getchar();
        if (value == EOF) { clearerr(stdin); vTaskDelay(kNoDataDelay); return ConsoleReadStatus::NoData; }
        const char ch = static_cast<char>(value);
        if (ch == '\r' || ch == '\n') {
            if (ch == '\n' && previous_was_cr_) { previous_was_cr_ = false; continue; }
            previous_was_cr_ = (ch == '\r');
            std::memcpy(out_line.value, buffer_, length_);
            out_line.value[length_] = '\0';
            out_line.length = length_;
            length_ = 0;
            return ConsoleReadStatus::Ok;
        }
        previous_was_cr_ = false;
        if (length_ + 1U >= sizeof(buffer_)) { length_ = 0; return ConsoleReadStatus::LineTooLong; }
        buffer_[length_++] = ch;
    }
}
}  // namespace secure_lab
