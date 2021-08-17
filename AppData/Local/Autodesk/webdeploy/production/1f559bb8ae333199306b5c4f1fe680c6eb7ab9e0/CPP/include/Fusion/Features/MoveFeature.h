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
# ifdef __COMPILING_ADSK_FUSION_MOVEFEATURE_CPP__
# define ADSK_FUSION_MOVEFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_MOVEFEATURE_API
# endif
#else
# define ADSK_FUSION_MOVEFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Occurrence;
}}
namespace adsk { namespace core {
    class Matrix3D;
    class ObjectCollection;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing move feature in a design.
class MoveFeature : public Feature {
public:

    /// Gets and sets the entities to move.
    /// This collection can only contain BRepBody objects in parametric modeling.
    core::Ptr<core::ObjectCollection> inputEntities() const;
    bool inputEntities(const core::Ptr<core::ObjectCollection>& value);

    /// Gets and sets the move transform of the input bodies.
    core::Ptr<core::Matrix3D> transform() const;
    bool transform(const core::Ptr<core::Matrix3D>& value);

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<MoveFeature> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<MoveFeature> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_MOVEFEATURE_API static const char* classType();
    ADSK_FUSION_MOVEFEATURE_API const char* objectType() const override;
    ADSK_FUSION_MOVEFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_MOVEFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::ObjectCollection* inputEntities_raw() const = 0;
    virtual bool inputEntities_raw(core::ObjectCollection* value) = 0;
    virtual core::Matrix3D* transform_raw() const = 0;
    virtual bool transform_raw(core::Matrix3D* value) = 0;
    virtual MoveFeature* nativeObject_raw() const = 0;
    virtual MoveFeature* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline core::Ptr<core::ObjectCollection> MoveFeature::inputEntities() const
{
    core::Ptr<core::ObjectCollection> res = inputEntities_raw();
    return res;
}

inline bool MoveFeature::inputEntities(const core::Ptr<core::ObjectCollection>& value)
{
    return inputEntities_raw(value.get());
}

inline core::Ptr<core::Matrix3D> MoveFeature::transform() const
{
    core::Ptr<core::Matrix3D> res = transform_raw();
    return res;
}

inline bool MoveFeature::transform(const core::Ptr<core::Matrix3D>& value)
{
    return transform_raw(value.get());
}

inline core::Ptr<MoveFeature> MoveFeature::nativeObject() const
{
    core::Ptr<MoveFeature> res = nativeObject_raw();
    return res;
}

inline core::Ptr<MoveFeature> MoveFeature::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<MoveFeature> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_MOVEFEATURE_API