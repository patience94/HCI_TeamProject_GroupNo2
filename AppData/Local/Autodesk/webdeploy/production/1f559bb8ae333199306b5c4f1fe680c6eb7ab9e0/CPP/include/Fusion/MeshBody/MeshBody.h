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
#include "../../Core/CoreTypeDefs.h"
#include "../../Core/Base.h"
#include "../FusionTypeDefs.h"
#include <string>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_MESHBODY_CPP__
# define ADSK_FUSION_MESHBODY_API XI_EXPORT
# else
# define ADSK_FUSION_MESHBODY_API
# endif
#else
# define ADSK_FUSION_MESHBODY_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Component;
    class Occurrence;
    class PolygonMesh;
    class TriangleMesh;
}}
namespace adsk { namespace core {
    class Appearance;
    class Attributes;
    class Material;
}}

namespace adsk { namespace fusion {

/// Provides access to a mesh body.
class MeshBody : public core::Base {
public:

    /// Gets and sets the name of the mesh body as displayed in the browser.
    std::string name() const;
    bool name(const std::string& value);

    /// Gets and sets if the mesh body is selectable in the graphics window.
    bool isSelectable() const;
    bool isSelectable(bool value);

    /// Is the light bulb (as displayed in the browser) on.
    /// A mesh body will only be visible if the light bulb is switched on. However,
    /// the light bulb can be on and the mesh body is still invisible if the light bulb
    /// for all bodies or the owning component is off.
    bool isLightBulbOn() const;
    bool isLightBulbOn(bool value);

    /// Gets if the mesh body point is visible.
    bool isVisible() const;

    /// Deletes the mesh body.
    /// Returns true in the case where the selection was successful.
    bool deleteMe();

    /// Returns the original mesh data that was imported. This can include triangles, quads, and polygons.
    core::Ptr<PolygonMesh> mesh() const;

    /// Returns the associated mesh that is used for the display. This will always be triangles and includes any textures.
    core::Ptr<TriangleMesh> displayMesh() const;

    /// Returns the parent Component.
    core::Ptr<Component> parentComponent() const;

    /// Returns the assembly occurrence (i.e. the occurrence) of this object
    /// in an assembly. This is only valid in the case where this is acting
    /// as a proxy in an assembly. Returns null in the case where the object
    /// is not in the context of an assembly but is already the native object.
    core::Ptr<Occurrence> assemblyContext() const;

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<MeshBody> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// Fails if this object is not the NativeObject.
    /// occurrence : The occurrence that represents the context you want to create this proxy in.
    /// Returns the proxy for the occurrence in the context of the specified occurrence. Returns null if it failed.
    core::Ptr<MeshBody> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    /// This property returns the base or form feature that this mesh body is associated with. It
    /// returns null in the case where the modeling design history is not being captured (direct edit model).
    core::Ptr<core::Base> baseOrFormFeature() const;

    /// Returns the collection of attributes associated with this mesh body.
    core::Ptr<core::Attributes> attributes() const;

    /// Gets and sets the physical material assigned to this mesh body.
    core::Ptr<core::Material> material() const;
    bool material(const core::Ptr<core::Material>& value);

    /// Read-write property that gets and sets the current appearance of the body. Setting this property will result in applying
    /// an override appearance to the body and the AppearanceSourceType property will return OverrideAppearanceSource. Setting
    /// this property to null will remove any override.
    core::Ptr<core::Appearance> appearance() const;
    bool appearance(const core::Ptr<core::Appearance>& value);

    /// Read-write property that gets the source of the appearance for the body. If this returns OverrideAppearanceSource, an override exists
    /// on this body. The override can be removed by setting the Appearance property to null.
    core::AppearanceSourceTypes appearanceSourceType() const;

    /// Gets and sets the opacity override assigned to this body. A value of 1.0 specifies
    /// that is it completely opaque and a value of 0.0 specifies that is it completely transparent.
    /// This value is not necessarily related to what the user sees because the opacity is inherited.
    /// For example, if you this body is in a component and that component's opacity is set to something
    /// other than 1.0, the body will also be shown as slightly transparent even though the opacity
    /// property for the body will return 1.0. Because the component that contains the body can be
    /// referenced as an occurrence in other components and they can have different opacity settings,
    /// it's possible that different instances of the same body can display using different opacity levels.
    /// To get the opacity that it is being displayed with use the MeshBody.visibleOpacity property.
    /// This is the API equivalent of the "Opacity Control" command available for the body in the browser.
    double opacity() const;
    bool opacity(double value);

    /// The user can set an override opacity for components and bodies these opacity overrides combine if
    /// children and parent components have overrides. This property returns the actual opacity that is
    /// being used to render the body. To set the opacity use the opacity property of the MeshBody object.
    double visibleOpacity() const;

    ADSK_FUSION_MESHBODY_API static const char* classType();
    ADSK_FUSION_MESHBODY_API const char* objectType() const override;
    ADSK_FUSION_MESHBODY_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_MESHBODY_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual char* name_raw() const = 0;
    virtual bool name_raw(const char * value) = 0;
    virtual bool isSelectable_raw() const = 0;
    virtual bool isSelectable_raw(bool value) = 0;
    virtual bool isLightBulbOn_raw() const = 0;
    virtual bool isLightBulbOn_raw(bool value) = 0;
    virtual bool isVisible_raw() const = 0;
    virtual bool deleteMe_raw() = 0;
    virtual PolygonMesh* mesh_raw() const = 0;
    virtual TriangleMesh* displayMesh_raw() const = 0;
    virtual Component* parentComponent_raw() const = 0;
    virtual Occurrence* assemblyContext_raw() const = 0;
    virtual MeshBody* nativeObject_raw() const = 0;
    virtual MeshBody* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
    virtual core::Base* baseOrFormFeature_raw() const = 0;
    virtual core::Attributes* attributes_raw() const = 0;
    virtual core::Material* material_raw() const = 0;
    virtual bool material_raw(core::Material* value) = 0;
    virtual core::Appearance* appearance_raw() const = 0;
    virtual bool appearance_raw(core::Appearance* value) = 0;
    virtual core::AppearanceSourceTypes appearanceSourceType_raw() const = 0;
    virtual double opacity_raw() const = 0;
    virtual bool opacity_raw(double value) = 0;
    virtual double visibleOpacity_raw() const = 0;
};

// Inline wrappers

inline std::string MeshBody::name() const
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

inline bool MeshBody::name(const std::string& value)
{
    return name_raw(value.c_str());
}

inline bool MeshBody::isSelectable() const
{
    bool res = isSelectable_raw();
    return res;
}

inline bool MeshBody::isSelectable(bool value)
{
    return isSelectable_raw(value);
}

inline bool MeshBody::isLightBulbOn() const
{
    bool res = isLightBulbOn_raw();
    return res;
}

inline bool MeshBody::isLightBulbOn(bool value)
{
    return isLightBulbOn_raw(value);
}

inline bool MeshBody::isVisible() const
{
    bool res = isVisible_raw();
    return res;
}

inline bool MeshBody::deleteMe()
{
    bool res = deleteMe_raw();
    return res;
}

inline core::Ptr<PolygonMesh> MeshBody::mesh() const
{
    core::Ptr<PolygonMesh> res = mesh_raw();
    return res;
}

inline core::Ptr<TriangleMesh> MeshBody::displayMesh() const
{
    core::Ptr<TriangleMesh> res = displayMesh_raw();
    return res;
}

inline core::Ptr<Component> MeshBody::parentComponent() const
{
    core::Ptr<Component> res = parentComponent_raw();
    return res;
}

inline core::Ptr<Occurrence> MeshBody::assemblyContext() const
{
    core::Ptr<Occurrence> res = assemblyContext_raw();
    return res;
}

inline core::Ptr<MeshBody> MeshBody::nativeObject() const
{
    core::Ptr<MeshBody> res = nativeObject_raw();
    return res;
}

inline core::Ptr<MeshBody> MeshBody::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<MeshBody> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}

inline core::Ptr<core::Base> MeshBody::baseOrFormFeature() const
{
    core::Ptr<core::Base> res = baseOrFormFeature_raw();
    return res;
}

inline core::Ptr<core::Attributes> MeshBody::attributes() const
{
    core::Ptr<core::Attributes> res = attributes_raw();
    return res;
}

inline core::Ptr<core::Material> MeshBody::material() const
{
    core::Ptr<core::Material> res = material_raw();
    return res;
}

inline bool MeshBody::material(const core::Ptr<core::Material>& value)
{
    return material_raw(value.get());
}

inline core::Ptr<core::Appearance> MeshBody::appearance() const
{
    core::Ptr<core::Appearance> res = appearance_raw();
    return res;
}

inline bool MeshBody::appearance(const core::Ptr<core::Appearance>& value)
{
    return appearance_raw(value.get());
}

inline core::AppearanceSourceTypes MeshBody::appearanceSourceType() const
{
    core::AppearanceSourceTypes res = appearanceSourceType_raw();
    return res;
}

inline double MeshBody::opacity() const
{
    double res = opacity_raw();
    return res;
}

inline bool MeshBody::opacity(double value)
{
    return opacity_raw(value);
}

inline double MeshBody::visibleOpacity() const
{
    double res = visibleOpacity_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_MESHBODY_API