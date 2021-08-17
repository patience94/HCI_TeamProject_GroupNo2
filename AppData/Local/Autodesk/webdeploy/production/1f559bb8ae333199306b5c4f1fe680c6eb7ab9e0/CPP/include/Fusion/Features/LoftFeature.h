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
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_LOFTFEATURE_CPP__
# define ADSK_FUSION_LOFTFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_LOFTFEATURE_API
# endif
#else
# define ADSK_FUSION_LOFTFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BRepBody;
    class BRepFace;
    class BRepFaces;
    class LoftCenterLineOrRails;
    class LoftSections;
    class Occurrence;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing loft feature in a design.
class LoftFeature : public Feature {
public:

    /// Returns the set of sections that the loft passes through.
    /// This property returns null in the case where the feature is non-parametric.
    core::Ptr<LoftSections> loftSections() const;

    /// Returns the single centerline or the set of rails that define the shape of the loft.
    /// This property returns null in the case where the feature is non-parametric.
    core::Ptr<LoftCenterLineOrRails> centerLineOrRails() const;

    /// Property that returns the face that caps the start of the loft and is coincident
    /// with the first section. In the case where the loft isn't capped and there isn't
    /// a start face, this property will return null.
    core::Ptr<BRepFace> startFace() const;

    /// Property that returns the face that caps the end of the loft and is coincident
    /// with the last section. In the case where the loft isn't capped and there isn't an end face,
    /// this property will return null.
    core::Ptr<BRepFace> endFace() const;

    /// Property that returns all of the side faces (i.e. those running through the sections)
    /// of the feature.
    core::Ptr<BRepFaces> sideFaces() const;

    /// Gets and sets the type of operation performed by the extrusion.
    FeatureOperations operation() const;
    bool operation(FeatureOperations value);

    /// Indicates if this feature was initially created as a solid or a surface.
    bool isSolid() const;

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<LoftFeature> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<LoftFeature> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    /// Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection.
    /// When setting or getting this property, you must roll the timeline back to just before the feature
    /// so that the model is in the state just before the feature is computed.
    std::vector<core::Ptr<BRepBody>> participantBodies() const;
    bool participantBodies(const std::vector<core::Ptr<BRepBody>>& value);

    ADSK_FUSION_LOFTFEATURE_API static const char* classType();
    ADSK_FUSION_LOFTFEATURE_API const char* objectType() const override;
    ADSK_FUSION_LOFTFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_LOFTFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual LoftSections* loftSections_raw() const = 0;
    virtual LoftCenterLineOrRails* centerLineOrRails_raw() const = 0;
    virtual BRepFace* startFace_raw() const = 0;
    virtual BRepFace* endFace_raw() const = 0;
    virtual BRepFaces* sideFaces_raw() const = 0;
    virtual FeatureOperations operation_raw() const = 0;
    virtual bool operation_raw(FeatureOperations value) = 0;
    virtual bool isSolid_raw() const = 0;
    virtual LoftFeature* nativeObject_raw() const = 0;
    virtual LoftFeature* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
    virtual BRepBody** participantBodies_raw(size_t& return_size) const = 0;
    virtual bool participantBodies_raw(BRepBody** value, size_t value_size) = 0;
};

// Inline wrappers

inline core::Ptr<LoftSections> LoftFeature::loftSections() const
{
    core::Ptr<LoftSections> res = loftSections_raw();
    return res;
}

inline core::Ptr<LoftCenterLineOrRails> LoftFeature::centerLineOrRails() const
{
    core::Ptr<LoftCenterLineOrRails> res = centerLineOrRails_raw();
    return res;
}

inline core::Ptr<BRepFace> LoftFeature::startFace() const
{
    core::Ptr<BRepFace> res = startFace_raw();
    return res;
}

inline core::Ptr<BRepFace> LoftFeature::endFace() const
{
    core::Ptr<BRepFace> res = endFace_raw();
    return res;
}

inline core::Ptr<BRepFaces> LoftFeature::sideFaces() const
{
    core::Ptr<BRepFaces> res = sideFaces_raw();
    return res;
}

inline FeatureOperations LoftFeature::operation() const
{
    FeatureOperations res = operation_raw();
    return res;
}

inline bool LoftFeature::operation(FeatureOperations value)
{
    return operation_raw(value);
}

inline bool LoftFeature::isSolid() const
{
    bool res = isSolid_raw();
    return res;
}

inline core::Ptr<LoftFeature> LoftFeature::nativeObject() const
{
    core::Ptr<LoftFeature> res = nativeObject_raw();
    return res;
}

inline core::Ptr<LoftFeature> LoftFeature::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<LoftFeature> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}

inline std::vector<core::Ptr<BRepBody>> LoftFeature::participantBodies() const
{
    std::vector<core::Ptr<BRepBody>> res;
    size_t s;

    BRepBody** p= participantBodies_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline bool LoftFeature::participantBodies(const std::vector<core::Ptr<BRepBody>>& value)
{
    BRepBody** value_ = new BRepBody*[value.size()];
    for(size_t i=0; i<value.size(); ++i)
        value_[i] = value[i].get();

    bool res = participantBodies_raw(value_, value.size());
    delete[] value_;
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_LOFTFEATURE_API