idf_component_register(
    SRCS "src/esp_system_clock.cpp" "src/stdio_console.cpp"
    INCLUDE_DIRS "include"
    REQUIRES lab01_domain esp_timer freertos
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
