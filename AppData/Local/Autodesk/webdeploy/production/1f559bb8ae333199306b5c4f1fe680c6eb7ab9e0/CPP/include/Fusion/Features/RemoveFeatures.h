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
# ifdef __COMPILING_ADSK_FUSION_REMOVEFEATURES_CPP__
# define ADSK_FUSION_REMOVEFEATURES_API XI_EXPORT
# else
# define ADSK_FUSION_REMOVEFEATURES_API
# endif
#else
# define ADSK_FUSION_REMOVEFEATURES_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class RemoveFeature;
}}

namespace adsk { namespace fusion {

/// Collection that provides access to all of the existing Remove features in a component
/// and supports the ability to create new Remove features.
class RemoveFeatures : public core::Base {
public:

    /// Function that returns the specified Remove feature using an index into the collection.
    /// index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<RemoveFeature> item(size_t index) const;

    /// Function that returns the specified remove feature using the name of the feature.
    /// name : The name of the feature within the collection to return. This is the name seen in the timeline.
    /// Returns the specified item or null if the specified name was not found.
    core::Ptr<RemoveFeature> itemByName(const std::string& name) const;

    /// The number of Remove features in the collection.
    size_t count() const;

    /// Creates a new Remove feature.
    /// itemToRemove : A single body (solid or surface) or component occurrence to remove.
    /// Returns the newly created RemoveFeature object or null if the creation failed.
    core::Ptr<RemoveFeature> add(const core::Ptr<core::Base>& itemToRemove);

    typedef RemoveFeature iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_REMOVEFEATURES_API static const char* classType();
    ADSK_FUSION_REMOVEFEATURES_API const char* objectType() const override;
    ADSK_FUSION_REMOVEFEATURES_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_REMOVEFEATURES_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual RemoveFeature* item_raw(size_t index) const = 0;
    virtual RemoveFeature* itemByName_raw(const char * name) const = 0;
    virtual size_t count_raw() const = 0;
    virtual RemoveFeature* add_raw(core::Base* itemToRemove) = 0;
};

// Inline wrappers

inline core::Ptr<RemoveFeature> RemoveFeatures::item(size_t index) const
{
    core::Ptr<RemoveFeature> res = item_raw(index);
    return res;
}

inline core::Ptr<RemoveFeature> RemoveFeatures::itemByName(const std::string& name) const
{
    core::Ptr<RemoveFeature> res = itemByName_raw(name.c_str());
    return res;
}

inline size_t RemoveFeatures::count() const
{
    size_t res = count_raw();
    return res;
}

inline core::Ptr<RemoveFeature> RemoveFeatures::add(const core::Ptr<core::Base>& itemToRemove)
{
    core::Ptr<RemoveFeature> res = add_raw(itemToRemove.get());
    return res;
}

template <class OutputIterator> inline void RemoveFeatures::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_REMOVEFEATURES_API