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
# ifdef __COMPILING_ADSK_FUSION_SYMMETRYCONSTRAINT_CPP__
# define ADSK_FUSION_SYMMETRYCONSTRAINT_API XI_EXPORT
# else
# define ADSK_FUSION_SYMMETRYCONSTRAINT_API
# endif
#else
# define ADSK_FUSION_SYMMETRYCONSTRAINT_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Occurrence;
    class SketchEntity;
    class SketchLine;
}}

namespace adsk { namespace fusion {

/// A symmetry constraint in a sketch.
class SymmetryConstraint : public GeometricConstraint {
public:

    /// Returns the first curve.
    core::Ptr<SketchEntity> entityOne() const;

    /// Returns the second curve.
    core::Ptr<SketchEntity> entityTwo() const;

    /// Returns the axis (SketchLine) that defines the symmetry.
    core::Ptr<SketchLine> symmetryLine() const;

    /// The NativeObject is the object outside the context of an assembly and
    /// in the context of it's parent component.
    /// Returns null in the case where this object is not in the context of
    /// an assembly but is already the native object.
    core::Ptr<SymmetryConstraint> nativeObject() const;

    /// Creates or returns a proxy for the native object
    /// - i.e. a new object that represents this object but adds the assembly context
    /// defined by the input occurrence.
    /// occurrence : The occurrence that defines the context to create the proxy in.
    /// Returns the proxy object or null if this isn't the NativeObject.
    core::Ptr<SymmetryConstraint> createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const;

    ADSK_FUSION_SYMMETRYCONSTRAINT_API static const char* classType();
    ADSK_FUSION_SYMMETRYCONSTRAINT_API const char* objectType() const override;
    ADSK_FUSION_SYMMETRYCONSTRAINT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_SYMMETRYCONSTRAINT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual SketchEntity* entityOne_raw() const = 0;
    virtual SketchEntity* entityTwo_raw() const = 0;
    virtual SketchLine* symmetryLine_raw() const = 0;
    virtual SymmetryConstraint* nativeObject_raw() const = 0;
    virtual SymmetryConstraint* createForAssemblyContext_raw(Occurrence* occurrence) const = 0;
};

// Inline wrappers

inline core::Ptr<SketchEntity> SymmetryConstraint::entityOne() const
{
    core::Ptr<SketchEntity> res = entityOne_raw();
    return res;
}

inline core::Ptr<SketchEntity> SymmetryConstraint::entityTwo() const
{
    core::Ptr<SketchEntity> res = entityTwo_raw();
    return res;
}

inline core::Ptr<SketchLine> SymmetryConstraint::symmetryLine() const
{
    core::Ptr<SketchLine> res = symmetryLine_raw();
    return res;
}

inline core::Ptr<SymmetryConstraint> SymmetryConstraint::nativeObject() const
{
    core::Ptr<SymmetryConstraint> res = nativeObject_raw();
    return res;
}

inline core::Ptr<SymmetryConstraint> SymmetryConstraint::createForAssemblyContext(const core::Ptr<Occurrence>& occurrence) const
{
    core::Ptr<SymmetryConstraint> res = createForAssemblyContext_raw(occurrence.get());
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_SYMMETRYCONSTRAINT_API