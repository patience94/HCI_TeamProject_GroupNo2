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
# ifdef __COMPILING_ADSK_FUSION_FEATURELIST_CPP__
# define ADSK_FUSION_FEATURELIST_API XI_EXPORT
# else
# define ADSK_FUSION_FEATURELIST_API
# endif
#else
# define ADSK_FUSION_FEATURELIST_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Feature;
}}

namespace adsk { namespace fusion {

/// Provides access to a list of features. This is used in the API to return
/// a list of features from an API call.
class FeatureList : public core::Base {
public:

    /// Returns the specified folder.
    /// index : The index of the feature to return. The first feature in the list has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<Feature> item(size_t index) const;

    /// The number of features in this collection.
    size_t count() const;

    typedef Feature iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_FEATURELIST_API static const char* classType();
    ADSK_FUSION_FEATURELIST_API const char* objectType() const override;
    ADSK_FUSION_FEATURELIST_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_FEATURELIST_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual Feature* item_raw(size_t index) const = 0;
    virtual size_t count_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<Feature> FeatureList::item(size_t index) const
{
    core::Ptr<Feature> res = item_raw(index);
    return res;
}

inline size_t FeatureList::count() const
{
    size_t res = count_raw();
    return res;
}

template <class OutputIterator> inline void FeatureList::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_FEATURELIST_API