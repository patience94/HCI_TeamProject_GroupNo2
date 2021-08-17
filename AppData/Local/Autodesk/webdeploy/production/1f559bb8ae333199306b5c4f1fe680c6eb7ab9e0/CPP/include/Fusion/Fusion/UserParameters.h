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
# ifdef __COMPILING_ADSK_FUSION_USERPARAMETERS_CPP__
# define ADSK_FUSION_USERPARAMETERS_API XI_EXPORT
# else
# define ADSK_FUSION_USERPARAMETERS_API
# endif
#else
# define ADSK_FUSION_USERPARAMETERS_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Design;
    class UserParameter;
}}
namespace adsk { namespace core {
    class ValueInput;
}}

namespace adsk { namespace fusion {

/// Provides access to the User Parameters within a design and provides
/// methods to create new user parameters.
class UserParameters : public core::Base {
public:

    /// Function that returns the specified User Parameter using an index into the collection.
    /// index : The index of the item within the collection to return. The first item in the collection
    /// has an index of 0.
    /// Returns the specified item or null if an invalid index was specified.
    core::Ptr<UserParameter> item(size_t index) const;

    /// Function that returns the specified User Parameter using the name of the parameter
    /// as it is displayed in the parameters dialog.
    /// name : The name of the User Parameter as it is displayed in the parameters dialog
    /// Returns the specified item or null if an invalid name was specified.
    core::Ptr<UserParameter> itemByName(const std::string& name) const;

    /// Returns the number of parameters in the collection.
    size_t count() const;

    /// Returns the design that owns the user parameters collection.
    core::Ptr<Design> design() const;

    /// Adds a new user parameter to the collection.
    /// name : The name of the parameter. This is the name shown in the parameters dialog
    /// value : ValueInput object that specifies the offset distance. If the ValueInput was created using
    /// a real, the value will be interpreted using the internal unit for the unit type specified by
    /// the "units" argument. For example, if the ValueInput was created using the real value 5 and
    /// the input to a "units" argument is any valid length unit the value will be interpreted at 5
    /// centimeters. If the "units" argument is a valid angle unit then the value will be interpreted
    /// as 5 radians.
    /// If the ValueInput was created using a string, the string is used as-is for the expression of
    /// the parameter. This means it must evaluate to the same unit type as that specified by the
    /// "units" argument and if no type is specified it will use the current default units specified
    /// for the current document. For example, if the ValueInput was created with the string "5 in",
    /// then the "units" argument must define any valid length so they are compatible. If the "units"
    /// argument is "cm" a parameter with the unit type of centimeter will be created and it will have
    /// the expression "5 in".
    /// When using a ValueInput created using a string, it's the same as creating a ValueInput in the
    /// user-interface. You can specify any valid expression, i.e. "5", "5 in", "5 in / 2", "5 + Length", etc.
    /// and you can choose from many different types of units. The only requirement is that the units
    /// must match in type. For example, they must both be lengths, or they must both be angles, etc.
    /// units : The units to use for the value of the parameter.
    /// Units specified must match the units specified (if any) in the ValueInput object.
    /// To create a parameter with no units you can specify either an empty string.
    /// comment : The comment to display in the parameters dialog. Specify an empty string ("") for no comment
    /// Returns the newly created UserParameter or null if the creation failed.
    core::Ptr<UserParameter> add(const std::string& name, const core::Ptr<core::ValueInput>& value, const std::string& units, const std::string& comment);

    typedef UserParameter iterable_type;
    template <class OutputIterator> void copyTo(OutputIterator result);

    ADSK_FUSION_USERPARAMETERS_API static const char* classType();
    ADSK_FUSION_USERPARAMETERS_API const char* objectType() const override;
    ADSK_FUSION_USERPARAMETERS_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_USERPARAMETERS_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual UserParameter* item_raw(size_t index) const = 0;
    virtual UserParameter* itemByName_raw(const char * name) const = 0;
    virtual size_t count_raw() const = 0;
    virtual Design* design_raw() const = 0;
    virtual UserParameter* add_raw(const char * name, core::ValueInput* value, const char * units, const char * comment) = 0;
};

// Inline wrappers

inline core::Ptr<UserParameter> UserParameters::item(size_t index) const
{
    core::Ptr<UserParameter> res = item_raw(index);
    return res;
}

inline core::Ptr<UserParameter> UserParameters::itemByName(const std::string& name) const
{
    core::Ptr<UserParameter> res = itemByName_raw(name.c_str());
    return res;
}

inline size_t UserParameters::count() const
{
    size_t res = count_raw();
    return res;
}

inline core::Ptr<Design> UserParameters::design() const
{
    core::Ptr<Design> res = design_raw();
    return res;
}

inline core::Ptr<UserParameter> UserParameters::add(const std::string& name, const core::Ptr<core::ValueInput>& value, const std::string& units, const std::string& comment)
{
    core::Ptr<UserParameter> res = add_raw(name.c_str(), value.get(), units.c_str(), comment.c_str());
    return res;
}

template <class OutputIterator> inline void UserParameters::copyTo(OutputIterator result)
{
    for (size_t i = 0;i < count();++i)
    {
        *result = item(i);
        ++result;
    }
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_USERPARAMETERS_API