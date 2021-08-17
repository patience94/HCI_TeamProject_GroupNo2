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
# ifdef __COMPILING_ADSK_FUSION_SPLITBODYFEATUREINPUT_CPP__
# define ADSK_FUSION_SPLITBODYFEATUREINPUT_API XI_EXPORT
# else
# define ADSK_FUSION_SPLITBODYFEATUREINPUT_API
# endif
#else
# define ADSK_FUSION_SPLITBODYFEATUREINPUT_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BaseFeature;
}}

namespace adsk { namespace fusion {

/// This class defines the methods and properties that pertain to the definition of a split body feature.
class SplitBodyFeatureInput : public core::Base {
public:

    /// Gets and sets the input solid or open bodies to be split. This can be a
    /// single BRepBody or an ObjectCollection if multiple bodies are to be split.
    core::Ptr<core::Base> splitBodies() const;
    bool splitBodies(const core::Ptr<core::Base>& value);

    /// Gets and sets the entity that defines the splitting tool. The splitting tool is a single
    /// entity that can be either a solid or open BRepBody, construction plane, profile, or a face.
    core::Ptr<core::Base> splittingTool() const;
    bool splittingTool(const core::Ptr<core::Base>& value);

    /// Gets and sets whether or not the splitting tool is to be automatically extended (if possible) so as to
    /// completely intersect the bodyToSplit.
    bool isSplittingToolExtended() const;
    bool isSplittingToolExtended(bool value);

    /// When creating a feature that is owned by a base feature, set this property to the
    /// base feature you want to associate the new feature with. By default, this is null,
    /// meaning it will not be associated with a base feature.
    /// Because of a current limitation, if you want to create a feature associated with a base
    /// feature, you must set this property AND call the startEdit method of the base feature,
    /// create the feature, and then call the finishEdit method of the base feature. The base
    /// feature must be in an "edit" state to be able to add any additional items to it.
    core::Ptr<BaseFeature> targetBaseFeature() const;
    bool targetBaseFeature(const core::Ptr<BaseFeature>& value);

    ADSK_FUSION_SPLITBODYFEATUREINPUT_API static const char* classType();
    ADSK_FUSION_SPLITBODYFEATUREINPUT_API const char* objectType() const override;
    ADSK_FUSION_SPLITBODYFEATUREINPUT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SPLITBODYFEATUREINPUT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::Base* splitBodies_raw() const = 0;
    virtual bool splitBodies_raw(core::Base* value) = 0;
    virtual core::Base* splittingTool_raw() const = 0;
    virtual bool splittingTool_raw(core::Base* value) = 0;
    virtual bool isSplittingToolExtended_raw() const = 0;
    virtual bool isSplittingToolExtended_raw(bool value) = 0;
    virtual BaseFeature* targetBaseFeature_raw() const = 0;
    virtual bool targetBaseFeature_raw(BaseFeature* value) = 0;
};

// Inline wrappers

inline core::Ptr<core::Base> SplitBodyFeatureInput::splitBodies() const
{
    core::Ptr<core::Base> res = splitBodies_raw();
    return res;
}

inline bool SplitBodyFeatureInput::splitBodies(const core::Ptr<core::Base>& value)
{
    return splitBodies_raw(value.get());
}

inline core::Ptr<core::Base> SplitBodyFeatureInput::splittingTool() const
{
    core::Ptr<core::Base> res = splittingTool_raw();
    return res;
}

inline bool SplitBodyFeatureInput::splittingTool(const core::Ptr<core::Base>& value)
{
    return splittingTool_raw(value.get());
}

inline bool SplitBodyFeatureInput::isSplittingToolExtended() const
{
    bool res = isSplittingToolExtended_raw();
    return res;
}

inline bool SplitBodyFeatureInput::isSplittingToolExtended(bool value)
{
    return isSplittingToolExtended_raw(value);
}

inline core::Ptr<BaseFeature> SplitBodyFeatureInput::targetBaseFeature() const
{
    core::Ptr<BaseFeature> res = targetBaseFeature_raw();
    return res;
}

inline bool SplitBodyFeatureInput::targetBaseFeature(const core::Ptr<BaseFeature>& value)
{
    return targetBaseFeature_raw(value.get());
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SPLITBODYFEATUREINPUT_API