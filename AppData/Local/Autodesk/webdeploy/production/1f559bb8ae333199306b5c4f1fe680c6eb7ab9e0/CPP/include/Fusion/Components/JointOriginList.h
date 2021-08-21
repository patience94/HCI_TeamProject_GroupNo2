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
# ifdef __COMPILING_ADSK_FUSION_JOINTORIGINLIST_CPP__
# define ADSK_FUSION_JOINTORIGINLIST_API XI_EXPORT
# else
# define ADSK_FUSION_JOINTORIGINLIST_API
# endif
#else
# define ADSK_FUSION_JOINTORIGINLIST_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class JointOrigin;
}}

namespace adsk { namespace fusion {

/// A list of joint origins.
class JointOriginList : public core::Base {
public:

    /// Function that returns the specified joint origin using an index into the list.
    /// index : The index of the item within the list to return. The first item in the list has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<JointOrigin> item(size_t index) const;

    /// Function that returns the specified joint origin using a name.
    /// name : The name of the item within the list to return.
    /// Returns the specified item or null if an invalid name was specified.
    core::Ptr<JointOrigin> itemByName(const std::string& name) const;

    /// Returns number of joint origins in the list.
    size_t count() const;

    typedef JointOrigin iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_JOINTORIGINLIST_API static const char* classType();
    ADSK_FUSION_JOINTORIGINLIST_API const char* objectType() const override;
    ADSK_FUSION_JOINTORIGINLIST_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_JOINTORIGINLIST_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual JointOrigin* item_raw(size_t index) const = 0;
    virtual JointOrigin* itemByName_raw(const char * name) const = 0;
    virtual size_t count_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<JointOrigin> JointOriginList::item(size_t index) const
{
    core::Ptr<JointOrigin> res = item_raw(index);
    return res;
}

inline core::Ptr<JointOrigin> JointOriginList::itemByName(const std::string& name) const
{
    core::Ptr<JointOrigin> res = itemByName_raw(name.c_str());
    return res;
}

inline size_t JointOriginList::count() const
{
    size_t res = count_raw();
    return res;
}

template <class OutputIterator> inline void JointOriginList::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_JOINTORIGINLIST_API