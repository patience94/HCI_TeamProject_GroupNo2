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
#include "../CAMTypeDefs.h"
#include <string>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef CAMXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_CAM_MACHINE_CPP__
# define ADSK_CAM_MACHINE_API XI_EXPORT
# else
# define ADSK_CAM_MACHINE_API
# endif
#else
# define ADSK_CAM_MACHINE_API XI_IMPORT
#endif

namespace adsk { namespace cam {

/// Object that represents an existing Machine.
class Machine : public core::Base {
public:

    /// Gets and sets the vendor name of the machine.
    std::string vendor() const;
    bool vendor(const std::string& value);

    /// Gets and sets the model name of the machine.
    std::string model() const;
    bool model(const std::string& value);

    /// Gets and sets the description of the machine.
    std::string description() const;
    bool description(const std::string& value);

    /// Gets the identifier of the machine.
    std::string id() const;

    ADSK_CAM_MACHINE_API static const char* classType();
    ADSK_CAM_MACHINE_API const char* objectType() const override;
    ADSK_CAM_MACHINE_API void* queryInterface(const char* id) const override;
    ADSK_CAM_MACHINE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual char* vendor_raw() const = 0;
    virtual bool vendor_raw(const char * value) = 0;
    virtual char* model_raw() const = 0;
    virtual bool model_raw(const char * value) = 0;
    virtual char* description_raw() const = 0;
    virtual bool description_raw(const char * value) = 0;
    virtual char* id_raw() const = 0;
};

// Inline wrappers

inline std::string Machine::vendor() const
{
    std::string res;

    char* p= vendor_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Machine::vendor(const std::string& value)
{
    return vendor_raw(value.c_str());
}

inline std::string Machine::model() const
{
    std::string res;

    char* p= model_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Machine::model(const std::string& value)
{
    return model_raw(value.c_str());
}

inline std::string Machine::description() const
{
    std::string res;

    char* p= description_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Machine::description(const std::string& value)
{
    return description_raw(value.c_str());
}

inline std::string Machine::id() const
{
    std::string res;

    char* p= id_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}
}// namespace cam
}// namespace adsk

#undef ADSK_CAM_MACHINE_API