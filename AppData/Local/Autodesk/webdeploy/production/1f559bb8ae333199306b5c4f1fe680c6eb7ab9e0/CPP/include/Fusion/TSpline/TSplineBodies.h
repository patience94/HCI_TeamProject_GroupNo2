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
# ifdef __COMPILING_ADSK_FUSION_TSPLINEBODIES_CPP__
# define ADSK_FUSION_TSPLINEBODIES_API XI_EXPORT
# else
# define ADSK_FUSION_TSPLINEBODIES_API
# endif
#else
# define ADSK_FUSION_TSPLINEBODIES_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class TSplineBody;
}}

namespace adsk { namespace fusion {

/// A collection of TSpline bodies.
class TSplineBodies : public core::Base {
public:

    /// Function that returns the specified T-Spline body using an index into the collection.
    /// index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<TSplineBody> item(size_t index) const;

    /// The number of bodies in the collection.
    size_t count() const;

    /// Returns a TSplineBody by specifying the name of the body as seen in the browser.
    /// name : The name of the body, as seen in the browser. This is case sensitive.
    /// Returns the specified item or null if a body with that name was not found.
    core::Ptr<TSplineBody> itemByName(const std::string& name) const;

    /// Creates a new TSplineBody by reading in a TSM file from disk.
    /// tsmFilename : The full filename of the TSM file on disk.
    /// Returns the newly created TSplineBody if successful or null in the case of failure.
    core::Ptr<TSplineBody> addByTSMFile(const std::string& tsmFilename);

    /// Creates a new TSplineBody using the T-Spline description provided by the input
    /// string which contains TSM formatted text.
    /// tsmDescription : A string that contains a T-Spline description in TSM form.
    /// Returns the newly created TSplineBody if successful or null in the case of failure.
    core::Ptr<TSplineBody> addByTSMDescription(const std::string& tsmDescription);

    typedef TSplineBody iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_TSPLINEBODIES_API static const char* classType();
    ADSK_FUSION_TSPLINEBODIES_API const char* objectType() const override;
    ADSK_FUSION_TSPLINEBODIES_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_TSPLINEBODIES_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual TSplineBody* item_raw(size_t index) const = 0;
    virtual size_t count_raw() const = 0;
    virtual TSplineBody* itemByName_raw(const char * name) const = 0;
    virtual TSplineBody* addByTSMFile_raw(const char * tsmFilename) = 0;
    virtual TSplineBody* addByTSMDescription_raw(const char * tsmDescription) = 0;
};

// Inline wrappers

inline core::Ptr<TSplineBody> TSplineBodies::item(size_t index) const
{
    core::Ptr<TSplineBody> res = item_raw(index);
    return res;
}

inline size_t TSplineBodies::count() const
{
    size_t res = count_raw();
    return res;
}

inline core::Ptr<TSplineBody> TSplineBodies::itemByName(const std::string& name) const
{
    core::Ptr<TSplineBody> res = itemByName_raw(name.c_str());
    return res;
}

inline core::Ptr<TSplineBody> TSplineBodies::addByTSMFile(const std::string& tsmFilename)
{
    core::Ptr<TSplineBody> res = addByTSMFile_raw(tsmFilename.c_str());
    return res;
}

inline core::Ptr<TSplineBody> TSplineBodies::addByTSMDescription(const std::string& tsmDescription)
{
    core::Ptr<TSplineBody> res = addByTSMDescription_raw(tsmDescription.c_str());
    return res;
}

template <class OutputIterator> inline void TSplineBodies::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_TSPLINEBODIES_API