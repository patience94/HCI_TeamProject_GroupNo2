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
# ifdef __COMPILING_ADSK_FUSION_GEOMETRICCONSTRAINTS_CPP__
# define ADSK_FUSION_GEOMETRICCONSTRAINTS_API XI_EXPORT
# else
# define ADSK_FUSION_GEOMETRICCONSTRAINTS_API
# endif
#else
# define ADSK_FUSION_GEOMETRICCONSTRAINTS_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class CoincidentConstraint;
    class CollinearConstraint;
    class ConcentricConstraint;
    class EqualConstraint;
    class GeometricConstraint;
    class HorizontalConstraint;
    class HorizontalPointsConstraint;
    class MidPointConstraint;
    class ParallelConstraint;
    class PerpendicularConstraint;
    class SketchCurve;
    class SketchEntity;
    class SketchLine;
    class SketchPoint;
    class SmoothConstraint;
    class SymmetryConstraint;
    class TangentConstraint;
    class VerticalConstraint;
    class VerticalPointsConstraint;
}}

namespace adsk { namespace fusion {

/// A collection of all of the geometric constraints in a sketch. This object
/// also supports the methods to create new geometric constraints.
class GeometricConstraints : public core::Base {
public:

    /// Function that returns the specified sketch constraint using an index into the collection.
    /// index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<GeometricConstraint> item(size_t index) const;

    /// Returns the number of constraints in the sketch.
    size_t count() const;

    /// Creates a new coincident constraint between two entities. The first argument
    /// is a sketch point. The second argument is a sketch curve or point.
    /// point : The SketchPoint that will be made coincident.
    /// entity : The SketchPoint or sketch curve that the point will be made coincident to.
    /// Returns the newly created CoincidentConstraint object or null if the creation failed.
    core::Ptr<CoincidentConstraint> addCoincident(const core::Ptr<SketchPoint>& point, const core::Ptr<SketchEntity>& entity);

    /// Creates a new collinear constraint between two lines.
    /// lineOne : The first line to create the constraint on.
    /// lineTwo : The second line to create the constraint on.
    /// Returns the newly created CollinearConstraint object or null if the creation failed.
    core::Ptr<CollinearConstraint> addCollinear(const core::Ptr<SketchLine>& lineOne, const core::Ptr<SketchLine>& lineTwo);

    /// Creates a new concentric constraint between two circles, arcs, ellipses, or elliptical arcs.
    /// entityOne : The first circle, arc, ellipse or elliptical arc.
    /// entityTwo : The second circle, arc, ellipse or elliptical arc.
    /// Returns the newly created ConcentricConstraint object or null if the creation failed.
    core::Ptr<ConcentricConstraint> addConcentric(const core::Ptr<SketchCurve>& entityOne, const core::Ptr<SketchCurve>& entityTwo);

    /// Creates a new midpoint constraint between a point and a curve.
    /// point : The point to constrain to the midpoint of a curve.
    /// midPointCurve : The curve that defines the midpoint to constraint to.
    /// Returns the newly created MidPointConstraint object or null if the creation failed.
    core::Ptr<MidPointConstraint> addMidPoint(const core::Ptr<SketchPoint>& point, const core::Ptr<SketchCurve>& midPointCurve);

    /// Creates a new parallel constraint between two lines.
    /// lineOne : The first SketchLine.
    /// lineTwo : The second SketchLine.
    /// Returns the newly created ParallelConstraint object or null if the creation failed.
    core::Ptr<ParallelConstraint> addParallel(const core::Ptr<SketchLine>& lineOne, const core::Ptr<SketchLine>& lineTwo);

    /// Creates a new perpendicular constraint between two lines.
    /// lineOne : The first SketchLine.
    /// lineTwo : The second SketchLine.
    /// Returns the newly created PerpendicularConstraint object or null if the creation failed.
    core::Ptr<PerpendicularConstraint> addPerpendicular(const core::Ptr<SketchLine>& lineOne, const core::Ptr<SketchLine>& lineTwo);

    /// Creates a new horizontal constraint on a line.
    /// line : The line to constrain horizontally.
    /// Returns the newly created HorizontalConstraint object or null if the creation failed.
    core::Ptr<HorizontalConstraint> addHorizontal(const core::Ptr<SketchLine>& line);

    /// Creates a new horizontal constraint between two points.
    /// pointOne : The first SketchPoint to constrain horizontally.
    /// pointTwo : The second SketchPoint to constrain horizontally.
    /// Returns the newly created HorizontalPointsConstraint object or null if the creation failed.
    core::Ptr<HorizontalPointsConstraint> addHorizontalPoints(const core::Ptr<SketchPoint>& pointOne, const core::Ptr<SketchPoint>& pointTwo);

    /// Creates a new vertical constraint on a line.
    /// line : The line to constrain vertically.
    /// Returns the newly created VerticalConstraint object or null if the creation failed.
    core::Ptr<VerticalConstraint> addVertical(const core::Ptr<SketchLine>& line);

    /// Creates a new vertical constraint between two points.
    /// pointOne : The first SketchPoint to constrain vertically.
    /// pointTwo : The second SketchPoint to constrain vertically.
    /// Returns the newly created VerticalPointsConstraint object or null if the creation failed.
    core::Ptr<VerticalPointsConstraint> addVerticalPoints(const core::Ptr<SketchPoint>& pointOne, const core::Ptr<SketchPoint>& pointTwo);

    /// Creates a new tangent constraint between two curves.
    /// curveOne : The first curve to be tangent.
    /// curveTwo : The second curve to be tangent.
    /// Returns the newly created TangentConstraint object or null if the creation failed.
    core::Ptr<TangentConstraint> addTangent(const core::Ptr<SketchCurve>& curveOne, const core::Ptr<SketchCurve>& curveTwo);

    /// Creates a new smooth constraint between two curves. One of the curves
    /// must be a spline. The other curve can be a spline or an arc.
    /// curveOne : The first curve to be smooth.
    /// curveTwo : The first curve to be smooth.
    /// Returns the newly created SmoothConstraint object or null if the creation failed.
    core::Ptr<SmoothConstraint> addSmooth(const core::Ptr<SketchCurve>& curveOne, const core::Ptr<SketchCurve>& curveTwo);

    /// Creates a new equal constraint between two lines, or between arcs and circles.
    /// curveOne : The first line, arc, or circle.
    /// curveTwo : The second line, arc, or circle.
    /// Returns the newly created EqualConstraint object or null if the creation failed.
    core::Ptr<EqualConstraint> addEqual(const core::Ptr<SketchCurve>& curveOne, const core::Ptr<SketchCurve>& curveTwo);

    /// Creates a new symmetry constraint.
    /// entityOne : The first sketch entity to be symmetric.
    /// entityTwo : The second sketch entity to be symmetric. It must be the same type as the first entity.
    /// symmetryLine : The SketchLine that defines the axis of symmetry.
    /// Returns the newly created SymmetryConstraint object or null if the creation failed.
    core::Ptr<SymmetryConstraint> addSymmetry(const core::Ptr<SketchEntity>& entityOne, const core::Ptr<SketchEntity>& entityTwo, const core::Ptr<SketchLine>& symmetryLine);

    typedef GeometricConstraint iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_GEOMETRICCONSTRAINTS_API static const char* classType();
    ADSK_FUSION_GEOMETRICCONSTRAINTS_API const char* objectType() const override;
    ADSK_FUSION_GEOMETRICCONSTRAINTS_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_GEOMETRICCONSTRAINTS_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual GeometricConstraint* item_raw(size_t index) const = 0;
    virtual size_t count_raw() const = 0;
    virtual CoincidentConstraint* addCoincident_raw(SketchPoint* point, SketchEntity* entity) = 0;
    virtual CollinearConstraint* addCollinear_raw(SketchLine* lineOne, SketchLine* lineTwo) = 0;
    virtual ConcentricConstraint* addConcentric_raw(SketchCurve* entityOne, SketchCurve* entityTwo) = 0;
    virtual MidPointConstraint* addMidPoint_raw(SketchPoint* point, SketchCurve* midPointCurve) = 0;
    virtual ParallelConstraint* addParallel_raw(SketchLine* lineOne, SketchLine* lineTwo) = 0;
    virtual PerpendicularConstraint* addPerpendicular_raw(SketchLine* lineOne, SketchLine* lineTwo) = 0;
    virtual HorizontalConstraint* addHorizontal_raw(SketchLine* line) = 0;
    virtual HorizontalPointsConstraint* addHorizontalPoints_raw(SketchPoint* pointOne, SketchPoint* pointTwo) = 0;
    virtual VerticalConstraint* addVertical_raw(SketchLine* line) = 0;
    virtual VerticalPointsConstraint* addVerticalPoints_raw(SketchPoint* pointOne, SketchPoint* pointTwo) = 0;
    virtual TangentConstraint* addTangent_raw(SketchCurve* curveOne, SketchCurve* curveTwo) = 0;
    virtual SmoothConstraint* addSmooth_raw(SketchCurve* curveOne, SketchCurve* curveTwo) = 0;
    virtual EqualConstraint* addEqual_raw(SketchCurve* curveOne, SketchCurve* curveTwo) = 0;
    virtual SymmetryConstraint* addSymmetry_raw(SketchEntity* entityOne, SketchEntity* entityTwo, SketchLine* symmetryLine) = 0;
};

// Inline wrappers

inline core::Ptr<GeometricConstraint> GeometricConstraints::item(size_t index) const
{
    core::Ptr<GeometricConstraint> res = item_raw(index);
    return res;
}

inline size_t GeometricConstraints::count() const
{
    size_t res = count_raw();
    return res;
}

inline core::Ptr<CoincidentConstraint> GeometricConstraints::addCoincident(const core::Ptr<SketchPoint>& point, const core::Ptr<SketchEntity>& entity)
{
    core::Ptr<CoincidentConstraint> res = addCoincident_raw(point.get(), entity.get());
    return res;
}

inline core::Ptr<CollinearConstraint> GeometricConstraints::addCollinear(const core::Ptr<SketchLine>& lineOne, const core::Ptr<SketchLine>& lineTwo)
{
    core::Ptr<CollinearConstraint> res = addCollinear_raw(lineOne.get(), lineTwo.get());
    return res;
}

inline core::Ptr<ConcentricConstraint> GeometricConstraints::addConcentric(const core::Ptr<SketchCurve>& entityOne, const core::Ptr<SketchCurve>& entityTwo)
{
    core::Ptr<ConcentricConstraint> res = addConcentric_raw(entityOne.get(), entityTwo.get());
    return res;
}

inline core::Ptr<MidPointConstraint> GeometricConstraints::addMidPoint(const core::Ptr<SketchPoint>& point, const core::Ptr<SketchCurve>& midPointCurve)
{
    core::Ptr<MidPointConstraint> res = addMidPoint_raw(point.get(), midPointCurve.get());
    return res;
}

inline core::Ptr<ParallelConstraint> GeometricConstraints::addParallel(const core::Ptr<SketchLine>& lineOne, const core::Ptr<SketchLine>& lineTwo)
{
    core::Ptr<ParallelConstraint> res = addParallel_raw(lineOne.get(), lineTwo.get());
    return res;
}

inline core::Ptr<PerpendicularConstraint> GeometricConstraints::addPerpendicular(const core::Ptr<SketchLine>& lineOne, const core::Ptr<SketchLine>& lineTwo)
{
    core::Ptr<PerpendicularConstraint> res = addPerpendicular_raw(lineOne.get(), lineTwo.get());
    return res;
}

inline core::Ptr<HorizontalConstraint> GeometricConstraints::addHorizontal(const core::Ptr<SketchLine>& line)
{
    core::Ptr<HorizontalConstraint> res = addHorizontal_raw(line.get());
    return res;
}

inline core::Ptr<HorizontalPointsConstraint> GeometricConstraints::addHorizontalPoints(const core::Ptr<SketchPoint>& pointOne, const core::Ptr<SketchPoint>& pointTwo)
{
    core::Ptr<HorizontalPointsConstraint> res = addHorizontalPoints_raw(pointOne.get(), pointTwo.get());
    return res;
}

inline core::Ptr<VerticalConstraint> GeometricConstraints::addVertical(const core::Ptr<SketchLine>& line)
{
    core::Ptr<VerticalConstraint> res = addVertical_raw(line.get());
    return res;
}

inline core::Ptr<VerticalPointsConstraint> GeometricConstraints::addVerticalPoints(const core::Ptr<SketchPoint>& pointOne, const core::Ptr<SketchPoint>& pointTwo)
{
    core::Ptr<VerticalPointsConstraint> res = addVerticalPoints_raw(pointOne.get(), pointTwo.get());
    return res;
}

inline core::Ptr<TangentConstraint> GeometricConstraints::addTangent(const core::Ptr<SketchCurve>& curveOne, const core::Ptr<SketchCurve>& curveTwo)
{
    core::Ptr<TangentConstraint> res = addTangent_raw(curveOne.get(), curveTwo.get());
    return res;
}

inline core::Ptr<SmoothConstraint> GeometricConstraints::addSmooth(const core::Ptr<SketchCurve>& curveOne, const core::Ptr<SketchCurve>& curveTwo)
{
    core::Ptr<SmoothConstraint> res = addSmooth_raw(curveOne.get(), curveTwo.get());
    return res;
}

inline core::Ptr<EqualConstraint> GeometricConstraints::addEqual(const core::Ptr<SketchCurve>& curveOne, const core::Ptr<SketchCurve>& curveTwo)
{
    core::Ptr<EqualConstraint> res = addEqual_raw(curveOne.get(), curveTwo.get());
    return res;
}

inline core::Ptr<SymmetryConstraint> GeometricConstraints::addSymmetry(const core::Ptr<SketchEntity>& entityOne, const core::Ptr<SketchEntity>& entityTwo, const core::Ptr<SketchLine>& symmetryLine)
{
    core::Ptr<SymmetryConstraint> res = addSymmetry_raw(entityOne.get(), entityTwo.get(), symmetryLine.get());
    return res;
}

template <class OutputIterator> inline void GeometricConstraints::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_GEOMETRICCONSTRAINTS_API