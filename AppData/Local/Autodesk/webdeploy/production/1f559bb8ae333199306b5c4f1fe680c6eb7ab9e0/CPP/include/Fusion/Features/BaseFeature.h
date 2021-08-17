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
# ifdef __COMPILING_ADSK_FUSION_BASEFEATURE_CPP__
# define ADSK_FUSION_BASEFEATURE_API XI_EXPORT
# else
# define ADSK_FUSION_BASEFEATURE_API
# endif
#else
# define ADSK_FUSION_BASEFEATURE_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class ConstructionAxis;
    class ConstructionPlane;
    class ConstructionPoint;
    class MeshBody;
    class Sketch;
}}

namespace adsk { namespace fusion {

/// The BaseFeature class represents a direct edit feature within a parametric design.
class BaseFeature : public Feature {
public:

    /// Returns an array of the construction planes associated with this base feature.
    std::vector<core::Ptr<ConstructionPlane>> constructionPlanes() const;

    /// Returns an array of the construction axes associated with this base feature.
    std::vector<core::Ptr<ConstructionAxis>> constructionAxes() const;

    /// Returns an array of the construction points associated with this base feature.
    std::vector<core::Ptr<ConstructionPoint>> constructionPoints() const;

    /// Returns an array of the sketches associated with this base feature.
    std::vector<core::Ptr<Sketch>> sketches() const;

    /// Returns an array of the mesh bodies associated with this base feature.
    std::vector<core::Ptr<MeshBody>> meshBodies() const;

    /// Set the user-interface so that the base body is in edit mode.
    /// Returns true if successful.
    bool startEdit();

    /// Exits from edit mode in the user-interface. If this base feature in not
    /// in edit mode, then nothing happens.
    /// Returns true if successful.
    bool finishEdit();

    ADSK_FUSION_BASEFEATURE_API static const char* classType();
    ADSK_FUSION_BASEFEATURE_API const char* objectType() const override;
    ADSK_FUSION_BASEFEATURE_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_BASEFEATURE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual ConstructionPlane** constructionPlanes_raw(size_t& return_size) const = 0;
    virtual ConstructionAxis** constructionAxes_raw(size_t& return_size) const = 0;
    virtual ConstructionPoint** constructionPoints_raw(size_t& return_size) const = 0;
    virtual Sketch** sketches_raw(size_t& return_size) const = 0;
    virtual MeshBody** meshBodies_raw(size_t& return_size) const = 0;
    virtual bool startEdit_raw() = 0;
    virtual bool finishEdit_raw() = 0;
};

// Inline wrappers

inline std::vector<core::Ptr<ConstructionPlane>> BaseFeature::constructionPlanes() const
{
    std::vector<core::Ptr<ConstructionPlane>> res;
    size_t s;

    ConstructionPlane** p= constructionPlanes_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<core::Ptr<ConstructionAxis>> BaseFeature::constructionAxes() const
{
    std::vector<core::Ptr<ConstructionAxis>> res;
    size_t s;

    ConstructionAxis** p= constructionAxes_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<core::Ptr<ConstructionPoint>> BaseFeature::constructionPoints() const
{
    std::vector<core::Ptr<ConstructionPoint>> res;
    size_t s;

    ConstructionPoint** p= constructionPoints_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<core::Ptr<Sketch>> BaseFeature::sketches() const
{
    std::vector<core::Ptr<Sketch>> res;
    size_t s;

    Sketch** p= sketches_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<core::Ptr<MeshBody>> BaseFeature::meshBodies() const
{
    std::vector<core::Ptr<MeshBody>> res;
    size_t s;

    MeshBody** p= meshBodies_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}

inline bool BaseFeature::startEdit()
{
    bool res = startEdit_raw();
    return res;
}

inline bool BaseFeature::finishEdit()
{
    bool res = finishEdit_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_BASEFEATURE_API