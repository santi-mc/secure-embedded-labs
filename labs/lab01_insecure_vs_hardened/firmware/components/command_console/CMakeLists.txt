idf_component_register(
    SRCS "src/command_console.cpp"
    INCLUDE_DIRS "include"
    REQUIRES app_config lab01_domain secure_log sensor_sim security_status
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
