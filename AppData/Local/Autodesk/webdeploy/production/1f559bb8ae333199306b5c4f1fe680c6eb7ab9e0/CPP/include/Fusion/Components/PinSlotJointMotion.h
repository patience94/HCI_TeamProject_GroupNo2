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
#include "JointMotion.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_PINSLOTJOINTMOTION_CPP__
# define ADSK_FUSION_PINSLOTJOINTMOTION_API XI_EXPORT
# else
# define ADSK_FUSION_PINSLOTJOINTMOTION_API
# endif
#else
# define ADSK_FUSION_PINSLOTJOINTMOTION_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class JointLimits;
}}
namespace adsk { namespace core {
    class Vector3D;
}}

namespace adsk { namespace fusion {

/// Represents the set of information specific to a pin slot joint.
class PinSlotJointMotion : public JointMotion {
public:

    /// Gets and sets the direction of the axis of rotation. This can be set to
    /// XAxisJointDirection, YAxisJointDirection, or ZAxisJointDirection. It can
    /// return those three directions and CustomJointDirection. If this returns
    /// CustomJointDirection then the customRotationAxisEntity will return an entity
    /// that defines the axis. If there is a custom rotation axis defined and this
    /// property is set to one of the three standard axes, the custom rotation will
    /// be removed and customRotationAxisEntity will return null.
    JointDirections rotationAxis() const;
    bool rotationAxis(JointDirections value);

    /// Returns the direction of the rotation axis. This property will return null in the case
    /// where the PinSlotJointMotion object was obtained from a JointInput object.
    core::Ptr<core::Vector3D> rotationAxisVector() const;

    /// This property can be set using various types of entities that can infer an
    /// axis. For example, a linear edge, sketch line, planar face, and cylindrical face.
    /// This property is only valid in the case where the rotationAxis property returns
    /// CustomJointDirection. Setting this property will automatically set
    /// the rotationAxis property to CustomJointDirection.
    core::Ptr<core::Base> customRotationAxisEntity() const;
    bool customRotationAxisEntity(const core::Ptr<core::Base>& value);

    /// Gets and sets the rotation value. This is in radians. Setting this value is
    /// the equivalent of using the Drive Joints command.
    double rotationValue() const;
    bool rotationValue(double value);

    /// Returns a JointLimits object that defines the rotation limits for this joint.
    /// Use the functionality of the returned JointLimits object to get, set, and modify
    /// the joint limits.
    core::Ptr<JointLimits> rotationLimits() const;

    /// Gets and sets the direction of the slide motion in the slot. This can be set to
    /// XAxisJointDirection, YAxisJointDirection, or ZAxisJointDirection. It can
    /// return those three directions and CustomJointDirection. If this returns
    /// CustomJointDirection then the customSlideDirectionEntity will return an entity
    /// that defines the direction. If there is a custom direction defined and this
    /// property is set to one of the three standard axes, the custom direction will
    /// be removed and customSlideDirectionEntity will return null.
    JointDirections slideDirection() const;
    bool slideDirection(JointDirections value);

    /// Returns the direction of the primary slide direction. This property will return null in the case
    /// where the PinSlotJointMotion object was obtained from a JointInput object.
    core::Ptr<core::Vector3D> slideDirectionVector() const;

    /// This property can be set using various types of entities that can infer a
    /// direction. For example, a linear edge, sketch line, planar face, and cylindrical face.
    /// This property is only valid in the case where the slideDirection property returns
    /// CustomJointDirection. Setting this property will automatically set
    /// the slideDirection property to CustomJointDirection.
    core::Ptr<core::Base> customSlideDirectionEntity() const;
    bool customSlideDirectionEntity(const core::Ptr<core::Base>& value);

    /// Gets and sets the slide value. This is in centimeters. Setting this value is
    /// the equivalent of using the Drive Joints command.
    double slideValue() const;
    bool slideValue(double value);

    /// Returns a JointLimits object that defines the slide limits for this joint.
    /// Use the functionality of the returned JointLimits object to get, set, and modify
    /// the joint limits.
    core::Ptr<JointLimits> slideLimits() const;

    ADSK_FUSION_PINSLOTJOINTMOTION_API static const char* classType();
    ADSK_FUSION_PINSLOTJOINTMOTION_API const char* objectType() const override;
    ADSK_FUSION_PINSLOTJOINTMOTION_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_PINSLOTJOINTMOTION_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual JointDirections rotationAxis_raw() const = 0;
    virtual bool rotationAxis_raw(JointDirections value) = 0;
    virtual core::Vector3D* rotationAxisVector_raw() const = 0;
    virtual core::Base* customRotationAxisEntity_raw() const = 0;
    virtual bool customRotationAxisEntity_raw(core::Base* value) = 0;
    virtual double rotationValue_raw() const = 0;
    virtual bool rotationValue_raw(double value) = 0;
    virtual JointLimits* rotationLimits_raw() const = 0;
    virtual JointDirections slideDirection_raw() const = 0;
    virtual bool slideDirection_raw(JointDirections value) = 0;
    virtual core::Vector3D* slideDirectionVector_raw() const = 0;
    virtual core::Base* customSlideDirectionEntity_raw() const = 0;
    virtual bool customSlideDirectionEntity_raw(core::Base* value) = 0;
    virtual double slideValue_raw() const = 0;
    virtual bool slideValue_raw(double value) = 0;
    virtual JointLimits* slideLimits_raw() const = 0;
};

// Inline wrappers

inline JointDirections PinSlotJointMotion::rotationAxis() const
{
    JointDirections res = rotationAxis_raw();
    return res;
}

inline bool PinSlotJointMotion::rotationAxis(JointDirections value)
{
    return rotationAxis_raw(value);
}

inline core::Ptr<core::Vector3D> PinSlotJointMotion::rotationAxisVector() const
{
    core::Ptr<core::Vector3D> res = rotationAxisVector_raw();
    return res;
}

inline core::Ptr<core::Base> PinSlotJointMotion::customRotationAxisEntity() const
{
    core::Ptr<core::Base> res = customRotationAxisEntity_raw();
    return res;
}

inline bool PinSlotJointMotion::customRotationAxisEntity(const core::Ptr<core::Base>& value)
{
    return customRotationAxisEntity_raw(value.get());
}

inline double PinSlotJointMotion::rotationValue() const
{
    double res = rotationValue_raw();
    return res;
}

inline bool PinSlotJointMotion::rotationValue(double value)
{
    return rotationValue_raw(value);
}

inline core::Ptr<JointLimits> PinSlotJointMotion::rotationLimits() const
{
    core::Ptr<JointLimits> res = rotationLimits_raw();
    return res;
}

inline JointDirections PinSlotJointMotion::slideDirection() const
{
    JointDirections res = slideDirection_raw();
    return res;
}

inline bool PinSlotJointMotion::slideDirection(JointDirections value)
{
    return slideDirection_raw(value);
}

inline core::Ptr<core::Vector3D> PinSlotJointMotion::slideDirectionVector() const
{
    core::Ptr<core::Vector3D> res = slideDirectionVector_raw();
    return res;
}

inline core::Ptr<core::Base> PinSlotJointMotion::customSlideDirectionEntity() const
{
    core::Ptr<core::Base> res = customSlideDirectionEntity_raw();
    return res;
}

inline bool PinSlotJointMotion::customSlideDirectionEntity(const core::Ptr<core::Base>& value)
{
    return customSlideDirectionEntity_raw(value.get());
}

inline double PinSlotJointMotion::slideValue() const
{
    double res = slideValue_raw();
    return res;
}

inline bool PinSlotJointMotion::slideValue(double value)
{
    return slideValue_raw(value);
}

inline core::Ptr<JointLimits> PinSlotJointMotion::slideLimits() const
{
    core::Ptr<JointLimits> res = slideLimits_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_PINSLOTJOINTMOTION_API