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
# ifdef __COMPILING_ADSK_FUSION_SKETCHTEXTINPUT_CPP__
# define ADSK_FUSION_SKETCHTEXTINPUT_API XI_EXPORT
# else
# define ADSK_FUSION_SKETCHTEXTINPUT_API
# endif
#else
# define ADSK_FUSION_SKETCHTEXTINPUT_API XI_IMPORT
#endif

namespace adsk { namespace core {
    class Point3D;
}}

namespace adsk { namespace fusion {

/// The SketchTextInput object is equivalent to the Sketch Text dialog in that it collects all of the input required
/// to create sketch text. Once the properties of the SketchTextInput object have been defined, use the add method
/// to create the sketch text. A SketchTextInput object is created by using the createInput of the SketchTexts object.
class SketchTextInput : public core::Base {
public:

    /// Gets and sets the height of the text in centimeters.
    double height() const;
    bool height(double value);

    /// Gets and sets the text.
    std::string text() const;
    bool text(const std::string& value);

    /// Gets and sets the position of the text on the x-y plane of the sketch. The text must lie on the x-y plane so the Z component
    /// of the point is ignored and always treated as zero.
    core::Ptr<core::Point3D> position() const;
    bool position(const core::Ptr<core::Point3D>& value);

    /// Gets and sets the name of the font to use.
    std::string fontName() const;
    bool fontName(const std::string& value);

    /// Gets and sets the angle of the text relative to the x-axis of the x-y plane of the sketch.
    double angle() const;
    bool angle(double value);

    /// Gets and sets the text style to apply to the entire text. This is a bitwise enum so styles
    /// can be combined to apply multiple styles. For example you can apply bold and underline.
    TextStyles textStyle() const;
    bool textStyle(TextStyles value);

    ADSK_FUSION_SKETCHTEXTINPUT_API static const char* classType();
    ADSK_FUSION_SKETCHTEXTINPUT_API const char* objectType() const override;
    ADSK_FUSION_SKETCHTEXTINPUT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SKETCHTEXTINPUT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual double height_raw() const = 0;
    virtual bool height_raw(double value) = 0;
    virtual char* text_raw() const = 0;
    virtual bool text_raw(const char * value) = 0;
    virtual core::Point3D* position_raw() const = 0;
    virtual bool position_raw(core::Point3D* value) = 0;
    virtual char* fontName_raw() const = 0;
    virtual bool fontName_raw(const char * value) = 0;
    virtual double angle_raw() const = 0;
    virtual bool angle_raw(double value) = 0;
    virtual TextStyles textStyle_raw() const = 0;
    virtual bool textStyle_raw(TextStyles value) = 0;
};

// Inline wrappers

inline double SketchTextInput::height() const
{
    double res = height_raw();
    return res;
}

inline bool SketchTextInput::height(double value)
{
    return height_raw(value);
}

inline std::string SketchTextInput::text() const
{
    std::string res;

    char* p= text_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool SketchTextInput::text(const std::string& value)
{
    return text_raw(value.c_str());
}

inline core::Ptr<core::Point3D> SketchTextInput::position() const
{
    core::Ptr<core::Point3D> res = position_raw();
    return res;
}

inline bool SketchTextInput::position(const core::Ptr<core::Point3D>& value)
{
    return position_raw(value.get());
}

inline std::string SketchTextInput::fontName() const
{
    std::string res;

    char* p= fontName_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool SketchTextInput::fontName(const std::string& value)
{
    return fontName_raw(value.c_str());
}

inline double SketchTextInput::angle() const
{
    double res = angle_raw();
    return res;
}

inline bool SketchTextInput::angle(double value)
{
    return angle_raw(value);
}

inline TextStyles SketchTextInput::textStyle() const
{
    TextStyles res = textStyle_raw();
    return res;
}

inline bool SketchTextInput::textStyle(TextStyles value)
{
    return textStyle_raw(value);
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SKETCHTEXTINPUT_API