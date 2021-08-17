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
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_SWEEPFEATUREINPUT_CPP__
# define ADSK_FUSION_SWEEPFEATUREINPUT_API XI_EXPORT
# else
# define ADSK_FUSION_SWEEPFEATUREINPUT_API
# endif
#else
# define ADSK_FUSION_SWEEPFEATUREINPUT_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BaseFeature;
    class BRepBody;
    class Occurrence;
    class Path;
}}
namespace adsk { namespace core {
    class ValueInput;
}}

namespace adsk { namespace fusion {

/// This class defines the methods and properties that pertain to the definition of a sweep
/// feature.
class SweepFeatureInput : public core::Base {
public:

    /// Gets and sets the profiles or planar faces used to define the shape of the sweep.
    /// This property can return or be set with a single Profile, a single planar face, or
    /// an ObjectCollection consisting of multiple profiles and planar faces. When an
    /// ObjectCollection is used all of the profiles and faces must be co-planar.
    core::Ptr<core::Base> profile() const;
    bool profile(const core::Ptr<core::Base>& value);

    /// Gets and sets the type of operation performed by the sweep.
    FeatureOperations operation() const;
    bool operation(FeatureOperations value);

    /// Gets and sets the path to create the sweep.
    core::Ptr<Path> path() const;
    bool path(const core::Ptr<Path>& value);

    /// Gets and sets the distance for the first side.
    /// The distance is a value from 0 to 1 indicating the position along the path where 0
    /// is at the start and 1 is at the end. The value is default to 1.0.
    core::Ptr<core::ValueInput> distanceOne() const;
    bool distanceOne(const core::Ptr<core::ValueInput>& value);

    /// Gets and sets the distance for the second side.
    /// The distance is a value from 0 to 1 indicating the position along the path where 0
    /// is at the start and 1 is at the end. The value defaults to 0 in the case where the path is closed, otherwise it defaults to 1.0.
    /// It is ignored if the path is only on one side of the profile or if the sweep definition includes a guide rail.
    /// It's always the distance against the normal of the profile if available.
    core::Ptr<core::ValueInput> distanceTwo() const;
    bool distanceTwo(const core::Ptr<core::ValueInput>& value);

    /// Gets and sets the sweep orientation. It defaults to PerpendicularOrientationType.
    /// This property is ignored when a guide rail has been specified.
    SweepOrientationTypes orientation() const;
    bool orientation(SweepOrientationTypes value);

    /// In order for geometry to be transformed correctly, an Occurrence for creation needs to be
    /// specified when the sweep is created based on geometry (e.g. a profile and/or face(s))
    /// in another component AND (the sweep) is not in the root component.
    /// The CreationOccurrence is analogous to the active occurrence in the UI
    core::Ptr<Occurrence> creationOccurrence() const;
    bool creationOccurrence(const core::Ptr<Occurrence>& value);

    /// Specifies if the sweep should be created as a solid or surface. If
    /// it's a surface then there aren't any end caps and it's open. This is
    /// initialized to true so a solid will be created if it's not changed.
    bool isSolid() const;
    bool isSolid(bool value);

    /// Gets and sets the guide rail to create the sweep. This can be set to
    /// null to remove the guide rail definition and have a single path sweep feature.
    core::Ptr<Path> guideRail() const;
    bool guideRail(const core::Ptr<Path>& value);

    /// Gets and sets if the direction of the sweep is flipped.
    /// This property only applies to sweep features that include a guide rail and whose path runs on both
    /// sides of the profile.
    bool isDirectionFlipped() const;
    bool isDirectionFlipped(bool value);

    /// Gets and sets the sweep profile scaling option. It defaults to SweepProfileScaleOption.
    /// This property is only used when a guide rail has been specified.
    SweepProfileScalingOptions profileScaling() const;
    bool profileScaling(SweepProfileScalingOptions value);

    /// When creating a feature that is owned by a base feature, set this property to the
    /// base feature you want to associate the new feature with. By default, this is null,
    /// meaning it will not be associated with a base feature.
    /// Because of a current limitation, if you want to create a feature associated with a base
    /// feature, you must set this property AND call the startEdit method of the base feature,
    /// create the feature, and then call the finishEdit method of the base feature. The base
    /// feature must be in an "edit" state to be able to add any additional items to it.
    core::Ptr<BaseFeature> targetBaseFeature() const;
    bool targetBaseFeature(const core::Ptr<BaseFeature>& value);

    /// Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection.
    /// If this property has not been set, the default behavior is that all bodies that are intersected by the
    /// feature will participate.
    /// This property can return null in the case where the feature has not been fully defined so that
    /// possible intersecting bodies can be computed.
    std::vector<core::Ptr<BRepBody>> participantBodies() const;
    bool participantBodies(const std::vector<core::Ptr<BRepBody>>& value);

    /// Gets and sets the taper angle of the sweep. This property is initialized with a taper angle of zero.
    /// A negative angle will taper the sweep inward while a positive value will taper
    /// the sweep outward. This property is valid for both parametric and non-parametric extrusions.
    core::Ptr<core::ValueInput> taperAngle() const;
    bool taperAngle(const core::Ptr<core::ValueInput>& value);

    /// Gets and sets the taper angle of the sweep. This property is initialized with a taper angle of zero.
    /// A negative angle will taper the sweep inward while a positive value will taper
    /// the sweep outward. This property is valid for both parametric and non-parametric extrusions.
    core::Ptr<core::ValueInput> twistAngle() const;
    bool twistAngle(const core::Ptr<core::ValueInput>& value);

    ADSK_FUSION_SWEEPFEATUREINPUT_API static const char* classType();
    ADSK_FUSION_SWEEPFEATUREINPUT_API const char* objectType() const override;
    ADSK_FUSION_SWEEPFEATUREINPUT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SWEEPFEATUREINPUT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::Base* profile_raw() const = 0;
    virtual bool profile_raw(core::Base* value) = 0;
    virtual FeatureOperations operation_raw() const = 0;
    virtual bool operation_raw(FeatureOperations value) = 0;
    virtual Path* path_raw() const = 0;
    virtual bool path_raw(Path* value) = 0;
    virtual core::ValueInput* distanceOne_raw() const = 0;
    virtual bool distanceOne_raw(core::ValueInput* value) = 0;
    virtual core::ValueInput* distanceTwo_raw() const = 0;
    virtual bool distanceTwo_raw(core::ValueInput* value) = 0;
    virtual SweepOrientationTypes orientation_raw() const = 0;
    virtual bool orientation_raw(SweepOrientationTypes value) = 0;
    virtual Occurrence* creationOccurrence_raw() const = 0;
    virtual bool creationOccurrence_raw(Occurrence* value) = 0;
    virtual bool isSolid_raw() const = 0;
    virtual bool isSolid_raw(bool value) = 0;
    virtual Path* guideRail_raw() const = 0;
    virtual bool guideRail_raw(Path* value) = 0;
    virtual bool isDirectionFlipped_raw() const = 0;
    virtual bool isDirectionFlipped_raw(bool value) = 0;
    virtual SweepProfileScalingOptions profileScaling_raw() const = 0;
    virtual bool profileScaling_raw(SweepProfileScalingOptions value) = 0;
    virtual BaseFeature* targetBaseFeature_raw() const = 0;
    virtual bool targetBaseFeature_raw(BaseFeature* value) = 0;
    virtual BRepBody** participantBodies_raw(size_t& return_size) const = 0;
    virtual bool participantBodies_raw(BRepBody** value, size_t value_size) = 0;
    virtual core::ValueInput* taperAngle_raw() const = 0;
    virtual bool taperAngle_raw(core::ValueInput* value) = 0;
    virtual core::ValueInput* twistAngle_raw() const = 0;
    virtual bool twistAngle_raw(core::ValueInput* value) = 0;
};

// Inline wrappers

inline core::Ptr<core::Base> SweepFeatureInput::profile() const
{
    core::Ptr<core::Base> res = profile_raw();
    return res;
}

inline bool SweepFeatureInput::profile(const core::Ptr<core::Base>& value)
{
    return profile_raw(value.get());
}

inline FeatureOperations SweepFeatureInput::operation() const
{
    FeatureOperations res = operation_raw();
    return res;
}

inline bool SweepFeatureInput::operation(FeatureOperations value)
{
    return operation_raw(value);
}

inline core::Ptr<Path> SweepFeatureInput::path() const
{
    core::Ptr<Path> res = path_raw();
    return res;
}

inline bool SweepFeatureInput::path(const core::Ptr<Path>& value)
{
    return path_raw(value.get());
}

inline core::Ptr<core::ValueInput> SweepFeatureInput::distanceOne() const
{
    core::Ptr<core::ValueInput> res = distanceOne_raw();
    return res;
}

inline bool SweepFeatureInput::distanceOne(const core::Ptr<core::ValueInput>& value)
{
    return distanceOne_raw(value.get());
}

inline core::Ptr<core::ValueInput> SweepFeatureInput::distanceTwo() const
{
    core::Ptr<core::ValueInput> res = distanceTwo_raw();
    return res;
}

inline bool SweepFeatureInput::distanceTwo(const core::Ptr<core::ValueInput>& value)
{
    return distanceTwo_raw(value.get());
}

inline SweepOrientationTypes SweepFeatureInput::orientation() const
{
    SweepOrientationTypes res = orientation_raw();
    return res;
}

inline bool SweepFeatureInput::orientation(SweepOrientationTypes value)
{
    return orientation_raw(value);
}

inline core::Ptr<Occurrence> SweepFeatureInput::creationOccurrence() const
{
    core::Ptr<Occurrence> res = creationOccurrence_raw();
    return res;
}

inline bool SweepFeatureInput::creationOccurrence(const core::Ptr<Occurrence>& value)
{
    return creationOccurrence_raw(value.get());
}

inline bool SweepFeatureInput::isSolid() const
{
    bool res = isSolid_raw();
    return res;
}

inline bool SweepFeatureInput::isSolid(bool value)
{
    return isSolid_raw(value);
}

inline core::Ptr<Path> SweepFeatureInput::guideRail() const
{
    core::Ptr<Path> res = guideRail_raw();
    return res;
}

inline bool SweepFeatureInput::guideRail(const core::Ptr<Path>& value)
{
    return guideRail_raw(value.get());
}

inline bool SweepFeatureInput::isDirectionFlipped() const
{
    bool res = isDirectionFlipped_raw();
    return res;
}

inline bool SweepFeatureInput::isDirectionFlipped(bool value)
{
    return isDirectionFlipped_raw(value);
}

inline SweepProfileScalingOptions SweepFeatureInput::profileScaling() const
{
    SweepProfileScalingOptions res = profileScaling_raw();
    return res;
}

inline bool SweepFeatureInput::profileScaling(SweepProfileScalingOptions value)
{
    return profileScaling_raw(value);
}

inline core::Ptr<BaseFeature> SweepFeatureInput::targetBaseFeature() const
{
    core::Ptr<BaseFeature> res = targetBaseFeature_raw();
    return res;
}

inline bool SweepFeatureInput::targetBaseFeature(const core::Ptr<BaseFeature>& value)
{
    return targetBaseFeature_raw(value.get());
}

inline std::vector<core::Ptr<BRepBody>> SweepFeatureInput::participantBodies() const
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

inline bool SweepFeatureInput::participantBodies(const std::vector<core::Ptr<BRepBody>>& value)
{
    BRepBody** value_ = new BRepBody*[value.size()];
    for(size_t i=0; i<value.size(); ++i)
        value_[i] = value[i].get();

    bool res = participantBodies_raw(value_, value.size());
    delete[] value_;
    return res;
}

inline core::Ptr<core::ValueInput> SweepFeatureInput::taperAngle() const
{
    core::Ptr<core::ValueInput> res = taperAngle_raw();
    return res;
}

inline bool SweepFeatureInput::taperAngle(const core::Ptr<core::ValueInput>& value)
{
    return taperAngle_raw(value.get());
}

inline core::Ptr<core::ValueInput> SweepFeatureInput::twistAngle() const
{
    core::Ptr<core::ValueInput> res = twistAngle_raw();
    return res;
}

inline bool SweepFeatureInput::twistAngle(const core::Ptr<core::ValueInput>& value)
{
    return twistAngle_raw(value.get());
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SWEEPFEATUREINPUT_API