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
#include "CustomGraphicsEntity.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_CUSTOMGRAPHICSCURVE_CPP__
# define ADSK_FUSION_CUSTOMGRAPHICSCURVE_API XI_EXPORT
# else
# define ADSK_FUSION_CUSTOMGRAPHICSCURVE_API
# endif
#else
# define ADSK_FUSION_CUSTOMGRAPHICSCURVE_API XI_IMPORT
#endif

namespace adsk { namespace core {
    class Curve3D;
}}

namespace adsk { namespace fusion {

/// This represents custom graphics that are based on any object derived from Curve3D (except InfiniteLine3D).
/// This is useful when drawing curved geometry where the alternative is to stroke the smooth curve and draw
/// it as a series of lines. Using this you can directly use the curve and Fusion 360 will automatically take care
/// of creating the correct display for the current level of detail.
class CustomGraphicsCurve : public CustomGraphicsEntity {
public:

    /// Gets and sets the curve associated with this graphics entity. Any of the curve types derived from Curve3D
    /// is valid except for InfiniteLine3D.
    core::Ptr<core::Curve3D> curve() const;
    bool curve(const core::Ptr<core::Curve3D>& value);

    /// Defines the thickness of the curve in pixels.
    double weight() const;
    bool weight(double value);

    ADSK_FUSION_CUSTOMGRAPHICSCURVE_API static const char* classType();
    ADSK_FUSION_CUSTOMGRAPHICSCURVE_API const char* objectType() const override;
    ADSK_FUSION_CUSTOMGRAPHICSCURVE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_CUSTOMGRAPHICSCURVE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::Curve3D* curve_raw() const = 0;
    virtual bool curve_raw(core::Curve3D* value) = 0;
    virtual double weight_raw() const = 0;
    virtual bool weight_raw(double value) = 0;
};

// Inline wrappers

inline core::Ptr<core::Curve3D> CustomGraphicsCurve::curve() const
{
    core::Ptr<core::Curve3D> res = curve_raw();
    return res;
}

inline bool CustomGraphicsCurve::curve(const core::Ptr<core::Curve3D>& value)
{
    return curve_raw(value.get());
}

inline double CustomGraphicsCurve::weight() const
{
    double res = weight_raw();
    return res;
}

inline bool CustomGraphicsCurve::weight(double value)
{
    return weight_raw(value);
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_CUSTOMGRAPHICSCURVE_API