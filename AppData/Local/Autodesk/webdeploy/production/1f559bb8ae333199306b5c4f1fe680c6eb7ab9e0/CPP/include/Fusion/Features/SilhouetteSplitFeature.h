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
#include "Feature.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_SILHOUETTESPLITFEATURE_CPP__
# define ADSK_FUSION_SILHOUETTESPLITFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_SILHOUETTESPLITFEATURE_API
# endif
#else
# define ADSK_FUSION_SILHOUETTESPLITFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BRepBody;
    class Occurrence;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing silhouette split feature in a design.
class SilhouetteSplitFeature : public Feature {
public:

    /// Gets and sets the entity that defines the silhouette view direction, which can be a
    /// construction axis, linear BRepEdge, planar BRepFace or a construction plane.
    core::Ptr<core::Base> viewDirection() const;
    bool viewDirection(const core::Ptr<core::Base>& value);

    /// Gets and sets the solid body to split.
    core::Ptr<BRepBody> targetBody() const;
    bool targetBody(const core::Ptr<BRepBody>& value);

    /// Gets the type of silhouette split operation.
    SilhouetteSplitOperations operation() const;

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<SilhouetteSplitFeature> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this is not the NativeObject.
    core::Ptr<SilhouetteSplitFeature> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_SILHOUETTESPLITFEATURE_API static const char* classType();
    ADSK_FUSION_SILHOUETTESPLITFEATURE_API const char* objectType() const override;
    ADSK_FUSION_SILHOUETTESPLITFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SILHOUETTESPLITFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::Base* viewDirection_raw() const = 0;
    virtual bool viewDirection_raw(core::Base* value) = 0;
    virtual BRepBody* targetBody_raw() const = 0;
    virtual bool targetBody_raw(BRepBody* value) = 0;
    virtual SilhouetteSplitOperations operation_raw() const = 0;
    virtual SilhouetteSplitFeature* nativeObject_raw() const = 0;
    virtual SilhouetteSplitFeature* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline core::Ptr<core::Base> SilhouetteSplitFeature::viewDirection() const
{
    core::Ptr<core::Base> res = viewDirection_raw();
    return res;
}

inline bool SilhouetteSplitFeature::viewDirection(const core::Ptr<core::Base>& value)
{
    return viewDirection_raw(value.get());
}

inline core::Ptr<BRepBody> SilhouetteSplitFeature::targetBody() const
{
    core::Ptr<BRepBody> res = targetBody_raw();
    return res;
}

inline bool SilhouetteSplitFeature::targetBody(const core::Ptr<BRepBody>& value)
{
    return targetBody_raw(value.get());
}

inline SilhouetteSplitOperations SilhouetteSplitFeature::operation() const
{
    SilhouetteSplitOperations res = operation_raw();
    return res;
}

inline core::Ptr<SilhouetteSplitFeature> SilhouetteSplitFeature::nativeObject() const
{
    core::Ptr<SilhouetteSplitFeature> res = nativeObject_raw();
    return res;
}

inline core::Ptr<SilhouetteSplitFeature> SilhouetteSplitFeature::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<SilhouetteSplitFeature> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SILHOUETTESPLITFEATURE_API