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
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_DELETEFACEFEATURE_CPP__
# define ADSK_FUSION_DELETEFACEFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_DELETEFACEFEATURE_API
# endif
#else
# define ADSK_FUSION_DELETEFACEFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class BRepFace;
    class Occurrence;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing DeleteFaceFeature object in a design.
/// The SurfaceDeleteFaceFeature and DeleteFaceFeature differ in that the SurfaceDeleteFaceFeature
/// can delete any face without any restrictions. If the body is a solid, it will become a surface
/// when the first face is deleted. The specified face is deleted without any other changes being
/// made to the body. The DeleteFaceFeature deletes the specified face and also modifies the other faces
/// in the body to heal or fill in the area of the deleted face. This means that a solid body will
/// remain solid.
class DeleteFaceFeature : public Feature {
public:

    /// Gets and sets the set of faces that are deleted by this feature. To
    /// be able to use this property to both get and set the faces, you need to
    /// first roll the timeline to immediately before this feature. This can be
    /// accomplished using the following code where thisFeature is a reference
    /// to a DeleteFaceFeature:
    /// thisFeature.timelineObject.rollTo(True)
    /// Setting this property can fail if Fusion 360 is unable to heal the body after
    /// deleting the specified faces.
    std::vector<core::Ptr<BRepFace>> deletedFaces() const;
    bool deletedFaces(const std::vector<core::Ptr<BRepFace>>& value);

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<DeleteFaceFeature> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this is not the NativeObject.
    core::Ptr<DeleteFaceFeature> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_DELETEFACEFEATURE_API static const char* classType();
    ADSK_FUSION_DELETEFACEFEATURE_API const char* objectType() const override;
    ADSK_FUSION_DELETEFACEFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_DELETEFACEFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual BRepFace** deletedFaces_raw(size_t& return_size) const = 0;
    virtual bool deletedFaces_raw(BRepFace** value, size_t value_size) = 0;
    virtual DeleteFaceFeature* nativeObject_raw() const = 0;
    virtual DeleteFaceFeature* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline std::vector<core::Ptr<BRepFace>> DeleteFaceFeature::deletedFaces() const
{
    std::vector<core::Ptr<BRepFace>> res;
    size_t s;

    BRepFace** p= deletedFaces_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline bool DeleteFaceFeature::deletedFaces(const std::vector<core::Ptr<BRepFace>>& value)
{
    BRepFace** value_ = new BRepFace*[value.size()];
    for(size_t i=0; i<value.size(); ++i)
        value_[i] = value[i].get();

    bool res = deletedFaces_raw(value_, value.size());
    delete[] value_;
    return res;
}

inline core::Ptr<DeleteFaceFeature> DeleteFaceFeature::nativeObject() const
{
    core::Ptr<DeleteFaceFeature> res = nativeObject_raw();
    return res;
}

inline core::Ptr<DeleteFaceFeature> DeleteFaceFeature::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<DeleteFaceFeature> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_DELETEFACEFEATURE_API