//Author-Autodesk Inc.
//Description-Simple script display a message.
#include <Core/Application/Application.h>
#include <Core/UserInterface/UserInterface.h>


using namespace adsk::core;

Ptr<UserInterface> ui;

extern "C" XI_EXPORT bool run(const char* context)
{
	Ptr<Application> app = Application::get();
	if (!app)
		return false;

	ui = app->userInterface();
	if (!ui)
		return false;

	ui->messageBox("Hello script");

	return true;
}

#ifdef XI_WIN

#include <windows.h>

BOOL APIENTRY DllMain(HMODULE hmodule, DWORD reason, LPVOID reserved)
{
	switch (reason)
	{
	case DLL_PROCESS_ATTACH:
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}

#endif // XI_WIN
