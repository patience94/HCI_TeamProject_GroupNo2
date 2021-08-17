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

#include "OSMacros.h"

#ifdef XINTERFACE_EXPORTS
# ifdef __COMPILING_xIDEALLOCATOR_CPP__
#  define xIDEALLOCATOR_API XI_EXPORT
# else
#  define xIDEALLOCATOR_API
# endif
#else
# define xIDEALLOCATOR_API XI_IMPORT
#endif


#define DEALLOCATEARRAYINTERNAL(T) \
	namespace adsk { namespace core {\
		xIDEALLOCATOR_API void DeallocateArrayInternal(T* p);\
	}}

#define DEALLOCATEARRAYINTERNALCLASS(space, T) \
	namespace adsk { namespace space {\
		class T;\
	}}\
	DEALLOCATEARRAYINTERNAL(adsk::space::T*)

DEALLOCATEARRAYINTERNAL(char)
DEALLOCATEARRAYINTERNAL(char*)
DEALLOCATEARRAYINTERNAL(int)
DEALLOCATEARRAYINTERNAL(short)
DEALLOCATEARRAYINTERNAL(double)
DEALLOCATEARRAYINTERNAL(bool)
DEALLOCATEARRAYINTERNAL(float)
DEALLOCATEARRAYINTERNAL(size_t)
DEALLOCATEARRAYINTERNALCLASS(core, Attribute)
DEALLOCATEARRAYINTERNALCLASS(core, Point3D)
DEALLOCATEARRAYINTERNALCLASS(core, Point2D)
DEALLOCATEARRAYINTERNALCLASS(core, CommandDefinition)
DEALLOCATEARRAYINTERNALCLASS(core, Vector3D)
DEALLOCATEARRAYINTERNALCLASS(core, Vector2D)
DEALLOCATEARRAYINTERNALCLASS(core, Color)
DEALLOCATEARRAYINTERNALCLASS(core, Base)
DEALLOCATEARRAYINTERNALCLASS(core, Curve3D)
DEALLOCATEARRAYINTERNALCLASS(core, User)
DEALLOCATEARRAYINTERNALCLASS(core, Selection)
DEALLOCATEARRAYINTERNALCLASS(fusion, BRepBody)
DEALLOCATEARRAYINTERNALCLASS(fusion, BRepEdge)
DEALLOCATEARRAYINTERNALCLASS(fusion, BRepFace)
DEALLOCATEARRAYINTERNALCLASS(fusion, ConstructionPlane)
DEALLOCATEARRAYINTERNALCLASS(fusion, ConstructionPoint)
DEALLOCATEARRAYINTERNALCLASS(fusion, ConstructionAxis)
DEALLOCATEARRAYINTERNALCLASS(fusion, Sketch)
DEALLOCATEARRAYINTERNALCLASS(fusion, MeshBody)
DEALLOCATEARRAYINTERNALCLASS(fusion, Occurrence)
DEALLOCATEARRAYINTERNALCLASS(fusion, SketchCurve)
DEALLOCATEARRAYINTERNALCLASS(fusion, SketchEntity)
DEALLOCATEARRAYINTERNALCLASS(fusion, SketchLine)
DEALLOCATEARRAYINTERNALCLASS(fusion, Joint)
DEALLOCATEARRAYINTERNALCLASS(fusion, AsBuiltJoint)
DEALLOCATEARRAYINTERNALCLASS(fusion, RigidGroup)
DEALLOCATEARRAYINTERNALCLASS(fusion, JointOrigin)
DEALLOCATEARRAYINTERNALCLASS(fusion, CustomGraphicsCoordinates)

namespace adsk
{
namespace core
{
	// delete an allocated address returned from an interface
	template<class T> void DeallocateArray(T* p) { DeallocateArrayInternal(p); }

} // namespace core
} // namespace adsk

#undef xIDEALLOCATOR_API