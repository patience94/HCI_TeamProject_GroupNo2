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

    //=========== MeshBodies ============
    // Provides access to the MeshBodies in the parent Component and
    // supports the creation of new mesh bodies.
    adsk.fusion.MeshBodies = function MeshBodies(handle) {
        if (!(this instanceof adsk.fusion.MeshBodies)) {
            return adsk.fusion.MeshBodies.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.MeshBodies.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.MeshBodies.prototype.constructor = adsk.fusion.MeshBodies;
    adsk.fusion.MeshBodies.classType = function classType () {
        return 'adsk::fusion::MeshBodies';
    };
    adsk.fusion.MeshBodies.interfaceId = 'adsk.fusion.MeshBodies';
    adsk.objectTypes['adsk.fusion.MeshBodies'] = adsk.fusion.MeshBodies;
    adsk.fusion.MeshBodies.cast = function (object) {
        return object instanceof adsk.fusion.MeshBodies ? object : null;
    };

    // Returns the number of mesh bodies in the collection.
    Object.defineProperty(adsk.fusion.MeshBodies.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Creates a new mesh body by importing an .stl or .obj file.
    // Because of a current limitation, if you want to create a mesh body in a parametric model,
    // you must first call the edit method of the base or form feature, use this method to create
    // the mesh body, and then call the finishEdit method of the base or form feature. The base
    // or form feature must be in an "edit" state to be able to add any additional items to it.
    // fullFilename : The full filename (path and file) of a .stl or .obj file.
    // units : The units to use when importing the file.
    // baseOrFormFeature : The BaseFeature or FormFeature object that this mesh body will be associated with. This is an optional
    // requirement and is required when the model design history is being captured (paremetric model) but is
    // ignored otherwise (direct edit model).
    // Returns a list of the newly created mesh bodies or null if the creation failed. Multiple
    // bodies can be created in the case where a .obj file that contains multiple bodies was imported.
    // stl files always contain a single body.
    adsk.fusion.MeshBodies.prototype.add = function (fullFilename, units, baseOrFormFeature) {
        if (fullFilename === undefined || fullFilename === null || fullFilename.constructor !== String) { throw new TypeError('fullFilename must be a string'); }
        if (!isFinite(units)) { throw new TypeError('units must be a number'); }
        if (baseOrFormFeature === null || (baseOrFormFeature !== undefined && baseOrFormFeature !== null && !(baseOrFormFeature instanceof adsk.core.Base))) { throw new TypeError('baseOrFormFeature must be a adsk.core.Base'); }
        var args = {
            fullFilename : fullFilename,
            units : Number(units)
        };
        if (baseOrFormFeature !== undefined) {
            args.baseOrFormFeature = (baseOrFormFeature === null ? baseOrFormFeature : baseOrFormFeature.handle);
        }
        var result = this._execute('add', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshBodyList) : null;
    };

    // Provides access to a mesh body within the collection.
    // index : The index of the mesh body to return, where an index of 0 is the first mesh body in the collection.
    // Returns the specified mesh body or null in the case of a invalid index.
    adsk.fusion.MeshBodies.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshBody) : null;
    };

    // Createa a new mesh body using the mesh description provided.
    // coordinates : Input array of doubles that defines the X, Y, Z coordinates of each node in the mesh. Each set of three numbers define
    // the coordinates of a node.
    // coordinateIndexList : An array of integers that represent indices into the coordinates to define the vertices of the triangles. If an empty
    // array is provided, then it's assumed that the first three coordinates defines the first triangle, the next three define
    // the second triangle, and so on.
    // normalVectors : An array of doubles that represent the x, y, z components of the normals at each coordinate. There should be a normal defined
    // for each coordinate. If an empty array is provided for the normal vectors, Fusion 360 will automatically calculate normal vectors
    // that are 90 degrees to the face of the triangle, making it appear flat.
    // normalIndexList : An array of integers that represent indices into the normal vectors to define the which vector corresponds to which vertex. This
    // should be the same size as the vertex index list. If an empty array is input and normal vectors are provided, it is assumed that
    // the normals match up one-to-one to each coordinate.
    // Returns the newly created MeshBody object or null in the case of a failure.
    adsk.fusion.MeshBodies.prototype.addByTriangleMeshData = function (coordinates, coordinateIndexList, normalVectors, normalIndexList) {
        if (!Array.isArray(coordinates)) { throw new TypeError('coordinates must be an array'); }
        var coordinatesLength = coordinates.length;
        var coordinatesIt;
        for (coordinatesIt = 0; coordinatesIt < coordinatesLength; ++coordinatesIt) {
            if (!isFinite(coordinates[coordinatesIt])) { throw new TypeError('coordinates[coordinatesIt] must be a number'); }
        }
        if (!Array.isArray(coordinateIndexList)) { throw new TypeError('coordinateIndexList must be an array'); }
        var coordinateIndexListLength = coordinateIndexList.length;
        var coordinateIndexListIt;
        for (coordinateIndexListIt = 0; coordinateIndexListIt < coordinateIndexListLength; ++coordinateIndexListIt) {
            if (!isFinite(coordinateIndexList[coordinateIndexListIt])) { throw new TypeError('coordinateIndexList[coordinateIndexListIt] must be a number'); }
        }
        if (!Array.isArray(normalVectors)) { throw new TypeError('normalVectors must be an array'); }
        var normalVectorsLength = normalVectors.length;
        var normalVectorsIt;
        for (normalVectorsIt = 0; normalVectorsIt < normalVectorsLength; ++normalVectorsIt) {
            if (!isFinite(normalVectors[normalVectorsIt])) { throw new TypeError('normalVectors[normalVectorsIt] must be a number'); }
        }
        if (!Array.isArray(normalIndexList)) { throw new TypeError('normalIndexList must be an array'); }
        var normalIndexListLength = normalIndexList.length;
        var normalIndexListIt;
        for (normalIndexListIt = 0; normalIndexListIt < normalIndexListLength; ++normalIndexListIt) {
            if (!isFinite(normalIndexList[normalIndexListIt])) { throw new TypeError('normalIndexList[normalIndexListIt] must be a number'); }
        }
        var args = {
            coordinates : coordinates,
            coordinateIndexList : coordinateIndexList,
            normalVectors : normalVectors,
            normalIndexList : normalIndexList
        };
        var result = this._execute('addByTriangleMeshData', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshBody) : null;
    };

    //=========== MeshBody ============
    // Provides access to a mesh body.
    adsk.fusion.MeshBody = function MeshBody(handle) {
        if (!(this instanceof adsk.fusion.MeshBody)) {
            return adsk.fusion.MeshBody.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.MeshBody.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.MeshBody.prototype.constructor = adsk.fusion.MeshBody;
    adsk.fusion.MeshBody.classType = function classType () {
        return 'adsk::fusion::MeshBody';
    };
    adsk.fusion.MeshBody.interfaceId = 'adsk.fusion.MeshBody';
    adsk.objectTypes['adsk.fusion.MeshBody'] = adsk.fusion.MeshBody;
    adsk.fusion.MeshBody.cast = function (object) {
        return object instanceof adsk.fusion.MeshBody ? object : null;
    };

    // Gets and sets the name of the mesh body as displayed in the browser.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'name', {
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

    // Gets and sets if the mesh body is selectable in the graphics window.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'isSelectable', {
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

    // Is the light bulb (as displayed in the browser) on.
    // A mesh body will only be visible if the light bulb is switched on. However,
    // the light bulb can be on and the mesh body is still invisible if the light bulb
    // for all bodies or the owning component is off.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'isLightBulbOn', {
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

    // Gets if the mesh body point is visible.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'isVisible', {
        get : function () {
            var result = this._execute('isVisible');
            return result ? result.value : undefined;
        }
    });

    // Returns the original mesh data that was imported. This can include triangles, quads, and polygons.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'mesh', {
        get : function () {
            var result = this._execute('mesh');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.PolygonMesh) : null;
        }
    });

    // Returns the associated mesh that is used for the display. This will always be triangles and includes any textures.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'displayMesh', {
        get : function () {
            var result = this._execute('displayMesh');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.TriangleMesh) : null;
        }
    });

    // Returns the parent Component.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'parentComponent', {
        get : function () {
            var result = this._execute('parentComponent');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Component) : null;
        }
    });

    // Returns the assembly occurrence (i.e. the occurrence) of this object
    // in an assembly. This is only valid in the case where this is acting
    // as a proxy in an assembly. Returns null in the case where the object
    // is not in the context of an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'assemblyContext', {
        get : function () {
            var result = this._execute('assemblyContext');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.Occurrence) : null;
        }
    });

    // The NativeObject is the object outside the context of an assembly and
    // in the context of it's parent component.
    // Returns null in the case where this object is not in the context of
    // an assembly but is already the native object.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'nativeObject', {
        get : function () {
            var result = this._execute('nativeObject');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshBody) : null;
        }
    });

    // This property returns the base or form feature that this mesh body is associated with. It
    // returns null in the case where the modeling design history is not being captured (direct edit model).
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'baseOrFormFeature', {
        get : function () {
            var result = this._execute('baseOrFormFeature');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Base) : null;
        }
    });

    // Returns the collection of attributes associated with this mesh body.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'attributes', {
        get : function () {
            var result = this._execute('attributes');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Attributes) : null;
        }
    });

    // Gets and sets the physical material assigned to this mesh body.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'material', {
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

    // Read-write property that gets and sets the current appearance of the body. Setting this property will result in applying
    // an override appearance to the body and the AppearanceSourceType property will return OverrideAppearanceSource. Setting
    // this property to null will remove any override.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'appearance', {
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
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'appearanceSourceType', {
        get : function () {
            var result = this._execute('appearanceSourceType');
            return result ? result.value : undefined;
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
    // To get the opacity that it is being displayed with use the MeshBody.visibleOpacity property.
    // This is the API equivalent of the "Opacity Control" command available for the body in the browser.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'opacity', {
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
    // being used to render the body. To set the opacity use the opacity property of the MeshBody object.
    Object.defineProperty(adsk.fusion.MeshBody.prototype, 'visibleOpacity', {
        get : function () {
            var result = this._execute('visibleOpacity');
            return result ? result.value : undefined;
        }
    });

    // Deletes the mesh body.
    // Returns true in the case where the selection was successful.
    adsk.fusion.MeshBody.prototype.deleteMe = function () {
        var result = this._execute('deleteMe');
        return result ? result.value : undefined;
    };

    // Creates or returns a proxy for the native object
    // - i.e. a new object that represents this object but adds the assembly context
    // defined by the input occurrence.
    // Fails if this object is not the NativeObject.
    // occurrence : The occurrence that represents the context you want to create this proxy in.
    // Returns the proxy for the occurrence in the context of the specified occurrence. Returns null if it failed.
    adsk.fusion.MeshBody.prototype.createForAssemblyContext = function (occurrence) {
        if (occurrence !== null && !(occurrence instanceof adsk.fusion.Occurrence)) { throw new TypeError('occurrence must be a adsk.fusion.Occurrence'); }
        var args = {
            occurrence : (occurrence === null ? occurrence : occurrence.handle)
        };
        var result = this._execute('createForAssemblyContext', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshBody) : null;
    };

    //=========== MeshBodyList ============
    // Provides access to a list of MeshBody objects.
    adsk.fusion.MeshBodyList = function MeshBodyList(handle) {
        if (!(this instanceof adsk.fusion.MeshBodyList)) {
            return adsk.fusion.MeshBodyList.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.MeshBodyList.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.MeshBodyList.prototype.constructor = adsk.fusion.MeshBodyList;
    adsk.fusion.MeshBodyList.classType = function classType () {
        return 'adsk::fusion::MeshBodyList';
    };
    adsk.fusion.MeshBodyList.interfaceId = 'adsk.fusion.MeshBodyList';
    adsk.objectTypes['adsk.fusion.MeshBodyList'] = adsk.fusion.MeshBodyList;
    adsk.fusion.MeshBodyList.cast = function (object) {
        return object instanceof adsk.fusion.MeshBodyList ? object : null;
    };

    // Returns the number of mesh bodies in the collection.
    Object.defineProperty(adsk.fusion.MeshBodyList.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Provides access to a mesh body within the collection.
    // index : The index of the mesh body to return, where an index of 0 is the first mesh body in the collection.
    // Returns the specified mesh body or null in the case of a invalid index.
    adsk.fusion.MeshBodyList.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.MeshBody) : null;
    };

    //=========== MeshUnits ============
    // The unit types that can be specified when importing a .stl or .obj file as a mesh.
    adsk.fusion.MeshUnits = {
        CentimeterMeshUnit : 0,
        MillimeterMeshUnit : 1,
        MeterMeshUnit : 2,
        InchMeshUnit : 3,
        FootMeshUnit : 4
    };

    return adsk;
}));