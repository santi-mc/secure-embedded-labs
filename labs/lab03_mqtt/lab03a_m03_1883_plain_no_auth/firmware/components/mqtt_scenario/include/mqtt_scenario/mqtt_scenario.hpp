#pragma once
#include "lab03_domain/types.hpp"
#include "secure_log/json_log.hpp"
#include <cstddef>
#include <string_view>
namespace secure_lab {
class MqttScenarioService {
public:
    const MqttScenario& selected() const noexcept;
    bool select(std::string_view id) noexcept;
    void logList(const JsonLog& log) const;
    void logStatus(const JsonLog& log) const;
    void logConnectDryRun(const JsonLog& log) const;
    void logPublishDryRun(const JsonLog& log) const;
private:
    std::size_t selected_index_{0};
};
}  // namespace secure_lab
