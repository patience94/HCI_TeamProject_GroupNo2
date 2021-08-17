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
# ifdef __COMPILING_ADSK_FUSION_JOINTORIGIN_CPP__
# define ADSK_FUSION_JOINTORIGIN_API XI_EXPORT
# else
# define ADSK_FUSION_JOINTORIGIN_API
# endif
#else
# define ADSK_FUSION_JOINTORIGIN_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Component;
    class JointGeometry;
    class ModelParameter;
    class Occurrence;
    class TimelineObject;
}}
namespace adsk { namespace core {
    class Attributes;
    class Vector3D;
}}

namespace adsk { namespace fusion {

/// Represents an existing joint origin in a design.
class JointOrigin : public core::Base {
public:

    /// Returns the parent component that owns this joint origin.
    core::Ptr<Component> parentComponent() const;

    /// Gets and sets the name of this joint origin. This is the name seen by the user in the timeline.
    std::string name() const;
    bool name(const std::string& value);

    /// Gets and sets the joint geometry for this joint origin input. This
    /// defines the location of the joint origin.
    core::Ptr<JointGeometry> geometry() const;
    bool geometry(const core::Ptr<JointGeometry>& value);

    /// Gets the parameter that controls the angle. The value can be changed
    /// using the functionality of the returned ModelParameter object.
    core::Ptr<ModelParameter> angle() const;

    /// Gets the parameter that controls the X offset direction. The value can be changed
    /// using the functionality of the returned ModelParameter object.
    core::Ptr<ModelParameter> offsetX() const;

    /// Gets the parameter that controls the Y offset direction. The value can be changed
    /// using the functionality of the returned ModelParameter object.
    core::Ptr<ModelParameter> offsetY() const;

    /// Gets the parameter that controls the Z offset direction. The value can be changed
    /// using the functionality of the returned ModelParameter object.
    core::Ptr<ModelParameter> offsetZ() const;

    /// Gets and sets if the joint origin direction is flipped or not.
    bool isFlipped() const;
    bool isFlipped(bool value);

    /// Gets and sets the entity that defines the X axis direction. This defaults
    /// to null meaning the X axis is inferred from the input geometry.
    core::Ptr<core::Base> xAxisEntity() const;
    bool xAxisEntity(const core::Ptr<core::Base>& value);

    /// Gets and sets the entity that defines the Z axis direction. This defaults
    /// to null meaning the Z axis is inferred from the input geometry.
    core::Ptr<core::Base> zAxisEntity() const;
    bool zAxisEntity(const core::Ptr<core::Base>& value);

    /// Returns the direction of the primary axis that's been calculated for this joint origin.
    core::Ptr<core::Vector3D> primaryAxisVector() const;

    /// Returns the direction of the secondary axis that's been calculated for this joint origin.
    core::Ptr<core::Vector3D> secondaryAxisVector() const;

    /// Returns the direction of the third axis that's been calculated for this joint origin.
    core::Ptr<core::Vector3D> thirdAxisVector() const;

    /// Deletes this joint origin.
    /// Returns true if successful.
    bool deleteMe();

    /// Returns the timeline object associated with this joint origin.
    core::Ptr<TimelineObject> timelineObject() const;

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<JointOrigin> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<JointOrigin> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    /// Returns the assembly occurrence (i.e. the occurrence) of this object
    /// in an assembly. This is only valid in the case where this is acting
    /// as a proxy in an assembly. Returns null in the case where the object
    /// is not in the context of an assembly but is already the native object.
    core::Ptr<Occurrence> assemblyContext() const;

    /// Returns the collection of attributes associated with this joint origin.
    core::Ptr<core::Attributes> attributes() const;

    ADSK_FUSION_JOINTORIGIN_API static const char* classType();
    ADSK_FUSION_JOINTORIGIN_API const char* objectType() const override;
    ADSK_FUSION_JOINTORIGIN_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_JOINTORIGIN_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual Component* parentComponent_raw() const = 0;
    virtual char* name_raw() const = 0;
    virtual bool name_raw(const char * value) = 0;
    virtual JointGeometry* geometry_raw() const = 0;
    virtual bool geometry_raw(JointGeometry* value) = 0;
    virtual ModelParameter* angle_raw() const = 0;
    virtual ModelParameter* offsetX_raw() const = 0;
    virtual ModelParameter* offsetY_raw() const = 0;
    virtual ModelParameter* offsetZ_raw() const = 0;
    virtual bool isFlipped_raw() const = 0;
    virtual bool isFlipped_raw(bool value) = 0;
    virtual core::Base* xAxisEntity_raw() const = 0;
    virtual bool xAxisEntity_raw(core::Base* value) = 0;
    virtual core::Base* zAxisEntity_raw() const = 0;
    virtual bool zAxisEntity_raw(core::Base* value) = 0;
    virtual core::Vector3D* primaryAxisVector_raw() const = 0;
    virtual core::Vector3D* secondaryAxisVector_raw() const = 0;
    virtual core::Vector3D* thirdAxisVector_raw() const = 0;
    virtual bool deleteMe_raw() = 0;
    virtual TimelineObject* timelineObject_raw() const = 0;
    virtual JointOrigin* nativeObject_raw() const = 0;
    virtual JointOrigin* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
    virtual Occurrence* assemblyContext_raw() const = 0;
    virtual core::Attributes* attributes_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<Component> JointOrigin::parentComponent() const
{
    core::Ptr<Component> res = parentComponent_raw();
    return res;
}

inline std::string JointOrigin::name() const
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

inline bool JointOrigin::name(const std::string& value)
{
    return name_raw(value.c_str());
}

inline core::Ptr<JointGeometry> JointOrigin::geometry() const
{
    core::Ptr<JointGeometry> res = geometry_raw();
    return res;
}

inline bool JointOrigin::geometry(const core::Ptr<JointGeometry>& value)
{
    return geometry_raw(value.get());
}

inline core::Ptr<ModelParameter> JointOrigin::angle() const
{
    core::Ptr<ModelParameter> res = angle_raw();
    return res;
}

inline core::Ptr<ModelParameter> JointOrigin::offsetX() const
{
    core::Ptr<ModelParameter> res = offsetX_raw();
    return res;
}

inline core::Ptr<ModelParameter> JointOrigin::offsetY() const
{
    core::Ptr<ModelParameter> res = offsetY_raw();
    return res;
}

inline core::Ptr<ModelParameter> JointOrigin::offsetZ() const
{
    core::Ptr<ModelParameter> res = offsetZ_raw();
    return res;
}

inline bool JointOrigin::isFlipped() const
{
    bool res = isFlipped_raw();
    return res;
}

inline bool JointOrigin::isFlipped(bool value)
{
    return isFlipped_raw(value);
}

inline core::Ptr<core::Base> JointOrigin::xAxisEntity() const
{
    core::Ptr<core::Base> res = xAxisEntity_raw();
    return res;
}

inline bool JointOrigin::xAxisEntity(const core::Ptr<core::Base>& value)
{
    return xAxisEntity_raw(value.get());
}

inline core::Ptr<core::Base> JointOrigin::zAxisEntity() const
{
    core::Ptr<core::Base> res = zAxisEntity_raw();
    return res;
}

inline bool JointOrigin::zAxisEntity(const core::Ptr<core::Base>& value)
{
    return zAxisEntity_raw(value.get());
}

inline core::Ptr<core::Vector3D> JointOrigin::primaryAxisVector() const
{
    core::Ptr<core::Vector3D> res = primaryAxisVector_raw();
    return res;
}

inline core::Ptr<core::Vector3D> JointOrigin::secondaryAxisVector() const
{
    core::Ptr<core::Vector3D> res = secondaryAxisVector_raw();
    return res;
}

inline core::Ptr<core::Vector3D> JointOrigin::thirdAxisVector() const
{
    core::Ptr<core::Vector3D> res = thirdAxisVector_raw();
    return res;
}

inline bool JointOrigin::deleteMe()
{
    bool res = deleteMe_raw();
    return res;
}

inline core::Ptr<TimelineObject> JointOrigin::timelineObject() const
{
    core::Ptr<TimelineObject> res = timelineObject_raw();
    return res;
}

inline core::Ptr<JointOrigin> JointOrigin::nativeObject() const
{
    core::Ptr<JointOrigin> res = nativeObject_raw();
    return res;
}

inline core::Ptr<JointOrigin> JointOrigin::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<JointOrigin> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}

inline core::Ptr<Occurrence> JointOrigin::assemblyContext() const
{
    core::Ptr<Occurrence> res = assemblyContext_raw();
    return res;
}

inline core::Ptr<core::Attributes> JointOrigin::attributes() const
{
    core::Ptr<core::Attributes> res = attributes_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_JOINTORIGIN_API