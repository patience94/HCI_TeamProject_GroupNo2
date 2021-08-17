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
#include "../../Core/Base.h"
#include "../FusionTypeDefs.h"
#include <string>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_CONSTRUCTIONAXIS_CPP__
# define ADSK_FUSION_CONSTRUCTIONAXIS_API XI_EXPORT
# else
# define ADSK_FUSION_CONSTRUCTIONAXIS_API
# endif
#else
# define ADSK_FUSION_CONSTRUCTIONAXIS_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BaseFeature;
    class Component;
    class ConstructionAxisDefinition;
    class Occurrence;
    class TimelineObject;
}}
namespace adsk { namespace core {
    class Attributes;
    class InfiniteLine3D;
}}

namespace adsk { namespace fusion {

/// ConstructionAxis Object
class ConstructionAxis : public core::Base {
public:

    /// Returns an infinite line that represents the position and orientation of the
    /// construction axis. This geometry is defined in the AssemblyContext of this
    /// ConstructionAxis.
    core::Ptr<core::InfiniteLine3D> geometry() const;

    /// The name of the construction axis as it is shown in the browser.
    std::string name() const;
    bool name(const std::string& value);

    /// Returns the construction axis definition object which provides access to the information
    /// defining the construction axis.
    core::Ptr<ConstructionAxisDefinition> definition() const;

    /// Deletes the construction axis.
    /// Returns a bool indicating if the delete was successful or not.
    bool deleteMe();

    /// Indicates if this construction axis is parametric or not.
    bool isParametric() const;

    /// Indicates if this construction axis can be deleted. Base
    /// construction axes can not be deleted.
    bool isDeletable() const;

    /// Indicates if the light bulb (as displayed in the browser) is on.
    /// A construction axis will only be visible if it's light bulb, and that of it's
    /// containing folder and parent component/s are also on.
    bool isLightBulbOn() const;
    bool isLightBulbOn(bool value);

    /// Gets if the construction plane is visible.
    /// This property is affected by the AssemblyContext of the construction axis.
    bool isVisible() const;

    /// Returns the parent component or base feature. If both the design and the construction
    /// axis are parametric, the parent will be a component. If the design is parametric and
    /// the construction axis is not, the parent will be a base feature. If
    /// the design is not parametric the parent will be a component.
    core::Ptr<core::Base> parent() const;

    /// Returns the component this construction plane belongs to.
    core::Ptr<Component> component() const;

    /// Returns the timeline object associated with this construction axis.
    core::Ptr<TimelineObject> timelineObject() const;

    /// Returns the assembly occurrence (i.e. the occurrence) of this object
    /// in an assembly. This is only valid in the case where this is acting
    /// as a proxy in an assembly. Returns null in the case where the object
    /// is not in the context of an assembly but is already the native object.
    core::Ptr<Occurrence> assemblyContext() const;

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<ConstructionAxis> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<ConstructionAxis> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    /// If this construction axis is associated with a base feature, this property will return that base feature.
    /// If it's not associated with a base feature, this property will return null.
    core::Ptr<BaseFeature> baseFeature() const;

    /// Returns the collection of attributes associated with this construction axis.
    core::Ptr<core::Attributes> attributes() const;

    /// Returns the current health state of this construction axis.
    FeatureHealthStates healthState() const;

    /// Returns the error or warning message in the case where the healthState property returns either
    /// WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.
    std::string errorOrWarningMessage() const;

    ADSK_FUSION_CONSTRUCTIONAXIS_API static const char* classType();
    ADSK_FUSION_CONSTRUCTIONAXIS_API const char* objectType() const override;
    ADSK_FUSION_CONSTRUCTIONAXIS_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_CONSTRUCTIONAXIS_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::InfiniteLine3D* geometry_raw() const = 0;
    virtual char* name_raw() const = 0;
    virtual bool name_raw(const char * value) = 0;
    virtual ConstructionAxisDefinition* definition_raw() const = 0;
    virtual bool deleteMe_raw() = 0;
    virtual bool isParametric_raw() const = 0;
    virtual bool isDeletable_raw() const = 0;
    virtual bool isLightBulbOn_raw() const = 0;
    virtual bool isLightBulbOn_raw(bool value) = 0;
    virtual bool isVisible_raw() const = 0;
    virtual core::Base* parent_raw() const = 0;
    virtual Component* component_raw() const = 0;
    virtual TimelineObject* timelineObject_raw() const = 0;
    virtual Occurrence* assemblyContext_raw() const = 0;
    virtual ConstructionAxis* nativeObject_raw() const = 0;
    virtual ConstructionAxis* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
    virtual BaseFeature* baseFeature_raw() const = 0;
    virtual core::Attributes* attributes_raw() const = 0;
    virtual FeatureHealthStates healthState_raw() const = 0;
    virtual char* errorOrWarningMessage_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<core::InfiniteLine3D> ConstructionAxis::geometry() const
{
    core::Ptr<core::InfiniteLine3D> res = geometry_raw();
    return res;
}

inline std::string ConstructionAxis::name() const
{
    std::string res;

    char* p= name_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool ConstructionAxis::name(const std::string& value)
{
    return name_raw(value.c_str());
}

inline core::Ptr<ConstructionAxisDefinition> ConstructionAxis::definition() const
{
    core::Ptr<ConstructionAxisDefinition> res = definition_raw();
    return res;
}

inline bool ConstructionAxis::deleteMe()
{
    bool res = deleteMe_raw();
    return res;
}

inline bool ConstructionAxis::isParametric() const
{
    bool res = isParametric_raw();
    return res;
}

inline bool ConstructionAxis::isDeletable() const
{
    bool res = isDeletable_raw();
    return res;
}

inline bool ConstructionAxis::isLightBulbOn() const
{
    bool res = isLightBulbOn_raw();
    return res;
}

inline bool ConstructionAxis::isLightBulbOn(bool value)
{
    return isLightBulbOn_raw(value);
}

inline bool ConstructionAxis::isVisible() const
{
    bool res = isVisible_raw();
    return res;
}

inline core::Ptr<core::Base> ConstructionAxis::parent() const
{
    core::Ptr<core::Base> res = parent_raw();
    return res;
}

inline core::Ptr<Component> ConstructionAxis::component() const
{
    core::Ptr<Component> res = component_raw();
    return res;
}

inline core::Ptr<TimelineObject> ConstructionAxis::timelineObject() const
{
    core::Ptr<TimelineObject> res = timelineObject_raw();
    return res;
}

inline core::Ptr<Occurrence> ConstructionAxis::assemblyContext() const
{
    core::Ptr<Occurrence> res = assemblyContext_raw();
    return res;
}

inline core::Ptr<ConstructionAxis> ConstructionAxis::nativeObject() const
{
    core::Ptr<ConstructionAxis> res = nativeObject_raw();
    return res;
}

inline core::Ptr<ConstructionAxis> ConstructionAxis::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<ConstructionAxis> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}

inline core::Ptr<BaseFeature> ConstructionAxis::baseFeature() const
{
    core::Ptr<BaseFeature> res = baseFeature_raw();
    return res;
}

inline core::Ptr<core::Attributes> ConstructionAxis::attributes() const
{
    core::Ptr<core::Attributes> res = attributes_raw();
    return res;
}

inline FeatureHealthStates ConstructionAxis::healthState() const
{
    FeatureHealthStates res = healthState_raw();
    return res;
}

inline std::string ConstructionAxis::errorOrWarningMessage() const
{
    std::string res;

    char* p= errorOrWarningMessage_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_CONSTRUCTIONAXIS_API