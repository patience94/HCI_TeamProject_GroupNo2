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

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_PATCHFEATUREINPUT_CPP__
# define ADSK_FUSION_PATCHFEATUREINPUT_API XI_EXPORT
# else
# define ADSK_FUSION_PATCHFEATUREINPUT_API
# endif
#else
# define ADSK_FUSION_PATCHFEATUREINPUT_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BaseFeature;
    class Occurrence;
}}

namespace adsk { namespace fusion {

/// This class defines the methods and properties that pertain to the definition of a patch feature.
class PatchFeatureInput : public core::Base {
public:

    /// Gets and set the input geometry that will be used to define the boundary. This can be a sketch profile,
    /// a single sketch curve, a single B-Rep edge, or a Path object.
    /// If a single sketch curve or B-Rep edge is input, that is not closed, Fusion 360 will automatically find connected sketch curves
    /// or B-Rep edges in order to define a closed loop. All sketch curves are valid as input. BRepEdges are valid if they are
    /// an "open" edge, which means they are only used by one face.
    /// If a Path is input it must define a closed shape and the B-Rep edges must be valid "open" edges.
    core::Ptr<core::Base> boundaryCurve() const;
    bool boundaryCurve(const core::Ptr<core::Base>& value);

    /// Gets and sets the type of operation performed by the patch feature. Only 'NewBodyFeatureOperation' and 'NewComponentFeatureOperation' are
    /// valid operations for patch features.
    FeatureOperations operation() const;
    bool operation(FeatureOperations value);

    /// Gets and sets type of surface continuity to use when matching boundary edges to face edges. When a new PatchFeatureInput is
    /// created, this is initialized to ConnectedSurfaceContinuityType. This value is ignored when creating a patch for sketch curves.
    SurfaceContinuityTypes continuity() const;
    bool continuity(SurfaceContinuityTypes value);

    /// When creating a feature that is owned by a base feature, set this property to the
    /// base feature you want to associate the new feature with. By default, this is null,
    /// meaning it will not be associated with a base feature.
    /// Because of a current limitation, if you want to create a feature associated with a base
    /// feature, you must set this property AND call the startEdit method of the base feature,
    /// create the feature, and then call the finishEdit method of the base feature. The base
    /// feature must be in an "edit" state to be able to add any additional items to it.
    core::Ptr<BaseFeature> targetBaseFeature() const;
    bool targetBaseFeature(const core::Ptr<BaseFeature>& value);

    /// In order for geometry to be transformed correctly, an Occurrence for creation needs to be
    /// specified when the Patch feature is created based on geometry (e.g. a profile, edges, faces)
    /// in another component AND (the Patch feature) is not in the root component.
    /// The CreationOccurrence is analogous to the active occurrence in the UI
    core::Ptr<Occurrence> creationOccurrence() const;
    bool creationOccurrence(const core::Ptr<Occurrence>& value);

    ADSK_FUSION_PATCHFEATUREINPUT_API static const char* classType();
    ADSK_FUSION_PATCHFEATUREINPUT_API const char* objectType() const override;
    ADSK_FUSION_PATCHFEATUREINPUT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_PATCHFEATUREINPUT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::Base* boundaryCurve_raw() const = 0;
    virtual bool boundaryCurve_raw(core::Base* value) = 0;
    virtual FeatureOperations operation_raw() const = 0;
    virtual bool operation_raw(FeatureOperations value) = 0;
    virtual SurfaceContinuityTypes continuity_raw() const = 0;
    virtual bool continuity_raw(SurfaceContinuityTypes value) = 0;
    virtual BaseFeature* targetBaseFeature_raw() const = 0;
    virtual bool targetBaseFeature_raw(BaseFeature* value) = 0;
    virtual Occurrence* creationOccurrence_raw() const = 0;
    virtual bool creationOccurrence_raw(Occurrence* value) = 0;
};

// Inline wrappers

inline core::Ptr<core::Base> PatchFeatureInput::boundaryCurve() const
{
    core::Ptr<core::Base> res = boundaryCurve_raw();
    return res;
}

inline bool PatchFeatureInput::boundaryCurve(const core::Ptr<core::Base>& value)
{
    return boundaryCurve_raw(value.get());
}

inline FeatureOperations PatchFeatureInput::operation() const
{
    FeatureOperations res = operation_raw();
    return res;
}

inline bool PatchFeatureInput::operation(FeatureOperations value)
{
    return operation_raw(value);
}

inline SurfaceContinuityTypes PatchFeatureInput::continuity() const
{
    SurfaceContinuityTypes res = continuity_raw();
    return res;
}

inline bool PatchFeatureInput::continuity(SurfaceContinuityTypes value)
{
    return continuity_raw(value);
}

inline core::Ptr<BaseFeature> PatchFeatureInput::targetBaseFeature() const
{
    core::Ptr<BaseFeature> res = targetBaseFeature_raw();
    return res;
}

inline bool PatchFeatureInput::targetBaseFeature(const core::Ptr<BaseFeature>& value)
{
    return targetBaseFeature_raw(value.get());
}

inline core::Ptr<Occurrence> PatchFeatureInput::creationOccurrence() const
{
    core::Ptr<Occurrence> res = creationOccurrence_raw();
    return res;
}

inline bool PatchFeatureInput::creationOccurrence(const core::Ptr<Occurrence>& value)
{
    return creationOccurrence_raw(value.get());
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_PATCHFEATUREINPUT_API