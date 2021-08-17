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
# ifdef __COMPILING_ADSK_FUSION_PARAMETER_CPP__
# define ADSK_FUSION_PARAMETER_API XI_EXPORT
# else
# define ADSK_FUSION_PARAMETER_API
# endif
#else
# define ADSK_FUSION_PARAMETER_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class ParameterList;
}}
namespace adsk { namespace core {
    class Attributes;
}}

namespace adsk { namespace fusion {

/// The base class Parameter object that can represent model or user parameters.
class Parameter : public core::Base {
public:

    /// Gets and sets the real value (a double) of the parameter in database units.
    /// Setting this property will set/reset the expression value for this parameter
    double value() const;
    bool value(double value);

    /// Gets and sets the expression (ie. "22.064 mm") used to calculate the value of the parameter
    std::string expression() const;
    bool expression(const std::string& value);

    /// Gets and sets the name of the parameter. Setting the name can fail if the name
    /// is not unique with respect to all other parameters in the design.
    std::string name() const;
    bool name(const std::string& value);

    /// The unit type associated with this parameter. An empty string is returned for parameters
    /// that don't have a unit type.
    std::string unit() const;

    /// The comment associated with this parameter
    std::string comment() const;
    bool comment(const std::string& value);

    /// Gets and sets whether this parameter is included in the Favorites list in the
    /// parameters dialog
    bool isFavorite() const;
    bool isFavorite(bool value);

    /// Returns a list of parameters that are dependent on this parameter as a result
    /// of this parameter being referenced in their equation.
    core::Ptr<ParameterList> dependentParameters() const;

    /// Gets if this parameter can be deleted. Parameters that cannot be deleted are: Model Parameters and
    /// User Parameters that have dependents.
    bool isDeletable() const;

    /// Returns the collection of attributes associated with this face.
    core::Ptr<core::Attributes> attributes() const;

    ADSK_FUSION_PARAMETER_API static const char* classType();
    ADSK_FUSION_PARAMETER_API const char* objectType() const override;
    ADSK_FUSION_PARAMETER_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_PARAMETER_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual double value_raw() const = 0;
    virtual bool value_raw(double value) = 0;
    virtual char* expression_raw() const = 0;
    virtual bool expression_raw(const char * value) = 0;
    virtual char* name_raw() const = 0;
    virtual bool name_raw(const char * value) = 0;
    virtual char* unit_raw() const = 0;
    virtual char* comment_raw() const = 0;
    virtual bool comment_raw(const char * value) = 0;
    virtual bool isFavorite_raw() const = 0;
    virtual bool isFavorite_raw(bool value) = 0;
    virtual ParameterList* dependentParameters_raw() const = 0;
    virtual bool isDeletable_raw() const = 0;
    virtual core::Attributes* attributes_raw() const = 0;
    virtual void placeholderParameter0() {}
    virtual void placeholderParameter1() {}
    virtual void placeholderParameter2() {}
    virtual void placeholderParameter3() {}
    virtual void placeholderParameter4() {}
    virtual void placeholderParameter5() {}
    virtual void placeholderParameter6() {}
    virtual void placeholderParameter7() {}
    virtual void placeholderParameter8() {}
    virtual void placeholderParameter9() {}
    virtual void placeholderParameter10() {}
    virtual void placeholderParameter11() {}
    virtual void placeholderParameter12() {}
    virtual void placeholderParameter13() {}
    virtual void placeholderParameter14() {}
    virtual void placeholderParameter15() {}
    virtual void placeholderParameter16() {}
    virtual void placeholderParameter17() {}
};

// Inline wrappers

inline double Parameter::value() const
{
    double res = value_raw();
    return res;
}

inline bool Parameter::value(double value)
{
    return value_raw(value);
}

inline std::string Parameter::expression() const
{
    std::string res;

    char* p= expression_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Parameter::expression(const std::string& value)
{
    return expression_raw(value.c_str());
}

inline std::string Parameter::name() const
{
    std::string res;

    char* p= name_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Parameter::name(const std::string& value)
{
    return name_raw(value.c_str());
}

inline std::string Parameter::unit() const
{
    std::string res;

    char* p= unit_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline std::string Parameter::comment() const
{
    std::string res;

    char* p= comment_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool Parameter::comment(const std::string& value)
{
    return comment_raw(value.c_str());
}

inline bool Parameter::isFavorite() const
{
    bool res = isFavorite_raw();
    return res;
}

inline bool Parameter::isFavorite(bool value)
{
    return isFavorite_raw(value);
}

inline core::Ptr<ParameterList> Parameter::dependentParameters() const
{
    core::Ptr<ParameterList> res = dependentParameters_raw();
    return res;
}

inline bool Parameter::isDeletable() const
{
    bool res = isDeletable_raw();
    return res;
}

inline core::Ptr<core::Attributes> Parameter::attributes() const
{
    core::Ptr<core::Attributes> res = attributes_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_PARAMETER_API