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
# ifdef __COMPILING_ADSK_CAM_OPERATIONBASE_CPP__
# define ADSK_CAM_OPERATIONBASE_API XI_EXPORT
# else
# define ADSK_CAM_OPERATIONBASE_API
# endif
#else
# define ADSK_CAM_OPERATIONBASE_API XI_IMPORT
#endif

namespace adsk { namespace cam {
    class CAMParameters;
    class Setup;
}}

namespace adsk { namespace cam {

/// Base class object representing all operations, folders, patterns and setups.
class OperationBase : public core::Base {
public:

    /// Gets and sets the name of the operation as seen in the browser. This name is unique as compared
    /// to the names of all other operations in the document.
    std::string name() const;
    bool name(const std::string& value);

    /// Gets and sets the "protected" property value of the operation.
    /// Gets/sets true if the operation is protected.
    bool isProtected() const;
    bool isProtected(bool value);

    /// Gets and sets the "Optional" property value of the operation.
    /// Gets/sets true if the operation is optional.
    bool isOptional() const;
    bool isOptional(bool value);

    /// Gets and sets the "Suppressed" property value of the operation.
    /// Gets/sets true if the operation is suppressed.
    bool isSuppressed() const;
    bool isSuppressed(bool value);

    /// Gets the Setup this operation belongs to.
    core::Ptr<Setup> parentSetup() const;

    /// Gets if this operation is selected in the 'Setups' browser.
    bool isSelected() const;

    /// Gets and sets the notes of the operation.
    std::string notes() const;
    bool notes(const std::string& value);

    /// Returns the id of the operation. This id is unique as compared
    /// to the ids of all other operations in the document.
    /// This id will not change when changing the order or parent of the operation.
    /// This id will remain valid when the document is saved and reloaded.
    int operationId() const;

    /// Gets the CAMParameters collection for this operation.
    core::Ptr<CAMParameters> parameters() const;

    ADSK_CAM_OPERATIONBASE_API static const char* classType();
    ADSK_CAM_OPERATIONBASE_API const char* objectType() const override;
    ADSK_CAM_OPERATIONBASE_API void* queryInterface(const char* id) const override;
    ADSK_CAM_OPERATIONBASE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual char* name_raw() const = 0;
    virtual bool name_raw(const char * value) = 0;
    virtual bool isProtected_raw() const = 0;
    virtual bool isProtected_raw(bool value) = 0;
    virtual bool isOptional_raw() const = 0;
    virtual bool isOptional_raw(bool value) = 0;
    virtual bool isSuppressed_raw() const = 0;
    virtual bool isSuppressed_raw(bool value) = 0;
    virtual Setup* parentSetup_raw() const = 0;
    virtual bool isSelected_raw() const = 0;
    virtual char* notes_raw() const = 0;
    virtual bool notes_raw(const char * value) = 0;
    virtual int operationId_raw() const = 0;
    virtual CAMParameters* parameters_raw() const = 0;
    virtual void placeholderOperationBase0() {}
    virtual void placeholderOperationBase1() {}
    virtual void placeholderOperationBase2() {}
    virtual void placeholderOperationBase3() {}
    virtual void placeholderOperationBase4() {}
    virtual void placeholderOperationBase5() {}
    virtual void placeholderOperationBase6() {}
    virtual void placeholderOperationBase7() {}
    virtual void placeholderOperationBase8() {}
    virtual void placeholderOperationBase9() {}
    virtual void placeholderOperationBase10() {}
    virtual void placeholderOperationBase11() {}
    virtual void placeholderOperationBase12() {}
    virtual void placeholderOperationBase13() {}
    virtual void placeholderOperationBase14() {}
    virtual void placeholderOperationBase15() {}
    virtual void placeholderOperationBase16() {}
    virtual void placeholderOperationBase17() {}
    virtual void placeholderOperationBase18() {}
    virtual void placeholderOperationBase19() {}
    virtual void placeholderOperationBase20() {}
    virtual void placeholderOperationBase21() {}
    virtual void placeholderOperationBase22() {}
    virtual void placeholderOperationBase23() {}
    virtual void placeholderOperationBase24() {}
    virtual void placeholderOperationBase25() {}
    virtual void placeholderOperationBase26() {}
    virtual void placeholderOperationBase27() {}
    virtual void placeholderOperationBase28() {}
    virtual void placeholderOperationBase29() {}
    virtual void placeholderOperationBase30() {}
    virtual void placeholderOperationBase31() {}
    virtual void placeholderOperationBase32() {}
    virtual void placeholderOperationBase33() {}
    virtual void placeholderOperationBase34() {}
    virtual void placeholderOperationBase35() {}
    virtual void placeholderOperationBase36() {}
    virtual void placeholderOperationBase37() {}
    virtual void placeholderOperationBase38() {}
    virtual void placeholderOperationBase39() {}
    virtual void placeholderOperationBase40() {}
    virtual void placeholderOperationBase41() {}
    virtual void placeholderOperationBase42() {}
    virtual void placeholderOperationBase43() {}
    virtual void placeholderOperationBase44() {}
    virtual void placeholderOperationBase45() {}
    virtual void placeholderOperationBase46() {}
    virtual void placeholderOperationBase47() {}
    virtual void placeholderOperationBase48() {}
    virtual void placeholderOperationBase49() {}
};

// Inline wrappers

inline std::string OperationBase::name() const
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

inline bool OperationBase::name(const std::string& value)
{
    return name_raw(value.c_str());
}

inline bool OperationBase::isProtected() const
{
    bool res = isProtected_raw();
    return res;
}

inline bool OperationBase::isProtected(bool value)
{
    return isProtected_raw(value);
}

inline bool OperationBase::isOptional() const
{
    bool res = isOptional_raw();
    return res;
}

inline bool OperationBase::isOptional(bool value)
{
    return isOptional_raw(value);
}

inline bool OperationBase::isSuppressed() const
{
    bool res = isSuppressed_raw();
    return res;
}

inline bool OperationBase::isSuppressed(bool value)
{
    return isSuppressed_raw(value);
}

inline core::Ptr<Setup> OperationBase::parentSetup() const
{
    core::Ptr<Setup> res = parentSetup_raw();
    return res;
}

inline bool OperationBase::isSelected() const
{
    bool res = isSelected_raw();
    return res;
}

inline std::string OperationBase::notes() const
{
    std::string res;

    char* p= notes_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool OperationBase::notes(const std::string& value)
{
    return notes_raw(value.c_str());
}

inline int OperationBase::operationId() const
{
    int res = operationId_raw();
    return res;
}

inline core::Ptr<CAMParameters> OperationBase::parameters() const
{
    core::Ptr<CAMParameters> res = parameters_raw();
    return res;
}
}// namespace cam
}// namespace adsk

#undef ADSK_CAM_OPERATIONBASE_API