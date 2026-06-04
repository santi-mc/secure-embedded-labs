idf_component_register(
    SRCS "src/json_log.cpp"
    INCLUDE_DIRS "include"
    REQUIRES lab01_domain
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
