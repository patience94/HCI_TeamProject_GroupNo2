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
#include "Feature.h"

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_CUTPASTEBODY_CPP__
# define ADSK_FUSION_CUTPASTEBODY_API XI_EXPORT
# else
# define ADSK_FUSION_CUTPASTEBODY_API
# endif
#else
# define ADSK_FUSION_CUTPASTEBODY_API XI_IMPORT
#endif

namespace adsk { namespace core {
    class ObjectCollection;
}}

namespace adsk { namespace fusion {

/// Object that represents an existing Cut/Paste Body feature in a design.
class CutPasteBody : public Feature {
public:

    /// Returns the bodies that were cut to create the result bodies of this feature. An ObjectCollection
    /// is returned that will contain the original bodies. It's possible that the collection can be empty
    /// or contain less than the number of bodies originally copied. This happens in the case where a body
    /// has been deleted or consumed by some other operation. If you roll the timeline to a point immediately
    /// before or after the feature was created you can access the bodies.
    /// Returns the bodies that were cut to create the result bodies of this feature. An ObjectCollection
    /// is returned that will contain the original bodies. Because the body is removed as a result of this
    /// operation the cut bodies will never be available after the feature has been created. If you roll
    /// the timeline to a point immediately before the feature was created you can access the bodies.
    core::Ptr<core::ObjectCollection> sourceBody() const;

    ADSK_FUSION_CUTPASTEBODY_API static const char* classType();
    ADSK_FUSION_CUTPASTEBODY_API const char* objectType() const override;
    ADSK_FUSION_CUTPASTEBODY_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_CUTPASTEBODY_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::ObjectCollection* sourceBody_raw() const = 0;
};

// Inline wrappers

inline core::Ptr<core::ObjectCollection> CutPasteBody::sourceBody() const
{
    core::Ptr<core::ObjectCollection> res = sourceBody_raw();
    return res;
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_CUTPASTEBODY_API