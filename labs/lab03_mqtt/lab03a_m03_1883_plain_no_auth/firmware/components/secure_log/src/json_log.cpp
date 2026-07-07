#include "secure_log/json_log.hpp"
#include "esp_timer.h"
#include <cstdio>
namespace secure_lab {
namespace {
void printEscaped(std::string_view value) {
    for (const char ch : value) {
        if (ch == '"') { std::printf("\\\""); }
        else if (ch == '\\') { std::printf("\\\\"); }
        else { std::printf("%c", ch); }
    }
}
}
void JsonLog::event(std::string_view name, std::initializer_list<JsonField> fields) const {
    const auto uptime_ms = static_cast<long long>(esp_timer_get_time() / 1000LL);
    std::printf("{\"event\":\"");
    printEscaped(name);
    std::printf("\",\"schema_version\":1,\"uptime_ms\":%lld", uptime_ms);
    for (const auto& field : fields) {
        std::printf(",\"");
        printEscaped(field.key);
        std::printf("\":\"");
        printEscaped(field.value);
        std::printf("\"");
    }
    std::printf("}\n");
    std::fflush(stdout);
}
}  // namespace secure_lab
