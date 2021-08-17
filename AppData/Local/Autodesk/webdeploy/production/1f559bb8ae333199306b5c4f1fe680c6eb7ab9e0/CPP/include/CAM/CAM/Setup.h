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
#include "../Operations/OperationBase.h"
#include <string>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef CAMXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_CAM_SETUP_CPP__
# define ADSK_CAM_SETUP_API XI_EXPORT
# else
# define ADSK_CAM_SETUP_API
# endif
#else
# define ADSK_CAM_SETUP_API XI_IMPORT
#endif

namespace adsk { namespace cam {
    class CAMFolders;
    class CAMPatterns;
    class ChildOperationList;
    class Machine;
    class Operations;
}}
namespace adsk { namespace core {
    class ObjectCollection;
}}

namespace adsk { namespace cam {

/// Object that represents an existing Setup.
class Setup : public OperationBase {
public:

    /// Gets the Operation Type (MillingOperation or TurningOperation).
    OperationTypes operationType() const;

    /// Gets if this setup is active.
    bool isActive() const;

    /// Returns the Operations collection that provides access to existing operations
    /// in this setup.
    core::Ptr<Operations> operations() const;

    /// Returns the Folders collection that provides access to existing folders
    /// in this setup.
    core::Ptr<CAMFolders> folders() const;

    /// Returns the Patterns collection that provides access to existing patterns
    /// in this setup.
    core::Ptr<CAMPatterns> patterns() const;

    /// Returns a collection containing all of the immediate (top level) child operations, folders and patterns in this setup
    /// in the order they appear in the browser.
    core::Ptr<ChildOperationList> children() const;

    /// Gets a collection containing all of the operations in this setup.
    /// This includes all operations nested in folders and patterns.
    core::Ptr<core::ObjectCollection> allOperations() const;

    /// Gets and sets the bodies associated with the setup. Passing in an empty ObjectCollection
    /// will remove all current bodies. Valid input is MeshBody and/or BRepBody objects.
    core::Ptr<core::ObjectCollection> models() const;
    bool models(const core::Ptr<core::ObjectCollection>& value);

    /// Gets the fixtures associated with the setup.
    core::Ptr<core::ObjectCollection> fixtures() const;

    /// Gets the stock solids associated with the setup.
    core::Ptr<core::ObjectCollection> stockSolids() const;

    /// Gets the Machine associated with the setup.
    core::Ptr<Machine> machine() const;

    /// Create and add operations, folders or patterns from the specified template file to the end of this setup.
    /// templateFilePath : The full path to the template file.
    /// Returns the collection containing all of the operations, folders and patterns created from the template file.
    core::Ptr<core::ObjectCollection> createFromTemplate(const std::string& templateFilePath);

    ADSK_CAM_SETUP_API static const char* classType();
    ADSK_CAM_SETUP_API const char* objectType() const override;
    ADSK_CAM_SETUP_API void* queryInterface(const char* id) const override;
    ADSK_CAM_SETUP_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual OperationTypes operationType_raw() const = 0;
    virtual bool isActive_raw() const = 0;
    virtual Operations* operations_raw() const = 0;
    virtual CAMFolders* folders_raw() const = 0;
    virtual CAMPatterns* patterns_raw() const = 0;
    virtual ChildOperationList* children_raw() const = 0;
    virtual core::ObjectCollection* allOperations_raw() const = 0;
    virtual core::ObjectCollection* models_raw() const = 0;
    virtual bool models_raw(core::ObjectCollection* value) = 0;
    virtual core::ObjectCollection* fixtures_raw() const = 0;
    virtual core::ObjectCollection* stockSolids_raw() const = 0;
    virtual Machine* machine_raw() const = 0;
    virtual core::ObjectCollection* createFromTemplate_raw(const char * templateFilePath) = 0;
};

// Inline wrappers

inline OperationTypes Setup::operationType() const
{
    OperationTypes res = operationType_raw();
    return res;
}

inline bool Setup::isActive() const
{
    bool res = isActive_raw();
    return res;
}

inline core::Ptr<Operations> Setup::operations() const
{
    core::Ptr<Operations> res = operations_raw();
    return res;
}

inline core::Ptr<CAMFolders> Setup::folders() const
{
    core::Ptr<CAMFolders> res = folders_raw();
    return res;
}

inline core::Ptr<CAMPatterns> Setup::patterns() const
{
    core::Ptr<CAMPatterns> res = patterns_raw();
    return res;
}

inline core::Ptr<ChildOperationList> Setup::children() const
{
    core::Ptr<ChildOperationList> res = children_raw();
    return res;
}

inline core::Ptr<core::ObjectCollection> Setup::allOperations() const
{
    core::Ptr<core::ObjectCollection> res = allOperations_raw();
    return res;
}

inline core::Ptr<core::ObjectCollection> Setup::models() const
{
    core::Ptr<core::ObjectCollection> res = models_raw();
    return res;
}

inline bool Setup::models(const core::Ptr<core::ObjectCollection>& value)
{
    return models_raw(value.get());
}

inline core::Ptr<core::ObjectCollection> Setup::fixtures() const
{
    core::Ptr<core::ObjectCollection> res = fixtures_raw();
    return res;
}

inline core::Ptr<core::ObjectCollection> Setup::stockSolids() const
{
    core::Ptr<core::ObjectCollection> res = stockSolids_raw();
    return res;
}

inline core::Ptr<Machine> Setup::machine() const
{
    core::Ptr<Machine> res = machine_raw();
    return res;
}

inline core::Ptr<core::ObjectCollection> Setup::createFromTemplate(const std::string& templateFilePath)
{
    core::Ptr<core::ObjectCollection> res = createFromTemplate_raw(templateFilePath.c_str());
    return res;
}
}// namespace cam
}// namespace adsk

#undef ADSK_CAM_SETUP_API