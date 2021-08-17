//////////////////////////////////////////////////////////////////////////////
//
// Copyright 2016 Autodesk, Inc. All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software.
//
//////////////////////////////////////////////////////////////////////////////

#pragma once
#include "../FusionTypeDefs.h"
#include "../../Core/Application/Product.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_DESIGN_CPP__
# define ADSK_FUSION_DESIGN_API XI_EXPORT
# else
# define ADSK_FUSION_DESIGN_API
# endif
#else
# define ADSK_FUSION_DESIGN_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class AreaProperties;
    class Component;
    class Components;
    class ContactSets;
    class ExportManager;
    class FusionUnitsManager;
    class InterferenceInput;
    class InterferenceResults;
    class Occurrence;
    class ParameterList;
    class PhysicalProperties;
    class Snapshots;
    class Timeline;
    class UserParameters;
}}
namespace adsk { namespace core {
    class Appearances;
    class Materials;
    class ObjectCollection;
}}

namespace adsk { namespace fusion {

/// Object that represents an open Fusion 360 design. This derives from the
/// Design base class and adds the Fusion 360 specific functionality.
class Design : public core::Product {
public:

    /// Gets and sets the current design type (DirectDesignType or ParametricDesignType)
    /// Changing an exising design from ParametricDesignType to DirectDesignType will result in the timeline and all design
    /// history being removed and further operations will not be captured in the timeline.
    DesignTypes designType() const;
    bool designType(DesignTypes value);

    /// Returns the root Component
    core::Ptr<Component> rootComponent() const;

    /// Returns the Components collection that provides access to existing components
    /// in a design
    core::Ptr<Components> allComponents() const;

    /// Returns the current edit target as seen in the user interface. This edit target
    /// is defined as the container object that will be added to if something is created.
    /// For example, a component can be an edit target so that when new bodies are created they
    /// are added to that component. A sketch can also be an edit target.
    core::Ptr<core::Base> activeEditObject() const;

    /// Returns the component that is current being edited. This can return the root component
    /// or another component within the design.
    core::Ptr<Component> activeComponent() const;

    /// Returns the Snapshots object associated with this design which provides access to the
    /// existing snapshots and the creation of new snapshots.
    core::Ptr<Snapshots> snapshots() const;

    /// Returns the timeline associated with this design.
    core::Ptr<Timeline> timeline() const;

    /// Returns the collection of User Parameters in a design
    core::Ptr<UserParameters> userParameters() const;

    /// Returns a read only list of all parameters in the design. This includes
    /// the user parameters and model parameters from all components in this design. The parameters from Externally Referenced components
    /// are NOT included because they are in actuality, separate designs.
    core::Ptr<ParameterList> allParameters() const;

    /// Returns a specialized UnitsManager that can set the default length units and work
    /// with parameters.
    core::Ptr<FusionUnitsManager> fusionUnitsManager() const;

    /// Returns the ExportManager for this design. You use the ExportManager
    /// to export the current design in various formats.
    core::Ptr<ExportManager> exportManager() const;

    /// Gets whether the root component is the active edit target in the user interface.
    /// This is the same as checking the state of the radio button next to the root compoonent in the browser.
    /// To activate the root component use the ActivateRootComponent method.
    bool isRootComponentActive() const;

    /// Makes the root component the active component in the user interface. This is the same
    /// as enabling the radio button next to the root component in the browser.
    /// Returns true if the activation was successful.
    bool activateRootComponent();

    /// Returns the materials contained in this document.
    core::Ptr<core::Materials> materials() const;

    /// Returns the appearances contained in this document.
    core::Ptr<core::Appearances> appearances() const;

    /// Creates an InterferenceInput object. This object collects the entities and options that are
    /// used when calculating interference. To analyze interference you first create an InterferenceInput
    /// supplying the entities and set any other settings and then provide this object as input to the
    /// analyzeInterference method.
    /// entities : An ObjectCollection containing the BRepBody and/or Occurrence entities that will be used in the
    /// interference calculation. All entities must be in the context of the root component of the top-level design.
    /// Returns an InterferenceInput object which you can use to set any other interference settings and then
    /// use as input to the analyzeInterference method to calculate the interference. Returns null if the
    /// creation failed.
    core::Ptr<InterferenceInput> createInterferenceInput(const core::Ptr<core::ObjectCollection>& entities);

    /// Calculates the interference between the input bodies and/or occurrences.
    /// input : An InterferenceInput that defines all of the necessary input needed to calculate the interference.
    /// An InterferenceInput object is created using the createInterferenceInput method.
    /// Returns an InterferenceResults object that can be used to examine the interference results.
    core::Ptr<InterferenceResults> analyzeInterference(const core::Ptr<InterferenceInput>& input);

    /// Returns the occurrence that is currently activated, if any. This can return null in the case
    /// where no occurrence is activated and the root component is active.
    core::Ptr<Occurrence> activeOccurrence() const;

    /// Returns the AreaProperties object that has properties for getting the area, perimeter, centroid, etc
    /// for a collection of 2D sketch profiles and/or planar surfaces that all lie on the same plane.
    /// inputs : A collection of one or more 2D sketch profile and/or planar surface input objects to perform the calculations on.
    /// Supported input object types are 2D closed sketch profiles and planar surfaces. Object must all lie on the same plane.
    /// Calculation results reflect the sums of the input objects (i.e. total area of multiple sketch profiles)
    /// accuracy : Specifies the desired level of computational accuracy of the property calculations.
    /// The default value of 'LowCalculationAccuracy' returns results within a +/- 1% error margin.
    /// Returns an AreaProperties object that can be used to examine the area results.
    core::Ptr<AreaProperties> areaProperties(const core::Ptr<core::ObjectCollection>& inputs, CalculationAccuracy accuracy = adsk::fusion::LowCalculationAccuracy) const;

    /// Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc
    /// for a collection of 3D solid objects.
    /// inputs : A collection of one or more 3D solid input objects to perform the calculations on.
    /// Supported input object types are Components, Occurrences and BRepBodies.
    /// Calculation results reflect the sums of the input objects (i.e. total volume of multiple bodies)
    /// accuracy : Specifies the desired level of computational accuracy of the property calculations.
    /// The default value of 'LowCalculationAccuracy' returns results within a +/- 1% error margin.
    core::Ptr<PhysicalProperties> physicalProperties(const core::Ptr<core::ObjectCollection>& inputs, CalculationAccuracy accuracy = adsk::fusion::LowCalculationAccuracy) const;

    /// Returns the contact sets associated with this design.
    core::Ptr<ContactSets> contactSets() const;

    /// Gets and sets whether contact analysis is enabled for all components. This
    /// is the equivalent of the "Disable Contact / Enable Contact" command. If this
    /// if True then any contact analysis defined (either all or contact sets) is enabled.
    /// if False, then no contact analysis is performed.
    bool isContactAnalysisEnabled() const;
    bool isContactAnalysisEnabled(bool value);

    /// Gets and sets whether contact analysis is done using contact sets
    /// or between all bodies, independent of any contact sets. If True and
    /// the isContactAnalysisEnabled property is True then contact analysis
    /// is performed using contact sets. If False and isContactAnalysisEnabled
    /// is True, then contact analysis is performed between all bodies. If
    /// isContactAnalysisEnabled is False then no contact analysis is performed.
    bool isContactSetAnalysis() const;
    bool isContactSetAnalysis(bool value);

    ADSK_FUSION_DESIGN_API static const char* classType();
    ADSK_FUSION_DESIGN_API const char* objectType() const override;
    ADSK_FUSION_DESIGN_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_DESIGN_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual DesignTypes designType_raw() const = 0;
    virtual bool designType_raw(DesignTypes value) = 0;
    virtual Component* rootComponent_raw() const = 0;
    virtual Components* allComponents_raw() const = 0;
    virtual core::Base* activeEditObject_raw() const = 0;
    virtual Component* activeComponent_raw() const = 0;
    virtual Snapshots* snapshots_raw() const = 0;
    virtual Timeline* timeline_raw() const = 0;
    virtual UserParameters* userParameters_raw() const = 0;
    virtual ParameterList* allParameters_raw() const = 0;
    virtual FusionUnitsManager* fusionUnitsManager_raw() const = 0;
    virtual ExportManager* exportManager_raw() const = 0;
    virtual bool isRootComponentActive_raw() const = 0;
    virtual bool activateRootComponent_raw() = 0;
    virtual core::Materials* materials_raw() const = 0;
    virtual core::Appearances* appearances_raw() const = 0;
    virtual InterferenceInput* createInterferenceInput_raw(core::ObjectCollection* entities) = 0;
    virtual InterferenceResults* analyzeInterference_raw(InterferenceInput* input) = 0;
    virtual Occurrence* activeOccurrence_raw() const = 0;
    virtual AreaProperties* areaProperties_raw(core::ObjectCollection* inputs, CalculationAccuracy accuracy) const = 0;
    virtual PhysicalProperties* physicalProperties_raw(core::ObjectCollection* inputs, CalculationAccuracy accuracy) const = 0;
    virtual ContactSets* contactSets_raw() const = 0;
    virtual bool isContactAnalysisEnabled_raw() const = 0;
    virtual bool isContactAnalysisEnabled_raw(bool value) = 0;
    virtual bool isContactSetAnalysis_raw() const = 0;
    virtual bool isContactSetAnalysis_raw(bool value) = 0;
};

// Inline wrappers

inline DesignTypes Design::designType() const
{
    DesignTypes res = designType_raw();
    return res;
}

inline bool Design::designType(DesignTypes value)
{
    return designType_raw(value);
}

inline core::Ptr<Component> Design::rootComponent() const
{
    core::Ptr<Component> res = rootComponent_raw();
    return res;
}

inline core::Ptr<Components> Design::allComponents() const
{
    core::Ptr<Components> res = allComponents_raw();
    return res;
}

inline core::Ptr<core::Base> Design::activeEditObject() const
{
    core::Ptr<core::Base> res = activeEditObject_raw();
    return res;
}

inline core::Ptr<Component> Design::activeComponent() const
{
    core::Ptr<Component> res = activeComponent_raw();
    return res;
}

inline core::Ptr<Snapshots> Design::snapshots() const
{
    core::Ptr<Snapshots> res = snapshots_raw();
    return res;
}

inline core::Ptr<Timeline> Design::timeline() const
{
    core::Ptr<Timeline> res = timeline_raw();
    return res;
}

inline core::Ptr<UserParameters> Design::userParameters() const
{
    core::Ptr<UserParameters> res = userParameters_raw();
    return res;
}

inline core::Ptr<ParameterList> Design::allParameters() const
{
    core::Ptr<ParameterList> res = allParameters_raw();
    return res;
}

inline core::Ptr<FusionUnitsManager> Design::fusionUnitsManager() const
{
    core::Ptr<FusionUnitsManager> res = fusionUnitsManager_raw();
    return res;
}

inline core::Ptr<ExportManager> Design::exportManager() const
{
    core::Ptr<ExportManager> res = exportManager_raw();
    return res;
}

inline bool Design::isRootComponentActive() const
{
    bool res = isRootComponentActive_raw();
    return res;
}

inline bool Design::activateRootComponent()
{
    bool res = activateRootComponent_raw();
    return res;
}

inline core::Ptr<core::Materials> Design::materials() const
{
    core::Ptr<core::Materials> res = materials_raw();
    return res;
}

inline core::Ptr<core::Appearances> Design::appearances() const
{
    core::Ptr<core::Appearances> res = appearances_raw();
    return res;
}

inline core::Ptr<InterferenceInput> Design::createInterferenceInput(const core::Ptr<core::ObjectCollection>& entities)
{
    core::Ptr<InterferenceInput> res = createInterferenceInput_raw(entities.get());
    return res;
}

inline core::Ptr<InterferenceResults> Design::analyzeInterference(const core::Ptr<InterferenceInput>& input)
{
    core::Ptr<InterferenceResults> res = analyzeInterference_raw(input.get());
    return res;
}

inline core::Ptr<Occurrence> Design::activeOccurrence() const
{
    core::Ptr<Occurrence> res = activeOccurrence_raw();
    return res;
}

inline core::Ptr<AreaProperties> Design::areaProperties(const core::Ptr<core::ObjectCollection>& inputs, CalculationAccuracy accuracy) const
{
    core::Ptr<AreaProperties> res = areaProperties_raw(inputs.get(), accuracy);
    return res;
}

inline core::Ptr<PhysicalProperties> Design::physicalProperties(const core::Ptr<core::ObjectCollection>& inputs, CalculationAccuracy accuracy) const
{
    core::Ptr<PhysicalProperties> res = physicalProperties_raw(inputs.get(), accuracy);
    return res;
}

inline core::Ptr<ContactSets> Design::contactSets() const
{
    core::Ptr<ContactSets> res = contactSets_raw();
    return res;
}

inline bool Design::isContactAnalysisEnabled() const
{
    bool res = isContactAnalysisEnabled_raw();
    return res;
}

inline bool Design::isContactAnalysisEnabled(bool value)
{
    return isContactAnalysisEnabled_raw(value);
}

inline bool Design::isContactSetAnalysis() const
{
    bool res = isContactSetAnalysis_raw();
    return res;
}

inline bool Design::isContactSetAnalysis(bool value)
{
    return isContactSetAnalysis_raw(value);
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_DESIGN_API