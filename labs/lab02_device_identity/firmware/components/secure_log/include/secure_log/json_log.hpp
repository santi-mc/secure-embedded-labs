#pragma once

#include "lab02_domain/interfaces.hpp"

#include <initializer_list>
#include <string>
#include <string_view>

namespace secure_lab {

struct JsonField final {
    std::string_view key;
    std::string_view value;
};

class JsonLog final {
public:
    explicit JsonLog(const IClock& clock) noexcept;

    void event(std::string_view event_name,
               std::initializer_list<JsonField> fields = {}) const;

private:
    const IClock& clock_;

    static void appendEscaped(std::string& output, std::string_view input);
    static void appendStringField(std::string& output,
                                  std::string_view key,
                                  std::string_view value);
};

}  // namespace secure_lab
