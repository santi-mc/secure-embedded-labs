#pragma once
#include <initializer_list>
#include <string_view>
namespace secure_lab {
struct JsonField { std::string_view key; std::string_view value; };
class JsonLog { public: void event(std::string_view name, std::initializer_list<JsonField> fields = {}) const; };
}  // namespace secure_lab
