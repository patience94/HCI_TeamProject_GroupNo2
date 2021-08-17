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

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_FILLETEDGESET_CPP__
# define ADSK_FUSION_FILLETEDGESET_API XI_EXPORT
# else
# define ADSK_FUSION_FILLETEDGESET_API
# endif
#else
# define ADSK_FUSION_FILLETEDGESET_API XI_IMPORT
#endif

namespace adsk { namespace fusion {

/// The base class for the classes that define the different types of fillet edge sets.
class FilletEdgeSet : public core::Base {
public:

    ADSK_FUSION_FILLETEDGESET_API static const char* classType();
    ADSK_FUSION_FILLETEDGESET_API const char* objectType() const override;
    ADSK_FUSION_FILLETEDGESET_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_FILLETEDGESET_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual void placeholderFilletEdgeSet0() {}
    virtual void placeholderFilletEdgeSet1() {}
    virtual void placeholderFilletEdgeSet2() {}
    virtual void placeholderFilletEdgeSet3() {}
    virtual void placeholderFilletEdgeSet4() {}
    virtual void placeholderFilletEdgeSet5() {}
    virtual void placeholderFilletEdgeSet6() {}
    virtual void placeholderFilletEdgeSet7() {}
    virtual void placeholderFilletEdgeSet8() {}
    virtual void placeholderFilletEdgeSet9() {}
    virtual void placeholderFilletEdgeSet10() {}
    virtual void placeholderFilletEdgeSet11() {}
    virtual void placeholderFilletEdgeSet12() {}
    virtual void placeholderFilletEdgeSet13() {}
    virtual void placeholderFilletEdgeSet14() {}
    virtual void placeholderFilletEdgeSet15() {}
    virtual void placeholderFilletEdgeSet16() {}
    virtual void placeholderFilletEdgeSet17() {}
    virtual void placeholderFilletEdgeSet18() {}
    virtual void placeholderFilletEdgeSet19() {}
    virtual void placeholderFilletEdgeSet20() {}
    virtual void placeholderFilletEdgeSet21() {}
    virtual void placeholderFilletEdgeSet22() {}
    virtual void placeholderFilletEdgeSet23() {}
    virtual void placeholderFilletEdgeSet24() {}
    virtual void placeholderFilletEdgeSet25() {}
    virtual void placeholderFilletEdgeSet26() {}
    virtual void placeholderFilletEdgeSet27() {}
    virtual void placeholderFilletEdgeSet28() {}
    virtual void placeholderFilletEdgeSet29() {}
    virtual void placeholderFilletEdgeSet30() {}
    virtual void placeholderFilletEdgeSet31() {}
};

// Inline wrappers
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_FILLETEDGESET_API