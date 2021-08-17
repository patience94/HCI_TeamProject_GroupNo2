//Author-Autodesk Inc.
//Description-This is sample addin.
#include <Core/Utils.h>
#include <Core/Application/Application.h>
#include <Core/Application/Product.h>
#include <Core/Application/ValueInput.h>
#include <Core/Geometry/Plane.h>
#include <Core/Geometry/Point3D.h>
#include <Core/Geometry/Vector3D.h>
#include <Core/UserInterface/UserInterface.h>
#include <Core/UserInterface/CommandCreatedEventHandler.h>
#include <Core/UserInterface/CommandCreatedEvent.h>
#include <Core/UserInterface/CommandCreatedEventArgs.h>
#include <Core/UserInterface/CommandEvent.h>
#include <Core/UserInterface/CommandEventArgs.h>
#include <Core/UserInterface/CommandEventHandler.h>
#include <Core/UserInterface/InputChangedEvent.h>
#include <Core/UserInterface/InputChangedEventArgs.h>
#include <Core/UserInterface/InputChangedEventHandler.h>
#include <Core/UserInterface/Command.h>
#include <Core/UserInterface/CommandDefinition.h>
#include <Core/UserInterface/CommandDefinitions.h>
#include <Core/UserInterface/ListControlDefinition.h>
#include <Core/UserInterface/CommandInputs.h>
#include <Core/UserInterface/ValueCommandInput.h>
#include <Core/UserInterface/StringValueCommandInput.h>
#include <Core/UserInterface/BoolValueCommandInput.h>
#include <Core/UserInterface/SelectionCommandInput.h>
#include <Core/UserInterface/DropDownCommandInput.h>
#include <Core/UserInterface/FloatSliderCommandInput.h>
#include <Core/UserInterface/ButtonRowCommandInput.h>
#include <Core/UserInterface/DirectionCommandInput.h>
#include <Core/UserInterface/DistanceValueCommandInput.h>
#include <Core/UserInterface/CommandControl.h>
#include <Core/UserInterface/Toolbars.h>
#include <Core/UserInterface/Toolbar.h>
#include <Core/UserInterface/ToolbarControls.h>
#include <Core/UserInterface/ToolbarControl.h>
#include <Core/UserInterface/ToolbarPanels.h>
#include <Core/UserInterface/ToolbarPanel.h>
#include <Core/UserInterface/Workspaces.h>
#include <Core/UserInterface/Workspace.h>
#include <Core/UserInterface/ListItems.h>
#include <Core/UserInterface/ListItem.h>
#include <Core/UserInterface/Selection.h>
#include <Fusion/BRep/BRepFace.h>
#include <Fusion/Construction/ConstructionPlane.h>

#include <sstream>

using namespace adsk::core;
using namespace adsk::fusion;

const std::string btnCmdIdOnQAT = "demoButtonCommandOnQATCPP";
const std::string listCmdIdOnQAT = "demoListCommandOnQATCPP";
const std::string commandIdOnPanel = "demoCommandOnPanelCPP";
const std::string iconResources = "./resources";
const std::string selectionInputId = "selectionInput";
const std::string distanceInputId = "distanceValueCommandInput";
const std::string panelId = "SolidCreatePanel";

Ptr<Application> app;
Ptr<UserInterface> ui;

class CommandExecutedHandler : public adsk::core::CommandEventHandler
{
public:
	void notify(const Ptr<CommandEventArgs>& eventArgs) override
	{
		Ptr<Event> firingEvent = eventArgs->firingEvent();
		if (!firingEvent)
			return;

		Ptr<Command> command = firingEvent->sender();
		if (!command)
			return;

		Ptr<CommandDefinition> parentDefinition = command->parentCommandDefinition();
		if (!parentDefinition)
			return;

		std::stringstream ss;
		ss << "command: " + parentDefinition->id() << " executed successfully";

		ui->messageBox(ss.str());
	}
};

class InputChangedHandler : public adsk::core::InputChangedEventHandler
{
public:
	void notify(const Ptr<InputChangedEventArgs>& eventArgs) override
	{
		Ptr<Event> firingEvent = eventArgs->firingEvent();
		if (!firingEvent)
			return;

		Ptr<Command> command = firingEvent->sender();
		if (!command)
			return;

		Ptr<CommandDefinition> parentDefinition = command->parentCommandDefinition();
		if (!parentDefinition)
			return;

		Ptr<CommandInput> cmdInput = eventArgs->input();
		if(!cmdInput)
			return;

		if(cmdInput->id() != distanceInputId)
		{
			std::stringstream ss;
			ss << "Input: " << parentDefinition->id() << " changed event triggered";
			ui->messageBox(ss.str());
		}

		if(cmdInput->id() == selectionInputId){
			Ptr<CommandInputs> inputs = cmdInput->commandInputs();
			Ptr<DistanceValueCommandInput> distanceInput = inputs->itemById(distanceInputId);

			Ptr<SelectionCommandInput> selInput = cmdInput;
			if(selInput->selectionCount() > 0){
				Ptr<Selection> sel = selInput->selection(0);
				if(!sel)
					return;

				Ptr<Point3D> selPt = sel->point();
				if(!selPt)
					return;

				Ptr<Base> obj = sel->entity();
				if(!obj)
					return;

				Ptr<Plane> plane;
				if(Ptr<BRepFace> face = obj)
				{
					plane = face->geometry();
				}
				else if(Ptr<ConstructionPlane> constructionPlane = obj)
				{
					plane = constructionPlane->geometry();
				}
				if(!plane)
					return;

				distanceInput->setManipulator(selPt, plane->normal());
				distanceInput->expression("10mm * 2");
				distanceInput->isEnabled(true);
				distanceInput->isVisible(true);
			}
			else{
				distanceInput->isEnabled(false);
				distanceInput->isVisible(false);
			}
		}
	}
};

class CommandCreatedOnQATHandler : public adsk::core::CommandCreatedEventHandler
{
public:
	void notify(const Ptr<CommandCreatedEventArgs>& eventArgs) override
	{
		if (eventArgs)
		{
			Ptr<Command> command = eventArgs->command();
			if (!command)
				return;

			Ptr<CommandEvent> exec = command->execute();
			if (!exec)
				return;
			exec->add(&onCommandExecuted_);

			if (ui)
				ui->messageBox("QAT command created successfully");
		}
	}
private:
	CommandExecutedHandler onCommandExecuted_;
} onCommandCreatedOnQAT;

class CommandCreatedOnPanelHandler : public adsk::core::CommandCreatedEventHandler
{
public:
	void notify(const Ptr<CommandCreatedEventArgs>& eventArgs) override
	{
		if (eventArgs)
		{
			Ptr<Command> command = eventArgs->command();
			if (!command)
				return;

			command->helpFile("help.html");

			Ptr<CommandEvent> exec = command->execute();
			if (!exec)
				return;
			exec->add(&onCommandExecuted_);

			Ptr<InputChangedEvent> inputChanged = command->inputChanged();
			if (!inputChanged)
				return;
			inputChanged->add(&onInputChanged_);
			
			// Define the inputs.
			Ptr<CommandInputs> inputs = command->commandInputs();
			if (!inputs)
				return;

			inputs->addValueInput("valueInput_", "Value", "cm", ValueInput::createByString("0.0 cm"));
			inputs->addBoolValueInput("boolvalueInput_", "Bool", true);
			inputs->addStringValueInput("stringValueInput_", "String Value", "Default value");
			Ptr<SelectionCommandInput> selInput = inputs->addSelectionInput(selectionInputId, "Selection", "Select one");
			if (selInput)
			{
				selInput->setSelectionLimits(0);
				selInput->addSelectionFilter("PlanarFaces");
				selInput->addSelectionFilter("ConstructionPlanes");
			}

			Ptr<DropDownCommandInput> dropDownCommandInput = inputs->addDropDownCommandInput("dropdownCommandInput", "Drop Down", DropDownStyles::LabeledIconDropDownStyle);
			if (dropDownCommandInput)
			{
				Ptr<ListItems> dropdownItems = dropDownCommandInput->listItems();
				if (!dropdownItems)
					return;
				dropdownItems->add("ListItem 1", true);
				dropdownItems->add("ListItem 2", false);
				dropdownItems->add("ListItem 3", false);
			}
			Ptr<DropDownCommandInput> dropDownCommandInput2 = inputs->addDropDownCommandInput("dropDownCommandInput2", "Drop Down2", DropDownStyles::CheckBoxDropDownStyle);
			if (dropDownCommandInput2)
			{
				Ptr<ListItems> dropdownItems = dropDownCommandInput2->listItems();
				if (!dropdownItems)
					return;
				dropdownItems->add("ListItem 1", true);
				dropdownItems->add("ListItem 2", true);
				dropdownItems->add("ListItem 3", false);
			}
			inputs->addFloatSliderCommandInput("floatSliderCommandInput", "Slider", "cm", 0.0, 10.0, true);
			Ptr<ButtonRowCommandInput> buttonRowCommandInput = inputs->addButtonRowCommandInput("buttonRowCommandInput", "Button Row", false);
			if (buttonRowCommandInput)
			{
				Ptr<ListItems> buttonRowItems = buttonRowCommandInput->listItems();
				if (!buttonRowItems)
					return;
				buttonRowItems->add("ListItem 1", false, iconResources);
				buttonRowItems->add("ListItem 2", true, iconResources);
				buttonRowItems->add("ListItem 3", false, iconResources);
			}

			Ptr<DistanceValueCommandInput> distanceInput = inputs->addDistanceValueCommandInput(distanceInputId, "Distance", adsk::core::ValueInput::createByReal(0.0));
			if(distanceInput)
			{
				distanceInput->isEnabled(false);
				distanceInput->isVisible(false);
				distanceInput->minimumValue(1.0);
				distanceInput->maximumValue(10.0);
			}

			Ptr<DirectionCommandInput> directionInput = inputs->addDirectionCommandInput("directionInput", "Direction");
			if(directionInput)
			{
				directionInput->setManipulator(Point3D::create(0,0,0), Vector3D::create(1,0,0));
			}
			
			Ptr<DirectionCommandInput> directionInput2 = inputs->addDirectionCommandInput("directionInput2", "Direction2", iconResources);
			if(directionInput2)
			{
				directionInput2->setManipulator(Point3D::create(0,0,0), Vector3D::create(0,1,0));
			}

			ui->messageBox("Panel command created successfully");
		}
	}
private:
	CommandExecutedHandler onCommandExecuted_;
	InputChangedHandler onInputChanged_;
} onCommandCreatedOnPanel;

extern "C" XI_EXPORT bool run(const char* context)
{
	const std::string commandName = "Demo";
	const std::string commandDescription = "Demo Command";
	const std::string commandResources = "./resources";

	app = Application::get();
	if (!app)
		return false;

	ui = app->userInterface();
	if (!ui)
		return false;

	Ptr<CommandDefinitions> commandDefinitions = ui->commandDefinitions();
	if (!commandDefinitions)
		return false;

	// add a button command on Quick Access Toolbar
	Ptr<Toolbars> toolbars = ui->toolbars();
	if (!toolbars)
		return false;

	Ptr<Toolbar> toolbarQAT = toolbars->itemById("QAT");
	if (!toolbarQAT)
		return false;

	Ptr<ToolbarControls> toolbarControlsQAT = toolbarQAT->controls();
	if (!toolbarControlsQAT)
		return false;
	Ptr<ToolbarControl> btnCmdToolbarCtlQAT = toolbarControlsQAT->itemById(btnCmdIdOnQAT);
	if (!btnCmdToolbarCtlQAT)
	{
		Ptr<CommandDefinition> btnCmdDefinitionQAT = commandDefinitions->itemById(btnCmdIdOnQAT);
		if (!btnCmdDefinitionQAT)
		{
			btnCmdDefinitionQAT = commandDefinitions->addButtonDefinition(btnCmdIdOnQAT, commandName, commandDescription, commandResources);

		}

		Ptr<CommandCreatedEvent> btnCmdCreatedEvent = btnCmdDefinitionQAT->commandCreated();
		if (!btnCmdCreatedEvent)
			return false;
		btnCmdCreatedEvent->add(&onCommandCreatedOnQAT);
		btnCmdToolbarCtlQAT = toolbarControlsQAT->addCommand(btnCmdDefinitionQAT);
		if (!btnCmdToolbarCtlQAT)
			return false;
		btnCmdToolbarCtlQAT->isVisible(true);
		ui->messageBox("A demo button command is successfully added to the Quick Access Toolbar");
	}

	// add a list command on Quick Access Toolbar
	Ptr<ToolbarControl> listCmdToolbarCtlQAT = toolbarControlsQAT->itemById(listCmdIdOnQAT);
	if (!listCmdToolbarCtlQAT)
	{
		Ptr<CommandDefinition> listCmdDefinitionQAT = commandDefinitions->itemById(listCmdIdOnQAT);
		if (!listCmdDefinitionQAT)
		{
			listCmdDefinitionQAT = commandDefinitions->addListDefinition(listCmdIdOnQAT, commandName, ListControlDisplayTypes::CheckBoxListType, commandResources);
			if (!listCmdDefinitionQAT)
				return false;
			Ptr<ListControlDefinition> listCtlDefinition = listCmdDefinitionQAT->controlDefinition();
			if (!listCtlDefinition)
				return false;
			Ptr<ListItems> listItems = listCtlDefinition->listItems();
			if (!listItems)
				return false;
			listItems->add("Demo item 1", true);
			listItems->add("Demo item 2", false);
			listItems->add("Demo item 3", false);
		}

		Ptr<CommandCreatedEvent> listCmdCreatedEvent = listCmdDefinitionQAT->commandCreated();
		if (!listCmdCreatedEvent)
			return false;
		listCmdCreatedEvent->add(&onCommandCreatedOnQAT);
		listCmdToolbarCtlQAT = toolbarControlsQAT->addCommand(listCmdDefinitionQAT);
		if (!listCmdToolbarCtlQAT)
			return false;
		listCmdToolbarCtlQAT->isVisible(true);
		ui->messageBox("A demo list command is successfully added to the Quick Access Toolbar");
	}

	// add a command on create panel in modeling workspace
	Ptr<Workspaces> workspaces = ui->workspaces();
	if (!workspaces)
		return false;
	Ptr<Workspace> modelingWorkspace = workspaces->itemById("FusionSolidEnvironment");
	if (!modelingWorkspace)
		return false;
	Ptr<ToolbarPanels> toolbarPanels = modelingWorkspace->toolbarPanels();
	if (!toolbarPanels)
		return false;
	Ptr<ToolbarPanel> toolbarPanel = toolbarPanels->itemById(panelId); // add the new command under the CREATE panel
	if (!toolbarPanel)
		return false;
	Ptr<ToolbarControls> toolbarControlsPanel = toolbarPanel->controls();
	if (!toolbarControlsPanel)
		return false;
	Ptr<ToolbarControl> toolbarControlPanel = toolbarControlsPanel->itemById(commandIdOnPanel);
	if (!toolbarControlPanel)
	{
		Ptr<CommandDefinition> commandDefinitionPanel = commandDefinitions->itemById(commandIdOnPanel);
		if (!commandDefinitionPanel)
		{
			commandDefinitionPanel = commandDefinitions->addButtonDefinition(commandIdOnPanel, commandName, commandDescription, commandResources);
		}
		Ptr<CommandCreatedEvent> cmdCreatedEvent = commandDefinitionPanel->commandCreated();
		if (!cmdCreatedEvent)
			return false;
		cmdCreatedEvent->add(&onCommandCreatedOnPanel);
		toolbarControlPanel = toolbarControlsPanel->addCommand(commandDefinitionPanel);
		if (toolbarControlPanel)
			toolbarControlPanel->isVisible(true);
		ui->messageBox("A demo command is successfully added to the create panel in modeling workspace");
	}

	return true;
}

extern "C" XI_EXPORT bool stop(const char* context)
{
	if (!ui)
		return false;

	// Get controls and command definitions
	Ptr<Toolbars> toolbars = ui->toolbars();
	if (!toolbars)
		return false;
	Ptr<Toolbar> toolbarQAT = toolbars->itemById("QAT");
	if (!toolbarQAT)
		return false;
	Ptr<ToolbarControls> toolbarControlsQAT = toolbarQAT->controls();
	if (!toolbarControlsQAT)
		return false;
	Ptr<ToolbarControl> btnCmdToolbarCtlQAT = toolbarControlsQAT->itemById(btnCmdIdOnQAT);
	Ptr<ToolbarControl> listCmdToolbarCtlQAT = toolbarControlsQAT->itemById(listCmdIdOnQAT);
	Ptr<CommandDefinitions> commandDefinitions = ui->commandDefinitions();
	if (!commandDefinitions)
		return false;
	Ptr<CommandDefinition> btnCmdDefinitionQAT = commandDefinitions->itemById(btnCmdIdOnQAT);
	Ptr<CommandDefinition> listCmdDefinitionQAT = commandDefinitions->itemById(listCmdIdOnQAT);
	Ptr<Workspaces> workspaces = ui->workspaces();
	if (!workspaces)
		return false;
	Ptr<Workspace> modelingWorkspace = workspaces->itemById("FusionSolidEnvironment");
	if (!modelingWorkspace)
		return false;
	Ptr<ToolbarPanels> toolbarPanels = modelingWorkspace->toolbarPanels();
	if (!toolbarPanels)
		return false;
	Ptr<ToolbarPanel> toolbarPanel = toolbarPanels->itemById(panelId);
	if (!toolbarPanel)
		return false;
	Ptr<ToolbarControls> toolbarControlsPanel = toolbarPanel->controls();
	if (!toolbarControlsPanel)
		return false;
	Ptr<ToolbarControl> toolbarControlPanel = toolbarControlsPanel->itemById(commandIdOnPanel);
	Ptr<CommandDefinition> commandDefinitionPanel = commandDefinitions->itemById(commandIdOnPanel);
	
	// Delete controls and associated command definitions
	if (btnCmdToolbarCtlQAT)
		btnCmdToolbarCtlQAT->deleteMe();
	if (listCmdToolbarCtlQAT)
		listCmdToolbarCtlQAT->deleteMe();
	if (btnCmdDefinitionQAT)
		btnCmdDefinitionQAT->deleteMe();
	if (listCmdToolbarCtlQAT)
		listCmdToolbarCtlQAT->deleteMe();
	if (toolbarControlPanel)
		toolbarControlPanel->deleteMe();
	if (commandDefinitionPanel)
		commandDefinitionPanel->deleteMe();

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
