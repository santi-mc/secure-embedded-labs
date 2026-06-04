idf_component_register(
    SRCS "src/security_status.cpp"
    INCLUDE_DIRS "include"
    REQUIRES lab01_domain secure_log
    PRIV_REQUIRES bootloader_support efuse
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
