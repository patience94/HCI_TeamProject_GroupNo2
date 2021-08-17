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
#include "LoftEndCondition.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_LOFTPOINTTANGENTENDCONDITION_CPP__
# define ADSK_FUSION_LOFTPOINTTANGENTENDCONDITION_API XI_EXPORT
# else
# define ADSK_FUSION_LOFTPOINTTANGENTENDCONDITION_API
# endif
#else
# define ADSK_FUSION_LOFTPOINTTANGENTENDCONDITION_API XI_IMPORT
#endif

namespace adsk { namespace fusion {

/// Represents a "Point Tangent" loft end condition.
class LoftPointTangentEndCondition : public LoftEndCondition {
public:

    /// Gets the valueInput or Parameter that defines the weight of the loft.
    /// If this object was obtained from a LoftFeatureInput object then this will return a
    /// valueInput object with the initial value provided. If this object was obtained from
    /// an exiting LoftFeature then it returns a Parameter. In the case of a parameter, to change the weight,
    /// edit the value of the associated parameter.
    core::Ptr<core::Base> weight() const;

    ADSK_FUSION_LOFTPOINTTANGENTENDCONDITION_API static const char* classType();
    ADSK_FUSION_LOFTPOINTTANGENTENDCONDITION_API const char* objectType() const override;
    ADSK_FUSION_LOFTPOINTTANGENTENDCONDITION_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_LOFTPOINTTANGENTENDCONDITION_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::Base* weight_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<core::Base> LoftPointTangentEndCondition::weight() const
{
    core::Ptr<core::Base> res = weight_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_LOFTPOINTTANGENTENDCONDITION_API