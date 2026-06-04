idf_component_register(
    SRCS "src/application.cpp"
    INCLUDE_DIRS "include"
    REQUIRES app_config board_hal command_console lab01_domain secure_log security_status sensor_sim
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
