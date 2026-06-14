idf_component_register(
    SRCS "app_main.cpp"
    REQUIRES app_core
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
