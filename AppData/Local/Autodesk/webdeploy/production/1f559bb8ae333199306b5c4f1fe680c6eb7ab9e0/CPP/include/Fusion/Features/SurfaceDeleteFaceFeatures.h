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

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_SURFACEDELETEFACEFEATURES_CPP__
# define ADSK_FUSION_SURFACEDELETEFACEFEATURES_API XI_EXPORT
# else
# define ADSK_FUSION_SURFACEDELETEFACEFEATURES_API
# endif
#else
# define ADSK_FUSION_SURFACEDELETEFACEFEATURES_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class SurfaceDeleteFaceFeature;
}}

namespace adsk { namespace fusion {

/// Collection that provides access to all of the existing SurfaceDeleteFaceFeature features in a component
/// and supports the ability to create new SurfaceDeleteFaceFeature features.
/// The SurfaceDeleteFaceFeature and DeleteFaceFeature differ in that the SurfaceDeleteFaceFeature
/// can delete any face without any restrictions. If the body is a solid, it will become a surface
/// when the first face is deleted. The specified face is deleted without any other changes being
/// made to the body. The DeleteFaceFeature deletes the specified face and also modifies the other faces
/// in the body to heal or fill in the area of the deleted face. This means that a solid body will
/// remain solid.
class SurfaceDeleteFaceFeatures : public core::Base {
public:

    /// Function that returns the specified SurfaceDeleteFaceFeature object using an index into the collection.
    /// index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<SurfaceDeleteFaceFeature> item(size_t index) const;

    /// Function that returns the specified SurfaceDeleteFaceFeature object using the name of the feature.
    /// name : The name of the feature within the collection to return. This is the name seen in the timeline.
    /// Returns the specified item or null if the specified name was not found.
    core::Ptr<SurfaceDeleteFaceFeature> itemByName(const std::string& name) const;

    /// The number of SurfaceDeleteFaceFeature objects in the collection.
    size_t count() const;

    /// Creates a new SurfaceDeleteFaceFeature feature. This deletes the specified faces
    /// from their bodies without any attempt to heal the openings. This is equivalent
    /// to selecting and deleting faces when in the Patch workspace.
    /// facesToDelete : A single BRepFace or an ObjectCollection containing multiple BRepFace objects.
    /// Returns the newly created SurfaceDeleteFaceFeature object or null if the creation failed.
    core::Ptr<SurfaceDeleteFaceFeature> add(const core::Ptr<core::Base>& facesToDelete);

    typedef SurfaceDeleteFaceFeature iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_SURFACEDELETEFACEFEATURES_API static const char* classType();
    ADSK_FUSION_SURFACEDELETEFACEFEATURES_API const char* objectType() const override;
    ADSK_FUSION_SURFACEDELETEFACEFEATURES_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SURFACEDELETEFACEFEATURES_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual SurfaceDeleteFaceFeature* item_raw(size_t index) const = 0;
    virtual SurfaceDeleteFaceFeature* itemByName_raw(const char * name) const = 0;
    virtual size_t count_raw() const = 0;
    virtual SurfaceDeleteFaceFeature* add_raw(core::Base* facesToDelete) = 0;
};

// Inline wrappers

inline core::Ptr<SurfaceDeleteFaceFeature> SurfaceDeleteFaceFeatures::item(size_t index) const
{
    core::Ptr<SurfaceDeleteFaceFeature> res = item_raw(index);
    return res;
}

inline core::Ptr<SurfaceDeleteFaceFeature> SurfaceDeleteFaceFeatures::itemByName(const std::string& name) const
{
    core::Ptr<SurfaceDeleteFaceFeature> res = itemByName_raw(name.c_str());
    return res;
}

inline size_t SurfaceDeleteFaceFeatures::count() const
{
    size_t res = count_raw();
    return res;
}

inline core::Ptr<SurfaceDeleteFaceFeature> SurfaceDeleteFaceFeatures::add(const core::Ptr<core::Base>& facesToDelete)
{
    core::Ptr<SurfaceDeleteFaceFeature> res = add_raw(facesToDelete.get());
    return res;
}

template <class OutputIterator> inline void SurfaceDeleteFaceFeatures::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SURFACEDELETEFACEFEATURES_API