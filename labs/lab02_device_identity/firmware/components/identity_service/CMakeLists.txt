idf_component_register(
    SRCS "src/identity_service.cpp"
    INCLUDE_DIRS "include"
    REQUIRES lab02_domain secure_log mbedtls
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wall -Wextra -Werror)
