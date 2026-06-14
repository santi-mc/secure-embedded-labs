idf_component_register(
    SRCS "src/esp_system_clock.cpp" "src/esp_device_unique_source.cpp" "src/stdio_console.cpp"
    INCLUDE_DIRS "include"
    REQUIRES lab02_domain esp_timer efuse freertos
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
