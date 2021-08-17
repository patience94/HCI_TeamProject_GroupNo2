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
#include "ChamferTypeDefinition.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_TWODISTANCESCHAMFERTYPEDEFINITION_CPP__
# define ADSK_FUSION_TWODISTANCESCHAMFERTYPEDEFINITION_API XI_EXPORT
# else
# define ADSK_FUSION_TWODISTANCESCHAMFERTYPEDEFINITION_API
# endif
#else
# define ADSK_FUSION_TWODISTANCESCHAMFERTYPEDEFINITION_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class ModelParameter;
}}

namespace adsk { namespace fusion {

/// Provides information to create a chamfer that is defined by a two distances from the edge.
class TwoDistancesChamferTypeDefinition : public ChamferTypeDefinition {
public:

    /// Returns the parameter controlling the first distance. You can edit the distance
    /// by editing the value of the parameter object.
    core::Ptr<ModelParameter> distanceOne() const;

    /// Returns the parameter controlling the second distance. You can edit the distance
    /// by editing the value of the parameter object.
    core::Ptr<ModelParameter> distanceTwo() const;

    ADSK_FUSION_TWODISTANCESCHAMFERTYPEDEFINITION_API static const char* classType();
    ADSK_FUSION_TWODISTANCESCHAMFERTYPEDEFINITION_API const char* objectType() const override;
    ADSK_FUSION_TWODISTANCESCHAMFERTYPEDEFINITION_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_TWODISTANCESCHAMFERTYPEDEFINITION_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual ModelParameter* distanceOne_raw() const = 0;
    virtual ModelParameter* distanceTwo_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<ModelParameter> TwoDistancesChamferTypeDefinition::distanceOne() const
{
    core::Ptr<ModelParameter> res = distanceOne_raw();
    return res;
}

inline core::Ptr<ModelParameter> TwoDistancesChamferTypeDefinition::distanceTwo() const
{
    core::Ptr<ModelParameter> res = distanceTwo_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_TWODISTANCESCHAMFERTYPEDEFINITION_API