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
#include "../../Core/Application/UnitsManager.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_FUSIONUNITSMANAGER_CPP__
# define ADSK_FUSION_FUSIONUNITSMANAGER_API XI_EXPORT
# else
# define ADSK_FUSION_FUSIONUNITSMANAGER_API
# endif
#else
# define ADSK_FUSION_FUSIONUNITSMANAGER_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Design;
}}

namespace adsk { namespace fusion {

/// Utility class used to work with Values and control default units.
/// Internal values are held in SI units (e.g. seconds, radians, kg for time, angle, mass)
/// with the exception that all lengths are in cm rather than meter and this affects derived
/// units (e.g. velocity is cm/s, volume is cm^3). Units are specified flexibly via strings
/// (e.g. "cm", "in", "inch", "cm^3", "cm*cm*cm", "mph", "mps" "m/s").
class FusionUnitsManager : public core::UnitsManager {
public:

    /// Returns the the parent design
    core::Ptr<Design> design() const;

    /// Gets and sets the default distance units for this design.
    DistanceUnits distanceDisplayUnits() const;
    bool distanceDisplayUnits(DistanceUnits value);

    ADSK_FUSION_FUSIONUNITSMANAGER_API static const char* classType();
    ADSK_FUSION_FUSIONUNITSMANAGER_API const char* objectType() const override;
    ADSK_FUSION_FUSIONUNITSMANAGER_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_FUSIONUNITSMANAGER_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual Design* design_raw() const = 0;
    virtual DistanceUnits distanceDisplayUnits_raw() const = 0;
    virtual bool distanceDisplayUnits_raw(DistanceUnits value) = 0;
};

// Inline wrappers

inline core::Ptr<Design> FusionUnitsManager::design() const
{
    core::Ptr<Design> res = design_raw();
    return res;
}

inline DistanceUnits FusionUnitsManager::distanceDisplayUnits() const
{
    DistanceUnits res = distanceDisplayUnits_raw();
    return res;
}

inline bool FusionUnitsManager::distanceDisplayUnits(DistanceUnits value)
{
    return distanceDisplayUnits_raw(value);
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_FUSIONUNITSMANAGER_API