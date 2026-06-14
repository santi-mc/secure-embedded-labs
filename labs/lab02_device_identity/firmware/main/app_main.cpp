#include "app_core/application.hpp"

extern "C" void app_main(void)
{
    secure_lab::Application app;
    app.run();
}
