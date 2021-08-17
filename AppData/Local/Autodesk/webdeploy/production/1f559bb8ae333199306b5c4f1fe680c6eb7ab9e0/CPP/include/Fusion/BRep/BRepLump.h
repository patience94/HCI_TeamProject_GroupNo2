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
# ifdef __COMPILING_ADSK_FUSION_BREPLUMP_CPP__
# define ADSK_FUSION_BREPLUMP_API XI_EXPORT
# else
# define ADSK_FUSION_BREPLUMP_API
# endif
#else
# define ADSK_FUSION_BREPLUMP_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BRepBody;
    class BRepEdges;
    class BRepFaces;
    class BRepShells;
    class BRepVertices;
    class MeshManager;
    class Occurrence;
}}
namespace adsk { namespace core {
    class BoundingBox3D;
    class Point3D;
}}

namespace adsk { namespace fusion {

/// Represents an entirely connected set of entities. A BRepBody consists of BRepLumps.
class BRepLump : public core::Base {
public:

    /// Returns the BRepShells owned by the lump
    core::Ptr<BRepShells> shells() const;

    /// Returns the BRepFaces owned by the lump
    core::Ptr<BRepFaces> faces() const;

    /// Returns the BRepEdges owned by the lump
    core::Ptr<BRepEdges> edges() const;

    /// Returns the BRepVertices owned by the lump
    core::Ptr<BRepVertices> vertices() const;

    /// Returns the immediate owner BRepBody of the lump
    core::Ptr<BRepBody> body() const;

    /// Returns true of the lump is closed
    bool isClosed() const;

    /// Returns the bounding box of the lump
    core::Ptr<core::BoundingBox3D> boundingBox() const;

    /// Returns the area in cm ^ 2.
    double area() const;

    /// Returns the volume in cm ^ 3. Returns 0 in the case the lump is not solid.
    double volume() const;

    /// Determines the relationship of the input point with respect to this lump.
    /// point : The point to do the containment check for.
    /// Returns a value from the PointContainment enum indicating the relationship of
    /// the input point to the lump.
    PointContainment pointContainment(const core::Ptr<core::Point3D>& point);

    /// Returns the mesh manager object for this lump.
    core::Ptr<MeshManager> meshManager() const;

    /// Returns the assembly context that is directly referencing this
    /// object in an assembly. This is only valid in the case where this
    /// BRepLump object is acting as a proxy in an assembly. Returns null
    /// in the case where the object is not in the context of an assembly.
    /// but is already the native object.
    core::Ptr<Occurrence> assemblyContext() const;

    /// The NativeObject is the object outside the context of an assembly.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<BRepLump> nativeObject() const;

    /// Returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context for the created proxy.
    /// Returns the new BrepLump proxy or null if this isn't the NativeObject.
    core::Ptr<BRepLump> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_BREPLUMP_API static const char* classType();
    ADSK_FUSION_BREPLUMP_API const char* objectType() const override;
    ADSK_FUSION_BREPLUMP_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_BREPLUMP_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual BRepShells* shells_raw() const = 0;
    virtual BRepFaces* faces_raw() const = 0;
    virtual BRepEdges* edges_raw() const = 0;
    virtual BRepVertices* vertices_raw() const = 0;
    virtual BRepBody* body_raw() const = 0;
    virtual bool isClosed_raw() const = 0;
    virtual core::BoundingBox3D* boundingBox_raw() const = 0;
    virtual double area_raw() const = 0;
    virtual double volume_raw() const = 0;
    virtual PointContainment pointContainment_raw(core::Point3D* point) = 0;
    virtual MeshManager* meshManager_raw() const = 0;
    virtual Occurrence* assemblyContext_raw() const = 0;
    virtual BRepLump* nativeObject_raw() const = 0;
    virtual BRepLump* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline core::Ptr<BRepShells> BRepLump::shells() const
{
    core::Ptr<BRepShells> res = shells_raw();
    return res;
}

inline core::Ptr<BRepFaces> BRepLump::faces() const
{
    core::Ptr<BRepFaces> res = faces_raw();
    return res;
}

inline core::Ptr<BRepEdges> BRepLump::edges() const
{
    core::Ptr<BRepEdges> res = edges_raw();
    return res;
}

inline core::Ptr<BRepVertices> BRepLump::vertices() const
{
    core::Ptr<BRepVertices> res = vertices_raw();
    return res;
}

inline core::Ptr<BRepBody> BRepLump::body() const
{
    core::Ptr<BRepBody> res = body_raw();
    return res;
}

inline bool BRepLump::isClosed() const
{
    bool res = isClosed_raw();
    return res;
}

inline core::Ptr<core::BoundingBox3D> BRepLump::boundingBox() const
{
    core::Ptr<core::BoundingBox3D> res = boundingBox_raw();
    return res;
}

inline double BRepLump::area() const
{
    double res = area_raw();
    return res;
}

inline double BRepLump::volume() const
{
    double res = volume_raw();
    return res;
}

inline PointContainment BRepLump::pointContainment(const core::Ptr<core::Point3D>& point)
{
    PointContainment res = pointContainment_raw(point.get());
    return res;
}

inline core::Ptr<MeshManager> BRepLump::meshManager() const
{
    core::Ptr<MeshManager> res = meshManager_raw();
    return res;
}

inline core::Ptr<Occurrence> BRepLump::assemblyContext() const
{
    core::Ptr<Occurrence> res = assemblyContext_raw();
    return res;
}

inline core::Ptr<BRepLump> BRepLump::nativeObject() const
{
    core::Ptr<BRepLump> res = nativeObject_raw();
    return res;
}

inline core::Ptr<BRepLump> BRepLump::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<BRepLump> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_BREPLUMP_API