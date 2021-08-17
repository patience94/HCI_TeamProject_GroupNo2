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
# ifdef __COMPILING_ADSK_FUSION_SKETCHPOINTS_CPP__
# define ADSK_FUSION_SKETCHPOINTS_API XI_EXPORT
# else
# define ADSK_FUSION_SKETCHPOINTS_API
# endif
#else
# define ADSK_FUSION_SKETCHPOINTS_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class SketchPoint;
}}
namespace adsk { namespace core {
    class Point3D;
}}

namespace adsk { namespace fusion {

/// A collection of sketch points.
class SketchPoints : public core::Base {
public:

    /// Function that returns the specified sketch using an index into the collection.
    /// index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<SketchPoint> item(size_t index) const;

    /// Returns the number of sketch points in the sketch.
    size_t count() const;

    /// Creates a point at the specified location. This is the equivalent
    /// of creating a sketch point using the Point command in the user
    /// interface and will create a visible point in the graphics window.
    /// point : The coordinate location to create the sketch point.
    /// Returns the new sketch point or null if the creation fails.
    core::Ptr<SketchPoint> add(const core::Ptr<core::Point3D>& point);

    typedef SketchPoint iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_SKETCHPOINTS_API static const char* classType();
    ADSK_FUSION_SKETCHPOINTS_API const char* objectType() const override;
    ADSK_FUSION_SKETCHPOINTS_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SKETCHPOINTS_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual SketchPoint* item_raw(size_t index) const = 0;
    virtual size_t count_raw() const = 0;
    virtual SketchPoint* add_raw(core::Point3D* point) = 0;
};

// Inline wrappers

inline core::Ptr<SketchPoint> SketchPoints::item(size_t index) const
{
    core::Ptr<SketchPoint> res = item_raw(index);
    return res;
}

inline size_t SketchPoints::count() const
{
    size_t res = count_raw();
    return res;
}

inline core::Ptr<SketchPoint> SketchPoints::add(const core::Ptr<core::Point3D>& point)
{
    core::Ptr<SketchPoint> res = add_raw(point.get());
    return res;
}

template <class OutputIterator> inline void SketchPoints::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SKETCHPOINTS_API