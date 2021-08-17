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
#include "Feature.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_CHAMFERFEATURE_CPP__
# define ADSK_FUSION_CHAMFERFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_CHAMFERFEATURE_API
# endif
#else
# define ADSK_FUSION_CHAMFERFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class ChamferTypeDefinition;
    class Occurrence;
}}
namespace adsk { namespace core {
    class ObjectCollection;
    class ValueInput;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing chamfer feature in a design.
class ChamferFeature : public Feature {
public:

    /// Gets and sets the edges being chamfered. In order to access (get) the input edges
    /// of a chamfer, you must roll the timeline back to just before the chamfer feature
    /// whose edges you want to access. When setting the edges, if the IsTangentChain property is true then
    /// all edges that are tangent to the input edges will be include in the chamfer.
    /// This property returns nothing in the case where the feature is non-parametric.
    core::Ptr<core::ObjectCollection> edges() const;
    bool edges(const core::Ptr<core::ObjectCollection>& value);

    /// Gets and sets whether or not edges that are tangentially connected to
    /// the input edges (if any) will also be chamfered.
    bool isTangentChain() const;
    bool isTangentChain(bool value);

    /// Gets an enum indicating how the chamfer was defined. The valid return values are
    /// EqualDistanceType, TwoDistancesType and DistanceAndAngleType.
    /// This property returns nothing in the case where the feature is non-parametric.
    ChamferTypes chamferType() const;

    /// Gets the definition object that is defining the type of chamfer. Modifying the
    /// definition object will cause the chamfer to recompute. Various types of definition objects can
    /// be returned depending on how the chamfer is defined. The ChamferType property can
    /// be used to determine which type of definition will be returned.
    /// This property returns nothing in the case where the feature is non-parametric.
    core::Ptr<ChamferTypeDefinition> chamferTypeDefinition() const;

    /// Changes the type of chamfer to be an equal distance chamfer.
    /// distance : A ValueInput object that defines the distance of the chamfer. If the ValueInput uses
    /// a real then it is interpreted as centimeters. If it is a string then the units
    /// can be defined as part of the string (i.e. "2 in"). If no units are specified
    /// it is interpreted using the current default units for length.
    /// Returns true if the feature is successfully changed
    bool setEqualDistance(const core::Ptr<core::ValueInput>& distance);

    /// Changes the type of chamfer to be a two distances chamfer.
    /// distanceOne : A ValueInput object that defines the distanceOne of the chamfer. This distance
    /// is along the face which is on the left of the selected edge.
    /// If the ValueInput uses a real then it is interpreted as centimeters.
    /// If it is a string then the units can be defined as part of the string (i.e. "2 in").
    /// If no units are specified it is interpreted using the current default units for length.
    /// distanceTwo : A ValueInput object that defines the distanceTwo of the chamfer. This distance
    /// is along the face which is on the right of the selected edge.
    /// If the ValueInput uses a real then it is interpreted as centimeters.
    /// If it is a string then the units can be defined as part of the string (i.e. "2 in").
    /// If no units are specified it is interpreted using the current default units for length.
    /// Returns true if the feature is successfully changed
    bool setTwoDistances(const core::Ptr<core::ValueInput>& distanceOne, const core::Ptr<core::ValueInput>& distanceTwo);

    /// Changes the type of chamfer to be a distance and angle chamfer.
    /// distance : A ValueInput object that defines the distance of the chamfer. This distance
    /// is along the face which is on the right of the selected edge.
    /// If the ValueInput uses a real then it is interpreted as centimeters.
    /// If it is a string then the units can be defined as part of the string (i.e. "2 in").
    /// If no units are specified it is interpreted using the current default units for length.
    /// angle : A valueInput object that defines the angle. The direction will be towards to the face
    /// which is on the left of the selected edge. This can be a string or a value.
    /// If it's a string it is interpreted using the current document units and can include
    /// equations. For example all of the following are valid as long as they result in
    /// angle units; "45", "45 deg", "a1 / 2". If a value is input it is interpreted
    /// as radians.
    /// It cannot be negative.
    /// Returns true if the feature is successfully changed
    bool setDistanceAndAngle(const core::Ptr<core::ValueInput>& distance, const core::Ptr<core::ValueInput>& angle);

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<ChamferFeature> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<ChamferFeature> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_CHAMFERFEATURE_API static const char* classType();
    ADSK_FUSION_CHAMFERFEATURE_API const char* objectType() const override;
    ADSK_FUSION_CHAMFERFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_CHAMFERFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::ObjectCollection* edges_raw() const = 0;
    virtual bool edges_raw(core::ObjectCollection* value) = 0;
    virtual bool isTangentChain_raw() const = 0;
    virtual bool isTangentChain_raw(bool value) = 0;
    virtual ChamferTypes chamferType_raw() const = 0;
    virtual ChamferTypeDefinition* chamferTypeDefinition_raw() const = 0;
    virtual bool setEqualDistance_raw(core::ValueInput* distance) = 0;
    virtual bool setTwoDistances_raw(core::ValueInput* distanceOne, core::ValueInput* distanceTwo) = 0;
    virtual bool setDistanceAndAngle_raw(core::ValueInput* distance, core::ValueInput* angle) = 0;
    virtual ChamferFeature* nativeObject_raw() const = 0;
    virtual ChamferFeature* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline core::Ptr<core::ObjectCollection> ChamferFeature::edges() const
{
    core::Ptr<core::ObjectCollection> res = edges_raw();
    return res;
}

inline bool ChamferFeature::edges(const core::Ptr<core::ObjectCollection>& value)
{
    return edges_raw(value.get());
}

inline bool ChamferFeature::isTangentChain() const
{
    bool res = isTangentChain_raw();
    return res;
}

inline bool ChamferFeature::isTangentChain(bool value)
{
    return isTangentChain_raw(value);
}

inline ChamferTypes ChamferFeature::chamferType() const
{
    ChamferTypes res = chamferType_raw();
    return res;
}

inline core::Ptr<ChamferTypeDefinition> ChamferFeature::chamferTypeDefinition() const
{
    core::Ptr<ChamferTypeDefinition> res = chamferTypeDefinition_raw();
    return res;
}

inline bool ChamferFeature::setEqualDistance(const core::Ptr<core::ValueInput>& distance)
{
    bool res = setEqualDistance_raw(distance.get());
    return res;
}

inline bool ChamferFeature::setTwoDistances(const core::Ptr<core::ValueInput>& distanceOne, const core::Ptr<core::ValueInput>& distanceTwo)
{
    bool res = setTwoDistances_raw(distanceOne.get(), distanceTwo.get());
    return res;
}

inline bool ChamferFeature::setDistanceAndAngle(const core::Ptr<core::ValueInput>& distance, const core::Ptr<core::ValueInput>& angle)
{
    bool res = setDistanceAndAngle_raw(distance.get(), angle.get());
    return res;
}

inline core::Ptr<ChamferFeature> ChamferFeature::nativeObject() const
{
    core::Ptr<ChamferFeature> res = nativeObject_raw();
    return res;
}

inline core::Ptr<ChamferFeature> ChamferFeature::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<ChamferFeature> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_CHAMFERFEATURE_API