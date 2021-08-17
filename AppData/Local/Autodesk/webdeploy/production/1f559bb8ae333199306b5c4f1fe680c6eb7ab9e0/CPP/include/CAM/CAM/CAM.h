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
#include "../../Core/Application/Product.h"
#include <string>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef CAMXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_CAM_CAM_CPP__
# define ADSK_CAM_CAM_API XI_EXPORT
# else
# define ADSK_CAM_CAM_API
# endif
#else
# define ADSK_CAM_CAM_API XI_IMPORT
#endif

namespace adsk { namespace cam {
    class GenerateToolpathFuture;
    class MachiningTime;
    class PostProcessInput;
    class Setups;
}}
namespace adsk { namespace core {
    class ObjectCollection;
}}
namespace adsk { namespace fusion {
    class CustomGraphicsGroups;
    class Occurrence;
    class OccurrenceList;
}}

namespace adsk { namespace cam {

/// Object that represents the CAM environment of a Fusion document.
class CAM : public core::Product {
public:

    /// Returns the Setups collection that provides access to existing setups
    core::Ptr<Setups> setups() const;

    /// Exports the default additive setup's models into a 3mf file. The 3mf also contains machine and support information.
    /// True on success, false on errors or wrong setup type
    bool export3MFForDefaultAdditiveSetup(const std::string& filepath);

    /// Generates/Regenerates all of the toolpaths (including those nested in sub-folders or patterns)
    /// for the specified objects.
    /// operations : An Operation, Setup, Folder or Pattern object for which to generate the toolpath/s for. You can also
    /// specify a collection of any combination of these object types.
    /// Return GenerateToolpathFuture that includes the status of toolpath generation.
    core::Ptr<GenerateToolpathFuture> generateToolpath(const core::Ptr<core::Base>& operations);

    /// Generates/Regenerates all toolpaths (includes those nested in sub-folders or patterns) in the document.
    /// skipValid : Option to skip valid toolpaths and only regenerate invalid toolpaths.
    /// Return GenerateToolpathFuture that includes the status of toolpath generation.
    core::Ptr<GenerateToolpathFuture> generateAllToolpaths(bool skipValid);

    /// Clears all of the toolpaths (including those nested in sub-folders or patterns) for the specified objects.
    /// operations : An Operation, Setup, Folder or Pattern object for which to clear the toolpath/s for. You can also
    /// specify a collection of any combination of these object types.
    /// Return true if successful.
    bool clearToolpath(const core::Ptr<core::Base>& operations);

    /// Clears all the toolpaths (includes those nested in sub-folders or patterns) in the document
    /// Return true if successful.
    bool clearAllToolpaths();

    /// Checks if toolpath operations (including those nested in sub-folders or patterns) are valid for the specified objects.
    /// operations : An Operation, Setup, Folder or Pattern object for which to check the toolpath/s of. You can also
    /// specify a collection of any combination of these object types.
    /// Returns true if the toolpath operations are valid
    bool checkToolpath(const core::Ptr<core::Base>& operations);

    /// Checks if all the toolpath operations (includes those nested in sub-folders or patterns) in the document are valid
    /// Returns true if the all toolpath operations are valid
    bool checkAllToolpaths();

    /// Post all of the toolpaths (including those nested in sub-folders or patterns) for the specified objects
    /// operations : An Operation, Setup, Folder or Pattern object for which to post the toolpath/s of. You can also
    /// specify a collection of any combination of these object types.
    /// input : The PostProcessInput object that defines the post options and parameters.
    /// Returns true if successful
    bool postProcess(const core::Ptr<core::Base>& operations, const core::Ptr<PostProcessInput>& input);

    /// Post all of the toolpaths (includes those nested in sub-folders or patterns)in the document
    /// input : The PostProcessInput object that defines the post options and parameters.
    /// Returns true if successful
    bool postProcessAll(const core::Ptr<PostProcessInput>& input);

    /// Generate the setup sheets for the specified objects
    /// operations : An Operation, Setup, Folder or Pattern object for which to generate the setup sheet/s for. You can also
    /// specify a collection of any combination of these object types.
    /// format : The document format for the setup sheet. Valid options are HTMLFormat and ExcelFormat.
    /// Limitation: "ExcelFormat" can be used in windows OS only.
    /// folder : The destination folder to locate the setup sheet documents in.
    /// openDocument : An option to allow to open the document instantly after the generation. By default, the document is opened.
    /// Returns true if successful
    bool generateSetupSheet(const core::Ptr<core::Base>& operations, SetupSheetFormats format, const std::string& folder, bool openDocument = true);

    /// Generates all of the setup sheets for all of the operations in the document
    /// format : The document format for the setup sheet. Valid options are HTMLFormat and ExcelFormat.
    /// Limitation: "ExcelFormat" can be used in windows OS only.
    /// folder : The destination folder to locate the setup sheet documents in.
    /// openDocument : An option to allow to open the document instantly after the generation. By default, the document is opened.
    /// Returns true if successful
    bool generateAllSetupSheets(SetupSheetFormats format, const std::string& folder, bool openDocument = true);

    /// Gets a collection containing all of the operations in the document.
    /// This includes all operations nested in folders and patterns.
    core::Ptr<core::ObjectCollection> allOperations() const;

    /// Gets the installed post folder.
    std::string genericPostFolder() const;

    /// Gets the personal post folder.
    std::string personalPostFolder() const;

    /// Gets the folder for temporary files.
    std::string temporaryFolder() const;

    /// Get the machining time for the specified objects.
    /// operations : An Operation, Setup, Folder or Pattern object for which to get the machining time for. You can also
    /// specify a collection of any combination of these object types.
    /// feedScale : The feed scale value (%) to use.
    /// rapidFeed : The rapid feed rate in centimeters per second.
    /// toolChangeTime : The tool change time in seconds.
    /// Returns a MachiningTime object that has properties holding the calculation results.
    core::Ptr<MachiningTime> getMachiningTime(const core::Ptr<core::Base>& operations, double feedScale, double rapidFeed, double toolChangeTime);

    /// Returns the customGraphicsGroups object associated with the CAM product.
    core::Ptr<fusion::CustomGraphicsGroups> customGraphicsGroups() const;

    /// Returns the occurrence that references the design root component in CAM product.
    core::Ptr<fusion::Occurrence> designRootOccurrence() const;

    /// Returns a read only list of flat pattern occurrences in CAM product.
    core::Ptr<fusion::OccurrenceList> flatPatternOccurrences() const;

    /// Gets a collection containing all of the machines in the document.
    core::Ptr<core::ObjectCollection> allMachines() const;

    ADSK_CAM_CAM_API static const char* classType();
    ADSK_CAM_CAM_API const char* objectType() const override;
    ADSK_CAM_CAM_API void* queryInterface(const char* id) const override;
    ADSK_CAM_CAM_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual Setups* setups_raw() const = 0;
    virtual bool export3MFForDefaultAdditiveSetup_raw(const char * filepath) = 0;
    virtual GenerateToolpathFuture* generateToolpath_raw(core::Base* operations) = 0;
    virtual GenerateToolpathFuture* generateAllToolpaths_raw(bool skipValid) = 0;
    virtual bool clearToolpath_raw(core::Base* operations) = 0;
    virtual bool clearAllToolpaths_raw() = 0;
    virtual bool checkToolpath_raw(core::Base* operations) = 0;
    virtual bool checkAllToolpaths_raw() = 0;
    virtual bool postProcess_raw(core::Base* operations, PostProcessInput* input) = 0;
    virtual bool postProcessAll_raw(PostProcessInput* input) = 0;
    virtual bool generateSetupSheet_raw(core::Base* operations, SetupSheetFormats format, const char * folder, bool openDocument) = 0;
    virtual bool generateAllSetupSheets_raw(SetupSheetFormats format, const char * folder, bool openDocument) = 0;
    virtual core::ObjectCollection* allOperations_raw() const = 0;
    virtual char* genericPostFolder_raw() const = 0;
    virtual char* personalPostFolder_raw() const = 0;
    virtual char* temporaryFolder_raw() const = 0;
    virtual MachiningTime* getMachiningTime_raw(core::Base* operations, double feedScale, double rapidFeed, double toolChangeTime) = 0;
    virtual fusion::CustomGraphicsGroups* customGraphicsGroups_raw() const = 0;
    virtual fusion::Occurrence* designRootOccurrence_raw() const = 0;
    virtual fusion::OccurrenceList* flatPatternOccurrences_raw() const = 0;
    virtual core::ObjectCollection* allMachines_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<Setups> CAM::setups() const
{
    core::Ptr<Setups> res = setups_raw();
    return res;
}

inline bool CAM::export3MFForDefaultAdditiveSetup(const std::string& filepath)
{
    bool res = export3MFForDefaultAdditiveSetup_raw(filepath.c_str());
    return res;
}

inline core::Ptr<GenerateToolpathFuture> CAM::generateToolpath(const core::Ptr<core::Base>& operations)
{
    core::Ptr<GenerateToolpathFuture> res = generateToolpath_raw(operations.get());
    return res;
}

inline core::Ptr<GenerateToolpathFuture> CAM::generateAllToolpaths(bool skipValid)
{
    core::Ptr<GenerateToolpathFuture> res = generateAllToolpaths_raw(skipValid);
    return res;
}

inline bool CAM::clearToolpath(const core::Ptr<core::Base>& operations)
{
    bool res = clearToolpath_raw(operations.get());
    return res;
}

inline bool CAM::clearAllToolpaths()
{
    bool res = clearAllToolpaths_raw();
    return res;
}

inline bool CAM::checkToolpath(const core::Ptr<core::Base>& operations)
{
    bool res = checkToolpath_raw(operations.get());
    return res;
}

inline bool CAM::checkAllToolpaths()
{
    bool res = checkAllToolpaths_raw();
    return res;
}

inline bool CAM::postProcess(const core::Ptr<core::Base>& operations, const core::Ptr<PostProcessInput>& input)
{
    bool res = postProcess_raw(operations.get(), input.get());
    return res;
}

inline bool CAM::postProcessAll(const core::Ptr<PostProcessInput>& input)
{
    bool res = postProcessAll_raw(input.get());
    return res;
}

inline bool CAM::generateSetupSheet(const core::Ptr<core::Base>& operations, SetupSheetFormats format, const std::string& folder, bool openDocument)
{
    bool res = generateSetupSheet_raw(operations.get(), format, folder.c_str(), openDocument);
    return res;
}

inline bool CAM::generateAllSetupSheets(SetupSheetFormats format, const std::string& folder, bool openDocument)
{
    bool res = generateAllSetupSheets_raw(format, folder.c_str(), openDocument);
    return res;
}

inline core::Ptr<core::ObjectCollection> CAM::allOperations() const
{
    core::Ptr<core::ObjectCollection> res = allOperations_raw();
    return res;
}

inline std::string CAM::genericPostFolder() const
{
    std::string res;

    char* p= genericPostFolder_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline std::string CAM::personalPostFolder() const
{
    std::string res;

    char* p= personalPostFolder_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline std::string CAM::temporaryFolder() const
{
    std::string res;

    char* p= temporaryFolder_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline core::Ptr<MachiningTime> CAM::getMachiningTime(const core::Ptr<core::Base>& operations, double feedScale, double rapidFeed, double toolChangeTime)
{
    core::Ptr<MachiningTime> res = getMachiningTime_raw(operations.get(), feedScale, rapidFeed, toolChangeTime);
    return res;
}

inline core::Ptr<fusion::CustomGraphicsGroups> CAM::customGraphicsGroups() const
{
    core::Ptr<fusion::CustomGraphicsGroups> res = customGraphicsGroups_raw();
    return res;
}

inline core::Ptr<fusion::Occurrence> CAM::designRootOccurrence() const
{
    core::Ptr<fusion::Occurrence> res = designRootOccurrence_raw();
    return res;
}

inline core::Ptr<fusion::OccurrenceList> CAM::flatPatternOccurrences() const
{
    core::Ptr<fusion::OccurrenceList> res = flatPatternOccurrences_raw();
    return res;
}

inline core::Ptr<core::ObjectCollection> CAM::allMachines() const
{
    core::Ptr<core::ObjectCollection> res = allMachines_raw();
    return res;
}
}// namespace cam
}// namespace adsk

#undef ADSK_CAM_CAM_API