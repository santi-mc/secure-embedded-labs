#include "secure_log/json_log.hpp"

#include <cstdio>

namespace secure_lab {

JsonLog::JsonLog(const IClock& clock) noexcept : clock_(clock) {}

void JsonLog::appendEscaped(std::string& output, const std::string_view input)
{
    for (const char c : input) {
        switch (c) {
        case '"':
            output += "\\\"";
            break;
        case '\\':
            output += "\\\\";
            break;
        case '\n':
            output += "\\n";
            break;
        case '\r':
            output += "\\r";
            break;
        case '\t':
            output += "\\t";
            break;
        default:
            if (static_cast<unsigned char>(c) < 0x20U) {
                output += "?";
            } else {
                output += c;
            }
            break;
        }
    }
}

void JsonLog::appendStringField(std::string& output,
                                const std::string_view key,
                                const std::string_view value)
{
    output += ",\"";
    appendEscaped(output, key);
    output += "\":\"";
    appendEscaped(output, value);
    output += "\"";
}

void JsonLog::event(const std::string_view event_name,
                    const std::initializer_list<JsonField> fields) const
{
    std::string output;
    output.reserve(192U);
    output += "{\"event\":\"";
    appendEscaped(output, event_name);
    output += "\",\"schema_version\":1,\"uptime_ms\":";
    output += std::to_string(clock_.uptimeMs());

    for (const JsonField& field : fields) {
        appendStringField(output, field.key, field.value);
    }

    output += "}";
    static_cast<void>(std::printf("%s\n", output.c_str()));
    static_cast<void>(std::fflush(stdout));
}

}  // namespace secure_lab
