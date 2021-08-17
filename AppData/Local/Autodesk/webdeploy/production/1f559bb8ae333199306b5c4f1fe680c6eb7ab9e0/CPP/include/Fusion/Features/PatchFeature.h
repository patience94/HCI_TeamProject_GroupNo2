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
# ifdef __COMPILING_ADSK_FUSION_PATCHFEATURE_CPP__
# define ADSK_FUSION_PATCHFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_PATCHFEATURE_API
# endif
#else
# define ADSK_FUSION_PATCHFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Occurrence;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing patch feature in a design.
class PatchFeature : public Feature {
public:

    /// Returns an ObjectCollection that contains all of the sketch curves or B-Rep edges
    /// that define the closed outer boundary of the patch feature.
    /// When setting this property, the input can be a sketch profile, a single sketch curve, a single B-Rep edge,
    /// or an ObjectCollection of sketch curves or B-Rep edges.
    /// If a single sketch curve or B-Rep edge is input, that is not closed, Fusion 360 will automatically find connected sketch curves
    /// or B-Rep edges in order to define a closed loop. All sketch curves are valid as input. BRepEdges are valid if they are
    /// an "open" edge, which means they are only used by one face.
    /// If an ObjectCollection of sketch curves or B-Rep edges is input they must define a closed shape and the B-Rep
    /// edges must be valid "open" edges.
    core::Ptr<core::Base> boundaryCurve() const;
    bool boundaryCurve(const core::Ptr<core::Base>& value);

    /// Gets the type of operation performed by the patch feature.
    FeatureOperations operation() const;

    /// Gets and sets the type of surface continuity used when creating the patch face. This is only used when BRepEdges are input and
    /// defines the continuity of how the patch face connects to the face adjacent to each of the input edges.
    SurfaceContinuityTypes continuity() const;
    bool continuity(SurfaceContinuityTypes value);

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<PatchFeature> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this is not the NativeObject.
    core::Ptr<PatchFeature> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_PATCHFEATURE_API static const char* classType();
    ADSK_FUSION_PATCHFEATURE_API const char* objectType() const override;
    ADSK_FUSION_PATCHFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_PATCHFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::Base* boundaryCurve_raw() const = 0;
    virtual bool boundaryCurve_raw(core::Base* value) = 0;
    virtual FeatureOperations operation_raw() const = 0;
    virtual SurfaceContinuityTypes continuity_raw() const = 0;
    virtual bool continuity_raw(SurfaceContinuityTypes value) = 0;
    virtual PatchFeature* nativeObject_raw() const = 0;
    virtual PatchFeature* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline core::Ptr<core::Base> PatchFeature::boundaryCurve() const
{
    core::Ptr<core::Base> res = boundaryCurve_raw();
    return res;
}

inline bool PatchFeature::boundaryCurve(const core::Ptr<core::Base>& value)
{
    return boundaryCurve_raw(value.get());
}

inline FeatureOperations PatchFeature::operation() const
{
    FeatureOperations res = operation_raw();
    return res;
}

inline SurfaceContinuityTypes PatchFeature::continuity() const
{
    SurfaceContinuityTypes res = continuity_raw();
    return res;
}

inline bool PatchFeature::continuity(SurfaceContinuityTypes value)
{
    return continuity_raw(value);
}

inline core::Ptr<PatchFeature> PatchFeature::nativeObject() const
{
    core::Ptr<PatchFeature> res = nativeObject_raw();
    return res;
}

inline core::Ptr<PatchFeature> PatchFeature::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<PatchFeature> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_PATCHFEATURE_API