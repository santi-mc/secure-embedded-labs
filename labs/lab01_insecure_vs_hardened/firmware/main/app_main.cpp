#include "app_core/application.hpp"

extern "C" void app_main(void)
{
    static secure_lab::Application application;
    application.run();
}
