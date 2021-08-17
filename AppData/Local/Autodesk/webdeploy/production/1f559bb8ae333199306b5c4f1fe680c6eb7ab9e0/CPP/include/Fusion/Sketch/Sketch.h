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
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_SKETCH_CPP__
# define ADSK_FUSION_SKETCH_API XI_EXPORT
# else
# define ADSK_FUSION_SKETCH_API
# endif
#else
# define ADSK_FUSION_SKETCH_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BRepBody;
    class BRepFace;
    class Component;
    class GeometricConstraints;
    class Occurrence;
    class Profiles;
    class SketchCurve;
    class SketchCurves;
    class SketchDimensions;
    class SketchEntity;
    class SketchPoint;
    class SketchPoints;
    class SketchTexts;
    class TimelineObject;
}}
namespace adsk { namespace core {
    class Attributes;
    class BoundingBox3D;
    class Matrix3D;
    class ObjectCollection;
    class Point3D;
    class Vector3D;
}}

namespace adsk { namespace fusion {

/// Represents a sketch within a component.
class Sketch : public core::Base {
public:

    /// Gets and sets the name of this sketch as seen in the browser and timeline.
    std::string name() const;
    bool name(const std::string& value);

    /// Returns the sketch points collection associated with this sketch.
    /// This provides access to the existing sketch points and supports
    /// the creation of new sketch points.
    core::Ptr<SketchPoints> sketchPoints() const;

    /// Returns the sketch curves collection associated with this sketch.
    /// This provides access to the existing sketch curves which is all
    /// geometry in the sketch except for sketch points. It is through this
    /// collection that new sketch geometry gets created.
    core::Ptr<SketchCurves> sketchCurves() const;

    /// Returns the sketch dimensions collection associated with this sketch.
    /// This provides access to the existing sketch dimensions and supports
    /// the creation of new sketch dimensions.
    core::Ptr<SketchDimensions> sketchDimensions() const;

    /// Returns the sketch constraints collection associated with this sketch.
    /// This provides access to the existing sketch constraints and supports
    /// the creation of new sketch constraints.
    core::Ptr<GeometricConstraints> geometricConstraints() const;

    /// Projects the specified entity onto the x-y plane of the sketch
    /// and returns the created sketch entity(s).
    /// entity : The entity to project. This can be a sketch entity, an edge, a face to get all
    /// of its edges, a vertex, a construction axis, a construction point, or a
    /// construction plane that is perpendicular to the sketch to create a line.
    /// Returns a collection of the sketch entities that were created as a result of the
    /// projection.
    core::Ptr<core::ObjectCollection> project(const core::Ptr<core::Base>& entity);

    /// Intersects the specified body with the sketch plane and creates new
    /// curves representing the intersection.
    /// body : The body to be intersected by the sketch.
    /// Returns a collection of the sketch entities that were created a a result of the
    /// cut.
    core::Ptr<core::ObjectCollection> projectCutEdges(const core::Ptr<BRepBody>& body);

    /// Creates new sketch curves and points that represent the specified entity
    /// as sketch geometry. The sketch geometry is not projected but is created
    /// in the same location in space as the input geometry.
    /// entity : The entity to include into the sketch. This can be a sketch entity from
    /// another sketch, edge, face (which results in getting all of its edges, a
    /// vertex, construction axis, or construction point.
    /// Returns a collection of the sketch entities that were created as a result of the include.
    /// When including this curves it will be a single sketch curve, but for faces, multiple
    /// sketch curves will be created; one for each edge.
    core::Ptr<core::ObjectCollection> include(const core::Ptr<core::Base>& entity);

    /// Finds the sketch curves that are end connected to the input curve. This can be useful
    /// for many cases but is especially useful in gathering the input when creating an offset.
    /// curve : The initial sketch curve that will be used to find the connected curves.
    /// A collection of the connected curves. They are returned in their connected order with
    /// the original input curve being one of the curves.
    core::Ptr<core::ObjectCollection> findConnectedCurves(const core::Ptr<SketchCurve>& curve);

    /// Creates offset curves for the set of input curves. If the offset distance is not
    /// provided, the offset distance is defined by the direction point.
    /// curves : A set of end connected curves. The Sketch.FindConnectedCurves method is a convenient way to get
    /// this set of curves.
    /// directionPoint : Defines which side of the input curves to create the offset on
    /// offset : The distance to offset the curves in centimeters.
    /// A collection of the new offset sketch curves created
    core::Ptr<core::ObjectCollection> offset(const core::Ptr<core::ObjectCollection>& curves, const core::Ptr<core::Point3D>& directionPoint, double offset = 0);

    /// Gets and sets the transform of the sketch with respect to model space.
    /// This defines the transform from the parent component space
    /// to the sketch space. For example, if you have point coordinates in the space
    /// of the parent component and apply this transform it will result in the
    /// coordinates of the equivalent position in sketch space.
    /// The transform is sensitive to the assembly context.
    /// Setting the transform will fail in the case where the sketch is parametric
    core::Ptr<core::Matrix3D> transform() const;
    bool transform(const core::Ptr<core::Matrix3D>& value);

    /// A specified point in model space returns the equivalent point in sketch space.
    /// This is sensitive to the assembly context.
    /// modelCoordinate : A coordinate in model space.
    /// Returns the equivalent point in sketch space.
    core::Ptr<core::Point3D> modelToSketchSpace(const core::Ptr<core::Point3D>& modelCoordinate);

    /// A specified point in sketch space returns the equivalent point in model space.
    /// This is sensitive to the assembly context.
    /// sketchCoordinate : A coordinate in sketch space.
    /// Returns the equivalent point in model space.
    core::Ptr<core::Point3D> sketchToModelSpace(const core::Ptr<core::Point3D>& sketchCoordinate);

    /// Indicates if this sketch is parametric or not. For parametric sketches, you can also
    /// get the construction plane or face it is associative to using the ReferencePlane property.
    bool isParametric() const;

    /// Gets if this sketch is currently visible in the graphics window. Use the
    /// isLightBulbOn to change if the light bulb beside the sketch node in the
    /// browser is on or not. Parent nodes in the browser can have their light
    /// bulb off which affects all of their children. This property indicates
    /// the final result and whether this body is actually visible or not.
    bool isVisible() const;
    bool isVisible(bool value);

    /// Indicates if the dimensions of the sketch are displayed when the sketch is not active
    /// (in sketch edit mode)
    bool areDimensionsShown() const;
    bool areDimensionsShown(bool value);

    /// Indicates if the profiles of the sketch are displayed
    bool areProfilesShown() const;
    bool areProfilesShown(bool value);

    /// Returns the origin point of the sketch in model space.
    core::Ptr<core::Point3D> origin() const;

    /// Returns the X direction of the sketch as defined in model space.
    core::Ptr<core::Vector3D> xDirection() const;

    /// Returns the Y direction of the sketch as defined in model space.
    core::Ptr<core::Vector3D> yDirection() const;

    /// Gets and sets the construction plane or planar face the sketch is associated
    /// to. This is only valid when the IsParametric property is True otherwise this
    /// returns null and setting the property will fail.
    /// Setting this property is the equivalent of the Redefine command.
    core::Ptr<core::Base> referencePlane() const;
    bool referencePlane(const core::Ptr<core::Base>& value);

    /// Temporarily turns off the compute of the sketch. This is used to
    /// increase the performance as sketch geometry is created. Once the
    /// sketch is drawn the this property should be set to false to allow
    /// the sketch to recompute. This setting is not saved by the file and is
    /// always false when a file is opened.
    bool isComputeDeferred() const;
    bool isComputeDeferred(bool value);

    /// Moves the specified sketch entities using the specified transform.
    /// Transform respects any constraints that would normally prohibit the move.
    /// sketchEntities : A collection of sketch entities to transform.
    /// transform : The transform that defines the move, rotate or scale.
    /// Returns true if the move was successful.
    bool move(const core::Ptr<core::ObjectCollection>& sketchEntities, const core::Ptr<core::Matrix3D>& transform);

    /// Copies the specified sketch entities, applying the specified transform.
    /// Any geometric or dimension constraints associated with the entities will
    /// automatically be copied, if possible. For example, if there is a horizontal
    /// dimension and the transform defines a rotation then it will not be included in the
    /// result. This same behavior can be seen when performing a copy/paste operation
    /// in the user interface.
    /// sketchEntities : The collection of sketch entities to copy. They must all exist in this sketch.
    /// transform : The transform to apply to the copied entities.
    /// targetSketch : Optionally specifies the sketch to copy the entities to. If not provided the entities are copied to this sketch.
    /// Returns a collection of the new sketch entities that were created as a result of the copy.
    core::Ptr<core::ObjectCollection> copy(const core::Ptr<core::ObjectCollection>& sketchEntities, const core::Ptr<core::Matrix3D>& transform, const core::Ptr<Sketch>& targetSketch = NULL);

    /// Returns the profiles currently computed for the sketch.
    core::Ptr<Profiles> profiles() const;

    /// Deletes the sketch.
    /// Returns true if the delete was successful.
    bool deleteMe();

    /// Saves the contents of the sketch to a specified DXF file.
    /// fullFilename : The full filename, including the path, of the DXF file.
    /// Returns true if the operation was successful.
    bool saveAsDXF(const std::string& fullFilename);

    /// Imports the contents of an SVG file into the active sketch.
    /// fullFilename : The full filename, including the path, of the SVG file.
    /// xPosition : The X offset in centimeters in the sketch for the origin of the SVG data
    /// relative to the sketch origin.
    /// yPosition : The Y offset in centimeters in the sketch for the origin of the SVG data
    /// relative to the sketch origin.
    /// scale : The scale value to apply to the imported SVG data.
    /// Returns true if the import was successful.
    bool importSVG(const std::string& fullFilename, double xPosition, double yPosition, double scale);

    /// Returns the timeline object associated with this sketch.
    core::Ptr<TimelineObject> timelineObject() const;

    /// Returns the parent Component.
    core::Ptr<Component> parentComponent() const;

    /// Returns the assembly occurrence (i.e. the occurrence) of this
    /// object in an assembly. This is only valid in the case where this
    /// is acting as a proxy in an assembly. Returns null
    /// in the case where the object is not in the context of an assembly.
    /// but is already the native object.
    core::Ptr<Occurrence> assemblyContext() const;

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<Sketch> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<Sketch> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    /// Returns the 3D bounding box of the sketch
    core::Ptr<core::BoundingBox3D> boundingBox() const;

    /// Returns the sketch text collection associated with this sketch.
    /// This provides access to existing text and supports the creation
    /// of new text.
    core::Ptr<SketchTexts> sketchTexts() const;

    /// Returns the sketch point that was automatically created by projecting the
    /// origin construction point into the sketch.
    core::Ptr<SketchPoint> originPoint() const;

    /// Indicates if this sketch is fully constrained.
    bool isFullyConstrained() const;

    /// Changes which plane the sketch is based on.
    /// planarEntity : A construction plane or planar face that defines the sketch plane
    /// Returns true if the operation was successful.
    bool redefine(const core::Ptr<core::Base>& planarEntity);

    /// Returns the collection of attributes associated with this face.
    core::Ptr<core::Attributes> attributes() const;

    /// This property returns the base or form feature that this sketch is associated with. It returns
    /// null in the case wher the sketch is parametrically defined and is not related to a base or form
    /// feature. It also returns null in the case where the modeling design history is not being captured (direct edit model).
    core::Ptr<core::Base> baseOrFormFeature() const;

    /// Returns the current health state of this sketch.
    FeatureHealthStates healthState() const;

    /// Returns the error or warning message in the case where the healthState property returns either
    /// WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.
    std::string errorOrWarningMessage() const;

    /// Intersects the specified entities (BRepBody, BRepFace, BRepEdge, BRepVertex, SketchCurve, ConstructionPoint,
    /// ConstructionAxis, and ConstructionPlane) with the sketch plane and creates sketch geometry that represents
    /// the intersection.
    /// entities : An array containing the entities to intersect with the sketch plane.
    /// An array returning the sketch entities that were created as a result of the
    /// intersections. It's possible that this can come back empty in the case where the input
    /// entities don't intersect the sketch plane.
    std::vector<core::Ptr<SketchEntity>> intersectWithSketchPlane(const std::vector<core::Ptr<core::Base>>& entities);

    /// Projects the specified set of curves onto the specified set of faces using the specified method of projection.
    /// if the projection type is along a vector, then the directionEntity argument must be supplied. if the projectionType
    /// is the closest point method, the directionEntity argument is ignored.
    /// faces : An array of BRepFace objects that the curves will be projected onto.
    /// curves : An array of various curve objects that will be projected onto the faces. The curves can be sketch curves and points,
    /// BRepEdge objects, ConstructionAxis objects, and ConstructionPoint objects.
    /// projectType : Specifies which projection type to use which defines the direction of projection. If this is set to AlongVectorSurfaceProjectType
    /// the directionEntity argument must be provided.
    /// directionEntity : if the projectType argument is AlongVectorSurfaceProjectType, this argument must be specified and defines the
    /// direction of projection. It can be a linear BRepEdge, a BRepFace where the normal will be used, a SketchLine, or
    /// a ConstructionLine.
    /// Returns an array of the sketch entities that were created as a result of projection the specified curves onto
    /// the faces.
    std::vector<core::Ptr<SketchEntity>> projectToSurface(const std::vector<core::Ptr<BRepFace>>& faces, const std::vector<core::Ptr<core::Base>>& curves, SurfaceProjectTypes projectType, const core::Ptr<core::Base>& directionEntity = core::Ptr<core::Base>());

    /// Returns the current revision ID of the sketch. This ID changes any time the sketch is modified in any way. By getting
    /// and saving the ID when you create any data that is dependent on the sketch, you can then compare the saved
    /// ID with the current ID to determine if the sketch has changed to know if you should update your data.
    std::string revisionId() const;

    /// Indicates if the constraints of the sketch are displayed when the sketch is active.
    bool areConstraintsShown() const;
    bool areConstraintsShown(bool value);

    /// Indicates if the sketch points in the sketch are displayed. Points that are not connected to any other
    /// geometry will continue to be shown.
    bool arePointsShown() const;
    bool arePointsShown(bool value);

    /// Gets and set if the light bulb beside the sketch node in the
    /// browser is on or not. Parent nodes in the browser can have their light
    /// bulb off which affects all of their children so this property does not
    /// indicate if the body is actually visible, just that it should be visible
    /// if all of it's parent nodes are also visible. Use the isVisible property
    /// to determine if it's actually visible.
    bool isLightBulbOn() const;
    bool isLightBulbOn(bool value);

    ADSK_FUSION_SKETCH_API static const char* classType();
    ADSK_FUSION_SKETCH_API const char* objectType() const override;
    ADSK_FUSION_SKETCH_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SKETCH_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual char* name_raw() const = 0;
    virtual bool name_raw(const char * value) = 0;
    virtual SketchPoints* sketchPoints_raw() const = 0;
    virtual SketchCurves* sketchCurves_raw() const = 0;
    virtual SketchDimensions* sketchDimensions_raw() const = 0;
    virtual GeometricConstraints* geometricConstraints_raw() const = 0;
    virtual core::ObjectCollection* project_raw(core::Base* entity) = 0;
    virtual core::ObjectCollection* projectCutEdges_raw(BRepBody* body) = 0;
    virtual core::ObjectCollection* include_raw(core::Base* entity) = 0;
    virtual core::ObjectCollection* findConnectedCurves_raw(SketchCurve* curve) = 0;
    virtual core::ObjectCollection* offset_raw(core::ObjectCollection* curves, core::Point3D* directionPoint, double offset) = 0;
    virtual core::Matrix3D* transform_raw() const = 0;
    virtual bool transform_raw(core::Matrix3D* value) = 0;
    virtual core::Point3D* modelToSketchSpace_raw(core::Point3D* modelCoordinate) = 0;
    virtual core::Point3D* sketchToModelSpace_raw(core::Point3D* sketchCoordinate) = 0;
    virtual bool isParametric_raw() const = 0;
    virtual bool isVisible_raw() const = 0;
    virtual bool isVisible_raw(bool value) = 0;
    virtual bool areDimensionsShown_raw() const = 0;
    virtual bool areDimensionsShown_raw(bool value) = 0;
    virtual bool areProfilesShown_raw() const = 0;
    virtual bool areProfilesShown_raw(bool value) = 0;
    virtual core::Point3D* origin_raw() const = 0;
    virtual core::Vector3D* xDirection_raw() const = 0;
    virtual core::Vector3D* yDirection_raw() const = 0;
    virtual core::Base* referencePlane_raw() const = 0;
    virtual bool referencePlane_raw(core::Base* value) = 0;
    virtual bool isComputeDeferred_raw() const = 0;
    virtual bool isComputeDeferred_raw(bool value) = 0;
    virtual bool move_raw(core::ObjectCollection* sketchEntities, core::Matrix3D* transform) = 0;
    virtual core::ObjectCollection* copy_raw(core::ObjectCollection* sketchEntities, core::Matrix3D* transform, Sketch* targetSketch) = 0;
    virtual Profiles* profiles_raw() const = 0;
    virtual bool deleteMe_raw() = 0;
    virtual bool saveAsDXF_raw(const char * fullFilename) = 0;
    virtual bool importSVG_raw(const char * fullFilename, double xPosition, double yPosition, double scale) = 0;
    virtual TimelineObject* timelineObject_raw() const = 0;
    virtual Component* parentComponent_raw() const = 0;
    virtual Occurrence* assemblyContext_raw() const = 0;
    virtual Sketch* nativeObject_raw() const = 0;
    virtual Sketch* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
    virtual core::BoundingBox3D* boundingBox_raw() const = 0;
    virtual SketchTexts* sketchTexts_raw() const = 0;
    virtual SketchPoint* originPoint_raw() const = 0;
    virtual bool isFullyConstrained_raw() const = 0;
    virtual bool redefine_raw(core::Base* planarEntity) = 0;
    virtual core::Attributes* attributes_raw() const = 0;
    virtual core::Base* baseOrFormFeature_raw() const = 0;
    virtual FeatureHealthStates healthState_raw() const = 0;
    virtual char* errorOrWarningMessage_raw() const = 0;
    virtual SketchEntity** intersectWithSketchPlane_raw(core::Base** entities, size_t entities_size, size_t& return_size) = 0;
    virtual SketchEntity** projectToSurface_raw(BRepFace** faces, size_t faces_size, core::Base** curves, size_t curves_size, SurfaceProjectTypes projectType, core::Base* directionEntity, size_t& return_size) = 0;
    virtual char* revisionId_raw() const = 0;
    virtual bool areConstraintsShown_raw() const = 0;
    virtual bool areConstraintsShown_raw(bool value) = 0;
    virtual bool arePointsShown_raw() const = 0;
    virtual bool arePointsShown_raw(bool value) = 0;
    virtual bool isLightBulbOn_raw() const = 0;
    virtual bool isLightBulbOn_raw(bool value) = 0;
};

// Inline wrappers

inline std::string Sketch::name() const
{
    std::string res;

    char* p= name_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Sketch::name(const std::string& value)
{
    return name_raw(value.c_str());
}

inline core::Ptr<SketchPoints> Sketch::sketchPoints() const
{
    core::Ptr<SketchPoints> res = sketchPoints_raw();
    return res;
}

inline core::Ptr<SketchCurves> Sketch::sketchCurves() const
{
    core::Ptr<SketchCurves> res = sketchCurves_raw();
    return res;
}

inline core::Ptr<SketchDimensions> Sketch::sketchDimensions() const
{
    core::Ptr<SketchDimensions> res = sketchDimensions_raw();
    return res;
}

inline core::Ptr<GeometricConstraints> Sketch::geometricConstraints() const
{
    core::Ptr<GeometricConstraints> res = geometricConstraints_raw();
    return res;
}

inline core::Ptr<core::ObjectCollection> Sketch::project(const core::Ptr<core::Base>& entity)
{
    core::Ptr<core::ObjectCollection> res = project_raw(entity.get());
    return res;
}

inline core::Ptr<core::ObjectCollection> Sketch::projectCutEdges(const core::Ptr<BRepBody>& body)
{
    core::Ptr<core::ObjectCollection> res = projectCutEdges_raw(body.get());
    return res;
}

inline core::Ptr<core::ObjectCollection> Sketch::include(const core::Ptr<core::Base>& entity)
{
    core::Ptr<core::ObjectCollection> res = include_raw(entity.get());
    return res;
}

inline core::Ptr<core::ObjectCollection> Sketch::findConnectedCurves(const core::Ptr<SketchCurve>& curve)
{
    core::Ptr<core::ObjectCollection> res = findConnectedCurves_raw(curve.get());
    return res;
}

inline core::Ptr<core::ObjectCollection> Sketch::offset(const core::Ptr<core::ObjectCollection>& curves, const core::Ptr<core::Point3D>& directionPoint, double offset)
{
    core::Ptr<core::ObjectCollection> res = offset_raw(curves.get(), directionPoint.get(), offset);
    return res;
}

inline core::Ptr<core::Matrix3D> Sketch::transform() const
{
    core::Ptr<core::Matrix3D> res = transform_raw();
    return res;
}

inline bool Sketch::transform(const core::Ptr<core::Matrix3D>& value)
{
    return transform_raw(value.get());
}

inline core::Ptr<core::Point3D> Sketch::modelToSketchSpace(const core::Ptr<core::Point3D>& modelCoordinate)
{
    core::Ptr<core::Point3D> res = modelToSketchSpace_raw(modelCoordinate.get());
    return res;
}

inline core::Ptr<core::Point3D> Sketch::sketchToModelSpace(const core::Ptr<core::Point3D>& sketchCoordinate)
{
    core::Ptr<core::Point3D> res = sketchToModelSpace_raw(sketchCoordinate.get());
    return res;
}

inline bool Sketch::isParametric() const
{
    bool res = isParametric_raw();
    return res;
}

inline bool Sketch::isVisible() const
{
    bool res = isVisible_raw();
    return res;
}

inline bool Sketch::isVisible(bool value)
{
    return isVisible_raw(value);
}

inline bool Sketch::areDimensionsShown() const
{
    bool res = areDimensionsShown_raw();
    return res;
}

inline bool Sketch::areDimensionsShown(bool value)
{
    return areDimensionsShown_raw(value);
}

inline bool Sketch::areProfilesShown() const
{
    bool res = areProfilesShown_raw();
    return res;
}

inline bool Sketch::areProfilesShown(bool value)
{
    return areProfilesShown_raw(value);
}

inline core::Ptr<core::Point3D> Sketch::origin() const
{
    core::Ptr<core::Point3D> res = origin_raw();
    return res;
}

inline core::Ptr<core::Vector3D> Sketch::xDirection() const
{
    core::Ptr<core::Vector3D> res = xDirection_raw();
    return res;
}

inline core::Ptr<core::Vector3D> Sketch::yDirection() const
{
    core::Ptr<core::Vector3D> res = yDirection_raw();
    return res;
}

inline core::Ptr<core::Base> Sketch::referencePlane() const
{
    core::Ptr<core::Base> res = referencePlane_raw();
    return res;
}

inline bool Sketch::referencePlane(const core::Ptr<core::Base>& value)
{
    return referencePlane_raw(value.get());
}

inline bool Sketch::isComputeDeferred() const
{
    bool res = isComputeDeferred_raw();
    return res;
}

inline bool Sketch::isComputeDeferred(bool value)
{
    return isComputeDeferred_raw(value);
}

inline bool Sketch::move(const core::Ptr<core::ObjectCollection>& sketchEntities, const core::Ptr<core::Matrix3D>& transform)
{
    bool res = move_raw(sketchEntities.get(), transform.get());
    return res;
}

inline core::Ptr<core::ObjectCollection> Sketch::copy(const core::Ptr<core::ObjectCollection>& sketchEntities, const core::Ptr<core::Matrix3D>& transform, const core::Ptr<Sketch>& targetSketch)
{
    core::Ptr<core::ObjectCollection> res = copy_raw(sketchEntities.get(), transform.get(), targetSketch.get());
    return res;
}

inline core::Ptr<Profiles> Sketch::profiles() const
{
    core::Ptr<Profiles> res = profiles_raw();
    return res;
}

inline bool Sketch::deleteMe()
{
    bool res = deleteMe_raw();
    return res;
}

inline bool Sketch::saveAsDXF(const std::string& fullFilename)
{
    bool res = saveAsDXF_raw(fullFilename.c_str());
    return res;
}

inline bool Sketch::importSVG(const std::string& fullFilename, double xPosition, double yPosition, double scale)
{
    bool res = importSVG_raw(fullFilename.c_str(), xPosition, yPosition, scale);
    return res;
}

inline core::Ptr<TimelineObject> Sketch::timelineObject() const
{
    core::Ptr<TimelineObject> res = timelineObject_raw();
    return res;
}

inline core::Ptr<Component> Sketch::parentComponent() const
{
    core::Ptr<Component> res = parentComponent_raw();
    return res;
}

inline core::Ptr<Occurrence> Sketch::assemblyContext() const
{
    core::Ptr<Occurrence> res = assemblyContext_raw();
    return res;
}

inline core::Ptr<Sketch> Sketch::nativeObject() const
{
    core::Ptr<Sketch> res = nativeObject_raw();
    return res;
}

inline core::Ptr<Sketch> Sketch::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<Sketch> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}

inline core::Ptr<core::BoundingBox3D> Sketch::boundingBox() const
{
    core::Ptr<core::BoundingBox3D> res = boundingBox_raw();
    return res;
}

inline core::Ptr<SketchTexts> Sketch::sketchTexts() const
{
    core::Ptr<SketchTexts> res = sketchTexts_raw();
    return res;
}

inline core::Ptr<SketchPoint> Sketch::originPoint() const
{
    core::Ptr<SketchPoint> res = originPoint_raw();
    return res;
}

inline bool Sketch::isFullyConstrained() const
{
    bool res = isFullyConstrained_raw();
    return res;
}

inline bool Sketch::redefine(const core::Ptr<core::Base>& planarEntity)
{
    bool res = redefine_raw(planarEntity.get());
    return res;
}

inline core::Ptr<core::Attributes> Sketch::attributes() const
{
    core::Ptr<core::Attributes> res = attributes_raw();
    return res;
}

inline core::Ptr<core::Base> Sketch::baseOrFormFeature() const
{
    core::Ptr<core::Base> res = baseOrFormFeature_raw();
    return res;
}

inline FeatureHealthStates Sketch::healthState() const
{
    FeatureHealthStates res = healthState_raw();
    return res;
}

inline std::string Sketch::errorOrWarningMessage() const
{
    std::string res;

    char* p= errorOrWarningMessage_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<core::Ptr<SketchEntity>> Sketch::intersectWithSketchPlane(const std::vector<core::Ptr<core::Base>>& entities)
{
    std::vector<core::Ptr<SketchEntity>> res;
    size_t s;
    core::Base** entities_ = new core::Base*[entities.size()];
    for(size_t i=0; i<entities.size(); ++i)
        entities_[i] = entities[i].get();

    SketchEntity** p= intersectWithSketchPlane_raw(entities_, entities.size(), s);
    delete[] entities_;
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<core::Ptr<SketchEntity>> Sketch::projectToSurface(const std::vector<core::Ptr<BRepFace>>& faces, const std::vector<core::Ptr<core::Base>>& curves, SurfaceProjectTypes projectType, const core::Ptr<core::Base>& directionEntity)
{
    std::vector<core::Ptr<SketchEntity>> res;
    size_t s;
    BRepFace** faces_ = new BRepFace*[faces.size()];
    for(size_t i=0; i<faces.size(); ++i)
        faces_[i] = faces[i].get();
    core::Base** curves_ = new core::Base*[curves.size()];
    for(size_t i=0; i<curves.size(); ++i)
        curves_[i] = curves[i].get();

    SketchEntity** p= projectToSurface_raw(faces_, faces.size(), curves_, curves.size(), projectType, directionEntity.get(), s);
    delete[] faces_;
    delete[] curves_;
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline std::string Sketch::revisionId() const
{
    std::string res;

    char* p= revisionId_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Sketch::areConstraintsShown() const
{
    bool res = areConstraintsShown_raw();
    return res;
}

inline bool Sketch::areConstraintsShown(bool value)
{
    return areConstraintsShown_raw(value);
}

inline bool Sketch::arePointsShown() const
{
    bool res = arePointsShown_raw();
    return res;
}

inline bool Sketch::arePointsShown(bool value)
{
    return arePointsShown_raw(value);
}

inline bool Sketch::isLightBulbOn() const
{
    bool res = isLightBulbOn_raw();
    return res;
}

inline bool Sketch::isLightBulbOn(bool value)
{
    return isLightBulbOn_raw(value);
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SKETCH_API