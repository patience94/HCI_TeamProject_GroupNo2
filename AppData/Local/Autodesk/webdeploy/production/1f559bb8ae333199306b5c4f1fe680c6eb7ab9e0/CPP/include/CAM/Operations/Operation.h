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
#include "../CAMTypeDefs.h"
#include "OperationBase.h"
#include <string>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef CAMXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_CAM_OPERATION_CPP__
# define ADSK_CAM_OPERATION_API XI_EXPORT
# else
# define ADSK_CAM_OPERATION_API
# endif
#else
# define ADSK_CAM_OPERATION_API XI_IMPORT
#endif

namespace adsk { namespace cam {

/// Object that represents an operation in an existing Setup, Folder or Pattern.
class Operation : public OperationBase {
public:

    /// Gets the strategy type for this operation.
    OperationStrategyTypes strategyType() const;

    /// Gets if the toolpath for this operation is currently valid. (has not become invalidated by model changes).
    bool isToolpathValid() const;

    /// Gets if the toolpath is in the process of generating.
    bool isGenerating() const;

    /// Gets if problems were encountered when generating the toolpath for this operation.
    bool hasWarning() const;

    /// Returns the parent Setup, Folder or Pattern for this operation.
    core::Ptr<core::Base> parent() const;

    /// Gets if a toolpath currently exists (has been generated) for this operation.
    bool hasToolpath() const;

    /// Gets the current state of this operation.
    OperationStates operationState() const;

    /// Gets the toolpath generation progress value for this operation.
    std::string generatingProgress() const;

    ADSK_CAM_OPERATION_API static const char* classType();
    ADSK_CAM_OPERATION_API const char* objectType() const override;
    ADSK_CAM_OPERATION_API void* queryInterface(const char* id) const override;
    ADSK_CAM_OPERATION_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual OperationStrategyTypes strategyType_raw() const = 0;
    virtual bool isToolpathValid_raw() const = 0;
    virtual bool isGenerating_raw() const = 0;
    virtual bool hasWarning_raw() const = 0;
    virtual core::Base* parent_raw() const = 0;
    virtual bool hasToolpath_raw() const = 0;
    virtual OperationStates operationState_raw() const = 0;
    virtual char* generatingProgress_raw() const = 0;
};

// Inline wrappers

inline OperationStrategyTypes Operation::strategyType() const
{
    OperationStrategyTypes res = strategyType_raw();
    return res;
}

inline bool Operation::isToolpathValid() const
{
    bool res = isToolpathValid_raw();
    return res;
}

inline bool Operation::isGenerating() const
{
    bool res = isGenerating_raw();
    return res;
}

inline bool Operation::hasWarning() const
{
    bool res = hasWarning_raw();
    return res;
}

inline core::Ptr<core::Base> Operation::parent() const
{
    core::Ptr<core::Base> res = parent_raw();
    return res;
}

inline bool Operation::hasToolpath() const
{
    bool res = hasToolpath_raw();
    return res;
}

inline OperationStates Operation::operationState() const
{
    OperationStates res = operationState_raw();
    return res;
}

inline std::string Operation::generatingProgress() const
{
    std::string res;

    char* p= generatingProgress_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}
}// namespace cam
}// namespace adsk

#undef ADSK_CAM_OPERATION_API