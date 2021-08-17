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
# ifdef __COMPILING_ADSK_FUSION_FILLETFEATURE_CPP__
# define ADSK_FUSION_FILLETFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_FILLETFEATURE_API
# endif
#else
# define ADSK_FUSION_FILLETFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class FilletEdgeSets;
    class Occurrence;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing fillet feature in a design.
class FilletFeature : public Feature {
public:

    /// Returns the edge sets associated with this fillet.
    core::Ptr<FilletEdgeSets> edgeSets() const;

    /// Gets and sets if the fillet uses the G2 (curvature-continuity) surface quality option .
    bool isG2() const;
    bool isG2(bool value);

    /// Gets and sets if a rolling ball solution is to be used in any corners.
    bool isRollingBallCorner() const;
    bool isRollingBallCorner(bool value);

    /// Gets and sets whether or not edges that are tangentially connected to
    /// the input edges (if any) will also be filleted.
    bool isTangentChain() const;
    bool isTangentChain(bool value);

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of its parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<FilletFeature> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<FilletFeature> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_FILLETFEATURE_API static const char* classType();
    ADSK_FUSION_FILLETFEATURE_API const char* objectType() const override;
    ADSK_FUSION_FILLETFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_FILLETFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual FilletEdgeSets* edgeSets_raw() const = 0;
    virtual bool isG2_raw() const = 0;
    virtual bool isG2_raw(bool value) = 0;
    virtual bool isRollingBallCorner_raw() const = 0;
    virtual bool isRollingBallCorner_raw(bool value) = 0;
    virtual bool isTangentChain_raw() const = 0;
    virtual bool isTangentChain_raw(bool value) = 0;
    virtual FilletFeature* nativeObject_raw() const = 0;
    virtual FilletFeature* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline core::Ptr<FilletEdgeSets> FilletFeature::edgeSets() const
{
    core::Ptr<FilletEdgeSets> res = edgeSets_raw();
    return res;
}

inline bool FilletFeature::isG2() const
{
    bool res = isG2_raw();
    return res;
}

inline bool FilletFeature::isG2(bool value)
{
    return isG2_raw(value);
}

inline bool FilletFeature::isRollingBallCorner() const
{
    bool res = isRollingBallCorner_raw();
    return res;
}

inline bool FilletFeature::isRollingBallCorner(bool value)
{
    return isRollingBallCorner_raw(value);
}

inline bool FilletFeature::isTangentChain() const
{
    bool res = isTangentChain_raw();
    return res;
}

inline bool FilletFeature::isTangentChain(bool value)
{
    return isTangentChain_raw(value);
}

inline core::Ptr<FilletFeature> FilletFeature::nativeObject() const
{
    core::Ptr<FilletFeature> res = nativeObject_raw();
    return res;
}

inline core::Ptr<FilletFeature> FilletFeature::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<FilletFeature> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_FILLETFEATURE_API