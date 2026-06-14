idf_component_register(
    SRCS "src/command_console.cpp"
    INCLUDE_DIRS "include"
    REQUIRES identity_service lab02_domain secure_log security_status
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
