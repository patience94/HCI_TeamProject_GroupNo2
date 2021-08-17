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
# ifdef __COMPILING_ADSK_FUSION_SKETCHLINES_CPP__
# define ADSK_FUSION_SKETCHLINES_API XI_EXPORT
# else
# define ADSK_FUSION_SKETCHLINES_API
# endif
#else
# define ADSK_FUSION_SKETCHLINES_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class SketchLine;
    class SketchLineList;
}}
namespace adsk { namespace core {
    class Point3D;
}}

namespace adsk { namespace fusion {

/// The collection of lines in a sketch. This provides access to the existing
/// lines and supports the methods to create new lines.
class SketchLines : public core::Base {
public:

    /// Function that returns the specified sketch line using an index into the collection.
    /// index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<SketchLine> item(size_t index) const;

    /// Returns the number of lines in the sketch.
    size_t count() const;

    /// Creates a sketch line between the two input points. The input points
    /// can be either existing SketchPoints or Point3D objects. If a SketchPoint
    /// is used the new line will be based on that sketch point and update if the
    /// sketch point is modified.
    /// startPoint : The start point of the line. It can be a SketchPoint or Point3D object.
    /// endPoint : The end point of the line. It can be a SketchPoint or Point3D object.
    /// Returns the newly created SketchLine object or null if the creation failed.
    core::Ptr<SketchLine> addByTwoPoints(const core::Ptr<core::Base>& startPoint, const core::Ptr<core::Base>& endPoint);

    /// Creates four sketch lines representing a rectangle where the two points are the opposing corners
    /// of the rectangle. The input points can be either existing SketchPoints or Point3D objects.
    /// If a SketchPoint is used the new lines will be based on that sketch point and update if the
    /// sketch point is modified.
    /// pointOne : The first corner of the rectangle. It can be a SketchPoint or Point3D object.
    /// pointTwo : The second corner of the rectangle. It can be a SketchPoint or Point3D object.
    /// Returns the four new sketch lines or null if the creation failed.
    core::Ptr<SketchLineList> addTwoPointRectangle(const core::Ptr<core::Base>& pointOne, const core::Ptr<core::Base>& pointTwo);

    /// Creates four sketch lines representing a rectangle where the first two points are the base corners
    /// of the rectangle and the third point defines the height.
    /// pointOne : The first corner of the rectangle. It can be a SketchPoint or Point3D object.
    /// pointTwo : The first corner of the rectangle. It can be a SketchPoint or Point3D object.
    /// pointThree : The first corner of the rectangle. a Point3D object defining the height of the rectangle.
    /// Returns the four new sketch lines or null if the creation failed.
    core::Ptr<SketchLineList> addThreePointRectangle(const core::Ptr<core::Base>& pointOne, const core::Ptr<core::Base>& pointTwo, const core::Ptr<core::Point3D>& pointThree);

    /// Creates four sketch lines representing a rectangle where the first point represents the center of
    /// the rectangle. The second point is the corner of the rectangle and can be either an existing
    /// SketchPoint or Point3D object. The four sketch lines are returned.
    /// centerPoint : The center point of the rectangle
    /// cornerPoint : The corner of the rectangle. It can be a SketchPoint or Point3D object.
    /// Returns the four new sketch lines or null if the creation failed.
    core::Ptr<SketchLineList> addCenterPointRectangle(const core::Ptr<core::Point3D>& centerPoint, const core::Ptr<core::Base>& cornerPoint);

    typedef SketchLine iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_SKETCHLINES_API static const char* classType();
    ADSK_FUSION_SKETCHLINES_API const char* objectType() const override;
    ADSK_FUSION_SKETCHLINES_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SKETCHLINES_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual SketchLine* item_raw(size_t index) const = 0;
    virtual size_t count_raw() const = 0;
    virtual SketchLine* addByTwoPoints_raw(core::Base* startPoint, core::Base* endPoint) = 0;
    virtual SketchLineList* addTwoPointRectangle_raw(core::Base* pointOne, core::Base* pointTwo) = 0;
    virtual SketchLineList* addThreePointRectangle_raw(core::Base* pointOne, core::Base* pointTwo, core::Point3D* pointThree) = 0;
    virtual SketchLineList* addCenterPointRectangle_raw(core::Point3D* centerPoint, core::Base* cornerPoint) = 0;
};

// Inline wrappers

inline core::Ptr<SketchLine> SketchLines::item(size_t index) const
{
    core::Ptr<SketchLine> res = item_raw(index);
    return res;
}

inline size_t SketchLines::count() const
{
    size_t res = count_raw();
    return res;
}

inline core::Ptr<SketchLine> SketchLines::addByTwoPoints(const core::Ptr<core::Base>& startPoint, const core::Ptr<core::Base>& endPoint)
{
    core::Ptr<SketchLine> res = addByTwoPoints_raw(startPoint.get(), endPoint.get());
    return res;
}

inline core::Ptr<SketchLineList> SketchLines::addTwoPointRectangle(const core::Ptr<core::Base>& pointOne, const core::Ptr<core::Base>& pointTwo)
{
    core::Ptr<SketchLineList> res = addTwoPointRectangle_raw(pointOne.get(), pointTwo.get());
    return res;
}

inline core::Ptr<SketchLineList> SketchLines::addThreePointRectangle(const core::Ptr<core::Base>& pointOne, const core::Ptr<core::Base>& pointTwo, const core::Ptr<core::Point3D>& pointThree)
{
    core::Ptr<SketchLineList> res = addThreePointRectangle_raw(pointOne.get(), pointTwo.get(), pointThree.get());
    return res;
}

inline core::Ptr<SketchLineList> SketchLines::addCenterPointRectangle(const core::Ptr<core::Point3D>& centerPoint, const core::Ptr<core::Base>& cornerPoint)
{
    core::Ptr<SketchLineList> res = addCenterPointRectangle_raw(centerPoint.get(), cornerPoint.get());
    return res;
}

template <class OutputIterator> inline void SketchLines::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SKETCHLINES_API