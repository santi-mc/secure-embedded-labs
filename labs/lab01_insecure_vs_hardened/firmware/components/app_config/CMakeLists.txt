idf_component_register(
    SRCS "src/app_config.cpp"
    INCLUDE_DIRS "include"
    REQUIRES lab01_domain secure_log
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
