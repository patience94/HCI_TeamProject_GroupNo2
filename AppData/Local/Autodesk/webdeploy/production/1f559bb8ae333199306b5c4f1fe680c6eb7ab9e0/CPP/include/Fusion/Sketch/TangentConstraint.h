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
#include "GeometricConstraint.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_TANGENTCONSTRAINT_CPP__
# define ADSK_FUSION_TANGENTCONSTRAINT_API XI_EXPORT
# else
# define ADSK_FUSION_TANGENTCONSTRAINT_API
# endif
#else
# define ADSK_FUSION_TANGENTCONSTRAINT_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Occurrence;
    class SketchCurve;
}}

namespace adsk { namespace fusion {

/// A tangent constraint in a sketch.
class TangentConstraint : public GeometricConstraint {
public:

    /// Returns the first curve.
    core::Ptr<SketchCurve> curveOne() const;

    /// Returns the second curve.
    core::Ptr<SketchCurve> curveTwo() const;

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<TangentConstraint> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<TangentConstraint> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_TANGENTCONSTRAINT_API static const char* classType();
    ADSK_FUSION_TANGENTCONSTRAINT_API const char* objectType() const override;
    ADSK_FUSION_TANGENTCONSTRAINT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_TANGENTCONSTRAINT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual SketchCurve* curveOne_raw() const = 0;
    virtual SketchCurve* curveTwo_raw() const = 0;
    virtual TangentConstraint* nativeObject_raw() const = 0;
    virtual TangentConstraint* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline core::Ptr<SketchCurve> TangentConstraint::curveOne() const
{
    core::Ptr<SketchCurve> res = curveOne_raw();
    return res;
}

inline core::Ptr<SketchCurve> TangentConstraint::curveTwo() const
{
    core::Ptr<SketchCurve> res = curveTwo_raw();
    return res;
}

inline core::Ptr<TangentConstraint> TangentConstraint::nativeObject() const
{
    core::Ptr<TangentConstraint> res = nativeObject_raw();
    return res;
}

inline core::Ptr<TangentConstraint> TangentConstraint::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<TangentConstraint> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_TANGENTCONSTRAINT_API