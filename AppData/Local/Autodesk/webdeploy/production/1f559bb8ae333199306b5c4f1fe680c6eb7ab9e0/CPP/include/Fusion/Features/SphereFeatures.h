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
#include <string>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_SPHEREFEATURES_CPP__
# define ADSK_FUSION_SPHEREFEATURES_API XI_EXPORT
# else
# define ADSK_FUSION_SPHEREFEATURES_API
# endif
#else
# define ADSK_FUSION_SPHEREFEATURES_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class SphereFeature;
}}

namespace adsk { namespace fusion {

/// Collection that provides access to all of the existing torus features in a design.
class SphereFeatures : public core::Base {
public:

    /// Function that returns the specified sphere feature using an index into the collection.
    /// index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<SphereFeature> item(size_t index) const;

    /// Function that returns the specified sphere feature using the name of the feature.
    /// name : The name of the feature within the collection to return. This is the name seen in the timeline.
    /// Returns the specified item or null if the specified name was not found.
    core::Ptr<SphereFeature> itemByName(const std::string& name) const;

    /// The number of sphere features in the collection.
    size_t count() const;

    typedef SphereFeature iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_SPHEREFEATURES_API static const char* classType();
    ADSK_FUSION_SPHEREFEATURES_API const char* objectType() const override;
    ADSK_FUSION_SPHEREFEATURES_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SPHEREFEATURES_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual SphereFeature* item_raw(size_t index) const = 0;
    virtual SphereFeature* itemByName_raw(const char * name) const = 0;
    virtual size_t count_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<SphereFeature> SphereFeatures::item(size_t index) const
{
    core::Ptr<SphereFeature> res = item_raw(index);
    return res;
}

inline core::Ptr<SphereFeature> SphereFeatures::itemByName(const std::string& name) const
{
    core::Ptr<SphereFeature> res = itemByName_raw(name.c_str());
    return res;
}

inline size_t SphereFeatures::count() const
{
    size_t res = count_raw();
    return res;
}

template <class OutputIterator> inline void SphereFeatures::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SPHEREFEATURES_API