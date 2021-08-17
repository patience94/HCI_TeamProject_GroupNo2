#Author-Proto Labs, Inc.
#Description-Protolabs Autodesk Fusion helpers
#Copyright (c) 2019 Proto Labs, Inc. All Rights Reserved.

import adsk.fusion

from ._ProtoLabs_logging import getRootLogger
logger = getRootLogger().getChild('_ProtoLabs_ADFusion')

# There seems to be an issue with the Autodesk generators in Python 3.5
generatorWorkaround = True

def containsAnyBodies(design):
    if generatorWorkaround:
        return any([component.bRepBodies.count > 0 for component in design.allComponents])
    else:
        return any(component.bRepBodies.count > 0 for component in design.allComponents)

def getComponent(entity):
    if isinstance(entity, adsk.fusion.Component):
        return entity
    if isinstance(entity, adsk.fusion.BRepBody):
        return entity.parentComponent
    return entity.component

def getMatchingOccurrences(occurrence, includeInput=False):
    occurrences = getOccurrences(occurrence.component)
    if not includeInput:
        occurrences.remove(occurrence)
    return occurrences

def getOccurrences(component):
    allOccurrencesOfComponent = component.parentDesign.rootComponent.allOccurrencesByComponent(component)
    return [occurrence for occurrence in allOccurrencesOfComponent]

def getUniqueEntities(entities):
    # Fusion entities are not hashable, so we cannot convert to a set.
    uniqueEntities = []
    for entity in entities:
        if entity not in uniqueEntities:
            uniqueEntities.append(entity)
    return uniqueEntities

def createComponentWithMergedBodies(component):

    if getAllBodiesCount(component) <= 1:
        logger.debug('component does not require merging')

        return None

    logger.info('Merging bodies from component: ' + component.name)

    mergeSource = component

    # If there are nested components, we first need to copy all of the bodies
    # into a single component with the proper transformations.
    if getAllBodiesCount(component) != component.bRepBodies.count:

        # Create new component.
        newOccurrence = component.parentDesign.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        mergeSource = newOccurrence.component

        # Copy bodies into new component.
        copyAllBodiesToOccurrence(component, newOccurrence)

    # Merge bodies into single body.
    newComponent = mergeBodiesInComponent(mergeSource, mergeSource == component)

    # Update names for clarification in case the user re-applies our changes.
    newComponent.name = component.name + ' (merged)'
    newComponent.bRepBodies.item(0).name = 'merge'

    return newComponent

def copyAllBodiesToOccurrence(source, destOccurrence, startTransform = None):

    destComponent = destOccurrence.component
    sourceComponent = source
    combinedTransform = startTransform
    if isinstance(source, adsk.fusion.Occurrence):
        sourceComponent = source.component
        if not source.transform.isEqualTo(adsk.core.Matrix3D.create()):
            combinedTransform = source.transform.copy()
            if startTransform is not None:
                combinedTransform.transformBy(startTransform)

    if sourceComponent != destComponent:
        logger.debug('copying bodies from: ' + source.name)

        bodiesToMove = adsk.core.ObjectCollection.create()
        for body in sourceComponent.bRepBodies:
            bodiesToMove.add(body.copyToComponent(destOccurrence))

        if combinedTransform is not None:
            logger.debug('moving bodies')
            moveInput = destComponent.features.moveFeatures.createInput(bodiesToMove, combinedTransform)
            destComponent.features.moveFeatures.add(moveInput)

        for occurrence in sourceComponent.occurrences:
            copyAllBodiesToOccurrence(occurrence, destOccurrence, combinedTransform)

def mergeBodiesInComponent(component, createComponent):

    if component.bRepBodies.count < 1:
        return None

    body1 = component.bRepBodies.item(0)
    toolBodies = adsk.core.ObjectCollection.create()
    for index in range(1, component.bRepBodies.count):
        toolBodies.add(component.bRepBodies.item(index))

    combineInput = component.features.combineFeatures.createInput(body1, toolBodies)
    combineInput.isNewComponent = createComponent
    combineInput.isKeepToolBodies = createComponent

    combineFeature = component.features.combineFeatures.add(combineInput)

    return combineFeature.parentComponent


def getAllBodiesCount(component):
    if generatorWorkaround:
        return component.bRepBodies.count + sum([getAllBodiesCount(getComponent(occurrence)) for occurrence in component.occurrences])
    else:
        return component.bRepBodies.count + sum(getAllBodiesCount(getComponent(occurrence)) for occurrence in component.occurrences)

