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
# ifdef __COMPILING_ADSK_FUSION_JOINTGEOMETRY_CPP__
# define ADSK_FUSION_JOINTGEOMETRY_API XI_EXPORT
# else
# define ADSK_FUSION_JOINTGEOMETRY_API
# endif
#else
# define ADSK_FUSION_JOINTGEOMETRY_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BRepEdge;
    class BRepFace;
    class Profile;
    class SketchCurve;
}}
namespace adsk { namespace core {
    class Point3D;
    class Vector3D;
}}

namespace adsk { namespace fusion {

/// A transient object used to define and query the geometric input of a joint and the resulting coordinate
/// system it defines. New JointGeometry objects are created using its various static create methods and
/// are then used as input to the Joints.createInput method.
class JointGeometry : public core::Base {
public:

    /// Creates a new transient JointGeometry object based on a planar BRepFace object. A JointGeometry
    /// object can be used to create a joint or joint origin.
    /// face : The planar BRepFace object
    /// edge : A BRepEdge edge object that is one of the edges of the specified face. This argument can be
    /// null in the case where the keyPointType is CenterKeypoint indicating the center of the face
    /// is to be used. When an edge is used, the keyPointType specifies the position along the edge
    /// for the keypoint.
    /// keyPointType : Specifies the position along the edge where the joint keypoint will be located. For open edges
    /// this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. For closed edges (i.e. circles), it
    /// must be CenterKeyPoint. When no edge is specified, it must be CenterKeyPoint indicating the center
    /// of area of the face is to be used.
    /// Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure.
    static core::Ptr<JointGeometry> createByPlanarFace(const core::Ptr<BRepFace>& face, const core::Ptr<BRepEdge>& edge, JointKeyPointTypes keyPointType);

    /// Creates a new transient JointGeometry object based on a non-planar analytical BRepFace object. This is limited
    /// to cylinders, cones, spheres, and tori. A JointGeometry object can be used to create a joint or joint origin.
    /// face : The cylindrical, conical, spherical, or toroidal BRepFace object.
    /// keyPointType : Specifies the position relative to the input face where joint keypoint will be located. For cylinders
    /// and cones this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. For spheres and tori this must be
    /// CenterKeyPoint.
    /// Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure.
    static core::Ptr<JointGeometry> createByNonPlanarFace(const core::Ptr<BRepFace>& face, JointKeyPointTypes keyPointType);

    /// Creates a new transient JointGeometry object based on a planar BRepFace object. A JointGeometry
    /// object can be used to create a joint or joint origin.
    /// profile : The Profile object.
    /// sketchCurve : A sketch curve that is part of the input profile. This argument can be
    /// null in the case where the keyPointType is CenterKeypoint indicating the center of the profile
    /// is to be used. When a curve is used, the keyPointType specifies the position along the curve
    /// for the keypoint.
    /// keyPointType : Specifies the position along the curve where the joint keypoint will be located. For open curves (lines, arcs, elliptical arcs, and open splines)
    /// this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. For closed analytic (circles and ellipses), it
    /// must be CenterKeyPoint. When no curve is specified, it must be CenterKeyPoint indicating the center
    /// of area of the profile is to be used.
    /// Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure.
    static core::Ptr<JointGeometry> createByProfile(const core::Ptr<Profile>& profile, const core::Ptr<SketchCurve>& sketchCurve, JointKeyPointTypes keyPointType);

    /// Creates a new transient JointGeometry object using a BRepEdge or SketchCurve as input. A JointGeometry
    /// object can be used to create a joint or joint origin.
    /// curve : Input BRepEdge or SketchCurve.
    /// keyPointType : The position on the curve where to position the joint coordinate system. For any open curves
    /// the valid types are StartKeyPoint, MiddleKeyPoint, and EndKeyPoint. For circular and elliptical
    /// shaped curves the option is CenterKeyPoint. For closed spline curves either StartKeyPoint or
    /// EndKeyPoint can be used and the result is the same.
    /// Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure.
    static core::Ptr<JointGeometry> createByCurve(const core::Ptr<core::Base>& curve, JointKeyPointTypes keyPointType);

    /// Creates a new transient JointGeometry object using a ConstructionPoint, SketchPoint or BRepVertex as input.
    /// A JointGeometry object can be used to create a joint or joint origin.
    /// point : The ConstructionPoint, SketchPoint or BRepVertex object.
    /// Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure.
    static core::Ptr<JointGeometry> createByPoint(const core::Ptr<core::Base>& point);

    /// Returns the type of geometry this JointGeometry object represents.
    JointGeometryTypes geometryType() const;

    /// Returns the keypoint type this JointGeometry is using.
    JointKeyPointTypes keyPointType() const;

    /// The first entity that's defining this joint geometry. This can be various types of geometry depending
    /// on how this joint geometry is defined. The geometryType property indicates how this joint geometry is
    /// defined a provides a clue about the type of geometry to expect back from this property.
    core::Ptr<core::Base> entityOne() const;

    /// This is the second entity that defines this joint geometry. This isn't used for all joint geometry types
    /// and will return null in the cases where it's not used. A second geometry is used in the case where the geometryType
    /// property returns JointProfileGeometry, JointPlanarBRepFaceGeometry, or JointBetweenTowFacesGeometry.
    core::Ptr<core::Base> entityTwo() const;

    /// Returns the origin point that's been calculated for this joint geometry.
    core::Ptr<core::Point3D> origin() const;

    /// Returns the direction of the primary axis that's been calculated for this joint geometry.
    /// Conceptually, this is the X-axis of the computed coordinate system.
    core::Ptr<core::Vector3D> primaryAxisVector() const;

    /// Returns the direction of the secondary axis that's been calculated for this joint geometry.
    /// Conceptually, this is the Y-axis of the computed coordinate system.
    core::Ptr<core::Vector3D> secondaryAxisVector() const;

    /// Returns the direction of the third axis that's been calculated for this joint geometry.
    /// Conceptually, this is the Z-axis of the computed coordinate system.
    core::Ptr<core::Vector3D> thirdAxisVector() const;

    /// Creates a new transient JointGeometry object based on a plane bisecting the two input planes.
    /// planeOne : The first planar entity that the joint origin will be created between. This can be a planar BRepFace
    /// or a ConstructionPlane object.
    /// planeTwo : The second planar entity that the joint origin will be created between. This can be a planar BRepFace
    /// or a ConstructionPlane object.
    /// entityOne : Specifies the entity that is used to define the keypoint. This can be many types of geometry including
    /// edges, planar and non-planar faces, profiles, and sketch geometry.
    /// entityTwo : If the entityOne argument is a planar BRepFace or a Profile, then this argument specifies either
    /// an edge on the face or a sketch curve on the profile. For a planar face this argument is optional in the
    /// case where the keyPointType argument is CenterKeyPoint indicating the center of area of the face is to be used.
    /// keyPointType : Specifies the position on the keyPointGeometry where the keypoint will be defined. This keypoint is then
    /// projected onto the plane to define the position of the joint geometry.
    /// The values that are valid for this argument depend on the type of geometry specified for the geometry and edgeOrCurve
    /// arguments.
    /// If the geometry argument is a planar face and the edgeOrCurve argument is an open BRepEdge object
    /// then this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. If the geometry argument is a planar face and the edgeOrCurve argument
    /// is a closed BRepEdge object (i.e. circles), it must be CenterKeyPoint. If the geometry argument is a planar face and
    /// the edgeOrCurve argument is null, then this must be CenterKeyPoint indicating the center of area of the face.
    /// If the geometry argument is a non-planar face (cylinder, cone, sphere, or torus) this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint
    /// for cylinders and cones but must be CenterKeyPoint for spheres and tori. The edgeOrCurve argument is ignored in this case.
    /// If the geometry argument is a profile and the edgeOrCurve argument is null this can be CenterKeyPoint indicating the center of area
    /// of the profile. If the geometry argument is a profile and the edgeOrCurve argument is an open sketch curve on the profile
    /// then this can be StartKeyPoint, MiddleKeyPoint, or EndKeyPoint. If the geometry argument is a profile and the edgeOrCurve argument
    /// is a closed sketch curve (i.e. circles), it must be CenterKeyPoint.
    /// Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure.
    static core::Ptr<JointGeometry> createByBetweenTwoPlanes(const core::Ptr<core::Base>& planeOne, const core::Ptr<core::Base>& planeTwo, const core::Ptr<core::Base>& entityOne, const core::Ptr<core::Base>& entityTwo, JointKeyPointTypes keyPointType);

    /// Returns the first plane for joint geometry that is defined between two planes. Returns null in all other cases.
    core::Ptr<core::Base> planeOne() const;

    /// Returns the second plane for joint geometry that is defined between two planes. Returns null in all other cases.
    core::Ptr<core::Base> planeTwo() const;

    ADSK_FUSION_JOINTGEOMETRY_API static const char* classType();
    ADSK_FUSION_JOINTGEOMETRY_API const char* objectType() const override;
    ADSK_FUSION_JOINTGEOMETRY_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_JOINTGEOMETRY_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    ADSK_FUSION_JOINTGEOMETRY_API static JointGeometry* createByPlanarFace_raw(BRepFace* face, BRepEdge* edge, JointKeyPointTypes keyPointType);
    ADSK_FUSION_JOINTGEOMETRY_API static JointGeometry* createByNonPlanarFace_raw(BRepFace* face, JointKeyPointTypes keyPointType);
    ADSK_FUSION_JOINTGEOMETRY_API static JointGeometry* createByProfile_raw(Profile* profile, SketchCurve* sketchCurve, JointKeyPointTypes keyPointType);
    ADSK_FUSION_JOINTGEOMETRY_API static JointGeometry* createByCurve_raw(core::Base* curve, JointKeyPointTypes keyPointType);
    ADSK_FUSION_JOINTGEOMETRY_API static JointGeometry* createByPoint_raw(core::Base* point);
    virtual JointGeometryTypes geometryType_raw() const = 0;
    virtual JointKeyPointTypes keyPointType_raw() const = 0;
    virtual core::Base* entityOne_raw() const = 0;
    virtual core::Base* entityTwo_raw() const = 0;
    virtual core::Point3D* origin_raw() const = 0;
    virtual core::Vector3D* primaryAxisVector_raw() const = 0;
    virtual core::Vector3D* secondaryAxisVector_raw() const = 0;
    virtual core::Vector3D* thirdAxisVector_raw() const = 0;
    ADSK_FUSION_JOINTGEOMETRY_API static JointGeometry* createByBetweenTwoPlanes_raw(core::Base* planeOne, core::Base* planeTwo, core::Base* entityOne, core::Base* entityTwo, JointKeyPointTypes keyPointType);
    virtual core::Base* planeOne_raw() const = 0;
    virtual core::Base* planeTwo_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<JointGeometry> JointGeometry::createByPlanarFace(const core::Ptr<BRepFace>& face, const core::Ptr<BRepEdge>& edge, JointKeyPointTypes keyPointType)
{
    core::Ptr<JointGeometry> res = createByPlanarFace_raw(face.get(), edge.get(), keyPointType);
    return res;
}

inline core::Ptr<JointGeometry> JointGeometry::createByNonPlanarFace(const core::Ptr<BRepFace>& face, JointKeyPointTypes keyPointType)
{
    core::Ptr<JointGeometry> res = createByNonPlanarFace_raw(face.get(), keyPointType);
    return res;
}

inline core::Ptr<JointGeometry> JointGeometry::createByProfile(const core::Ptr<Profile>& profile, const core::Ptr<SketchCurve>& sketchCurve, JointKeyPointTypes keyPointType)
{
    core::Ptr<JointGeometry> res = createByProfile_raw(profile.get(), sketchCurve.get(), keyPointType);
    return res;
}

inline core::Ptr<JointGeometry> JointGeometry::createByCurve(const core::Ptr<core::Base>& curve, JointKeyPointTypes keyPointType)
{
    core::Ptr<JointGeometry> res = createByCurve_raw(curve.get(), keyPointType);
    return res;
}

inline core::Ptr<JointGeometry> JointGeometry::createByPoint(const core::Ptr<core::Base>& point)
{
    core::Ptr<JointGeometry> res = createByPoint_raw(point.get());
    return res;
}

inline JointGeometryTypes JointGeometry::geometryType() const
{
    JointGeometryTypes res = geometryType_raw();
    return res;
}

inline JointKeyPointTypes JointGeometry::keyPointType() const
{
    JointKeyPointTypes res = keyPointType_raw();
    return res;
}

inline core::Ptr<core::Base> JointGeometry::entityOne() const
{
    core::Ptr<core::Base> res = entityOne_raw();
    return res;
}

inline core::Ptr<core::Base> JointGeometry::entityTwo() const
{
    core::Ptr<core::Base> res = entityTwo_raw();
    return res;
}

inline core::Ptr<core::Point3D> JointGeometry::origin() const
{
    core::Ptr<core::Point3D> res = origin_raw();
    return res;
}

inline core::Ptr<core::Vector3D> JointGeometry::primaryAxisVector() const
{
    core::Ptr<core::Vector3D> res = primaryAxisVector_raw();
    return res;
}

inline core::Ptr<core::Vector3D> JointGeometry::secondaryAxisVector() const
{
    core::Ptr<core::Vector3D> res = secondaryAxisVector_raw();
    return res;
}

inline core::Ptr<core::Vector3D> JointGeometry::thirdAxisVector() const
{
    core::Ptr<core::Vector3D> res = thirdAxisVector_raw();
    return res;
}

inline core::Ptr<JointGeometry> JointGeometry::createByBetweenTwoPlanes(const core::Ptr<core::Base>& planeOne, const core::Ptr<core::Base>& planeTwo, const core::Ptr<core::Base>& entityOne, const core::Ptr<core::Base>& entityTwo, JointKeyPointTypes keyPointType)
{
    core::Ptr<JointGeometry> res = createByBetweenTwoPlanes_raw(planeOne.get(), planeTwo.get(), entityOne.get(), entityTwo.get(), keyPointType);
    return res;
}

inline core::Ptr<core::Base> JointGeometry::planeOne() const
{
    core::Ptr<core::Base> res = planeOne_raw();
    return res;
}

inline core::Ptr<core::Base> JointGeometry::planeTwo() const
{
    core::Ptr<core::Base> res = planeTwo_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_JOINTGEOMETRY_API