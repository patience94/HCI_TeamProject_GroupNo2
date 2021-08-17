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
#include "GeometricConstraint.h"
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_POLYGONCONSTRAINT_CPP__
# define ADSK_FUSION_POLYGONCONSTRAINT_API XI_EXPORT
# else
# define ADSK_FUSION_POLYGONCONSTRAINT_API
# endif
#else
# define ADSK_FUSION_POLYGONCONSTRAINT_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class SketchLine;
}}

namespace adsk { namespace fusion {

/// A polygon constraint in a sketch.
class PolygonConstraint : public GeometricConstraint {
public:

    /// Returns the sketch lines that represent the polygon.
    std::vector<core::Ptr<SketchLine>> lines() const;

    ADSK_FUSION_POLYGONCONSTRAINT_API static const char* classType();
    ADSK_FUSION_POLYGONCONSTRAINT_API const char* objectType() const override;
    ADSK_FUSION_POLYGONCONSTRAINT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_POLYGONCONSTRAINT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual SketchLine** lines_raw(size_t& return_size) const = 0;
};

// Inline wrappers

inline std::vector<core::Ptr<SketchLine>> PolygonConstraint::lines() const
{
    std::vector<core::Ptr<SketchLine>> res;
    size_t s;

    SketchLine** p= lines_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_POLYGONCONSTRAINT_API