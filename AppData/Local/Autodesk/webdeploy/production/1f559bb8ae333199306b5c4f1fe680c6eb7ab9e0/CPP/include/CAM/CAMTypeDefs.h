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

namespace adsk { namespace cam {

/// List of the formats to choose from when generating setup sheets
enum SetupSheetFormats
{
    HTMLFormat,
    ExcelFormat
};

/// The valid options for the Operation Type of a Setup.
enum OperationTypes
{
    MillingOperation,
    TurningOperation,
    JetOperation
};

/// List of the valid options for the outputUnit property on a PostProcessInput object .
enum PostOutputUnitOptions
{
    DocumentUnitsOutput,
    InchesOutput,
    MillimetersOutput
};

/// The valid options for the Strategy Type of an operation.
enum OperationStrategyTypes
{
    AdaptiveClearing2D,
    Pocket2D,
    Face,
    Contour2D,
    Slot,
    Trace,
    Thread,
    Bore,
    Circular,
    Engrave,
    AdaptiveClearing,
    PocketClearing,
    Parallel,
    Contour,
    Ramp,
    Horizontal,
    Pencil,
    Scallop,
    Spiral,
    Radial,
    MorphedSpiral,
    Projection,
    Drilling,
    Jet2D,
    TurningChamfer,
    TurningFace,
    TurningGroove,
    TurningPart,
    TurningProfile,
    TurningProfileGroove,
    TurningStockTransfer,
    TurningThread
};

/// The possible states of an operation
enum OperationStates
{
    IsValidOperationState,
    IsInvalidOperationState,
    SuppressedOperationState,
    NoToolpathOperationState
};
}// namespace cam
}// namespace adsk
