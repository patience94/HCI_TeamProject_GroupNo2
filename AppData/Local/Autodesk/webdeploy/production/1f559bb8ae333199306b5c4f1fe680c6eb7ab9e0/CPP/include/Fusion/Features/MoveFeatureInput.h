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
# ifdef __COMPILING_ADSK_FUSION_MOVEFEATUREINPUT_CPP__
# define ADSK_FUSION_MOVEFEATUREINPUT_API XI_EXPORT
# else
# define ADSK_FUSION_MOVEFEATUREINPUT_API
# endif
#else
# define ADSK_FUSION_MOVEFEATUREINPUT_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BaseFeature;
}}
namespace adsk { namespace core {
    class Matrix3D;
    class ObjectCollection;
}}

namespace adsk { namespace fusion {

/// This class defines the methods and properties that pertain to the definition of a move feature.
class MoveFeatureInput : public core::Base {
public:

    /// Gets and sets the entities to move.
    /// This collection can only contain BRepBody objects in parametric modeling.
    /// It can be BRep bodies, T-Spline bodies and mesh bodies mixed or faces and features mixed in non-parametric modeling.
    core::Ptr<core::ObjectCollection> inputEntities() const;
    bool inputEntities(const core::Ptr<core::ObjectCollection>& value);

    /// Gets and sets the tranform to apply to the input entities. This can describe a move (translation)
    /// or a rotation. The matrix must define an orthogonal transform. That is the axes remain
    /// perpendicular to each other and there isn't any scale or mirror defined.
    core::Ptr<core::Matrix3D> transform() const;
    bool transform(const core::Ptr<core::Matrix3D>& value);

    /// When creating a feature that is owned by a base feature, set this property to the
    /// base feature you want to associate the new feature with. By default, this is null,
    /// meaning it will not be associated with a base feature.
    /// Because of a current limitation, if you want to create a feature associated with a base
    /// feature, you must set this property AND call the startEdit method of the base feature,
    /// create the feature, and then call the finishEdit method of the base feature. The base
    /// feature must be in an "edit" state to be able to add any additional items to it.
    core::Ptr<BaseFeature> targetBaseFeature() const;
    bool targetBaseFeature(const core::Ptr<BaseFeature>& value);

    ADSK_FUSION_MOVEFEATUREINPUT_API static const char* classType();
    ADSK_FUSION_MOVEFEATUREINPUT_API const char* objectType() const override;
    ADSK_FUSION_MOVEFEATUREINPUT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_MOVEFEATUREINPUT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::ObjectCollection* inputEntities_raw() const = 0;
    virtual bool inputEntities_raw(core::ObjectCollection* value) = 0;
    virtual core::Matrix3D* transform_raw() const = 0;
    virtual bool transform_raw(core::Matrix3D* value) = 0;
    virtual BaseFeature* targetBaseFeature_raw() const = 0;
    virtual bool targetBaseFeature_raw(BaseFeature* value) = 0;
};

// Inline wrappers

inline core::Ptr<core::ObjectCollection> MoveFeatureInput::inputEntities() const
{
    core::Ptr<core::ObjectCollection> res = inputEntities_raw();
    return res;
}

inline bool MoveFeatureInput::inputEntities(const core::Ptr<core::ObjectCollection>& value)
{
    return inputEntities_raw(value.get());
}

inline core::Ptr<core::Matrix3D> MoveFeatureInput::transform() const
{
    core::Ptr<core::Matrix3D> res = transform_raw();
    return res;
}

inline bool MoveFeatureInput::transform(const core::Ptr<core::Matrix3D>& value)
{
    return transform_raw(value.get());
}

inline core::Ptr<BaseFeature> MoveFeatureInput::targetBaseFeature() const
{
    core::Ptr<BaseFeature> res = targetBaseFeature_raw();
    return res;
}

inline bool MoveFeatureInput::targetBaseFeature(const core::Ptr<BaseFeature>& value)
{
    return targetBaseFeature_raw(value.get());
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_MOVEFEATUREINPUT_API