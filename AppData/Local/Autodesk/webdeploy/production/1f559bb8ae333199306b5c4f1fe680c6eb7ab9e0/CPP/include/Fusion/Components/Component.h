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
#include "../FusionTypeDefs.h"
#include "BaseComponent.h"
#include <string>
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_COMPONENT_CPP__
# define ADSK_FUSION_COMPONENT_API XI_EXPORT
# else
# define ADSK_FUSION_COMPONENT_API
# endif
#else
# define ADSK_FUSION_COMPONENT_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class AsBuiltJoint;
    class AsBuiltJoints;
    class ConstructionAxis;
    class ConstructionPlane;
    class ConstructionPoint;
    class CustomGraphicsGroups;
    class Features;
    class Joint;
    class JointOrigin;
    class JointOrigins;
    class Joints;
    class MeshBodies;
    class ModelParameters;
    class Occurrence;
    class PhysicalProperties;
    class Profile;
    class RigidGroup;
    class RigidGroups;
    class Sketches;
}}
namespace adsk { namespace core {
    class Attributes;
    class BoundingBox3D;
    class DataFileFuture;
    class DataFolder;
    class Material;
    class Matrix3D;
}}

namespace adsk { namespace fusion {

/// Represents a component in the data model.
/// A component represents a set of geometry, features, and parameters that make up an item in the design.
/// A component can be referenced multiple times into a design with a Occurrence object.
class Component : public BaseComponent {
public:

    /// Returns the sketches collection associated with this component.
    /// This provides access to the existing sketches and supports
    /// the creation of new sketches.
    core::Ptr<Sketches> sketches() const;

    /// Returns the collection that provides access to all of the features
    /// associated with this component.
    core::Ptr<Features> features() const;

    /// Returns the mesh bodies collection associated with this component.
    core::Ptr<MeshBodies> meshBodies() const;

    /// Returns the collection of model parameters in the Component.
    core::Ptr<ModelParameters> modelParameters() const;

    /// Gets and sets if the light bulb of the origin folder as seen in the browser is on or off.
    /// This controls the visibility of the origin construction geometry.
    bool isOriginFolderLightBulbOn() const;
    bool isOriginFolderLightBulbOn(bool value);

    /// Gets and sets if the light bulb of the construction folder as seen in the browser is on or off.
    /// This controls the visibility of the (non-origin) construction geometry
    /// (i.e. planes, points, axes).
    bool isConstructionFolderLightBulbOn() const;
    bool isConstructionFolderLightBulbOn(bool value);

    /// Gets and sets if the light bulb of the sketch folder as seen in the browser is on or off.
    /// This controls the visibility of the sketches in this component.
    bool isSketchFolderLightBulbOn() const;
    bool isSketchFolderLightBulbOn(bool value);

    /// Returns the XY origin construction plane.
    core::Ptr<ConstructionPlane> xYConstructionPlane() const;

    /// Returns the XZ origin construction plane.
    core::Ptr<ConstructionPlane> xZConstructionPlane() const;

    /// Returns the YZ origin construction plane.
    core::Ptr<ConstructionPlane> yZConstructionPlane() const;

    /// Returns the X origin construction axis.
    core::Ptr<ConstructionAxis> xConstructionAxis() const;

    /// Returns the Y origin construction axis.
    core::Ptr<ConstructionAxis> yConstructionAxis() const;

    /// Returns the Z origin construction axis.
    core::Ptr<ConstructionAxis> zConstructionAxis() const;

    /// Returns the origin construction point.
    core::Ptr<ConstructionPoint> originConstructionPoint() const;

    /// Gets and sets the part number associated with this component. Setting this
    /// to an empty string will reset it to be the same as the component name.
    std::string partNumber() const;
    bool partNumber(const std::string& value);

    /// Gets and sets the description associated with this component.
    std::string description() const;
    bool description(const std::string& value);

    /// Creates an open profile based on the input curve(s).
    /// curves : A SketchCurve or an ObjectCollection containing multiple sketch entities. If a single sketch curve
    /// is input the chainCurves argument is checked to determine if connected curves (they do not need to be tangent)
    /// should be automatically found. If multiple curves are provided the chainCurves argument is always
    /// treated as false so you must provide all of the curves in the object collection that you want included in the profile.
    /// The provided curves must all connect together in a single path.
    /// The input curves do not need to be in the same sketch, but they do need to geometrically connect for
    /// a valid profile to be created.
    /// chainCurves : If true, this finds any curves within the same sketch that connect to the single input curve and automatically includes them in the profile. If
    /// false, only the curves provided will be used to define the profile. This argument is ignored and treated as false if multiple curves are input.
    /// Returns the new Profile object or null in the case of a failure.
    core::Ptr<Profile> createOpenProfile(const core::Ptr<core::Base>& curves, bool chainCurves = true);

    /// Creates a profile based on the outside open edges of a BRepFace.
    /// edges : A single BRepEdge object or an ObjectCollection containing multiple BRepEdge objects, or a BRepLoop object. If a single edge
    /// is input, the chainEdges argument is checked to determine if connected edges (they do not need to be tangent)
    /// should be automatically found. If multiple edges are provided the chainEdges argument is always
    /// treated as false so you must provide all of the edges in the object collection that you want included in the profile.
    /// and the edges must all connect together in a single path. if a BRepLoop object is provided, all of the edges in the loop
    /// are included in the profile and the chainEdges argument is ignored.
    /// chainEdges : If true, this finds any edges that connect to the single input edge and automatically includes them in the profile. If
    /// false, only the edges provided will be used to define the profile. This argument is ignored and treated as false if multipled edges
    /// or a BRepLoop is input.
    /// Returns the new Profile object or null in the case of a failure.
    core::Ptr<Profile> createBRepEdgeProfile(const core::Ptr<core::Base>& edges, bool chainEdges = true);

    /// Returns the collection of joints associated with this component.
    core::Ptr<Joints> joints() const;

    /// This property was incorrectly spelled and has been replaced with the JointOrigins property.
    /// However, this needs to remain in the implementation to continue to support programs that
    /// already used it, but it will be hidden in the documentation.
    core::Ptr<JointOrigins> jointOrgins() const;

    /// Returns the collection of as-built joints associated with this component.
    core::Ptr<AsBuiltJoints> asBuiltJoints() const;

    /// Returns the collection of rigid groups associated with this component.
    core::Ptr<RigidGroups> rigidGroups() const;

    /// Gets and sets the physical material assigned to this component.
    core::Ptr<core::Material> material() const;
    bool material(const core::Ptr<core::Material>& value);

    /// Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc
    /// of this component. Property values will be calulated using the 'LowCalculationAccuracy' setting when using this property
    /// to get the PhysicalProperties object. To specify a higher calculation tolerance, use the getPhysicalProperties method instead.
    core::Ptr<PhysicalProperties> physicalProperties() const;

    /// Performs a Save Copy As on this component. This saves the specified component as a new document
    /// in the specified location.
    /// name : The name to use for the new document. If this is an empty string, Fusion 360 will use the
    /// name of the component being saved.
    /// dataFolder : The data folder to save the new document to.
    /// description : The description string of the document. This can be an empty string.
    /// tag : The tag string of the document. This can be an empty string.
    /// Returns a DataFileFuture object that can be used to track the progress of the upload and get the
    /// resulting DataFile once it's available on A360.
    core::Ptr<core::DataFileFuture> saveCopyAs(const std::string& name, const core::Ptr<core::DataFolder>& dataFolder, const std::string& description, const std::string& tag) const;

    /// Returns the bounding box of this component. This is always in world space of the component.
    core::Ptr<core::BoundingBox3D> boundingBox() const;

    /// Gets and sets if the light bulb of the joints folder as seen in the browser is on or off.
    /// This controls the visibility of the joints in this occurrence. The light bulb for the
    /// folder is component specific and will turn off the joints for all occurrences referencing
    /// the component.
    bool isJointsFolderLightBulbOn() const;
    bool isJointsFolderLightBulbOn(bool value);

    /// Returns the collection of attributes associated with this face.
    core::Ptr<core::Attributes> attributes() const;

    /// Gets and sets if the light bulb of the bodies folder as seen in the browser is on or off.
    /// This controls the visibility of the solid/surface bodies and the mesh bodies in this component.
    bool isBodiesFolderLightBulbOn() const;
    bool isBodiesFolderLightBulbOn(bool value);

    /// Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc
    /// of this component.
    /// accuracy : Specifies the desired level of computational accuracy of the property calculations.
    /// The default value of 'LowCalculationAccuracy' returns results within a +/- 1% error margin.
    core::Ptr<PhysicalProperties> getPhysicalProperties(CalculationAccuracy accuracy = adsk::fusion::LowCalculationAccuracy) const;

    /// Transforms a set of occurrences in one step. This provides better performance than transforming them one at a time.
    /// This method is only valid when called on the root component because Fusion 360 flattens the entire assembly structure
    /// when manipulating the assembly so all transforms are relative to the root component.
    /// occurrences : An array of Occurrence objects that you want to transform. These must all be in the context of the root component which
    /// means proxies must be used for occurrences that are in sub-components.
    /// transforms : An array of Matrix3D objects that defines the transform to apply to each occurrence. This array must be the same size
    /// as the array provided for the occurrences argument and the transform will be applied to the occurrence at the same index
    /// in the occurrences array.
    /// ignoreJoints : Specifies if the joints are to be ignored and the occurrences are to be positioned based on then specified transform or if
    /// the joints should be used and the occurrence is transformed the best it can while still honoring the joints.
    /// Returns true if the transform was successful.
    bool transformOccurrences(const std::vector<core::Ptr<Occurrence>>& occurrences, const std::vector<core::Ptr<core::Matrix3D>>& transforms, bool ignoreJoints);

    /// Returns all joints in this component and any sub components. The joints returned are all in the context
    /// of this component so any joints in sub components will be proxies. This is primarily useful when used
    /// from the root component because Fusion 360 flattens the assembly structure, including joints, when manipulating
    /// an assembly.
    std::vector<core::Ptr<Joint>> allJoints() const;

    /// Returns all joint origins in this component and any sub components. The joint origins returned are all in the context
    /// of this component so any joint origins in sub components will be proxies. This is primarily useful when used
    /// from the root component because Fusion 360 flattens the assembly structure, including joint origins, when manipulating
    /// an assembly.
    std::vector<core::Ptr<AsBuiltJoint>> allAsBuiltJoints() const;

    /// Returns all as-built joints in this component and any sub components. The as-built joints returned are all in the context
    /// of this component so any as-built joints in sub components will be proxies. This is primarily useful when used
    /// from the root component because Fusion 360 flattens the assembly structure, including as-built joints, when manipulating
    /// an assembly.
    std::vector<core::Ptr<JointOrigin>> allJointOrigins() const;

    /// Returns all rigid groups in this component and any sub components. The rigid groups returned are all in the context
    /// of this component so any rigid groups in sub components will be proxies. This is primarily useful when used
    /// from the root component because Fusion 360 flattens the assembly structure, including rigid groups, when manipulating
    /// an assembly.
    std::vector<core::Ptr<RigidGroup>> allRigidGroups() const;

    /// Gets and sets the opacity override assigned to this component. A value of 1.0 specifies
    /// that is it completely opaque and a value of 0.0 specifies that is it completely transparent.
    /// This is only applicable for a non-root local component.
    /// This value is not necessarily related to what the user sees because the opacity is inherited.
    /// For example, if you have TopComponent and it has a component in it called SubComponent and you
    /// set the opacity of TopComponent to be 0.5, SubComponent will also be shown as slightly transparent
    /// even though the opacity property for it will return 1.0. Because a component can be referenced as
    /// an occurrence in other components and they can have different opacity settings, it's possible that
    /// different instances of the same component can display using different opacity levels. To get the
    /// opacity that it is being displayed with use the Occurrence.visibleOpacity property.
    double opacity() const;
    bool opacity(double value);

    /// Returns the collection of joint origins associated with this component.
    core::Ptr<JointOrigins> jointOrigins() const;

    /// Returns the customGraphicsGroups object in this component.
    core::Ptr<CustomGraphicsGroups> customGraphicsGroups() const;

    /// Returns the current revision ID of the component. This ID changes any time the component is modified in any way. By getting
    /// and saving the ID when you create any data that is dependent on the component, you can then compare the saved
    /// ID with the current ID to determine if the component has changed to know if you should update your data.
    std::string revisionId() const;

    ADSK_FUSION_COMPONENT_API static const char* classType();
    ADSK_FUSION_COMPONENT_API const char* objectType() const override;
    ADSK_FUSION_COMPONENT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_COMPONENT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual Sketches* sketches_raw() const = 0;
    virtual Features* features_raw() const = 0;
    virtual MeshBodies* meshBodies_raw() const = 0;
    virtual ModelParameters* modelParameters_raw() const = 0;
    virtual bool isOriginFolderLightBulbOn_raw() const = 0;
    virtual bool isOriginFolderLightBulbOn_raw(bool value) = 0;
    virtual bool isConstructionFolderLightBulbOn_raw() const = 0;
    virtual bool isConstructionFolderLightBulbOn_raw(bool value) = 0;
    virtual bool isSketchFolderLightBulbOn_raw() const = 0;
    virtual bool isSketchFolderLightBulbOn_raw(bool value) = 0;
    virtual ConstructionPlane* xYConstructionPlane_raw() const = 0;
    virtual ConstructionPlane* xZConstructionPlane_raw() const = 0;
    virtual ConstructionPlane* yZConstructionPlane_raw() const = 0;
    virtual ConstructionAxis* xConstructionAxis_raw() const = 0;
    virtual ConstructionAxis* yConstructionAxis_raw() const = 0;
    virtual ConstructionAxis* zConstructionAxis_raw() const = 0;
    virtual ConstructionPoint* originConstructionPoint_raw() const = 0;
    virtual char* partNumber_raw() const = 0;
    virtual bool partNumber_raw(const char * value) = 0;
    virtual char* description_raw() const = 0;
    virtual bool description_raw(const char * value) = 0;
    virtual Profile* createOpenProfile_raw(core::Base* curves, bool chainCurves) = 0;
    virtual Profile* createBRepEdgeProfile_raw(core::Base* edges, bool chainEdges) = 0;
    virtual Joints* joints_raw() const = 0;
    virtual JointOrigins* jointOrgins_raw() const = 0;
    virtual AsBuiltJoints* asBuiltJoints_raw() const = 0;
    virtual RigidGroups* rigidGroups_raw() const = 0;
    virtual core::Material* material_raw() const = 0;
    virtual bool material_raw(core::Material* value) = 0;
    virtual PhysicalProperties* physicalProperties_raw() const = 0;
    virtual core::DataFileFuture* saveCopyAs_raw(const char * name, core::DataFolder* dataFolder, const char * description, const char * tag) const = 0;
    virtual core::BoundingBox3D* boundingBox_raw() const = 0;
    virtual bool isJointsFolderLightBulbOn_raw() const = 0;
    virtual bool isJointsFolderLightBulbOn_raw(bool value) = 0;
    virtual core::Attributes* attributes_raw() const = 0;
    virtual bool isBodiesFolderLightBulbOn_raw() const = 0;
    virtual bool isBodiesFolderLightBulbOn_raw(bool value) = 0;
    virtual PhysicalProperties* getPhysicalProperties_raw(CalculationAccuracy accuracy) const = 0;
    virtual bool transformOccurrences_raw(Occurrence** occurrences, size_t occurrences_size, core::Matrix3D** transforms, size_t transforms_size, bool ignoreJoints) = 0;
    virtual Joint** allJoints_raw(size_t& return_size) const = 0;
    virtual AsBuiltJoint** allAsBuiltJoints_raw(size_t& return_size) const = 0;
    virtual JointOrigin** allJointOrigins_raw(size_t& return_size) const = 0;
    virtual RigidGroup** allRigidGroups_raw(size_t& return_size) const = 0;
    virtual double opacity_raw() const = 0;
    virtual bool opacity_raw(double value) = 0;
    virtual JointOrigins* jointOrigins_raw() const = 0;
    virtual CustomGraphicsGroups* customGraphicsGroups_raw() const = 0;
    virtual char* revisionId_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<Sketches> Component::sketches() const
{
    core::Ptr<Sketches> res = sketches_raw();
    return res;
}

inline core::Ptr<Features> Component::features() const
{
    core::Ptr<Features> res = features_raw();
    return res;
}

inline core::Ptr<MeshBodies> Component::meshBodies() const
{
    core::Ptr<MeshBodies> res = meshBodies_raw();
    return res;
}

inline core::Ptr<ModelParameters> Component::modelParameters() const
{
    core::Ptr<ModelParameters> res = modelParameters_raw();
    return res;
}

inline bool Component::isOriginFolderLightBulbOn() const
{
    bool res = isOriginFolderLightBulbOn_raw();
    return res;
}

inline bool Component::isOriginFolderLightBulbOn(bool value)
{
    return isOriginFolderLightBulbOn_raw(value);
}

inline bool Component::isConstructionFolderLightBulbOn() const
{
    bool res = isConstructionFolderLightBulbOn_raw();
    return res;
}

inline bool Component::isConstructionFolderLightBulbOn(bool value)
{
    return isConstructionFolderLightBulbOn_raw(value);
}

inline bool Component::isSketchFolderLightBulbOn() const
{
    bool res = isSketchFolderLightBulbOn_raw();
    return res;
}

inline bool Component::isSketchFolderLightBulbOn(bool value)
{
    return isSketchFolderLightBulbOn_raw(value);
}

inline core::Ptr<ConstructionPlane> Component::xYConstructionPlane() const
{
    core::Ptr<ConstructionPlane> res = xYConstructionPlane_raw();
    return res;
}

inline core::Ptr<ConstructionPlane> Component::xZConstructionPlane() const
{
    core::Ptr<ConstructionPlane> res = xZConstructionPlane_raw();
    return res;
}

inline core::Ptr<ConstructionPlane> Component::yZConstructionPlane() const
{
    core::Ptr<ConstructionPlane> res = yZConstructionPlane_raw();
    return res;
}

inline core::Ptr<ConstructionAxis> Component::xConstructionAxis() const
{
    core::Ptr<ConstructionAxis> res = xConstructionAxis_raw();
    return res;
}

inline core::Ptr<ConstructionAxis> Component::yConstructionAxis() const
{
    core::Ptr<ConstructionAxis> res = yConstructionAxis_raw();
    return res;
}

inline core::Ptr<ConstructionAxis> Component::zConstructionAxis() const
{
    core::Ptr<ConstructionAxis> res = zConstructionAxis_raw();
    return res;
}

inline core::Ptr<ConstructionPoint> Component::originConstructionPoint() const
{
    core::Ptr<ConstructionPoint> res = originConstructionPoint_raw();
    return res;
}

inline std::string Component::partNumber() const
{
    std::string res;

    char* p= partNumber_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Component::partNumber(const std::string& value)
{
    return partNumber_raw(value.c_str());
}

inline std::string Component::description() const
{
    std::string res;

    char* p= description_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Component::description(const std::string& value)
{
    return description_raw(value.c_str());
}

inline core::Ptr<Profile> Component::createOpenProfile(const core::Ptr<core::Base>& curves, bool chainCurves)
{
    core::Ptr<Profile> res = createOpenProfile_raw(curves.get(), chainCurves);
    return res;
}

inline core::Ptr<Profile> Component::createBRepEdgeProfile(const core::Ptr<core::Base>& edges, bool chainEdges)
{
    core::Ptr<Profile> res = createBRepEdgeProfile_raw(edges.get(), chainEdges);
    return res;
}

inline core::Ptr<Joints> Component::joints() const
{
    core::Ptr<Joints> res = joints_raw();
    return res;
}

inline core::Ptr<JointOrigins> Component::jointOrgins() const
{
    core::Ptr<JointOrigins> res = jointOrgins_raw();
    return res;
}

inline core::Ptr<AsBuiltJoints> Component::asBuiltJoints() const
{
    core::Ptr<AsBuiltJoints> res = asBuiltJoints_raw();
    return res;
}

inline core::Ptr<RigidGroups> Component::rigidGroups() const
{
    core::Ptr<RigidGroups> res = rigidGroups_raw();
    return res;
}

inline core::Ptr<core::Material> Component::material() const
{
    core::Ptr<core::Material> res = material_raw();
    return res;
}

inline bool Component::material(const core::Ptr<core::Material>& value)
{
    return material_raw(value.get());
}

inline core::Ptr<PhysicalProperties> Component::physicalProperties() const
{
    core::Ptr<PhysicalProperties> res = physicalProperties_raw();
    return res;
}

inline core::Ptr<core::DataFileFuture> Component::saveCopyAs(const std::string& name, const core::Ptr<core::DataFolder>& dataFolder, const std::string& description, const std::string& tag) const
{
    core::Ptr<core::DataFileFuture> res = saveCopyAs_raw(name.c_str(), dataFolder.get(), description.c_str(), tag.c_str());
    return res;
}

inline core::Ptr<core::BoundingBox3D> Component::boundingBox() const
{
    core::Ptr<core::BoundingBox3D> res = boundingBox_raw();
    return res;
}

inline bool Component::isJointsFolderLightBulbOn() const
{
    bool res = isJointsFolderLightBulbOn_raw();
    return res;
}

inline bool Component::isJointsFolderLightBulbOn(bool value)
{
    return isJointsFolderLightBulbOn_raw(value);
}

inline core::Ptr<core::Attributes> Component::attributes() const
{
    core::Ptr<core::Attributes> res = attributes_raw();
    return res;
}

inline bool Component::isBodiesFolderLightBulbOn() const
{
    bool res = isBodiesFolderLightBulbOn_raw();
    return res;
}

inline bool Component::isBodiesFolderLightBulbOn(bool value)
{
    return isBodiesFolderLightBulbOn_raw(value);
}

inline core::Ptr<PhysicalProperties> Component::getPhysicalProperties(CalculationAccuracy accuracy) const
{
    core::Ptr<PhysicalProperties> res = getPhysicalProperties_raw(accuracy);
    return res;
}

inline bool Component::transformOccurrences(const std::vector<core::Ptr<Occurrence>>& occurrences, const std::vector<core::Ptr<core::Matrix3D>>& transforms, bool ignoreJoints)
{
    Occurrence** occurrences_ = new Occurrence*[occurrences.size()];
    for(size_t i=0; i<occurrences.size(); ++i)
        occurrences_[i] = occurrences[i].get();
    core::Matrix3D** transforms_ = new core::Matrix3D*[transforms.size()];
    for(size_t i=0; i<transforms.size(); ++i)
        transforms_[i] = transforms[i].get();

    bool res = transformOccurrences_raw(occurrences_, occurrences.size(), transforms_, transforms.size(), ignoreJoints);
    delete[] occurrences_;
    delete[] transforms_;
    return res;
}

inline std::vector<core::Ptr<Joint>> Component::allJoints() const
{
    std::vector<core::Ptr<Joint>> res;
    size_t s;

    Joint** p= allJoints_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<core::Ptr<AsBuiltJoint>> Component::allAsBuiltJoints() const
{
    std::vector<core::Ptr<AsBuiltJoint>> res;
    size_t s;

    AsBuiltJoint** p= allAsBuiltJoints_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<core::Ptr<JointOrigin>> Component::allJointOrigins() const
{
    std::vector<core::Ptr<JointOrigin>> res;
    size_t s;

    JointOrigin** p= allJointOrigins_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<core::Ptr<RigidGroup>> Component::allRigidGroups() const
{
    std::vector<core::Ptr<RigidGroup>> res;
    size_t s;

    RigidGroup** p= allRigidGroups_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline double Component::opacity() const
{
    double res = opacity_raw();
    return res;
}

inline bool Component::opacity(double value)
{
    return opacity_raw(value);
}

inline core::Ptr<JointOrigins> Component::jointOrigins() const
{
    core::Ptr<JointOrigins> res = jointOrigins_raw();
    return res;
}

inline core::Ptr<CustomGraphicsGroups> Component::customGraphicsGroups() const
{
    core::Ptr<CustomGraphicsGroups> res = customGraphicsGroups_raw();
    return res;
}

inline std::string Component::revisionId() const
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
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_COMPONENT_API