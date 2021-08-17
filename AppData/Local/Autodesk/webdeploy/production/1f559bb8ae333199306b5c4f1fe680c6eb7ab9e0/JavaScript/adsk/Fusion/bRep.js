/*global console*/
/*global define*/
/*global window*/
/*jslint vars: true, nomen: true, plusplus: true*/

(function (root, factory) {

    'use strict';

    if (typeof define === 'function' && define.amd) {
        // using require.js
        define(['./application.js'], factory);
    } else {
        root.adsk = factory(root.adsk);
    }
}(this, function (adsk) {

    'use strict';

    if (adsk === undefined) {
        adsk = {
            objectTypes: {}
        };
    }
    if (adsk.fusion === undefined) {
        adsk.fusion = {};
    }

    //=========== BooleanTypes ============
    // Defines the different type of boolean operations that are supported.
    adsk.fusion.BooleanTypes = {
        DifferenceBooleanType : 0,
        IntersectionBooleanType : 1,
        UnionBooleanType : 2
    };

    //=========== BRepBodies ============
    // The BRepBodies collection provides access to all of the B-Rep
    // bodies within a component.
    adsk.fusion.BRepBodies = function BRepBodies(handle) {
        if (!(this instanceof adsk.fusion.BRepBodies)) {
            return adsk.fusion.BRepBodies.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepBodies.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepBodies.prototype.constructor = adsk.fusion.BRepBodies;
    adsk.fusion.BRepBodies.classType = function classType () {
        return 'adsk::fusion::BRepBodies';
    };
    adsk.fusion.BRepBodies.interfaceId = 'adsk.fusion.BRepBodies';
    adsk.objectTypes['adsk.fusion.BRepBodies'] = adsk.fusion.BRepBodies;
    adsk.fusion.BRepBodies.cast = function (object) {
        return object instanceof adsk.fusion.BRepBodies ? object : null;
    };

    // Returns the number of bodies in the collection.
    Object.defineProperty(adsk.fusion.BRepBodies.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified body using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.BRepBodies.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Returns a specific body using the name of the body within the collection.
    // name : The name of the body, as seen in the browser, to return.
    // The BRepBody or null if a body with the defined name is not found.
    adsk.fusion.BRepBodies.prototype.itemByName = function (name) {
        if (name === undefined || name === null || name.constructor !== String) { throw new TypeError('name must be a string'); }
        var args = {
            name : name
        };
        var result = this._execute('itemByName', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a new BRepBody object. The input can be a persisted or transient BRepBody and the
    // result is a persisted BRepBody. In a model where the design history is ignored (direct edit model)
    // the BRepBody is created within the component the BRepBodies collection was obtained from. In
    // a model where the design history is captured (parametric model), the new BRepBody is created
    // within the specified Base Feature.
    // Because of a current limitation, if you want to create a BRepBody in a parametric model,
    // you must first call the edit method of the base feature, then use the add method to create
    // the body, and finally call the finishEdit method of the base feature. The base
    // feature must be in an "edit" state to be able to add any additional items to it.
    // body : The input BRepBody. Typically this is a transient BRepBody but that's not a requirement. In
    // any case, there is not any association back to the original BRepBody.
    // targetBaseFeature : The BaseFeature object that this B-Rep body will be associated with. This is an optional
    // requirement but is required when the model design history is being captured (parametric model) but is
    // ignored otherwise (direct edit model).
    // Returns the newly created BRepBody or null if the creation failed.
    adsk.fusion.BRepBodies.prototype.add = function (body, targetBaseFeature) {
        if (body !== null && !(body instanceof adsk.fusion.BRepBody)) { throw new TypeError('body must be a adsk.fusion.BRepBody'); }
        if (targetBaseFeature === null || (targetBaseFeature !== undefined && targetBaseFeature !== null && !(targetBaseFeature instanceof adsk.fusion.BaseFeature))) { throw new TypeError('targetBaseFeature must be a adsk.fusion.BaseFeature'); }
        var args = {
            body : (body === null ? body : body.handle)
        };
        if (targetBaseFeature !== undefined) {
            args.targetBaseFeature = (targetBaseFeature === null ? targetBaseFeature : targetBaseFeature.handle);
        }
        var result = this._execute('add', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    //=========== BRepBody ============
    // Represents a B-Rep (Boundary Representation) body.
    adsk.fusion.BRepBody = function BRepBody(handle) {
        if (!(this instanceof adsk.fusion.BRepBody)) {
            return adsk.fusion.BRepBody.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepBody.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepBody.prototype.constructor = adsk.fusion.BRepBody;
    adsk.fusion.BRepBody.classType = function classType () {
        return 'adsk::fusion::BRepBody';
    };
    adsk.fusion.BRepBody.interfaceId = 'adsk.fusion.BRepBody';
    adsk.objectTypes['adsk.fusion.BRepBody'] = adsk.fusion.BRepBody;
    adsk.fusion.BRepBody.cast = function (object) {
        return object instanceof adsk.fusion.BRepBody ? object : null;
    };

    // Returns the component this body is owned by.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'parentComponent', {
        get : function () {
            var result = this._execute('parentComponent');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Component) : null;
        }
    });

    // Returns a collection of all of the lumps in the body.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'lumps', {
        get : function () {
            var result = this._execute('lumps');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLumps) : null;
        }
    });

    // Returns a collection of all of the shells in the body.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'shells', {
        get : function () {
            var result = this._execute('shells');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepShells) : null;
        }
    });

    // Returns a collection of all of the faces in the body.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'faces', {
        get : function () {
            var result = this._execute('faces');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFaces) : null;
        }
    });

    // Returns a collection of all of the edges in the body.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'edges', {
        get : function () {
            var result = this._execute('edges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdges) : null;
        }
    });

    // Returns a collection of all of the vertices in the body.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'vertices', {
        get : function () {
            var result = this._execute('vertices');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertices) : null;
        }
    });

    // Returns whether this body is closed (solid) or not.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'isSolid', {
        get : function () {
            var result = this._execute('isSolid');
            return result ? result.value : undefined;
        }
    });

    // Returns the bounding box of this body.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'boundingBox', {
        get : function () {
            var result = this._execute('boundingBox');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.BoundingBox3D) : null;
        }
    });

    // Returns all of the edges that connect concave faces.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'concaveEdges', {
        get : function () {
            var result = this._execute('concaveEdges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdges) : null;
        }
    });

    // Returns all of the edges that connect convex faces.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'convexEdges', {
        get : function () {
            var result = this._execute('convexEdges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdges) : null;
        }
    });

    // Returns the area in cm ^ 2.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'area', {
        get : function () {
            var result = this._execute('area');
            return result ? result.value : undefined;
        }
    });

    // Returns the volume in cm ^ 3. Returns 0 in the case the body is not solid.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'volume', {
        get : function () {
            var result = this._execute('volume');
            return result ? result.value : undefined;
        }
    });

    // Indicates if this body is represented in the model or is transient.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'isTransient', {
        get : function () {
            var result = this._execute('isTransient');
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the name of the body.
    // This property is only valid if the IsTransient property is false.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'name', {
        get : function () {
            var result = this._execute('name');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (value === undefined || value === null || value.constructor !== String) { throw new TypeError('value must be a string'); }
            var args = {
                value : value
            };
            var result = this._execute('name', args);
            return result ? result.value : undefined;
        }
    });

    // Gets if this body is currently visible in the graphics window. Use the
    // isLightBulbOn to change if the light bulb beside the body node in the
    // browser is on or not. Parent nodes in the browser can have their light
    // bulb off which affects all of their children. This property indicates
    // the final result and whether this body is actually visible or not.
    // This property is only valid if the IsTransient property is false.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'isVisible', {
        get : function () {
            var result = this._execute('isVisible');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isVisible', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets if this body is selectable.
    // This property is only valid if the IsTransient property is false.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'isSelectable', {
        get : function () {
            var result = this._execute('isSelectable');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isSelectable', args);
            return result ? result.value : undefined;
        }
    });

    // Read-write property that gets and sets the current appearance of the body. Setting this property will result in applying
    // an override appearance to the body and the AppearanceSourceType property will return OverrideAppearanceSource. Setting
    // this property to null will remove any override.
    // This property is only valid if the IsTransient property is false.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'appearance', {
        get : function () {
            var result = this._execute('appearance');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Appearance) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Appearance)) { throw new TypeError('value must be a adsk.core.Appearance'); }
            var args = {
                value : value
            };
            var result = this._execute('appearance', args);
            return result ? result.value : undefined;
        }
    });

    // Read-write property that gets the source of the appearance for the body. If this returns OverrideAppearanceSource, an override exists
    // on this body. The override can be removed by setting the Appearance property to null.
    // This property is only valid if the IsTransient property is false.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'appearanceSourceType', {
        get : function () {
            var result = this._execute('appearanceSourceType');
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the material assigned to this body.
    // This property is only valid if the IsTransient property is false.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'material', {
        get : function () {
            var result = this._execute('material');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Material) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Material)) { throw new TypeError('value must be a adsk.core.Material'); }
            var args = {
                value : value
            };
            var result = this._execute('material', args);
            return result ? result.value : undefined;
        }
    });

    // Returns the mesh manager object for this body.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'meshManager', {
        get : function () {
            var result = this._execute('meshManager');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshManager) : null;
        }
    });

    // Returns the assembly occurrence (i.e. the occurrence) of this
    // object in an assembly. This is only valid in the case where this
    // BRepBody object is acting as a proxy in an assembly. Returns null
    // in the case where the object is not in the context of an assembly.
    // but is already the native object. Also returns null in the case
    // where this body is transient.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    // Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc
    // of this body. Property values will be calulated using the 'LowCalculationAccuracy' setting when using this property
    // to get the PhysicalProperties object. To specify a higher calculation tolerance, use the getPhysicalProperties method
    // on the Design class instead.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'physicalProperties', {
        get : function () {
            var result = this._execute('physicalProperties');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.PhysicalProperties) : null;
        }
    });

    // Gets and set if the light bulb beside the body node in the
    // browser is on or not. Parent nodes in the browser can have their light
    // bulb off which affects all of their children so this property does not
    // indicate if the body is actually visible, just that it should be visible
    // if all of it's parent nodes are also visible. Use the isVisible property
    // to determine if it's actually visible.
    // This property is only valid if the IsTransient property is false.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'isLightBulbOn', {
        get : function () {
            var result = this._execute('isLightBulbOn');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isLightBulbOn', args);
            return result ? result.value : undefined;
        }
    });

    // Returns the collection of attributes associated with this face.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'attributes', {
        get : function () {
            var result = this._execute('attributes');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Attributes) : null;
        }
    });

    // If this body is associated with a base feature, this property will return that base feature.
    // If it's not associated with a base feature, this property will return null.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'baseFeature', {
        get : function () {
            var result = this._execute('baseFeature');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BaseFeature) : null;
        }
    });

    // Gets and sets the opacity override assigned to this body. A value of 1.0 specifies
    // that is it completely opaque and a value of 0.0 specifies that is it completely transparent.
    // This value is not necessarily related to what the user sees because the opacity is inherited.
    // For example, if you this body is in a component and that component's opacity is set to something
    // other than 1.0, the body will also be shown as slightly transparent even though the opacity
    // property for the body will return 1.0. Because the component that contains the body can be
    // referenced as an occurrence in other components and they can have different opacity settings,
    // it's possible that different instances of the same body can display using different opacity levels.
    // To get the opacity that it is being displayed with use the BrepBody.visibleOpacity property.
    // This is the API equivalent of the "Opacity Control" command available for the body in the browser.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'opacity', {
        get : function () {
            var result = this._execute('opacity');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('opacity', args);
            return result ? result.value : undefined;
        }
    });

    // The user can set an override opacity for components and bodies these opacity overrides combine if
    // children and parent components have overrides. This property returns the actual opacity that is
    // being used to render the body. To set the opacity use the opacity property of the BRepBody object.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'visibleOpacity', {
        get : function () {
            var result = this._execute('visibleOpacity');
            return result ? result.value : undefined;
        }
    });

    // Returns the current revision ID of the body. This ID changes any time the body is modified in any way. By getting
    // and saving the ID when you create any data that is dependent on the body, you can then compare the saved
    // ID with the current ID to determine if the body has changed to know if you should update your data.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'revisionId', {
        get : function () {
            var result = this._execute('revisionId');
            return result ? result.value : undefined;
        }
    });

    // Returns any wire bodies that exist within this body.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'wires', {
        get : function () {
            var result = this._execute('wires');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepWires) : null;
        }
    });

    // Indicates if this body is represented in the model or is temporary.
    Object.defineProperty(adsk.fusion.BRepBody.prototype, 'isTemporary', {
        get : function () {
            var result = this._execute('isTemporary');
            return result ? result.value : undefined;
        }
    });

    // Determines the relationship of the input point with respect to this body.
    // point : The point to do the containment check for.
    // Returns a value from the PointContainment enum indicating the relationship of
    // the input point to the body.
    adsk.fusion.BRepBody.prototype.pointContainment = function (point) {
        if (point !== null && !(point instanceof adsk.core.Point3D)) { throw new TypeError('point must be a adsk.core.Point3D'); }
        var args = {
            point : (point === null ? point : point.handle)
        };
        var result = this._execute('pointContainment', args);
        return result ? result.value : undefined;
    };

    // Deletes the body.
    // This property is only valid if the IsTransient property is false.
    // Returns true if the delete was successful.
    adsk.fusion.BRepBody.prototype.deleteMe = function () {
        var result = this._execute('deleteMe');
        return result ? result.value : undefined;
    };

    // Copies the body to the clipboard.
    // This property is only valid if the IsTransient property is false.
    // Returns true if the copy was successful.
    adsk.fusion.BRepBody.prototype.copy = function () {
        var result = this._execute('copy');
        return result ? result.value : undefined;
    };

    // Cuts the body to the clipboard.
    // This property is only valid if the IsTransient property is false.
    // Returns true if the cut was successful.
    adsk.fusion.BRepBody.prototype.cut = function () {
        var result = this._execute('cut');
        return result ? result.value : undefined;
    };

    // Returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // This method is only valid if the IsTransient property is false.
    // occurrence : The occurrence that defines the context for the created proxy.
    // Returns the new BRepBoy proxy or null if this isn't the NativeObject.
    adsk.fusion.BRepBody.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a new component and occurrence within the component that currently owns this body.
    // This body is moved into the new component and returned. The newly created component can be
    // obtained by using the parentComponent property of the BRepBody object.
    // This method is only valid if the IsTransient property is false.
    // Returns the BRrepBody in the new component or null in the case the creation failed.
    adsk.fusion.BRepBody.prototype.createComponent = function () {
        var result = this._execute('createComponent');
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Moves this body from it's current component into the root component or the component owned by the
    // specified occurrence.
    // target : The target can be either the root component or an occurrence.
    // In the case where an occurrence is specified, the body will be moved into the parent component of the target
    // occurrence and the target occurrence defines the transform of how the body will be copied so that the body
    // maintains it's same position with respect to the assembly.
    // Returns the moved BRepBody or null in the case the move failed.
    adsk.fusion.BRepBody.prototype.moveToComponent = function (target) {
        if (target !== null && !(target instanceof adsk.core.Base)) { throw new TypeError('target must be a adsk.core.Base'); }
        var args = {
            target : (target === null ? target : target.handle)
        };
        var result = this._execute('moveToComponent', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a copy of this body into the specified target.
    // target : The target can be either the root component or an occurrence.
    // In the case where an occurrence is specified, the body will be copied into the parent component of the target
    // occurrence and the target occurrence defines the transform of how the body will be copied so that the body
    // maintains it's same position with respect to the assembly.
    // If target is null, then a copy of the body is created in the owning component of the original body.
    // Returns the moved BRepBody or null in the case the move failed.
    adsk.fusion.BRepBody.prototype.copyToComponent = function (target) {
        if (target !== null && !(target instanceof adsk.core.Base)) { throw new TypeError('target must be a adsk.core.Base'); }
        var args = {
            target : (target === null ? target : target.handle)
        };
        var result = this._execute('copyToComponent', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a new body where the faces and edges are converted to different
    // types of geometry based on the input options. This is particularly useful
    // when you need a body made up entirely of NURBS surfaces.
    // The tempId on the faces, edges, and vertices on the new body will match
    // with the corresponding tempId on the original body. In cases where faces are
    // split as a result of the conversion there can be more than one face or edge in
    // the new body that matches to a single face or edge in the original body. The
    // findByTempId method will find the entity with the matching id.
    // options : Input options that define how the conversion should be done. These are
    // bitwise options so they can be combined.
    // Returns the new converted body or null in the case of failure.
    adsk.fusion.BRepBody.prototype.convert = function (options) {
        if (!isFinite(options)) { throw new TypeError('options must be a number'); }
        var args = {
            options : Number(options)
        };
        var result = this._execute('convert', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Returns all of the faces, edges, or vertices that match the input ID.
    // tempId : The ID of the B-Rep entity to find.
    // Returns an array of entities that have the specified ID. This
    // returns an array because it's possible that a body created by converting a
    // body can have multiple entities with the same ID in the case where a curve
    // or face was split. Returns an empty array in the case where no match is found.
    adsk.fusion.BRepBody.prototype.findByTempId = function (tempId) {
        if (!isFinite(tempId)) { throw new TypeError('tempId must be a number'); }
        var args = {
            tempId : Number(tempId)
        };
        var result = this._execute('findByTempId', args);
        if (!result || !Array.isArray(result.value)) {
            return undefined
        }
        var resultIter;
        var resultValue = [];
        for (resultIter = 0; resultIter < result.value.length; ++resultIter) {
            resultValue[resultIter] = (result.value[resultIter] !== undefined) ? adsk.createObject(result.value[resultIter], adsk.core.Base) : null;
        }
        return resultValue
    };

    //=========== BRepCoEdge ============
    // Represents the use of a BRepEdge by a BRepFace.
    adsk.fusion.BRepCoEdge = function BRepCoEdge(handle) {
        if (!(this instanceof adsk.fusion.BRepCoEdge)) {
            return adsk.fusion.BRepCoEdge.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepCoEdge.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepCoEdge.prototype.constructor = adsk.fusion.BRepCoEdge;
    adsk.fusion.BRepCoEdge.classType = function classType () {
        return 'adsk::fusion::BRepCoEdge';
    };
    adsk.fusion.BRepCoEdge.interfaceId = 'adsk.fusion.BRepCoEdge';
    adsk.objectTypes['adsk.fusion.BRepCoEdge'] = adsk.fusion.BRepCoEdge;
    adsk.fusion.BRepCoEdge.cast = function (object) {
        return object instanceof adsk.fusion.BRepCoEdge ? object : null;
    };

    // Returns the edge this co-edge is associated with.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'edge', {
        get : function () {
            var result = this._execute('edge');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdge) : null;
        }
    });

    // Returns the loop this co-edge is part of.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'loop', {
        get : function () {
            var result = this._execute('loop');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLoop) : null;
        }
    });

    // Returns a curve evaluator that can be used to perform geometric evaluations on the co-edge.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'evaluator', {
        get : function () {
            var result = this._execute('evaluator');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.CurveEvaluator2D) : null;
        }
    });

    // Returns a geometry object that represents the shape of this co-edge in parameter space of the parent face's surface.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'geometry', {
        get : function () {
            var result = this._execute('geometry');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Curve2D) : null;
        }
    });

    // Indicates if the orientation of this co-edge is in the same direction or opposed to its associated edge.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'isOpposedToEdge', {
        get : function () {
            var result = this._execute('isOpposedToEdge');
            return result ? result.value : undefined;
        }
    });

    // Returns if the parametric direction of this co-edge is reversed
    // from the parametric direction of the underlying curve obtained from the geometry property.
    // A co-edge's parametric direction is from the start vertex to the end vertex.
    // But the underlying curve geometry may have the opposite parameterization.
    // This property indicates if the parameterization order of the evaluator obtained from
    // this co-edge is reversed from the order of the geometry curve's evaluator.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'isParamReversed', {
        get : function () {
            var result = this._execute('isParamReversed');
            return result ? result.value : undefined;
        }
    });

    // Returns the next co-edge in the loop.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'next', {
        get : function () {
            var result = this._execute('next');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepCoEdge) : null;
        }
    });

    // Returns the body this co-edge is part of.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'body', {
        get : function () {
            var result = this._execute('body');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    // Returns the co-edge on the adjacent face
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'partner', {
        get : function () {
            var result = this._execute('partner');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepCoEdge) : null;
        }
    });

    // Returns the previous co-edge in the loop.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'previous', {
        get : function () {
            var result = this._execute('previous');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepCoEdge) : null;
        }
    });

    // Returns the assembly occurrence (i.e. the occurrence) of this
    // object in an assembly. This is only valid in the case where this
    // BRepCoEdge object is acting as a proxy in an assembly. Returns null
    // in the case where the object is not in the context of an assembly.
    // but is already the native object.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.BRepCoEdge.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepCoEdge) : null;
        }
    });

    // Returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // occurrence : The occurrence that defines the context for the created proxy.
    // Returns the new BrepCoEdge proxy or null if this isn't the NativeObject.
    adsk.fusion.BRepCoEdge.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepCoEdge) : null;
    };

    //=========== BRepCoEdges ============
    // BRepCoEdge Collection.
    adsk.fusion.BRepCoEdges = function BRepCoEdges(handle) {
        if (!(this instanceof adsk.fusion.BRepCoEdges)) {
            return adsk.fusion.BRepCoEdges.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepCoEdges.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepCoEdges.prototype.constructor = adsk.fusion.BRepCoEdges;
    adsk.fusion.BRepCoEdges.classType = function classType () {
        return 'adsk::fusion::BRepCoEdges';
    };
    adsk.fusion.BRepCoEdges.interfaceId = 'adsk.fusion.BRepCoEdges';
    adsk.objectTypes['adsk.fusion.BRepCoEdges'] = adsk.fusion.BRepCoEdges;
    adsk.fusion.BRepCoEdges.cast = function (object) {
        return object instanceof adsk.fusion.BRepCoEdges ? object : null;
    };

    // The number of co-edges in the collection.
    Object.defineProperty(adsk.fusion.BRepCoEdges.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified co-edge using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.BRepCoEdges.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepCoEdge) : null;
    };

    //=========== BRepConvertOptions ============
    // Defines the various options when converting the geometry of a B-Rep body or face
    // to NURBS. This is used by the convert method of the BRepBody and BRepFace objects.
    adsk.fusion.BRepConvertOptions = {
        ProceduralToNURBSConversion : 0,
        AnalyticsToNURBSConversion : 1,
        PlanesToNURBSConversion : 2,
        SplitPeriodicFacesConversion : 4
    };

    //=========== BRepEdge ============
    // Represents a one-dimensional topological element that can be used to bound a BRepFace A BRepEdge uses a single, connected and bounded subset of a curve for it geometry.
    adsk.fusion.BRepEdge = function BRepEdge(handle) {
        if (!(this instanceof adsk.fusion.BRepEdge)) {
            return adsk.fusion.BRepEdge.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepEdge.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepEdge.prototype.constructor = adsk.fusion.BRepEdge;
    adsk.fusion.BRepEdge.classType = function classType () {
        return 'adsk::fusion::BRepEdge';
    };
    adsk.fusion.BRepEdge.interfaceId = 'adsk.fusion.BRepEdge';
    adsk.objectTypes['adsk.fusion.BRepEdge'] = adsk.fusion.BRepEdge;
    adsk.fusion.BRepEdge.cast = function (object) {
        return object instanceof adsk.fusion.BRepEdge ? object : null;
    };

    // Returns the BRepVertex that bounds its low parameter end.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'startVertex', {
        get : function () {
            var result = this._execute('startVertex');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertex) : null;
        }
    });

    // Returns the BRepVertex that bounds its high parameter end.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'endVertex', {
        get : function () {
            var result = this._execute('endVertex');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertex) : null;
        }
    });

    // Returns the BRepFaces that are associated with this edge through its BRepCoEdges.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'faces', {
        get : function () {
            var result = this._execute('faces');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFaces) : null;
        }
    });

    // Returns the parent shell of the edge.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'shell', {
        get : function () {
            var result = this._execute('shell');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepShell) : null;
        }
    });

    // Returns the parent body of the edge.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'body', {
        get : function () {
            var result = this._execute('body');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    // Returns if the edge's geometry is degenerate.
    // For example, the apex of a cone is a degerate edge.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'isDegenerate', {
        get : function () {
            var result = this._execute('isDegenerate');
            return result ? result.value : undefined;
        }
    });

    // Returns CurveEvaluator3D for evaluation.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'evaluator', {
        get : function () {
            var result = this._execute('evaluator');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.CurveEvaluator3D) : null;
        }
    });

    // Returns the underlying curve geometry of the edge.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'geometry', {
        get : function () {
            var result = this._execute('geometry');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Curve3D) : null;
        }
    });

    // Returns if the edge is tolerant.
    // The tolerance used is available from the tolerance property.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'isTolerant', {
        get : function () {
            var result = this._execute('isTolerant');
            return result ? result.value : undefined;
        }
    });

    // Returns the tolerance used by a tolerant edge.
    // This value is only useful when isTolerant is true.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'tolerance', {
        get : function () {
            var result = this._execute('tolerance');
            return result ? result.value : undefined;
        }
    });

    // Returns a sample point guaranteed to lie on the edge's curve, within its boundaries,
    // and not on a vertex (unless this is a degenerate edge).
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'pointOnEdge', {
        get : function () {
            var result = this._execute('pointOnEdge');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Point3D) : null;
        }
    });

    // Returns the BRepCoEdges on the edge.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'coEdges', {
        get : function () {
            var result = this._execute('coEdges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepCoEdges) : null;
        }
    });

    // Returns if the parametric direction of this edge is reversed
    // from the parametric direction of the underlying curve obtained from the geometry property.
    // An edge's parametric direction is from the start vertex to the end vertex.
    // But the underlying curve geometry may have the opposite parameterization.
    // This property indicates if the parameterization order of the evaluator obtained from
    // this edge is reversed from the order of the geometry curve's evaluator.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'isParamReversed', {
        get : function () {
            var result = this._execute('isParamReversed');
            return result ? result.value : undefined;
        }
    });

    // Returns a collection of edges that includes all of the edges tangentially connected
    // to this edge. The result includes this edge. The edges are in the collection
    // in their connected order.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'tangentiallyConnectedEdges', {
        get : function () {
            var result = this._execute('tangentiallyConnectedEdges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.ObjectCollection) : null;
        }
    });

    // Returns the assembly occurrence (i.e. the occurrence) of this
    // object in an assembly. This is only valid in the case where this
    // BRepEdge object is acting as a proxy in an assembly. Returns null
    // in the case where the object is not in the context of an assembly.
    // but is already the native object.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdge) : null;
        }
    });

    // Returns the collection of attributes associated with this face.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'attributes', {
        get : function () {
            var result = this._execute('attributes');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Attributes) : null;
        }
    });

    // Returns the length of the edge in centimeters.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'length', {
        get : function () {
            var result = this._execute('length');
            return result ? result.value : undefined;
        }
    });

    // Returns the temporary ID of this edge. This ID is only good while the document
    // remains open and as long as the owning BRepBody is not modified in any way.
    // The findByTempId method of the BRepBody will return the entity in the body with the given ID.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'tempId', {
        get : function () {
            var result = this._execute('tempId');
            return result ? result.value : undefined;
        }
    });

    // Returns the bounding box of this edge.
    Object.defineProperty(adsk.fusion.BRepEdge.prototype, 'boundingBox', {
        get : function () {
            var result = this._execute('boundingBox');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.BoundingBox3D) : null;
        }
    });

    // Returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // occurrence : The occurrence that defines the context for the created proxy.
    // Returns the new BrepEdge proxy or null if this isn't the NativeObject.
    adsk.fusion.BRepEdge.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdge) : null;
    };

    //=========== BRepEdges ============
    // BRepEdge collection.
    adsk.fusion.BRepEdges = function BRepEdges(handle) {
        if (!(this instanceof adsk.fusion.BRepEdges)) {
            return adsk.fusion.BRepEdges.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepEdges.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepEdges.prototype.constructor = adsk.fusion.BRepEdges;
    adsk.fusion.BRepEdges.classType = function classType () {
        return 'adsk::fusion::BRepEdges';
    };
    adsk.fusion.BRepEdges.interfaceId = 'adsk.fusion.BRepEdges';
    adsk.objectTypes['adsk.fusion.BRepEdges'] = adsk.fusion.BRepEdges;
    adsk.fusion.BRepEdges.cast = function (object) {
        return object instanceof adsk.fusion.BRepEdges ? object : null;
    };

    // The number of edges in the collection.
    Object.defineProperty(adsk.fusion.BRepEdges.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified edge using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.BRepEdges.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdge) : null;
    };

    //=========== BRepFace ============
    // Represent a connected region on a single geometric surface.
    adsk.fusion.BRepFace = function BRepFace(handle) {
        if (!(this instanceof adsk.fusion.BRepFace)) {
            return adsk.fusion.BRepFace.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepFace.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepFace.prototype.constructor = adsk.fusion.BRepFace;
    adsk.fusion.BRepFace.classType = function classType () {
        return 'adsk::fusion::BRepFace';
    };
    adsk.fusion.BRepFace.interfaceId = 'adsk.fusion.BRepFace';
    adsk.objectTypes['adsk.fusion.BRepFace'] = adsk.fusion.BRepFace;
    adsk.fusion.BRepFace.cast = function (object) {
        return object instanceof adsk.fusion.BRepFace ? object : null;
    };

    // Returns the BRepEdges used by this face
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'edges', {
        get : function () {
            var result = this._execute('edges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdges) : null;
        }
    });

    // Returns the BRepVertices used by this face
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'vertices', {
        get : function () {
            var result = this._execute('vertices');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertices) : null;
        }
    });

    // Returns the parent shell of the face.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'shell', {
        get : function () {
            var result = this._execute('shell');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepShell) : null;
        }
    });

    // Returns the BRepLoops owned by this face
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'loops', {
        get : function () {
            var result = this._execute('loops');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLoops) : null;
        }
    });

    // Returns the parent body of the face.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'body', {
        get : function () {
            var result = this._execute('body');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    // Returns the underlying surface geometry of this face
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'geometry', {
        get : function () {
            var result = this._execute('geometry');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Surface) : null;
        }
    });

    // Returns a SurfaceEvaluator to allow geometric evaluations across the face's surface.
    // This evaluator differs from the evaluator available from the Surface obtained from the geometry
    // property by being bounded by the topological boundaries of this face.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'evaluator', {
        get : function () {
            var result = this._execute('evaluator');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.SurfaceEvaluator) : null;
        }
    });

    // Returns a sample point guaranteed to lie on the face's surface, within the face's boundaries, and not on a boundary edge.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'pointOnFace', {
        get : function () {
            var result = this._execute('pointOnFace');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Point3D) : null;
        }
    });

    // Returns the set of faces that are tengentially adjacent to this face.
    // In other words, it is the set of faces that are adjacent to this face's edges
    // and have a smooth transition across those edges.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'tangentiallyConnectedFaces', {
        get : function () {
            var result = this._execute('tangentiallyConnectedFaces');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFaces) : null;
        }
    });

    // Returns a MeshManager object that allows access to existing and new meshes of this face.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'meshManager', {
        get : function () {
            var result = this._execute('meshManager');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshManager) : null;
        }
    });

    // Read-write property that gets and sets the current appearance of the face. Setting this property will result in applying
    // an override appearance to the face and the AppearanceSourceType property will return OverrideAppearanceSource. Setting
    // this property to null will remove any override.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'appearance', {
        get : function () {
            var result = this._execute('appearance');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Appearance) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Appearance)) { throw new TypeError('value must be a adsk.core.Appearance'); }
            var args = {
                value : value
            };
            var result = this._execute('appearance', args);
            return result ? result.value : undefined;
        }
    });

    // Read-write property that gets the source of the appearance for the face. If this returns OverrideAppearanceSource, an override exists
    // on this face. The override can be removed by setting the Appearance property to null.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'appearanceSourceType', {
        get : function () {
            var result = this._execute('appearanceSourceType');
            return result ? result.value : undefined;
        }
    });

    // Returns the assembly occurrence (i.e. the occurrence) of this
    // object in an assembly. This is only valid in the case where this
    // BRepFace object is acting as a proxy in an assembly. Returns null
    // in the case where the object is not in the context of an assembly.
    // but is already the native object.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFace) : null;
        }
    });

    // Returns the area in cm ^ 2.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'area', {
        get : function () {
            var result = this._execute('area');
            return result ? result.value : undefined;
        }
    });

    // Returns the bounding box of this face
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'boundingBox', {
        get : function () {
            var result = this._execute('boundingBox');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.BoundingBox3D) : null;
        }
    });

    // Returns a point at the centroid (aka, geometric center) of the face.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'centroid', {
        get : function () {
            var result = this._execute('centroid');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Point3D) : null;
        }
    });

    // Returns the collection of attributes associated with this face.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'attributes', {
        get : function () {
            var result = this._execute('attributes');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Attributes) : null;
        }
    });

    // Returns the temporary ID of this face. This ID is only good while the document
    // remains open and as long as the owning BRepBody is not modified in any way.
    // The findByTempId method of the BRepBody will return the entity in the body with the given ID.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'tempId', {
        get : function () {
            var result = this._execute('tempId');
            return result ? result.value : undefined;
        }
    });

    // Gets if the normal of this face is reversed with respect to the surface geometry associated
    // with this face.
    Object.defineProperty(adsk.fusion.BRepFace.prototype, 'isParamReversed', {
        get : function () {
            var result = this._execute('isParamReversed');
            return result ? result.value : undefined;
        }
    });

    // Returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // occurrence : The occurrence that defines the context for the created proxy.
    // Returns the new BRepFace proxy or null if this isn't the NativeObject.
    adsk.fusion.BRepFace.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFace) : null;
    };

    // Creates a new body where this face and its edges are converted to different
    // types of geometry based on the input options.
    // The tempId on the faces, edges, and vertices on the new body will match
    // with the corresponding tempId on the original body. In cases where the face is
    // split as a result of the conversion there can be more than one face or edge in
    // the new body that matches to a single face or edge in the original body.
    // options : Input options that define how the conversion should be done. These are
    // bitwise options so they can be combined.
    // Returns the new converted body or null in the case of failure.
    adsk.fusion.BRepFace.prototype.convert = function (options) {
        if (!isFinite(options)) { throw new TypeError('options must be a number'); }
        var args = {
            options : Number(options)
        };
        var result = this._execute('convert', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    //=========== BRepFaces ============
    // BRepFace collection.
    adsk.fusion.BRepFaces = function BRepFaces(handle) {
        if (!(this instanceof adsk.fusion.BRepFaces)) {
            return adsk.fusion.BRepFaces.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepFaces.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepFaces.prototype.constructor = adsk.fusion.BRepFaces;
    adsk.fusion.BRepFaces.classType = function classType () {
        return 'adsk::fusion::BRepFaces';
    };
    adsk.fusion.BRepFaces.interfaceId = 'adsk.fusion.BRepFaces';
    adsk.objectTypes['adsk.fusion.BRepFaces'] = adsk.fusion.BRepFaces;
    adsk.fusion.BRepFaces.cast = function (object) {
        return object instanceof adsk.fusion.BRepFaces ? object : null;
    };

    // The number of faces in the collection.
    Object.defineProperty(adsk.fusion.BRepFaces.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified face using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.BRepFaces.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFace) : null;
    };

    //=========== BRepLoop ============
    // Represents a connected portion of a BRepFace boundary. It consists of a chain of BRepCoEdges.
    adsk.fusion.BRepLoop = function BRepLoop(handle) {
        if (!(this instanceof adsk.fusion.BRepLoop)) {
            return adsk.fusion.BRepLoop.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepLoop.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepLoop.prototype.constructor = adsk.fusion.BRepLoop;
    adsk.fusion.BRepLoop.classType = function classType () {
        return 'adsk::fusion::BRepLoop';
    };
    adsk.fusion.BRepLoop.interfaceId = 'adsk.fusion.BRepLoop';
    adsk.objectTypes['adsk.fusion.BRepLoop'] = adsk.fusion.BRepLoop;
    adsk.fusion.BRepLoop.cast = function (object) {
        return object instanceof adsk.fusion.BRepLoop ? object : null;
    };

    // Returns the BRepEdges used by this loop
    Object.defineProperty(adsk.fusion.BRepLoop.prototype, 'edges', {
        get : function () {
            var result = this._execute('edges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdges) : null;
        }
    });

    // Returns the BRepCoEdges consisting this loop
    Object.defineProperty(adsk.fusion.BRepLoop.prototype, 'coEdges', {
        get : function () {
            var result = this._execute('coEdges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepCoEdges) : null;
        }
    });

    // Returns true of this loop is an outer loop of a face
    Object.defineProperty(adsk.fusion.BRepLoop.prototype, 'isOuter', {
        get : function () {
            var result = this._execute('isOuter');
            return result ? result.value : undefined;
        }
    });

    // Returns the bounding box of this loop
    Object.defineProperty(adsk.fusion.BRepLoop.prototype, 'boundingBox', {
        get : function () {
            var result = this._execute('boundingBox');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.BoundingBox3D) : null;
        }
    });

    // Returns the parent face of the loop.
    Object.defineProperty(adsk.fusion.BRepLoop.prototype, 'face', {
        get : function () {
            var result = this._execute('face');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFace) : null;
        }
    });

    // Returns the parent body of the loop.
    Object.defineProperty(adsk.fusion.BRepLoop.prototype, 'body', {
        get : function () {
            var result = this._execute('body');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    // Returns the assembly occurrence (i.e. the occurrence) of this
    // object in an assembly. This is only valid in the case where this
    // BRepLoop object is acting as a proxy in an assembly. Returns null
    // in the case where the object is not in the context of an assembly.
    // but is already the native object.
    Object.defineProperty(adsk.fusion.BRepLoop.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.BRepLoop.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLoop) : null;
        }
    });

    // Returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // occurrence : The occurrence that defines the context for the created proxy.
    // Returns the new BrepLoop proxy or null if this isn't the NativeObject.
    adsk.fusion.BRepLoop.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLoop) : null;
    };

    //=========== BRepLoops ============
    // BRepLoop collection.
    adsk.fusion.BRepLoops = function BRepLoops(handle) {
        if (!(this instanceof adsk.fusion.BRepLoops)) {
            return adsk.fusion.BRepLoops.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepLoops.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepLoops.prototype.constructor = adsk.fusion.BRepLoops;
    adsk.fusion.BRepLoops.classType = function classType () {
        return 'adsk::fusion::BRepLoops';
    };
    adsk.fusion.BRepLoops.interfaceId = 'adsk.fusion.BRepLoops';
    adsk.objectTypes['adsk.fusion.BRepLoops'] = adsk.fusion.BRepLoops;
    adsk.fusion.BRepLoops.cast = function (object) {
        return object instanceof adsk.fusion.BRepLoops ? object : null;
    };

    // The number of loops in the collection.
    Object.defineProperty(adsk.fusion.BRepLoops.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified loop using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.BRepLoops.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLoop) : null;
    };

    //=========== BRepLump ============
    // Represents an entirely connected set of entities. A BRepBody consists of BRepLumps.
    adsk.fusion.BRepLump = function BRepLump(handle) {
        if (!(this instanceof adsk.fusion.BRepLump)) {
            return adsk.fusion.BRepLump.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepLump.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepLump.prototype.constructor = adsk.fusion.BRepLump;
    adsk.fusion.BRepLump.classType = function classType () {
        return 'adsk::fusion::BRepLump';
    };
    adsk.fusion.BRepLump.interfaceId = 'adsk.fusion.BRepLump';
    adsk.objectTypes['adsk.fusion.BRepLump'] = adsk.fusion.BRepLump;
    adsk.fusion.BRepLump.cast = function (object) {
        return object instanceof adsk.fusion.BRepLump ? object : null;
    };

    // Returns the BRepShells owned by the lump
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'shells', {
        get : function () {
            var result = this._execute('shells');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepShells) : null;
        }
    });

    // Returns the BRepFaces owned by the lump
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'faces', {
        get : function () {
            var result = this._execute('faces');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFaces) : null;
        }
    });

    // Returns the BRepEdges owned by the lump
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'edges', {
        get : function () {
            var result = this._execute('edges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdges) : null;
        }
    });

    // Returns the BRepVertices owned by the lump
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'vertices', {
        get : function () {
            var result = this._execute('vertices');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertices) : null;
        }
    });

    // Returns the immediate owner BRepBody of the lump
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'body', {
        get : function () {
            var result = this._execute('body');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    // Returns true of the lump is closed
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'isClosed', {
        get : function () {
            var result = this._execute('isClosed');
            return result ? result.value : undefined;
        }
    });

    // Returns the bounding box of the lump
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'boundingBox', {
        get : function () {
            var result = this._execute('boundingBox');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.BoundingBox3D) : null;
        }
    });

    // Returns the area in cm ^ 2.
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'area', {
        get : function () {
            var result = this._execute('area');
            return result ? result.value : undefined;
        }
    });

    // Returns the volume in cm ^ 3. Returns 0 in the case the lump is not solid.
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'volume', {
        get : function () {
            var result = this._execute('volume');
            return result ? result.value : undefined;
        }
    });

    // Returns the mesh manager object for this lump.
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'meshManager', {
        get : function () {
            var result = this._execute('meshManager');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshManager) : null;
        }
    });

    // Returns the assembly context that is directly referencing this
    // object in an assembly. This is only valid in the case where this
    // BRepLump object is acting as a proxy in an assembly. Returns null
    // in the case where the object is not in the context of an assembly.
    // but is already the native object.
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.BRepLump.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLump) : null;
        }
    });

    // Determines the relationship of the input point with respect to this lump.
    // point : The point to do the containment check for.
    // Returns a value from the PointContainment enum indicating the relationship of
    // the input point to the lump.
    adsk.fusion.BRepLump.prototype.pointContainment = function (point) {
        if (point !== null && !(point instanceof adsk.core.Point3D)) { throw new TypeError('point must be a adsk.core.Point3D'); }
        var args = {
            point : (point === null ? point : point.handle)
        };
        var result = this._execute('pointContainment', args);
        return result ? result.value : undefined;
    };

    // Returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // occurrence : The occurrence that defines the context for the created proxy.
    // Returns the new BrepLump proxy or null if this isn't the NativeObject.
    adsk.fusion.BRepLump.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLump) : null;
    };

    //=========== BRepLumps ============
    // BRepLump collection.
    adsk.fusion.BRepLumps = function BRepLumps(handle) {
        if (!(this instanceof adsk.fusion.BRepLumps)) {
            return adsk.fusion.BRepLumps.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepLumps.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepLumps.prototype.constructor = adsk.fusion.BRepLumps;
    adsk.fusion.BRepLumps.classType = function classType () {
        return 'adsk::fusion::BRepLumps';
    };
    adsk.fusion.BRepLumps.interfaceId = 'adsk.fusion.BRepLumps';
    adsk.objectTypes['adsk.fusion.BRepLumps'] = adsk.fusion.BRepLumps;
    adsk.fusion.BRepLumps.cast = function (object) {
        return object instanceof adsk.fusion.BRepLumps ? object : null;
    };

    // Returns the number of lumps in the collection.
    Object.defineProperty(adsk.fusion.BRepLumps.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified lump using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.BRepLumps.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLump) : null;
    };

    //=========== BRepShell ============
    // Represents an entirely connected set of BRepFaces. A BRepLump may contain multiple BRepShells.
    adsk.fusion.BRepShell = function BRepShell(handle) {
        if (!(this instanceof adsk.fusion.BRepShell)) {
            return adsk.fusion.BRepShell.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepShell.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepShell.prototype.constructor = adsk.fusion.BRepShell;
    adsk.fusion.BRepShell.classType = function classType () {
        return 'adsk::fusion::BRepShell';
    };
    adsk.fusion.BRepShell.interfaceId = 'adsk.fusion.BRepShell';
    adsk.objectTypes['adsk.fusion.BRepShell'] = adsk.fusion.BRepShell;
    adsk.fusion.BRepShell.cast = function (object) {
        return object instanceof adsk.fusion.BRepShell ? object : null;
    };

    // Returns the BRepFaces directly owned by this shell
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'faces', {
        get : function () {
            var result = this._execute('faces');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFaces) : null;
        }
    });

    // returns the BRepEdges owned by this shell
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'edges', {
        get : function () {
            var result = this._execute('edges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdges) : null;
        }
    });

    // Returns the BRepVertices owned by this shell
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'vertices', {
        get : function () {
            var result = this._execute('vertices');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertices) : null;
        }
    });

    // Returns the parent lump of this shell.
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'lump', {
        get : function () {
            var result = this._execute('lump');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepLump) : null;
        }
    });

    // Returns the parent body of the shell.
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'body', {
        get : function () {
            var result = this._execute('body');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    // Returns the bounding box of this shell
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'boundingBox', {
        get : function () {
            var result = this._execute('boundingBox');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.BoundingBox3D) : null;
        }
    });

    // Returns true if this shell is closed
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'isClosed', {
        get : function () {
            var result = this._execute('isClosed');
            return result ? result.value : undefined;
        }
    });

    // Returns true if the faces of this shell bound a void or an empty space within an outer shell.
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'isVoid', {
        get : function () {
            var result = this._execute('isVoid');
            return result ? result.value : undefined;
        }
    });

    // Returns the area in cm ^ 2.
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'area', {
        get : function () {
            var result = this._execute('area');
            return result ? result.value : undefined;
        }
    });

    // Returns the volume in cm ^ 3. Returns 0 in the case the shell is not solid.
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'volume', {
        get : function () {
            var result = this._execute('volume');
            return result ? result.value : undefined;
        }
    });

    // Returns the mesh manager object for this shell.
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'meshManager', {
        get : function () {
            var result = this._execute('meshManager');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshManager) : null;
        }
    });

    // Returns the assembly occurrence (i.e. the occurrence) of this
    // object in an assembly. This is only valid in the case where this
    // BRepShell object is acting as a proxy in an assembly. Returns null
    // in the case where the object is not in the context of an assembly.
    // but is already the native object.
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepShell) : null;
        }
    });

    // Returns the wire body, if any, that exists in this shell. Returns null if the
    // shell doesn't have a wire body.
    Object.defineProperty(adsk.fusion.BRepShell.prototype, 'wire', {
        get : function () {
            var result = this._execute('wire');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepWire) : null;
        }
    });

    // Determines the relationship of the input point with respect to this shell.
    // point : The point to do the containment check for.
    // Returns a value from the PointContainment enum indicating the relationship of
    // the input point to the shell.
    adsk.fusion.BRepShell.prototype.pointContainment = function (point) {
        if (point !== null && !(point instanceof adsk.core.Point3D)) { throw new TypeError('point must be a adsk.core.Point3D'); }
        var args = {
            point : (point === null ? point : point.handle)
        };
        var result = this._execute('pointContainment', args);
        return result ? result.value : undefined;
    };

    // Returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // occurrence : The occurrence that defines the context for the created proxy.
    // Returns the new BrepShell proxy or null if this isn't the NativeObject.
    adsk.fusion.BRepShell.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepShell) : null;
    };

    //=========== BRepShells ============
    // BRepShell collection.
    adsk.fusion.BRepShells = function BRepShells(handle) {
        if (!(this instanceof adsk.fusion.BRepShells)) {
            return adsk.fusion.BRepShells.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepShells.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepShells.prototype.constructor = adsk.fusion.BRepShells;
    adsk.fusion.BRepShells.classType = function classType () {
        return 'adsk::fusion::BRepShells';
    };
    adsk.fusion.BRepShells.interfaceId = 'adsk.fusion.BRepShells';
    adsk.objectTypes['adsk.fusion.BRepShells'] = adsk.fusion.BRepShells;
    adsk.fusion.BRepShells.cast = function (object) {
        return object instanceof adsk.fusion.BRepShells ? object : null;
    };

    // The number of shells in the collection.
    Object.defineProperty(adsk.fusion.BRepShells.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified shell using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.BRepShells.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepShell) : null;
    };

    //=========== BRepVertex ============
    // A 0-dimentional topological entity that bounds a BRepEdge.
    adsk.fusion.BRepVertex = function BRepVertex(handle) {
        if (!(this instanceof adsk.fusion.BRepVertex)) {
            return adsk.fusion.BRepVertex.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepVertex.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepVertex.prototype.constructor = adsk.fusion.BRepVertex;
    adsk.fusion.BRepVertex.classType = function classType () {
        return 'adsk::fusion::BRepVertex';
    };
    adsk.fusion.BRepVertex.interfaceId = 'adsk.fusion.BRepVertex';
    adsk.objectTypes['adsk.fusion.BRepVertex'] = adsk.fusion.BRepVertex;
    adsk.fusion.BRepVertex.cast = function (object) {
        return object instanceof adsk.fusion.BRepVertex ? object : null;
    };

    // Returns the BRepFaces that uses this vertex through BRepEdge
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'faces', {
        get : function () {
            var result = this._execute('faces');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepFaces) : null;
        }
    });

    // Returns the BRepEdges bounded by this vertex
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'edges', {
        get : function () {
            var result = this._execute('edges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdges) : null;
        }
    });

    // Returns if the vertex is tolerant.
    // The tolerance used is available from the tolerance property.
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'isTolerant', {
        get : function () {
            var result = this._execute('isTolerant');
            return result ? result.value : undefined;
        }
    });

    // Returns the tolerance used by a tolerant vertex.
    // This value is only useful when isTolerant is true.
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'tolerance', {
        get : function () {
            var result = this._execute('tolerance');
            return result ? result.value : undefined;
        }
    });

    // Returns the underlying geometry point
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'geometry', {
        get : function () {
            var result = this._execute('geometry');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Point3D) : null;
        }
    });

    // Returns the parent shell.
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'shell', {
        get : function () {
            var result = this._execute('shell');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepShell) : null;
        }
    });

    // Returns the parent body.
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'body', {
        get : function () {
            var result = this._execute('body');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    // Returns the assembly occurrence (i.e. the occurrence) of this
    // object in an assembly. This is only valid in the case where this
    // BRepVertex object is acting as a proxy in an assembly. Returns null
    // in the case where the object is not in the context of an assembly.
    // but is already the native object.
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertex) : null;
        }
    });

    // Returns the collection of attributes associated with this face.
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'attributes', {
        get : function () {
            var result = this._execute('attributes');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Attributes) : null;
        }
    });

    // Returns the temporary ID of this vertex. This ID is only good while the document
    // remains open and as long as the owning BRepBody is not modified in any way.
    // The findByTempId method of the BRepBody will return the entity in the body with the given ID.
    Object.defineProperty(adsk.fusion.BRepVertex.prototype, 'tempId', {
        get : function () {
            var result = this._execute('tempId');
            return result ? result.value : undefined;
        }
    });

    // Returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // occurrence : The occurrence that defines the context for the created proxy.
    // Returns the new BrepVertex proxy or null if this isn't the NativeObject.
    adsk.fusion.BRepVertex.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertex) : null;
    };

    //=========== BRepVertices ============
    // BRepVertex collection.
    adsk.fusion.BRepVertices = function BRepVertices(handle) {
        if (!(this instanceof adsk.fusion.BRepVertices)) {
            return adsk.fusion.BRepVertices.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepVertices.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepVertices.prototype.constructor = adsk.fusion.BRepVertices;
    adsk.fusion.BRepVertices.classType = function classType () {
        return 'adsk::fusion::BRepVertices';
    };
    adsk.fusion.BRepVertices.interfaceId = 'adsk.fusion.BRepVertices';
    adsk.objectTypes['adsk.fusion.BRepVertices'] = adsk.fusion.BRepVertices;
    adsk.fusion.BRepVertices.cast = function (object) {
        return object instanceof adsk.fusion.BRepVertices ? object : null;
    };

    // The number of vertices in the collection.
    Object.defineProperty(adsk.fusion.BRepVertices.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified vertex using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.BRepVertices.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertex) : null;
    };

    //=========== BRepWire ============
    // Represents a single B-Rep wire body. A wire body consists of one or
    // more edges and their vertices.
    adsk.fusion.BRepWire = function BRepWire(handle) {
        if (!(this instanceof adsk.fusion.BRepWire)) {
            return adsk.fusion.BRepWire.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepWire.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepWire.prototype.constructor = adsk.fusion.BRepWire;
    adsk.fusion.BRepWire.classType = function classType () {
        return 'adsk::fusion::BRepWire';
    };
    adsk.fusion.BRepWire.interfaceId = 'adsk.fusion.BRepWire';
    adsk.objectTypes['adsk.fusion.BRepWire'] = adsk.fusion.BRepWire;
    adsk.fusion.BRepWire.cast = function (object) {
        return object instanceof adsk.fusion.BRepWire ? object : null;
    };

    // Returns the B-Rep edges associated with this wire body.
    Object.defineProperty(adsk.fusion.BRepWire.prototype, 'edges', {
        get : function () {
            var result = this._execute('edges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepEdges) : null;
        }
    });

    // Returns the B-Rep vertices associated with this wire body.
    Object.defineProperty(adsk.fusion.BRepWire.prototype, 'vertices', {
        get : function () {
            var result = this._execute('vertices');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepVertices) : null;
        }
    });

    // Returns the co-edges associated with this wire body. The co-edges record
    // the connections between the edges in the wire body.
    Object.defineProperty(adsk.fusion.BRepWire.prototype, 'coEdges', {
        get : function () {
            var result = this._execute('coEdges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepCoEdges) : null;
        }
    });

    // Indicates if this entities making up this wire body are planar and all lie on the same plane.
    Object.defineProperty(adsk.fusion.BRepWire.prototype, 'isPlanar', {
        get : function () {
            var result = this._execute('isPlanar');
            return result ? result.value : undefined;
        }
    });

    // Returns the parent BRepBody object that contains this wire.
    Object.defineProperty(adsk.fusion.BRepWire.prototype, 'parent', {
        get : function () {
            var result = this._execute('parent');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    // Returns the assembly occurrence (i.e. the occurrence) of this
    // object in an assembly. This is only valid in the case where this
    // BRepFace object is acting as a proxy in an assembly. Returns null
    // in the case where the object is not in the context of an assembly.
    // but is already the native object.
    Object.defineProperty(adsk.fusion.BRepWire.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.BRepWire.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepWire) : null;
        }
    });

    // Method that computes the offset for a planar wire. A BRepBody containing the resulting
    // BRepWire object(s) is returned. It's possible that the offset result of a single wire
    // can result in multiple wires.
    // planeNormal : Input Vector3D object that defines the positive direction of the
    // plane the plane the wire lies on. This vector must be normal to the plane and is used to
    // determine the side to offset the curves to. A positive offset distance is in the direction
    // of the cross product (wire_tangent x wire_plane_normal). A negative offset is in the
    // opposite direction.
    // distance : The offset distance in centimeters. See the description for the Normal argument to see how
    // a positive or negative value for the distance specifies the direction of the offset.
    // cornerType : Specifies how the corners are connected when offseting the curves results in gaps in the corners.
    // See the documentation of the enum for a detailed description of each option.
    // Returns a new temporary BRepBody that contains one or more wires that represent the offset.
    adsk.fusion.BRepWire.prototype.offsetPlanarWire = function (planeNormal, distance, cornerType) {
        if (planeNormal !== null && !(planeNormal instanceof adsk.core.Vector3D)) { throw new TypeError('planeNormal must be a adsk.core.Vector3D'); }
        if (!isFinite(distance)) { throw new TypeError('distance must be a number'); }
        if (!isFinite(cornerType)) { throw new TypeError('cornerType must be a number'); }
        var args = {
            planeNormal : (planeNormal === null ? planeNormal : planeNormal.handle),
            distance : Number(distance),
            cornerType : Number(cornerType)
        };
        var result = this._execute('offsetPlanarWire', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // occurrence : The occurrence that defines the context for the created proxy.
    // Returns the new BRepWire proxy or null if this isn't the NativeObject.
    adsk.fusion.BRepWire.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepWire) : null;
    };

    //=========== BRepWires ============
    // Provides access to B-Rep wire bodies.
    adsk.fusion.BRepWires = function BRepWires(handle) {
        if (!(this instanceof adsk.fusion.BRepWires)) {
            return adsk.fusion.BRepWires.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.BRepWires.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.BRepWires.prototype.constructor = adsk.fusion.BRepWires;
    adsk.fusion.BRepWires.classType = function classType () {
        return 'adsk::fusion::BRepWires';
    };
    adsk.fusion.BRepWires.interfaceId = 'adsk.fusion.BRepWires';
    adsk.objectTypes['adsk.fusion.BRepWires'] = adsk.fusion.BRepWires;
    adsk.fusion.BRepWires.cast = function (object) {
        return object instanceof adsk.fusion.BRepWires ? object : null;
    };

    // The number of B-Rep wire bodies in the collection.
    Object.defineProperty(adsk.fusion.BRepWires.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified wire using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.BRepWires.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepWire) : null;
    };

    //=========== OffsetCornerTypes ============
    // Specifies the different types of corners that can be created when offsetting a wire body.
    adsk.fusion.OffsetCornerTypes = {
        CircularOffsetCornerType : 0,
        LinearOffsetCornerType : 1,
        ExtendedOffsetCornerType : 2
    };

    //=========== PointContainment ============
    // Types that define the nature of the relationship between a point and a containing entity.
    adsk.fusion.PointContainment = {
        PointInsidePointContainment : 0,
        PointOnPointContainment : 1,
        PointOutsidePointContainment : 2,
        UnknownPointContainment : 3
    };

    //=========== TemporaryBRepManager ============
    // A utility object that provides functionality to create and manipulate B-Rep data outside
    // the context of a document. The provides direct access to the modeling core without the
    // overhead of parametrics, persistence, transactions, or graphics. It also provides a way
    // of directly defining and creating B-Rep data.
    adsk.fusion.TemporaryBRepManager = function TemporaryBRepManager(handle) {
        if (!(this instanceof adsk.fusion.TemporaryBRepManager)) {
            return adsk.fusion.TemporaryBRepManager.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.TemporaryBRepManager.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.TemporaryBRepManager.prototype.constructor = adsk.fusion.TemporaryBRepManager;
    adsk.fusion.TemporaryBRepManager.classType = function classType () {
        return 'adsk::fusion::TemporaryBRepManager';
    };
    adsk.fusion.TemporaryBRepManager.interfaceId = 'adsk.fusion.TemporaryBRepManager';
    adsk.objectTypes['adsk.fusion.TemporaryBRepManager'] = adsk.fusion.TemporaryBRepManager;
    adsk.fusion.TemporaryBRepManager.cast = function (object) {
        return object instanceof adsk.fusion.TemporaryBRepManager ? object : null;
    };

    // Gets the TempoaryBRepManager object. This object provides access to functionality to
    // create an manipulate temporary B-Rep data outside the context of a document.
    // Returns the TemporaryBRepManager object.
    adsk.fusion.TemporaryBRepManager.get = function () {
        var result = adsk.core.Base._executeStatic('adsk.fusion.TemporaryBRepManager', 'get');
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.TemporaryBRepManager) : null;
    };

    // Creates a temporary copy of the input BRepBody, BRepFace, or BRepEdge object.
    // bRepEntity : The BRepBody, BRepFace, BRepLoop, or BRepEdge to create a copy of. This can be a parametric
    // B-Rep entity or a temporary B-Rep entity.
    // Returns a BRepBody that contains the result. If a BRepBody is input the copy is
    // of the entire body. If a BRepFace is input, then the result is a BRepBody that
    // contains a single face. If a BRepLoop is input then the result is a BRepBody that
    // contains a wire where each edge in the loop will have a corresponding edge in the wire.
    // If a BRepEdge is input then the result is a BRepBody that contains a wire that contains
    // the single edge.
    adsk.fusion.TemporaryBRepManager.prototype.copy = function (bRepEntity) {
        if (bRepEntity !== null && !(bRepEntity instanceof adsk.core.Base)) { throw new TypeError('bRepEntity must be a adsk.core.Base'); }
        var args = {
            bRepEntity : (bRepEntity === null ? bRepEntity : bRepEntity.handle)
        };
        var result = this._execute('copy', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Calculates the intersection between the input body and plane and creates a
    // wire body that represents the intersection curves.
    // body : The BRepBody to intersection.
    // plane : The geometry Plane to intersect with the body.
    // Returns a BRepBody that contains a wire body that represents the intersection.
    adsk.fusion.TemporaryBRepManager.prototype.planeIntersection = function (body, plane) {
        if (body !== null && !(body instanceof adsk.fusion.BRepBody)) { throw new TypeError('body must be a adsk.fusion.BRepBody'); }
        if (plane !== null && !(plane instanceof adsk.core.Plane)) { throw new TypeError('plane must be a adsk.core.Plane'); }
        var args = {
            body : (body === null ? body : body.handle),
            plane : (plane === null ? plane : plane.handle)
        };
        var result = this._execute('planeIntersection', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a new body by creating a ruled surface between the two input wire bodies.
    // sectionOne : BRepWire that defines the shape of the first section.
    // sectionTwo : BRepWire that defines the shape of the second section.
    // Returns the created ruled surface as a BRepBody object.
    adsk.fusion.TemporaryBRepManager.prototype.createRuledSurface = function (sectionOne, sectionTwo) {
        if (sectionOne !== null && !(sectionOne instanceof adsk.fusion.BRepWire)) { throw new TypeError('sectionOne must be a adsk.fusion.BRepWire'); }
        if (sectionTwo !== null && !(sectionTwo instanceof adsk.fusion.BRepWire)) { throw new TypeError('sectionTwo must be a adsk.fusion.BRepWire'); }
        var args = {
            sectionOne : (sectionOne === null ? sectionOne : sectionOne.handle),
            sectionTwo : (sectionTwo === null ? sectionTwo : sectionTwo.handle)
        };
        var result = this._execute('createRuledSurface', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Calculates the silhouette curve geometry for a given face as viewed from a given direction.
    // face : Input BRepFace object to calculate the silhouette curve for.
    // viewDirection : Input Vector3D object that defines the view direction to calculate the silhouette curve relative to.
    // The silhouette curve(s) will lie along the path where the face normal is perpendicular to the view direction.
    // returnCoincidentSilhouettes : Input Boolean that specifies if silhouette curves that are coincident to the edges of the face should be
    // returned or not. If true, these curves will be returned.
    // Returns a SurfaceBody object that will contain one or more BRepWire objects that represent the silhouette curve(s).
    // This method can return null in the case where there is not a silhouette curve for the specified face.
    adsk.fusion.TemporaryBRepManager.prototype.createSilhouetteCurves = function (face, viewDirection, returnCoincidentSilhouettes) {
        if (face !== null && !(face instanceof adsk.fusion.BRepFace)) { throw new TypeError('face must be a adsk.fusion.BRepFace'); }
        if (viewDirection !== null && !(viewDirection instanceof adsk.core.Vector3D)) { throw new TypeError('viewDirection must be a adsk.core.Vector3D'); }
        if (typeof returnCoincidentSilhouettes !== 'boolean') { throw new TypeError('returnCoincidentSilhouettes must be a boolean'); }
        var args = {
            face : (face === null ? face : face.handle),
            viewDirection : (viewDirection === null ? viewDirection : viewDirection.handle),
            returnCoincidentSilhouettes : returnCoincidentSilhouettes
        };
        var result = this._execute('createSilhouetteCurves', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Deletes one or more faces from a temporary BRepBody. The body that will be modified is determined
    // by getting the parent body of the input faces.
    // faces : An array of BRepFace objects to delete. If more than one face is provided,
    // all of the faces must exist within the same body.
    // deleteSpecifiedFaces : This allows you to either delete the faces that were input or to keep those faces and delete all the
    // other faces in the body.
    // Returns true if the operation was successful.
    adsk.fusion.TemporaryBRepManager.prototype.deleteFaces = function (faces, deleteSpecifiedFaces) {
        if (!Array.isArray(faces)) { throw new TypeError('faces must be an array'); }
        var facesLength = faces.length;
        var facesIt;
        for (facesIt = 0; facesIt < facesLength; ++facesIt) {
            if (faces[facesIt] !== null && !(faces[facesIt] instanceof adsk.fusion.BRepFace)) { throw new TypeError('faces[facesIt] must be a adsk.fusion.BRepFace'); }
        }
        if (typeof deleteSpecifiedFaces !== 'boolean') { throw new TypeError('deleteSpecifiedFaces must be a boolean'); }
        var args = {
            faces : faces,
            deleteSpecifiedFaces : deleteSpecifiedFaces
        };
        var result = this._execute('deleteFaces', args);
        return result ? result.value : undefined;
    };

    // Performs the specified Boolean operation between the two input bodies. The input bodies need
    // not be solid but can be faces that are combined or trimmed.
    // targetBody : The target body that will be modified as a result of the Boolean operation.
    // toolBody : The tool body that will be used to operate on the target body.
    // booleanType : The type of Boolean operation to perform.
    // Returns true if the operation was successful. If successful, the target body is modified as a result of the
    // Boolean operation. Because of this the targetBody must always be a temporary BRepBody. The toolbody is not
    // modified. This is analogous to a machining operation where you have the target that is being machined and
    // the tool that removes material.
    adsk.fusion.TemporaryBRepManager.prototype.booleanOperation = function (targetBody, toolBody, booleanType) {
        if (targetBody !== null && !(targetBody instanceof adsk.fusion.BRepBody)) { throw new TypeError('targetBody must be a adsk.fusion.BRepBody'); }
        if (toolBody !== null && !(toolBody instanceof adsk.fusion.BRepBody)) { throw new TypeError('toolBody must be a adsk.fusion.BRepBody'); }
        if (!isFinite(booleanType)) { throw new TypeError('booleanType must be a number'); }
        var args = {
            targetBody : (targetBody === null ? targetBody : targetBody.handle),
            toolBody : (toolBody === null ? toolBody : toolBody.handle),
            booleanType : Number(booleanType)
        };
        var result = this._execute('booleanOperation', args);
        return result ? result.value : undefined;
    };

    // Transforms the input body using the specified transformation matrix.
    // body : The BRepBody object to transform.
    // transform : The transformation matrix that defines the transform to apply to the body.
    // Returns true if the specified transform was successfully applied to the body.
    adsk.fusion.TemporaryBRepManager.prototype.transform = function (body, transform) {
        if (body !== null && !(body instanceof adsk.fusion.BRepBody)) { throw new TypeError('body must be a adsk.fusion.BRepBody'); }
        if (transform !== null && !(transform instanceof adsk.core.Matrix3D)) { throw new TypeError('transform must be a adsk.core.Matrix3D'); }
        var args = {
            body : (body === null ? body : body.handle),
            transform : (transform === null ? transform : transform.handle)
        };
        var result = this._execute('transform', args);
        return result ? result.value : undefined;
    };

    // Creates new BRepBody objects based on the contents of the specified file.
    // filename : The full path and name of the file to read in. This can be a SMT, SMB, SAT, or SAB file.
    // A BRepBodies collection object is returned which can contain multiple BRepBody objects.
    // null is returned in the case where it was unable to read the file.
    adsk.fusion.TemporaryBRepManager.prototype.createFromFile = function (filename) {
        if (filename === undefined || filename === null || filename.constructor !== String) { throw new TypeError('filename must be a string'); }
        var args = {
            filename : filename
        };
        var result = this._execute('createFromFile', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBodies) : null;
    };

    // Exports the input bodies to the specified file.
    // bodies : An array of BRepBody objects that you want to export.
    // filename : The filename to write the BRepBody objects to. The type of file to create
    // is inferred from the extension of the file. The valid extensions are ".sat" and ".smt".
    // Returns true if the export was successful.
    adsk.fusion.TemporaryBRepManager.prototype.exportToFile = function (bodies, filename) {
        if (!Array.isArray(bodies)) { throw new TypeError('bodies must be an array'); }
        var bodiesLength = bodies.length;
        var bodiesIt;
        for (bodiesIt = 0; bodiesIt < bodiesLength; ++bodiesIt) {
            if (bodies[bodiesIt] !== null && !(bodies[bodiesIt] instanceof adsk.fusion.BRepBody)) { throw new TypeError('bodies[bodiesIt] must be a adsk.fusion.BRepBody'); }
        }
        if (filename === undefined || filename === null || filename.constructor !== String) { throw new TypeError('filename must be a string'); }
        var args = {
            bodies : bodies,
            filename : filename
        };
        var result = this._execute('exportToFile', args);
        return result ? result.value : undefined;
    };

    // Creates a new temporary solid box BRepBody object.
    // box : The OrientedBoundingBox3D object that defines the position, orientation, and
    // size of the box to crate.
    // Returns the newly created temporary BRepBody object or null in the case of failure.
    adsk.fusion.TemporaryBRepManager.prototype.createBox = function (box) {
        if (box !== null && !(box instanceof adsk.core.OrientedBoundingBox3D)) { throw new TypeError('box must be a adsk.core.OrientedBoundingBox3D'); }
        var args = {
            box : (box === null ? box : box.handle)
        };
        var result = this._execute('createBox', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a temporary solid cylinder or cone BRepBody object.
    // pointOne : A point at one end of the cylinder or cone.
    // pointOneRadius : The radius of the cylinder or cone at the point one end, in centimeters.
    // pointTwo : A point at the opposite end of the cylinder or cone.
    // pointTwoRadius : The radius of the cylinder or cone at the point two end, in centimeters.
    // For a cylinder the pointTwoRadius should be equal to the pointOneRadius.
    // Returns the newly created temporary BRepBody object or null in the case of failure.
    adsk.fusion.TemporaryBRepManager.prototype.createCylinderOrCone = function (pointOne, pointOneRadius, pointTwo, pointTwoRadius) {
        if (pointOne !== null && !(pointOne instanceof adsk.core.Point3D)) { throw new TypeError('pointOne must be a adsk.core.Point3D'); }
        if (!isFinite(pointOneRadius)) { throw new TypeError('pointOneRadius must be a number'); }
        if (pointTwo !== null && !(pointTwo instanceof adsk.core.Point3D)) { throw new TypeError('pointTwo must be a adsk.core.Point3D'); }
        if (!isFinite(pointTwoRadius)) { throw new TypeError('pointTwoRadius must be a number'); }
        var args = {
            pointOne : (pointOne === null ? pointOne : pointOne.handle),
            pointOneRadius : Number(pointOneRadius),
            pointTwo : (pointTwo === null ? pointTwo : pointTwo.handle),
            pointTwoRadius : Number(pointTwoRadius)
        };
        var result = this._execute('createCylinderOrCone', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a temporary elliptical solid cylinder or cone BrepBody object.
    // pointOne : A point at one end of the cylinder or cone.
    // pointOneMajorRadius : The major radius of the cylinder or cone at the point one end, in centimeters.
    // pointOneMinorRadius : The minor radius of the cylinder or cone at the point one end, in centimeters.
    // pointTwo : A point at the opposite end of the cone.
    // pointTwoMajorRadius : The major radius of the cylinder or cone at the point two end, in centimeters. The
    // minor radius is automatically determined using the point one ratio of the minor and major
    // radii.
    // majorAxisDirection : A Vector3D object that defines the direction of the major axis.
    // Returns the newly created temporary BRepBody object or null in the case of failure.
    adsk.fusion.TemporaryBRepManager.prototype.createEllipticalCylinderOrCone = function (pointOne, pointOneMajorRadius, pointOneMinorRadius, pointTwo, pointTwoMajorRadius, majorAxisDirection) {
        if (pointOne !== null && !(pointOne instanceof adsk.core.Point3D)) { throw new TypeError('pointOne must be a adsk.core.Point3D'); }
        if (!isFinite(pointOneMajorRadius)) { throw new TypeError('pointOneMajorRadius must be a number'); }
        if (!isFinite(pointOneMinorRadius)) { throw new TypeError('pointOneMinorRadius must be a number'); }
        if (pointTwo !== null && !(pointTwo instanceof adsk.core.Point3D)) { throw new TypeError('pointTwo must be a adsk.core.Point3D'); }
        if (!isFinite(pointTwoMajorRadius)) { throw new TypeError('pointTwoMajorRadius must be a number'); }
        if (majorAxisDirection !== null && !(majorAxisDirection instanceof adsk.core.Vector3D)) { throw new TypeError('majorAxisDirection must be a adsk.core.Vector3D'); }
        var args = {
            pointOne : (pointOne === null ? pointOne : pointOne.handle),
            pointOneMajorRadius : Number(pointOneMajorRadius),
            pointOneMinorRadius : Number(pointOneMinorRadius),
            pointTwo : (pointTwo === null ? pointTwo : pointTwo.handle),
            pointTwoMajorRadius : Number(pointTwoMajorRadius),
            majorAxisDirection : (majorAxisDirection === null ? majorAxisDirection : majorAxisDirection.handle)
        };
        var result = this._execute('createEllipticalCylinderOrCone', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a temporary spherical BRepBody object.
    // center : The center point of the sphere.
    // radius : The radius of the sphere in centimeters.
    // Returns the newly created temporary BRepBody object or null in the case of failure.
    adsk.fusion.TemporaryBRepManager.prototype.createSphere = function (center, radius) {
        if (center !== null && !(center instanceof adsk.core.Point3D)) { throw new TypeError('center must be a adsk.core.Point3D'); }
        if (!isFinite(radius)) { throw new TypeError('radius must be a number'); }
        var args = {
            center : (center === null ? center : center.handle),
            radius : Number(radius)
        };
        var result = this._execute('createSphere', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a temporary torioidal BRepBody object.
    // center : The center point of the torus.
    // axis : The axis of the torus.
    // majorRadius : The radius, in centimeters, of the major radius of the torus. If the torus was created
    // by sweeping a circle around another cirlce this would be the radius of the path circle.
    // minorRadius : The radius, in centimeters, of the minor radius of the torus. If the torus was created
    // by sweeping a circle around another cirlce this would be the radius of the profile circle.
    // Returns the newly created temporary BRepBody object or null in the case of failure.
    adsk.fusion.TemporaryBRepManager.prototype.createTorus = function (center, axis, majorRadius, minorRadius) {
        if (center !== null && !(center instanceof adsk.core.Point3D)) { throw new TypeError('center must be a adsk.core.Point3D'); }
        if (axis !== null && !(axis instanceof adsk.core.Vector3D)) { throw new TypeError('axis must be a adsk.core.Vector3D'); }
        if (!isFinite(majorRadius)) { throw new TypeError('majorRadius must be a number'); }
        if (!isFinite(minorRadius)) { throw new TypeError('minorRadius must be a number'); }
        var args = {
            center : (center === null ? center : center.handle),
            axis : (axis === null ? axis : axis.handle),
            majorRadius : Number(majorRadius),
            minorRadius : Number(minorRadius)
        };
        var result = this._execute('createTorus', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a body from multiple wires that all lie within the same plane. Multiple wires are
    // used when creating a plane with interior holes. One wire defines the outer shape and the
    // other wires define the interior loops of the created face.
    // wireBodies : An array of bodies that contiain planar wires. Each wire must be closed, they should not overlap,
    // and they should all lie on the same plane.
    // Returns a BRepBody containing the created BRepFace object or null in the case of failure.
    adsk.fusion.TemporaryBRepManager.prototype.createFaceFromPlanarWires = function (wireBodies) {
        if (!Array.isArray(wireBodies)) { throw new TypeError('wireBodies must be an array'); }
        var wireBodiesLength = wireBodies.length;
        var wireBodiesIt;
        for (wireBodiesIt = 0; wireBodiesIt < wireBodiesLength; ++wireBodiesIt) {
            if (wireBodies[wireBodiesIt] !== null && !(wireBodies[wireBodiesIt] instanceof adsk.fusion.BRepBody)) { throw new TypeError('wireBodies[wireBodiesIt] must be a adsk.fusion.BRepBody'); }
        }
        var args = {
            wireBodies : wireBodies
        };
        var result = this._execute('createFaceFromPlanarWires', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // <p>Method that finds regions of faces on two bodies which overlap and creates new bodies where the faces
    // are split at the edges of the overlaps. This does not modify the original bodies but creates new
    // temporary bodies that contain the imprints.</p>
    // <p>The picture below shows an example of imprinting. The picture on the left shows the initial two bodies
    // that are positioned so there are coincident faces. The picture on the right shows the two bodies individually
    // so you can see the result of the imprint and how the coincident faces were split. </p>
    // <br/><br/><center><img src="../Images/ImprintBodies.png"></center><br/>
    // <p>The ability to imprint solids can be important to applications that need to mesh models. By creating edges
    // at the poins where solids connect, it guarantees that there will be mesh nodes along those boundaries.</p>
    // bodyOne : Input BRepBody that will participate in the imprint operation. This body can be either a parametric
    // or temporary body.
    // bodyTwo : Input BRepBody that will participate in the imprint operation. This body can be either a parametric
    // or temporary body.
    // imprintCoincidentEdges : <p>Input Boolean that indicates if overlapping edges should be included in the result. The picture below
    // shows an example of when this argument will make a difference. The two bodies have overlapping faces
    // and there is also an overlapping edge. If this argument is true, then the edge shown in red below
    // will be included in the output as an overlapping edge. If False it will not be included and only
    // the edges of the overlapping faces will be in the overlapping faces collections.</p>
    // <br/><br/><center><img src="../Images/ImprintOverlappingEdges.png"></center>
    // resultBodyOne : Output temporary BRepBody that contains the imprinted body that corresponds to the body provided through the bodyOne argument.
    // resultBodyTwo : Output temporary BRepBody that contains the imprinted body that corresponds to the body provided through the bodyTwo argument.
    // bodyOneOverlappingFaces : Output array of BRepFace objects that represent the overlapping faces that are part of resultBodyOne. Faces at the same index within the
    // collection returned here and that returned by the bodyTwoOverlappingFaces are overlapping.
    // bodyTwoOverlappingFaces : Output array of BRepFace objects that represent the overlapping faces that are part of resultBodyTwo. Faces at the same index within the
    // collection returned here and that returned by the bodyOneOverlappingFaces are overlapping.
    // bodyOneOverlappingEdges : Output array of BRepEdge objects that represent the overlapping edges that are part of resultBodyOne. Edges at the same index within the
    // collection returned here and that returned by the bodyTwoOverlappingEdges are overlapping.
    // bodyTwoOverlappingEdges : Output array of BRepEdge objects that represent the overlapping edges that are part of resultBodyTwo. Edges at the same index within the
    // collection returned here and that returned by the bodyOneOverlappingEdges are overlapping.
    // tolerance : Optional Input double that specifies the tolerance, in centimeters, to use when comparing the bodies. If not specified, or a value of zero
    // is specified, the internal modeling tolerance will be used.
    // Returns true if the imprint calculation was successful.
    adsk.fusion.TemporaryBRepManager.prototype.imprintOverlapBodies = function (bodyOne, bodyTwo, imprintCoincidentEdges, resultBodyOne, resultBodyTwo, bodyOneOverlappingFaces, bodyTwoOverlappingFaces, bodyOneOverlappingEdges, bodyTwoOverlappingEdges, tolerance) {
        if (bodyOne !== null && !(bodyOne instanceof adsk.fusion.BRepBody)) { throw new TypeError('bodyOne must be a adsk.fusion.BRepBody'); }
        if (bodyTwo !== null && !(bodyTwo instanceof adsk.fusion.BRepBody)) { throw new TypeError('bodyTwo must be a adsk.fusion.BRepBody'); }
        if (typeof imprintCoincidentEdges !== 'boolean') { throw new TypeError('imprintCoincidentEdges must be a boolean'); }
        if (typeof resultBodyOne !== 'object') { throw new TypeError('resultBodyOne must be an object'); }
        if (typeof resultBodyTwo !== 'object') { throw new TypeError('resultBodyTwo must be an object'); }
        if (typeof bodyOneOverlappingFaces !== 'object') { throw new TypeError('bodyOneOverlappingFaces must be an object'); }
        if (typeof bodyTwoOverlappingFaces !== 'object') { throw new TypeError('bodyTwoOverlappingFaces must be an object'); }
        if (typeof bodyOneOverlappingEdges !== 'object') { throw new TypeError('bodyOneOverlappingEdges must be an object'); }
        if (typeof bodyTwoOverlappingEdges !== 'object') { throw new TypeError('bodyTwoOverlappingEdges must be an object'); }
        if (tolerance === null || (tolerance !== undefined && !isFinite(tolerance))) { throw new TypeError('tolerance must be a number'); }
        var args = {
            bodyOne : (bodyOne === null ? bodyOne : bodyOne.handle),
            bodyTwo : (bodyTwo === null ? bodyTwo : bodyTwo.handle),
            imprintCoincidentEdges : imprintCoincidentEdges,
            resultBodyOne : null,
            resultBodyTwo : null,
            bodyOneOverlappingFaces : null,
            bodyTwoOverlappingFaces : null,
            bodyOneOverlappingEdges : null,
            bodyTwoOverlappingEdges : null
        };
        if (tolerance !== undefined) {
            args.tolerance = Number(tolerance);
        }
        var result = this._execute('imprintOverlapBodies', args);
        if (result && result.outargs) {
            resultBodyOne.value = (result.outargs.resultBodyOne !== undefined) ? adsk.createObject(result.outargs.resultBodyOne, adsk.fusion.BRepBody) : null;
            resultBodyTwo.value = (result.outargs.resultBodyTwo !== undefined) ? adsk.createObject(result.outargs.resultBodyTwo, adsk.fusion.BRepBody) : null;
            if (Array.isArray(result.outargs.bodyOneOverlappingFaces)) {
                var bodyOneOverlappingFacesIter;
                bodyOneOverlappingFaces.value = [];
                for (bodyOneOverlappingFacesIter = 0; bodyOneOverlappingFacesIter < result.outargs.bodyOneOverlappingFaces.length; ++bodyOneOverlappingFacesIter) {
                    bodyOneOverlappingFaces.value[bodyOneOverlappingFacesIter] = (result.outargs.bodyOneOverlappingFaces[bodyOneOverlappingFacesIter] !== undefined) ? adsk.createObject(result.outargs.bodyOneOverlappingFaces[bodyOneOverlappingFacesIter], adsk.fusion.BRepFace) : null;
                }
            }
            if (Array.isArray(result.outargs.bodyTwoOverlappingFaces)) {
                var bodyTwoOverlappingFacesIter;
                bodyTwoOverlappingFaces.value = [];
                for (bodyTwoOverlappingFacesIter = 0; bodyTwoOverlappingFacesIter < result.outargs.bodyTwoOverlappingFaces.length; ++bodyTwoOverlappingFacesIter) {
                    bodyTwoOverlappingFaces.value[bodyTwoOverlappingFacesIter] = (result.outargs.bodyTwoOverlappingFaces[bodyTwoOverlappingFacesIter] !== undefined) ? adsk.createObject(result.outargs.bodyTwoOverlappingFaces[bodyTwoOverlappingFacesIter], adsk.fusion.BRepFace) : null;
                }
            }
            if (Array.isArray(result.outargs.bodyOneOverlappingEdges)) {
                var bodyOneOverlappingEdgesIter;
                bodyOneOverlappingEdges.value = [];
                for (bodyOneOverlappingEdgesIter = 0; bodyOneOverlappingEdgesIter < result.outargs.bodyOneOverlappingEdges.length; ++bodyOneOverlappingEdgesIter) {
                    bodyOneOverlappingEdges.value[bodyOneOverlappingEdgesIter] = (result.outargs.bodyOneOverlappingEdges[bodyOneOverlappingEdgesIter] !== undefined) ? adsk.createObject(result.outargs.bodyOneOverlappingEdges[bodyOneOverlappingEdgesIter], adsk.fusion.BRepEdge) : null;
                }
            }
            if (Array.isArray(result.outargs.bodyTwoOverlappingEdges)) {
                var bodyTwoOverlappingEdgesIter;
                bodyTwoOverlappingEdges.value = [];
                for (bodyTwoOverlappingEdgesIter = 0; bodyTwoOverlappingEdgesIter < result.outargs.bodyTwoOverlappingEdges.length; ++bodyTwoOverlappingEdgesIter) {
                    bodyTwoOverlappingEdges.value[bodyTwoOverlappingEdgesIter] = (result.outargs.bodyTwoOverlappingEdges[bodyTwoOverlappingEdgesIter] !== undefined) ? adsk.createObject(result.outargs.bodyTwoOverlappingEdges[bodyTwoOverlappingEdgesIter], adsk.fusion.BRepEdge) : null;
                }
            }
        }
        return result ? result.value : undefined;
    };

    // Give an array of curve geometry objects, this method creates a new wire body.
    // curves : An array containing the input Curve3D objects. These can be Arc3D, Circle3D, Ellipse3D, EllipticalArc3D or Line3D objects.
    // edgeMap : An array of edges in the returned body. The order that the edges are in this collection is the
    // same order as the original corresponding Curve3D object is in the input curves array. This allows you to
    // map between the original input curve and created edge.
    // allowSelfIntersections : Specifies if you want to allow self-intersection in the input curves or not.
    // Returns the B-Rep body containing the created wire or null in the case of failure.
    adsk.fusion.TemporaryBRepManager.prototype.createWireFromCurves = function (curves, edgeMap, allowSelfIntersections) {
        if (!Array.isArray(curves)) { throw new TypeError('curves must be an array'); }
        var curvesLength = curves.length;
        var curvesIt;
        for (curvesIt = 0; curvesIt < curvesLength; ++curvesIt) {
            if (curves[curvesIt] !== null && !(curves[curvesIt] instanceof adsk.core.Curve3D)) { throw new TypeError('curves[curvesIt] must be a adsk.core.Curve3D'); }
        }
        if (typeof edgeMap !== 'object') { throw new TypeError('edgeMap must be an object'); }
        if (allowSelfIntersections === null || (allowSelfIntersections !== undefined && typeof allowSelfIntersections !== 'boolean')) { throw new TypeError('allowSelfIntersections must be a boolean'); }
        var args = {
            curves : curves,
            edgeMap : null
        };
        if (allowSelfIntersections !== undefined) {
            args.allowSelfIntersections = allowSelfIntersections;
        }
        var result = this._execute('createWireFromCurves', args);
        if (result && result.outargs) {
            if (Array.isArray(result.outargs.edgeMap)) {
                var edgeMapIter;
                edgeMap.value = [];
                for (edgeMapIter = 0; edgeMapIter < result.outargs.edgeMap.length; ++edgeMapIter) {
                    edgeMap.value[edgeMapIter] = (result.outargs.edgeMap[edgeMapIter] !== undefined) ? adsk.createObject(result.outargs.edgeMap[edgeMapIter], adsk.fusion.BRepEdge) : null;
                }
            }
        }
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    // Creates a B-Rep body that contains a wire with a single edge that represents a helical curve.
    // axisPoint : A Point3D object that defines a point along the axis of the helix.
    // axisVector : A Vector3D object that defines the direction of the axis of the hellix.
    // startPoint : A Point3D that defines the start point of the helix. This is a point on the helix and defines the starting
    // point of the helix. The distance of this point to the axis defines the starting radius of the helix.
    // pitch : The pitch of the helix, or the distance between each of the turns, in centimeters.
    // turns : The number of turns of the helix.
    // taperAngle : The taper angle of the helix in radians.
    //
    adsk.fusion.TemporaryBRepManager.prototype.createHelixWire = function (axisPoint, axisVector, startPoint, pitch, turns, taperAngle) {
        if (axisPoint !== null && !(axisPoint instanceof adsk.core.Point3D)) { throw new TypeError('axisPoint must be a adsk.core.Point3D'); }
        if (axisVector !== null && !(axisVector instanceof adsk.core.Vector3D)) { throw new TypeError('axisVector must be a adsk.core.Vector3D'); }
        if (startPoint !== null && !(startPoint instanceof adsk.core.Point3D)) { throw new TypeError('startPoint must be a adsk.core.Point3D'); }
        if (!isFinite(pitch)) { throw new TypeError('pitch must be a number'); }
        if (!isFinite(turns)) { throw new TypeError('turns must be a number'); }
        if (!isFinite(taperAngle)) { throw new TypeError('taperAngle must be a number'); }
        var args = {
            axisPoint : (axisPoint === null ? axisPoint : axisPoint.handle),
            axisVector : (axisVector === null ? axisVector : axisVector.handle),
            startPoint : (startPoint === null ? startPoint : startPoint.handle),
            pitch : Number(pitch),
            turns : Number(turns),
            taperAngle : Number(taperAngle)
        };
        var result = this._execute('createHelixWire', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
    };

    return adsk;
}));