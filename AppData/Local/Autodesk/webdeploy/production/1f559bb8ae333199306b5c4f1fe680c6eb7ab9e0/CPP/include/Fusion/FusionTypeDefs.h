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

namespace adsk { namespace fusion {

/// Types that define the nature of the relationship between a point and a containing entity.
enum PointContainment
{
    PointInsidePointContainment,
    PointOnPointContainment,
    PointOutsidePointContainment,
    UnknownPointContainment
};

/// Defines the various options when converting the geometry of a B-Rep body or face
/// to NURBS. This is used by the convert method of the BRepBody and BRepFace objects.
enum BRepConvertOptions
{
    ProceduralToNURBSConversion,
    AnalyticsToNURBSConversion,
    PlanesToNURBSConversion,
    SplitPeriodicFacesConversion = 4
};

/// Specifies the different types of corners that can be created when offsetting a wire body.
enum OffsetCornerTypes
{
    CircularOffsetCornerType,
    LinearOffsetCornerType,
    ExtendedOffsetCornerType
};

/// Defines the different type of boolean operations that are supported.
enum BooleanTypes
{
    DifferenceBooleanType,
    IntersectionBooleanType,
    UnionBooleanType
};

/// Used by the findBRepUsingRay and findBRepUsingPoint methods to specify the desired return type.
enum BRepEntityTypes
{
    BRepBodyEntityType,
    BRepFaceEntityType,
    BRepEdgeEntityType,
    BRepVertexEntityType
};

/// The different accuracy settings for calculating area and physical property related values.
/// The higher the accuracy setting, the longer it will take to perform the calculations.
enum CalculationAccuracy
{
    LowCalculationAccuracy,
    MediumCalculationAccuracy,
    HighCalculationAccuracy,
    VeryHighCalculationAccuracy
};

/// Specifies the different types of directions that can be used to define directions of a joint.
enum JointDirections
{
    XAxisJointDirection,
    YAxisJointDirection,
    ZAxisJointDirection,
    CustomJointDirection
};

/// The various states that a feature can be in. This is used for the
/// states of modeling features, construction geometry, and sketches.
enum FeatureHealthStates
{
    HealthyFeatureHealthState,
    WarningFeatureHealthState,
    ErrorFeatureHealthState,
    SuppressedFeatureHealthState,
    RolledBackFeatureHealthState,
    UnknownFeatureHealthState
};

/// List of the various keypoints of geometry that can be used when defining joint geometry.
enum JointKeyPointTypes
{
    StartKeyPoint,
    MiddleKeyPoint,
    EndKeyPoint,
    CenterKeyPoint
};

/// List of the different types of ways that geometry for a joint can be defined.
enum JointGeometryTypes
{
    JointConstructionPointGeometry,
    JointSketchPointGeometry,
    JointBRepVertexGeometry,
    JointBRepEdgeGeometry,
    JointSketchCurveGeometry,
    JointProfileGeometry,
    JointPlanarBRepFaceGeometry,
    JointNonPlanarBRepFaceGeometry,
    JointBetweenTwoPlanesGeometry
};

/// List of the various types of joints.
enum JointTypes
{
    RigidJointType,
    RevoluteJointType,
    SliderJointType,
    CylindricalJointType,
    PinSlotJointType,
    PlanarJointType,
    BallJointType
};

/// List of the valid extent directions.
enum ExtentDirections
{
    PositiveExtentDirection,
    NegativeExtentDirection,
    SymmetricExtentDirection
};

/// List of the different operations a feature can perform.
enum FeatureOperations
{
    JoinFeatureOperation,
    CutFeatureOperation,
    IntersectFeatureOperation,
    NewBodyFeatureOperation,
    NewComponentFeatureOperation
};

/// Specifies the different types of entities that can be patterned.
enum PatternEntityTypes
{
    FacesPatternType,
    FeaturesPatternType,
    BodiesPatternType,
    OccurrencesPatternType
};

/// Used to indicate which type of extent is used for a feature.
enum FeatureExtentTypes
{
    OneSideFeatureExtentType,
    TwoSidesFeatureExtentType,
    SymmetricFeatureExtentType
};

/// List of the different types of holes.
enum HoleTypes
{
    SimpleHoleType,
    CounterboreHoleType,
    CountersinkHoleType
};

/// List of the valid edge positions for holes.
enum HoleEdgePositions
{
    EdgeStartPointPosition,
    EdgeMidPointPosition,
    EdgeEndPointPosition
};

/// List of the different ways a chamfer can be defined.
enum ChamferTypes
{
    EqualDistanceChamferType,
    TwoDistancesChamferType,
    DistanceAndAngleChamferType
};

/// Controls options used when creating a Path and determing the rules for how curves are
/// considered to be chained or connected.
enum ChainedCurveOptions
{
    noChainedCurves,
    connectedChainedCurves,
    tangentChainedCurves,
    openEdgesChainedCurves,
    tangentAndOpenEdgesChainedCurves
};

/// List of the types of sweep orientation.
enum SweepOrientationTypes
{
    ParallelOrientationType,
    PerpendicularOrientationType
};

/// List of the sweep profile scaling options.
enum SweepProfileScalingOptions
{
    SweepProfileScaleOption,
    SweepProfileStretchOption,
    SweepProfileNoScalingOption
};

/// List of the compute options for mirroring and patterning features in the parametric modeling environment.
enum PatternComputeOptions
{
    OptimizedPatternCompute,
    IdenticalPatternCompute,
    AdjustPatternCompute
};

/// Defines the different ways to specify the spacing between elements in a pattern.
enum PatternDistanceType
{
    ExtentPatternDistanceType,
    SpacingPatternDistanceType
};

/// List of the types of thread location.
enum ThreadLocations
{
    HighEndThreadLocation,
    LowEndThreadLocation
};

/// List of the ways to split a face using the split face feature.
enum SplitFaceSplitTypes
{
    surfaceIntersectionSplitType,
    alongVectorSplitType,
    closestPointSplitType
};

/// List of Silhouette Split feature operations.
enum SilhouetteSplitOperations
{
    SilhouetteSplitFacesOnlyOperation,
    SilhouetteSplitShelledBodyOperation,
    SilhouetteSplitSolidBodyOperation
};

/// List of the coil types.
enum CoilFeatureTypes
{
    RevolutionsAndHeightCoilFeatureType,
    RevolutionsAndPitchCoilFeatureType,
    HeightAndPitchCoilFeatureType,
    SpiralCoilFeatureType
};

/// List of the section types of coil primitive feature.
enum CoilFeatureSectionTypes
{
    CircularCoilFeatureSectionType,
    SquareCoilFeatureSectionType,
    TriangularExternalCoilFeatureSectionType,
    TriangularInternalCoilFeatureSectionType
};

/// List of the section positions of coil feature.
enum CoilFeatureSectionPositions
{
    InsideCoilFeatureSectionPosition,
    OnCenterCoilFeatureSectionPosition,
    OutsideCoilFeatureSectionPosition
};

/// List of Surface Continuity Types.
enum SurfaceContinuityTypes
{
    ConnectedSurfaceContinuityType,
    TangentSurfaceContinuityType,
    CurvatureSurfaceContinuityType
};

/// List of Surface Extend Types.
enum SurfaceExtendTypes
{
    NaturalSurfaceExtendType,
    TangentSurfaceExtendType,
    PerpendicularSurfaceExtendType
};

/// Valid unit types for distance
enum DistanceUnits
{
    MillimeterDistanceUnits,
    CentimeterDistanceUnits,
    MeterDistanceUnits,
    InchDistanceUnits,
    FootDistanceUnits
};

/// The valid options for the Design History (default design type) setting.
enum DefaultDesignTypeOptions
{
    PromptForDesignTypeOption,
    DirectDesignTypeOption,
    ParametricDesignTypeOption
};

/// The valid options for the Default workspaces setting.
enum DefaultWorkspaces
{
    ModelWorkspace,
    SculptWorkspace,
    PatchWorkspace
};

/// Fusion 360 design types
enum DesignTypes
{
    DirectDesignType,
    ParametricDesignType
};

/// The expression of the parameter. Setting this can fail because of an invalid expression or
/// because a cyclic reference is created between parameters.
enum ExpressionError
{
    CyclicParameterReferenceError = 200
};

/// Specific error types for DeleteMe methods.
enum DeleteMeError
{
    ParameterReferencedByOtherParameterError = 200
};

/// The different refinement settings supported when exporting the design as an STL file.
enum MeshRefinementSettings
{
    MeshRefinementHigh,
    MeshRefinementMedium,
    MeshRefinementLow,
    MeshRefinementCustom
};

/// The various culling modes supported by custom graphics.
enum CustomGraphicsCullModes
{
    CustomGraphicsCullFront,
    CustomGraphicsCullBack,
    CustomGraphicsCullNone
};

/// Specifies the different styles that can be used to control billboarding.
enum CustomGraphicsBillBoardStyles
{
    ScreenBillBoardStyle = 1,
    AxialBillBoardStyle,
    RightReadingBillBoardStyle
};

/// Specifies which of the four view corners custom graphics will be drawn in relation to. The
/// notUsedViewCorner setting indicates the graphics are not positioned with respect to the view.
enum ViewCorners
{
    upperLeftViewCorner,
    upperRightViewCorner,
    lowerLeftViewCorner,
    lowerRightViewCorner
};

/// A list of predefined point images that you can use for a CustomGraphicsPointSet.
enum CustomGraphicsPointTypes
{
    UserDefinedCustomGraphicsPointType,
    PointCloudCustomGraphicsPointType
};

/// Specifies the line styles that can be applied to custom graphics lines and curves.
enum LineStylePatterns
{
    continuousLineStylePattern,
    centerLineStylePattern,
    dashedLineStylePattern,
    dotLineStylePattern,
    hiddenLineStylePattern,
    phantomLineStylePattern,
    tracksLineStylePattern,
    zigzagLineStylePattern
};

/// The unit types that can be specified when importing a .stl or .obj file as a mesh.
enum MeshUnits
{
    CentimeterMeshUnit,
    MillimeterMeshUnit,
    MeterMeshUnit,
    InchMeshUnit,
    FootMeshUnit
};

/// Types that indicate the level of quality of a triangle mesh.
enum TriangleMeshQualityOptions
{
    LowQualityTriangleMesh = 8,
    NormalQualityTriangleMesh = 11,
    HighQualityTriangleMesh = 13,
    VeryHighQualityTriangleMesh = 15
};

/// Used by the Sketch.projectToSurface method when defined how to project a curve onto a surface.
enum SurfaceProjectTypes
{
    ClosestPointSurfaceProjectType,
    AlongVectorSurfaceProjectType
};

/// Defines the various text style formatting options that can be applied to text. These are
/// bitwise values to they can be combined.
enum TextStyles
{
    TextStyleBold = 1,
    TextStyleItalic,
    TextStyleUnderline = 4
};

/// The different dimension orientations.
enum DimensionOrientations
{
    AlignedDimensionOrientation,
    HorizontalDimensionOrientation,
    VerticalDimensionOrientation
};
}// namespace fusion
}// namespace adsk
