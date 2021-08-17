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
#include "Feature.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_REVERSENORMALFEATURE_CPP__
# define ADSK_FUSION_REVERSENORMALFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_REVERSENORMALFEATURE_API
# endif
#else
# define ADSK_FUSION_REVERSENORMALFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Occurrence;
}}
namespace adsk { namespace core {
    class ObjectCollection;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing Reverse Normal feature in a design.
class ReverseNormalFeature : public Feature {
public:

    /// Gets and sets the surface bodies (open BRepBodies) whose faces normals are to be reversed.
    /// All faces of the input surface bodies get reversed.
    core::Ptr<core::ObjectCollection> surfaces() const;
    bool surfaces(const core::Ptr<core::ObjectCollection>& value);

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<ReverseNormalFeature> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this is not the NativeObject.
    core::Ptr<ReverseNormalFeature> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_REVERSENORMALFEATURE_API static const char* classType();
    ADSK_FUSION_REVERSENORMALFEATURE_API const char* objectType() const override;
    ADSK_FUSION_REVERSENORMALFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_REVERSENORMALFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::ObjectCollection* surfaces_raw() const = 0;
    virtual bool surfaces_raw(core::ObjectCollection* value) = 0;
    virtual ReverseNormalFeature* nativeObject_raw() const = 0;
    virtual ReverseNormalFeature* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline core::Ptr<core::ObjectCollection> ReverseNormalFeature::surfaces() const
{
    core::Ptr<core::ObjectCollection> res = surfaces_raw();
    return res;
}

inline bool ReverseNormalFeature::surfaces(const core::Ptr<core::ObjectCollection>& value)
{
    return surfaces_raw(value.get());
}

inline core::Ptr<ReverseNormalFeature> ReverseNormalFeature::nativeObject() const
{
    core::Ptr<ReverseNormalFeature> res = nativeObject_raw();
    return res;
}

inline core::Ptr<ReverseNormalFeature> ReverseNormalFeature::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<ReverseNormalFeature> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_REVERSENORMALFEATURE_API