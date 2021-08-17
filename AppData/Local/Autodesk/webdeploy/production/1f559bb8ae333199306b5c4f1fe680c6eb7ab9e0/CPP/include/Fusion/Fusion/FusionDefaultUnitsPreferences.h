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
#include "../../Core/Application/DefaultUnitsPreferences.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_FUSIONDEFAULTUNITSPREFERENCES_CPP__
# define ADSK_FUSION_FUSIONDEFAULTUNITSPREFERENCES_API XI_EXPORT
# else
# define ADSK_FUSION_FUSIONDEFAULTUNITSPREFERENCES_API
# endif
#else
# define ADSK_FUSION_FUSIONDEFAULTUNITSPREFERENCES_API XI_IMPORT
#endif

namespace adsk { namespace fusion {

/// Fusion 360 Default Units for Design Preferences
class FusionDefaultUnitsPreferences : public core::DefaultUnitsPreferences {
public:

    /// Gets and sets the default units for length when creating a new Fusion 360 file.
    DistanceUnits distanceDisplayUnits() const;
    bool distanceDisplayUnits(DistanceUnits value);

    ADSK_FUSION_FUSIONDEFAULTUNITSPREFERENCES_API static const char* classType();
    ADSK_FUSION_FUSIONDEFAULTUNITSPREFERENCES_API const char* objectType() const override;
    ADSK_FUSION_FUSIONDEFAULTUNITSPREFERENCES_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_FUSIONDEFAULTUNITSPREFERENCES_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual DistanceUnits distanceDisplayUnits_raw() const = 0;
    virtual bool distanceDisplayUnits_raw(DistanceUnits value) = 0;
};

// Inline wrappers

inline DistanceUnits FusionDefaultUnitsPreferences::distanceDisplayUnits() const
{
    DistanceUnits res = distanceDisplayUnits_raw();
    return res;
}

inline bool FusionDefaultUnitsPreferences::distanceDisplayUnits(DistanceUnits value)
{
    return distanceDisplayUnits_raw(value);
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_FUSIONDEFAULTUNITSPREFERENCES_API