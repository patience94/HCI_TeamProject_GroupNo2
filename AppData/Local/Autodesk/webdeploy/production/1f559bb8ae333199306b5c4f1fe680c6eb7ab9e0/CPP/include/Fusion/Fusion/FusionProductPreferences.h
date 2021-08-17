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
#include "../../Core/Application/ProductPreferences.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_FUSIONPRODUCTPREFERENCES_CPP__
# define ADSK_FUSION_FUSIONPRODUCTPREFERENCES_API XI_EXPORT
# else
# define ADSK_FUSION_FUSIONPRODUCTPREFERENCES_API
# endif
#else
# define ADSK_FUSION_FUSIONPRODUCTPREFERENCES_API XI_IMPORT
#endif

namespace adsk { namespace fusion {

/// Fusion 360 General Design Preferences
class FusionProductPreferences : public core::ProductPreferences {
public:

    /// Gets and sets the Active Component Visibility option
    bool isActiveComponentVisibilityUsed() const;
    bool isActiveComponentVisibilityUsed(bool value);

    /// Gets and sets the Design History (default design type) setting
    DefaultDesignTypeOptions defaultDesignType() const;
    bool defaultDesignType(DefaultDesignTypeOptions value);

    /// Gets and sets the Default workspace setting. (Model, Sculpt or Patch)
    DefaultWorkspaces defaultWorkspace() const;
    bool defaultWorkspace(DefaultWorkspaces value);

    /// Gets and sets the Animate joint preview option
    bool isJointPreviewAnimated() const;
    bool isJointPreviewAnimated(bool value);

    /// Gets and sets the Allow 3D sketching of lines and splines option
    /// which controls if 3D sketching is allowed or if sketching is forced to
    /// be on the x-y plane of the sketch.
    bool is3DSketchingAllowed() const;
    bool is3DSketchingAllowed(bool value);

    /// Gets and sets the Show ghosted result body option
    bool isGhostedResultBodyShown() const;
    bool isGhostedResultBodyShown(bool value);

    /// Gets and sets if dimension value is edited when the dimension is created.
    bool isDimensionEditedWhenCreated() const;
    bool isDimensionEditedWhenCreated(bool value);

    /// Gets and sets if the view is re-oriented to view the newly created sketch.
    bool isAutoLookAtSketch() const;
    bool isAutoLookAtSketch(bool value);

    /// Gets and Sets if geometry, not in the active sketch plane, is to be automatically projected.
    bool isAutoProjectGeometry() const;
    bool isAutoProjectGeometry(bool value);

    ADSK_FUSION_FUSIONPRODUCTPREFERENCES_API static const char* classType();
    ADSK_FUSION_FUSIONPRODUCTPREFERENCES_API const char* objectType() const override;
    ADSK_FUSION_FUSIONPRODUCTPREFERENCES_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_FUSIONPRODUCTPREFERENCES_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual bool isActiveComponentVisibilityUsed_raw() const = 0;
    virtual bool isActiveComponentVisibilityUsed_raw(bool value) = 0;
    virtual DefaultDesignTypeOptions defaultDesignType_raw() const = 0;
    virtual bool defaultDesignType_raw(DefaultDesignTypeOptions value) = 0;
    virtual DefaultWorkspaces defaultWorkspace_raw() const = 0;
    virtual bool defaultWorkspace_raw(DefaultWorkspaces value) = 0;
    virtual bool isJointPreviewAnimated_raw() const = 0;
    virtual bool isJointPreviewAnimated_raw(bool value) = 0;
    virtual bool is3DSketchingAllowed_raw() const = 0;
    virtual bool is3DSketchingAllowed_raw(bool value) = 0;
    virtual bool isGhostedResultBodyShown_raw() const = 0;
    virtual bool isGhostedResultBodyShown_raw(bool value) = 0;
    virtual bool isDimensionEditedWhenCreated_raw() const = 0;
    virtual bool isDimensionEditedWhenCreated_raw(bool value) = 0;
    virtual bool isAutoLookAtSketch_raw() const = 0;
    virtual bool isAutoLookAtSketch_raw(bool value) = 0;
    virtual bool isAutoProjectGeometry_raw() const = 0;
    virtual bool isAutoProjectGeometry_raw(bool value) = 0;
};

// Inline wrappers

inline bool FusionProductPreferences::isActiveComponentVisibilityUsed() const
{
    bool res = isActiveComponentVisibilityUsed_raw();
    return res;
}

inline bool FusionProductPreferences::isActiveComponentVisibilityUsed(bool value)
{
    return isActiveComponentVisibilityUsed_raw(value);
}

inline DefaultDesignTypeOptions FusionProductPreferences::defaultDesignType() const
{
    DefaultDesignTypeOptions res = defaultDesignType_raw();
    return res;
}

inline bool FusionProductPreferences::defaultDesignType(DefaultDesignTypeOptions value)
{
    return defaultDesignType_raw(value);
}

inline DefaultWorkspaces FusionProductPreferences::defaultWorkspace() const
{
    DefaultWorkspaces res = defaultWorkspace_raw();
    return res;
}

inline bool FusionProductPreferences::defaultWorkspace(DefaultWorkspaces value)
{
    return defaultWorkspace_raw(value);
}

inline bool FusionProductPreferences::isJointPreviewAnimated() const
{
    bool res = isJointPreviewAnimated_raw();
    return res;
}

inline bool FusionProductPreferences::isJointPreviewAnimated(bool value)
{
    return isJointPreviewAnimated_raw(value);
}

inline bool FusionProductPreferences::is3DSketchingAllowed() const
{
    bool res = is3DSketchingAllowed_raw();
    return res;
}

inline bool FusionProductPreferences::is3DSketchingAllowed(bool value)
{
    return is3DSketchingAllowed_raw(value);
}

inline bool FusionProductPreferences::isGhostedResultBodyShown() const
{
    bool res = isGhostedResultBodyShown_raw();
    return res;
}

inline bool FusionProductPreferences::isGhostedResultBodyShown(bool value)
{
    return isGhostedResultBodyShown_raw(value);
}

inline bool FusionProductPreferences::isDimensionEditedWhenCreated() const
{
    bool res = isDimensionEditedWhenCreated_raw();
    return res;
}

inline bool FusionProductPreferences::isDimensionEditedWhenCreated(bool value)
{
    return isDimensionEditedWhenCreated_raw(value);
}

inline bool FusionProductPreferences::isAutoLookAtSketch() const
{
    bool res = isAutoLookAtSketch_raw();
    return res;
}

inline bool FusionProductPreferences::isAutoLookAtSketch(bool value)
{
    return isAutoLookAtSketch_raw(value);
}

inline bool FusionProductPreferences::isAutoProjectGeometry() const
{
    bool res = isAutoProjectGeometry_raw();
    return res;
}

inline bool FusionProductPreferences::isAutoProjectGeometry(bool value)
{
    return isAutoProjectGeometry_raw(value);
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_FUSIONPRODUCTPREFERENCES_API