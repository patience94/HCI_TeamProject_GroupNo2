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
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_THREADDATAQUERY_CPP__
# define ADSK_FUSION_THREADDATAQUERY_API XI_EXPORT
# else
# define ADSK_FUSION_THREADDATAQUERY_API
# endif
#else
# define ADSK_FUSION_THREADDATAQUERY_API XI_IMPORT
#endif

namespace adsk { namespace fusion {

/// This object provides methods to query the thread data contained in the XML files under ThreadData folder.
class ThreadDataQuery : public core::Base {
public:

    /// Gets all the available thread types (families).
    std::vector<std::string> allThreadTypes() const;

    /// Method that returns all the available thread sizes for a given thread type.
    /// threadType : Specify the thread type.
    /// Returns the specified thread sizes or empty array if an invalid thread type was specified.
    std::vector<std::string> allSizes(const std::string& threadType) const;

    /// Method that returns all the available thread designations for a thread type of a given size.
    /// threadType : Specify the thread type.
    /// size : Specify the thread size.
    /// Returns the specified thread designations or empty array if an invalid thread type or size was specified.
    std::vector<std::string> allDesignations(const std::string& threadType, const std::string& size) const;

    /// Method that returns all the available classes for a thread type of a given thread designation.
    /// isInternal : Indicates if the thread is an internal or external thread.
    /// threadType : Specify the thread type.
    /// designation : Specify the thread designation.
    /// Returns the specified thread classes or empty array if an invalid thread type or designation was specified.
    std::vector<std::string> allClasses(bool isInternal, const std::string& threadType, const std::string& designation) const;

    /// Method that returns the custom name for a given thread type.
    /// threadType : Thread type identifier string.
    /// Returns the specified custom name or empty string if an invalid thread type was specified.
    std::string threadTypeCustomName(const std::string& threadType) const;

    /// Method that returns the unit for a given thread type.
    /// threadType : Specify the thread type.
    /// Returns the specified unit or empty string if an invalid thread type was specified.
    std::string threadTypeUnit(const std::string& threadType) const;

    /// Method that gets the recommended thread data for a given model diameter.
    /// modelDiameter : The model diameter. The unit is centimeter.
    /// isInternal : Indicates if the thread is an internal or external thread.
    /// threadType : Specifies the thread type to query the thread data.
    /// designation : The output thread designation.
    /// threadClass : The output thread class.
    /// Returns true if successful.
    bool recommendThreadData(double modelDiameter, bool isInternal, const std::string& threadType, std::string& designation, std::string& threadClass) const;

    /// Gets the default inch thread type.
    std::string defaultInchThreadType() const;

    /// Gets the default metric thread type.
    std::string defaultMetricThreadType() const;

    ADSK_FUSION_THREADDATAQUERY_API static const char* classType();
    ADSK_FUSION_THREADDATAQUERY_API const char* objectType() const override;
    ADSK_FUSION_THREADDATAQUERY_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_THREADDATAQUERY_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual char** allThreadTypes_raw(size_t& return_size) const = 0;
    virtual char** allSizes_raw(const char * threadType, size_t& return_size) const = 0;
    virtual char** allDesignations_raw(const char * threadType, const char * size, size_t& return_size) const = 0;
    virtual char** allClasses_raw(bool isInternal, const char * threadType, const char * designation, size_t& return_size) const = 0;
    virtual char* threadTypeCustomName_raw(const char * threadType) const = 0;
    virtual char* threadTypeUnit_raw(const char * threadType) const = 0;
    virtual bool recommendThreadData_raw(double modelDiameter, bool isInternal, const char * threadType, char*& designation, char*& threadClass) const = 0;
    virtual char* defaultInchThreadType_raw() const = 0;
    virtual char* defaultMetricThreadType_raw() const = 0;
};

// Inline wrappers

inline std::vector<std::string> ThreadDataQuery::allThreadTypes() const
{
    std::vector<std::string> res;
    size_t s;

    char** p= allThreadTypes_raw(s);
    if(p)
    {
        res.resize(s);
        for(size_t i=0; i<s; ++i)
        {
            char* pChar = p[i];
            if(pChar)
                res[i] = pChar;
            core::DeallocateArray(pChar);
        }
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<std::string> ThreadDataQuery::allSizes(const std::string& threadType) const
{
    std::vector<std::string> res;
    size_t s;

    char** p= allSizes_raw(threadType.c_str(), s);
    if(p)
    {
        res.resize(s);
        for(size_t i=0; i<s; ++i)
        {
            char* pChar = p[i];
            if(pChar)
                res[i] = pChar;
            core::DeallocateArray(pChar);
        }
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<std::string> ThreadDataQuery::allDesignations(const std::string& threadType, const std::string& size) const
{
    std::vector<std::string> res;
    size_t s;

    char** p= allDesignations_raw(threadType.c_str(), size.c_str(), s);
    if(p)
    {
        res.resize(s);
        for(size_t i=0; i<s; ++i)
        {
            char* pChar = p[i];
            if(pChar)
                res[i] = pChar;
            core::DeallocateArray(pChar);
        }
        core::DeallocateArray(p);
    }
    return res;
}

inline std::vector<std::string> ThreadDataQuery::allClasses(bool isInternal, const std::string& threadType, const std::string& designation) const
{
    std::vector<std::string> res;
    size_t s;

    char** p= allClasses_raw(isInternal, threadType.c_str(), designation.c_str(), s);
    if(p)
    {
        res.resize(s);
        for(size_t i=0; i<s; ++i)
        {
            char* pChar = p[i];
            if(pChar)
                res[i] = pChar;
            core::DeallocateArray(pChar);
        }
        core::DeallocateArray(p);
    }
    return res;
}

inline std::string ThreadDataQuery::threadTypeCustomName(const std::string& threadType) const
{
    std::string res;

    char* p= threadTypeCustomName_raw(threadType.c_str());
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline std::string ThreadDataQuery::threadTypeUnit(const std::string& threadType) const
{
    std::string res;

    char* p= threadTypeUnit_raw(threadType.c_str());
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool ThreadDataQuery::recommendThreadData(double modelDiameter, bool isInternal, const std::string& threadType, std::string& designation, std::string& threadClass) const
{
    char* designation_ = nullptr;
    char* threadClass_ = nullptr;

    bool res = recommendThreadData_raw(modelDiameter, isInternal, threadType.c_str(), designation_, threadClass_);
    designation = designation_;
    core::DeallocateArray(designation_);
    threadClass = threadClass_;
    core::DeallocateArray(threadClass_);
    return res;
}

inline std::string ThreadDataQuery::defaultInchThreadType() const
{
    std::string res;

    char* p= defaultInchThreadType_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline std::string ThreadDataQuery::defaultMetricThreadType() const
{
    std::string res;

    char* p= defaultMetricThreadType_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_THREADDATAQUERY_API