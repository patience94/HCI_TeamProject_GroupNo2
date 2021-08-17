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
# ifdef __COMPILING_ADSK_FUSION_LOFTCENTERLINEORRAIL_CPP__
# define ADSK_FUSION_LOFTCENTERLINEORRAIL_API XI_EXPORT
# else
# define ADSK_FUSION_LOFTCENTERLINEORRAIL_API
# endif
#else
# define ADSK_FUSION_LOFTCENTERLINEORRAIL_API XI_IMPORT
#endif

namespace adsk { namespace fusion {

/// Represent a centerline or a single rail used by a loft feature.
class LoftCenterLineOrRail : public core::Base {
public:

    /// Indicates if this object is a loft centerline (true) or a rail (false).
    bool isCenterLine() const;

    /// Gets and sets the entitiy that defines the centerline or rail. This can be a single sketch entity,
    /// a single BRepEdge, a Path, or a Profile.
    core::Ptr<core::Base> entity() const;
    bool entity(const core::Ptr<core::Base>& value);

    /// Deletes the centerline or rail.
    /// Returns true if the operation was successful.
    bool deleteMe();

    ADSK_FUSION_LOFTCENTERLINEORRAIL_API static const char* classType();
    ADSK_FUSION_LOFTCENTERLINEORRAIL_API const char* objectType() const override;
    ADSK_FUSION_LOFTCENTERLINEORRAIL_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_LOFTCENTERLINEORRAIL_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual bool isCenterLine_raw() const = 0;
    virtual core::Base* entity_raw() const = 0;
    virtual bool entity_raw(core::Base* value) = 0;
    virtual bool deleteMe_raw() = 0;
};

// Inline wrappers

inline bool LoftCenterLineOrRail::isCenterLine() const
{
    bool res = isCenterLine_raw();
    return res;
}

inline core::Ptr<core::Base> LoftCenterLineOrRail::entity() const
{
    core::Ptr<core::Base> res = entity_raw();
    return res;
}

inline bool LoftCenterLineOrRail::entity(const core::Ptr<core::Base>& value)
{
    return entity_raw(value.get());
}

inline bool LoftCenterLineOrRail::deleteMe()
{
    bool res = deleteMe_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_LOFTCENTERLINEORRAIL_API