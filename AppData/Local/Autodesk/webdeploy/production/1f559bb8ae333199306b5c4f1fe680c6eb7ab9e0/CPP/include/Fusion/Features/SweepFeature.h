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
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_SWEEPFEATURE_CPP__
# define ADSK_FUSION_SWEEPFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_SWEEPFEATURE_API
# endif
#else
# define ADSK_FUSION_SWEEPFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BRepBody;
    class BRepFaces;
    class ModelParameter;
    class Occurrence;
    class Path;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing sweep feature in a design.
class SweepFeature : public Feature {
public:

    /// Gets and sets the profiles or planar faces used to define the shape of the sweep.
    /// This property can return or be set with a single Profile, a single planar face, or
    /// an ObjectCollection consisting of multiple profiles and planar faces. When an
    /// ObjectCollection is used all of the profiles and faces must be co-planar.
    /// This property returns nothing in the case where the feature is non-parametric.
    core::Ptr<core::Base> profile() const;
    bool profile(const core::Ptr<core::Base>& value);

    /// Gets and sets the type of operation performed by the sweep.
    FeatureOperations operation() const;
    bool operation(FeatureOperations value);

    /// Gets and sets the path to create the sweep.
    /// This property returns nothing in the case where the feature is non-parametric.
    core::Ptr<Path> path() const;
    bool path(const core::Ptr<Path>& value);

    /// Gets the distance for the first side.
    /// This property returns nothing in the case where the feature is non-parametric.
    core::Ptr<ModelParameter> distanceOne() const;

    /// Gets the distance for the second side.
    /// Returns nothing if the path is only on one side of the profile or if the sweep definition includes a guide rail.
    /// It's always the distance against the normal of the profile if available.
    /// This property returns nothing in the case where the feature is non-parametric.
    core::Ptr<ModelParameter> distanceTwo() const;

    /// Gets and sets the sweep orientation. It defaults to PerpendicularOrientationType.
    SweepOrientationTypes orientation() const;
    bool orientation(SweepOrientationTypes value);

    /// Property that returns the set of that cap one end of the sweep that are coincident with the sketch plane.
    /// In the cases where there aren't any start faces this property will return Nothing.
    core::Ptr<BRepFaces> startFaces() const;

    /// Property that returns the set of that cap one end of the sweep that are coincident with the sketch plane.
    /// The end faces are those not coincident to the sketch plane of the feature's profile.
    /// In the case of a symmetric revolution these faces are the ones on the negative normal side of the sketch plane.
    /// In the cases where there aren't any end faces this property will return Nothing.
    core::Ptr<BRepFaces> endFaces() const;

    /// Property that returns a object that provides access to all of the faces created around the perimeter of the feature.
    core::Ptr<BRepFaces> sideFaces() const;

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<SweepFeature> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<SweepFeature> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    /// Indicates if this feature was initially created as a solid or a surface.
    bool isSolid() const;

    /// Gets and sets the guide rail to create the sweep. This can be set to null
    /// to have a path only sweep.
    core::Ptr<Path> guideRail() const;
    bool guideRail(const core::Ptr<Path>& value);

    /// Gets and sets if the direction of the sweep is flipped.
    /// This property only applies to sweep features that include a guide rail and whose path runs on both
    /// sides of the profile.
    bool isDirectionFlipped() const;
    bool isDirectionFlipped(bool value);

    /// Gets and sets the sweep profile scaling option. It defaults to SweepProfileScaleOption. This
    /// property is only used when a guide rail has been specified.
    SweepProfileScalingOptions profileScaling() const;
    bool profileScaling(SweepProfileScalingOptions value);

    /// Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection.
    /// When setting or getting this property, you must roll the timeline back to just before the feature
    /// so that the model is in the state just before the feature is computed.
    std::vector<core::Ptr<BRepBody>> participantBodies() const;
    bool participantBodies(const std::vector<core::Ptr<BRepBody>>& value);

    /// Gets the ModelParameter that defines the taper angle of the sweep feature.
    /// The value of the angle can be edited by using the properties on the ModelParameter object to edit the parameter.
    core::Ptr<ModelParameter> taperAngle() const;

    /// Gets the ModelParameter that defines the twist angle of the sweep feature.
    /// The value of the angle can be edited by using the properties on the ModelParameter object to edit the parameter.
    core::Ptr<ModelParameter> twistAngle() const;

    ADSK_FUSION_SWEEPFEATURE_API static const char* classType();
    ADSK_FUSION_SWEEPFEATURE_API const char* objectType() const override;
    ADSK_FUSION_SWEEPFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SWEEPFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::Base* profile_raw() const = 0;
    virtual bool profile_raw(core::Base* value) = 0;
    virtual FeatureOperations operation_raw() const = 0;
    virtual bool operation_raw(FeatureOperations value) = 0;
    virtual Path* path_raw() const = 0;
    virtual bool path_raw(Path* value) = 0;
    virtual ModelParameter* distanceOne_raw() const = 0;
    virtual ModelParameter* distanceTwo_raw() const = 0;
    virtual SweepOrientationTypes orientation_raw() const = 0;
    virtual bool orientation_raw(SweepOrientationTypes value) = 0;
    virtual BRepFaces* startFaces_raw() const = 0;
    virtual BRepFaces* endFaces_raw() const = 0;
    virtual BRepFaces* sideFaces_raw() const = 0;
    virtual SweepFeature* nativeObject_raw() const = 0;
    virtual SweepFeature* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
    virtual bool isSolid_raw() const = 0;
    virtual Path* guideRail_raw() const = 0;
    virtual bool guideRail_raw(Path* value) = 0;
    virtual bool isDirectionFlipped_raw() const = 0;
    virtual bool isDirectionFlipped_raw(bool value) = 0;
    virtual SweepProfileScalingOptions profileScaling_raw() const = 0;
    virtual bool profileScaling_raw(SweepProfileScalingOptions value) = 0;
    virtual BRepBody** participantBodies_raw(size_t& return_size) const = 0;
    virtual bool participantBodies_raw(BRepBody** value, size_t value_size) = 0;
    virtual ModelParameter* taperAngle_raw() const = 0;
    virtual ModelParameter* twistAngle_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<core::Base> SweepFeature::profile() const
{
    core::Ptr<core::Base> res = profile_raw();
    return res;
}

inline bool SweepFeature::profile(const core::Ptr<core::Base>& value)
{
    return profile_raw(value.get());
}

inline FeatureOperations SweepFeature::operation() const
{
    FeatureOperations res = operation_raw();
    return res;
}

inline bool SweepFeature::operation(FeatureOperations value)
{
    return operation_raw(value);
}

inline core::Ptr<Path> SweepFeature::path() const
{
    core::Ptr<Path> res = path_raw();
    return res;
}

inline bool SweepFeature::path(const core::Ptr<Path>& value)
{
    return path_raw(value.get());
}

inline core::Ptr<ModelParameter> SweepFeature::distanceOne() const
{
    core::Ptr<ModelParameter> res = distanceOne_raw();
    return res;
}

inline core::Ptr<ModelParameter> SweepFeature::distanceTwo() const
{
    core::Ptr<ModelParameter> res = distanceTwo_raw();
    return res;
}

inline SweepOrientationTypes SweepFeature::orientation() const
{
    SweepOrientationTypes res = orientation_raw();
    return res;
}

inline bool SweepFeature::orientation(SweepOrientationTypes value)
{
    return orientation_raw(value);
}

inline core::Ptr<BRepFaces> SweepFeature::startFaces() const
{
    core::Ptr<BRepFaces> res = startFaces_raw();
    return res;
}

inline core::Ptr<BRepFaces> SweepFeature::endFaces() const
{
    core::Ptr<BRepFaces> res = endFaces_raw();
    return res;
}

inline core::Ptr<BRepFaces> SweepFeature::sideFaces() const
{
    core::Ptr<BRepFaces> res = sideFaces_raw();
    return res;
}

inline core::Ptr<SweepFeature> SweepFeature::nativeObject() const
{
    core::Ptr<SweepFeature> res = nativeObject_raw();
    return res;
}

inline core::Ptr<SweepFeature> SweepFeature::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<SweepFeature> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}

inline bool SweepFeature::isSolid() const
{
    bool res = isSolid_raw();
    return res;
}

inline core::Ptr<Path> SweepFeature::guideRail() const
{
    core::Ptr<Path> res = guideRail_raw();
    return res;
}

inline bool SweepFeature::guideRail(const core::Ptr<Path>& value)
{
    return guideRail_raw(value.get());
}

inline bool SweepFeature::isDirectionFlipped() const
{
    bool res = isDirectionFlipped_raw();
    return res;
}

inline bool SweepFeature::isDirectionFlipped(bool value)
{
    return isDirectionFlipped_raw(value);
}

inline SweepProfileScalingOptions SweepFeature::profileScaling() const
{
    SweepProfileScalingOptions res = profileScaling_raw();
    return res;
}

inline bool SweepFeature::profileScaling(SweepProfileScalingOptions value)
{
    return profileScaling_raw(value);
}

inline std::vector<core::Ptr<BRepBody>> SweepFeature::participantBodies() const
{
    std::vector<core::Ptr<BRepBody>> res;
    size_t s;

    BRepBody** p= participantBodies_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline bool SweepFeature::participantBodies(const std::vector<core::Ptr<BRepBody>>& value)
{
    BRepBody** value_ = new BRepBody*[value.size()];
    for(size_t i=0; i<value.size(); ++i)
        value_[i] = value[i].get();

    bool res = participantBodies_raw(value_, value.size());
    delete[] value_;
    return res;
}

inline core::Ptr<ModelParameter> SweepFeature::taperAngle() const
{
    core::Ptr<ModelParameter> res = taperAngle_raw();
    return res;
}

inline core::Ptr<ModelParameter> SweepFeature::twistAngle() const
{
    core::Ptr<ModelParameter> res = twistAngle_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SWEEPFEATURE_API