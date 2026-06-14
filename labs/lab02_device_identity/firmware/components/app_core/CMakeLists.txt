idf_component_register(
    SRCS "src/application.cpp"
    INCLUDE_DIRS "include"
    REQUIRES board_hal command_console identity_service lab02_domain secure_log security_status
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
