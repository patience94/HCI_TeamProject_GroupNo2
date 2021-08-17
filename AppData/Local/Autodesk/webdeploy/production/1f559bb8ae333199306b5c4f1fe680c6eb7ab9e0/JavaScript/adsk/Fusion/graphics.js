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

    //=========== CustomGraphicsBillBoard ============
    // Used to specify if the orientation of custom graphics are defined relative to the screen instead of model space.
    // This is commonly used for legends and symbols that you want to always face the user, even as the
    // camera is rotated.
    adsk.fusion.CustomGraphicsBillBoard = function CustomGraphicsBillBoard(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsBillBoard)) {
            return adsk.fusion.CustomGraphicsBillBoard.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsBillBoard.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsBillBoard.prototype.constructor = adsk.fusion.CustomGraphicsBillBoard;
    adsk.fusion.CustomGraphicsBillBoard.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsBillBoard';
    };
    adsk.fusion.CustomGraphicsBillBoard.interfaceId = 'adsk.fusion.CustomGraphicsBillBoard';
    adsk.objectTypes['adsk.fusion.CustomGraphicsBillBoard'] = adsk.fusion.CustomGraphicsBillBoard;
    adsk.fusion.CustomGraphicsBillBoard.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsBillBoard ? object : null;
    };

    // Specifies the coordinate in model or view space that the graphics will anchor to. For graphics that
    // represent a label, this will typically be the point where the label attaches to the model. A
    // CustomGraphicsAnchorPoint can be created using the static create method on the CustomGraphicsAnchorPoint
    // object.
    Object.defineProperty(adsk.fusion.CustomGraphicsBillBoard.prototype, 'anchorPoint', {
        get : function () {
            var result = this._execute('anchorPoint');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Point3D) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Point3D)) { throw new TypeError('value must be a adsk.core.Point3D'); }
            var args = {
                value : value
            };
            var result = this._execute('anchorPoint', args);
            return result ? result.value : undefined;
        }
    });

    // Specifies the type of billboarding to use. When a new CustomGraphicsBillBoard object is created
    // this defaults to ScreenBillBoardStyle so the graphics will all be facing the view plane. It can also
    // be set to an arbitrary plane by setting this to AxialBillBoardStyle and can be defined so that it never
    // appear backwards by setting it to RightReadingBillBoardStyle.
    Object.defineProperty(adsk.fusion.CustomGraphicsBillBoard.prototype, 'billBoardStyle', {
        get : function () {
            var result = this._execute('billBoardStyle');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('billBoardStyle', args);
            return result ? result.value : undefined;
        }
    });

    // When the billBoardStyle property is set to AxialBillBoardStyle, this is used to control the direction
    // of the graphics. Otherwise it uses the x axis of the view.
    Object.defineProperty(adsk.fusion.CustomGraphicsBillBoard.prototype, 'axis', {
        get : function () {
            var result = this._execute('axis');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Vector3D) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Vector3D)) { throw new TypeError('value must be a adsk.core.Vector3D'); }
            var args = {
                value : value
            };
            var result = this._execute('axis', args);
            return result ? result.value : undefined;
        }
    });

    // Creates a new CustomGraphicsBillBoard object that can be used when calling the billBoarding property
    // of the CustomGraphicsEntity object to specify the billboarding behavior of some custom graphics. Once
    // created you can assign it to a custom graphics entity using its billBoarding property.
    // anchorPoint : Specifies the coordinate that the graphics will anchor to. The anchor point is the point where the
    // custom graphics are anchored in world space. As the user manipulates the camera and rotates around
    // the model, making it appear that world space is rotating, the graphics remain facing the camera and
    // the anchor point defines the common location between world space and the graphics.
    // For graphics where the If the isViewDependent property of the graphics entity is true, then the
    // anchor point is defined in pixels relative to the upper-left corner of the view and the z component
    // of the input point is ignored.
    // Returns the newly created CustomGraphicsBillBoard object or null in the case of failure. This can be assigned
    // to a custom graphics entity using its billBoarding property.
    adsk.fusion.CustomGraphicsBillBoard.create = function (anchorPoint) {
        if (anchorPoint !== null && !(anchorPoint instanceof adsk.core.Point3D)) { throw new TypeError('anchorPoint must be a adsk.core.Point3D'); }
        var args = {
            anchorPoint : (anchorPoint === null ? anchorPoint : anchorPoint.handle)
        };
        var result = adsk.core.Base._executeStatic('adsk.fusion.CustomGraphicsBillBoard', 'create', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsBillBoard) : null;
    };

    //=========== CustomGraphicsBillBoardStyles ============
    // Specifies the different styles that can be used to control billboarding.
    adsk.fusion.CustomGraphicsBillBoardStyles = {
        ScreenBillBoardStyle : 1,
        AxialBillBoardStyle : 2,
        RightReadingBillBoardStyle : 3
    };

    //=========== CustomGraphicsBRepEdges ============
    // A collection of CustomGraphicsBRepEdge objects associated with a specific CustomGraphics body object.
    adsk.fusion.CustomGraphicsBRepEdges = function CustomGraphicsBRepEdges(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsBRepEdges)) {
            return adsk.fusion.CustomGraphicsBRepEdges.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsBRepEdges.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsBRepEdges.prototype.constructor = adsk.fusion.CustomGraphicsBRepEdges;
    adsk.fusion.CustomGraphicsBRepEdges.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsBRepEdges';
    };
    adsk.fusion.CustomGraphicsBRepEdges.interfaceId = 'adsk.fusion.CustomGraphicsBRepEdges';
    adsk.objectTypes['adsk.fusion.CustomGraphicsBRepEdges'] = adsk.fusion.CustomGraphicsBRepEdges;
    adsk.fusion.CustomGraphicsBRepEdges.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsBRepEdges ? object : null;
    };

    //=========== CustomGraphicsBRepFaces ============
    // A collection of CustomGraphicsBRepFace objects associated with a specific CustomGraphicsBRepBody object.
    adsk.fusion.CustomGraphicsBRepFaces = function CustomGraphicsBRepFaces(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsBRepFaces)) {
            return adsk.fusion.CustomGraphicsBRepFaces.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsBRepFaces.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsBRepFaces.prototype.constructor = adsk.fusion.CustomGraphicsBRepFaces;
    adsk.fusion.CustomGraphicsBRepFaces.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsBRepFaces';
    };
    adsk.fusion.CustomGraphicsBRepFaces.interfaceId = 'adsk.fusion.CustomGraphicsBRepFaces';
    adsk.objectTypes['adsk.fusion.CustomGraphicsBRepFaces'] = adsk.fusion.CustomGraphicsBRepFaces;
    adsk.fusion.CustomGraphicsBRepFaces.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsBRepFaces ? object : null;
    };

    //=========== CustomGraphicsBRepVertices ============
    // A collection of CustomGraphicsBRepVertex objects associated with a specific CustomGraphics body object.
    adsk.fusion.CustomGraphicsBRepVertices = function CustomGraphicsBRepVertices(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsBRepVertices)) {
            return adsk.fusion.CustomGraphicsBRepVertices.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsBRepVertices.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsBRepVertices.prototype.constructor = adsk.fusion.CustomGraphicsBRepVertices;
    adsk.fusion.CustomGraphicsBRepVertices.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsBRepVertices';
    };
    adsk.fusion.CustomGraphicsBRepVertices.interfaceId = 'adsk.fusion.CustomGraphicsBRepVertices';
    adsk.objectTypes['adsk.fusion.CustomGraphicsBRepVertices'] = adsk.fusion.CustomGraphicsBRepVertices;
    adsk.fusion.CustomGraphicsBRepVertices.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsBRepVertices ? object : null;
    };

    //=========== CustomGraphicsColorEffect ============
    // The base class for all custom graphics color effects.
    adsk.fusion.CustomGraphicsColorEffect = function CustomGraphicsColorEffect(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsColorEffect)) {
            return adsk.fusion.CustomGraphicsColorEffect.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsColorEffect.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsColorEffect.prototype.constructor = adsk.fusion.CustomGraphicsColorEffect;
    adsk.fusion.CustomGraphicsColorEffect.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsColorEffect';
    };
    adsk.fusion.CustomGraphicsColorEffect.interfaceId = 'adsk.fusion.CustomGraphicsColorEffect';
    adsk.objectTypes['adsk.fusion.CustomGraphicsColorEffect'] = adsk.fusion.CustomGraphicsColorEffect;
    adsk.fusion.CustomGraphicsColorEffect.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsColorEffect ? object : null;
    };

    //=========== CustomGraphicsCoordinates ============
    // Represents coordinates that are used to define vertices in custom graphics.
    adsk.fusion.CustomGraphicsCoordinates = function CustomGraphicsCoordinates(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsCoordinates)) {
            return adsk.fusion.CustomGraphicsCoordinates.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsCoordinates.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsCoordinates.prototype.constructor = adsk.fusion.CustomGraphicsCoordinates;
    adsk.fusion.CustomGraphicsCoordinates.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsCoordinates';
    };
    adsk.fusion.CustomGraphicsCoordinates.interfaceId = 'adsk.fusion.CustomGraphicsCoordinates';
    adsk.objectTypes['adsk.fusion.CustomGraphicsCoordinates'] = adsk.fusion.CustomGraphicsCoordinates;
    adsk.fusion.CustomGraphicsCoordinates.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsCoordinates ? object : null;
    };

    // Gets and sets the coordinate data associated with this CustomGraphicsCoordinates object.
    // This data represents the x, y, z components of the coordinates where the unit of measure is centimeters.
    Object.defineProperty(adsk.fusion.CustomGraphicsCoordinates.prototype, 'coordinates', {
        get : function () {
            var result = this._execute('coordinates');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!Array.isArray(value)) { throw new TypeError('value must be an array'); }
            var valueLength = value.length;
            var valueIt;
            for (valueIt = 0; valueIt < valueLength; ++valueIt) {
                if (!isFinite(value[valueIt])) { throw new TypeError('value[valueIt] must be a number'); }
            }
            var args = {
                value : value
            };
            var result = this._execute('coordinates', args);
            return result ? result.value : undefined;
        }
    });

    // Returns the number of coordinates defined in the CustomGraphicsCoordinates object.
    Object.defineProperty(adsk.fusion.CustomGraphicsCoordinates.prototype, 'coordinateCount', {
        get : function () {
            var result = this._execute('coordinateCount');
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the colors assoicated with the coordinate data. This is used when a mesh is
    // displayed using per-vertex coloring.
    // The color at each vertex is represented by four values where they are the red, green, blue,
    // and alpha values. This should contain the same number of colors as vertices.
    Object.defineProperty(adsk.fusion.CustomGraphicsCoordinates.prototype, 'colors', {
        get : function () {
            var result = this._execute('colors');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!Array.isArray(value)) { throw new TypeError('value must be an array'); }
            var valueLength = value.length;
            var valueIt;
            for (valueIt = 0; valueIt < valueLength; ++valueIt) {
                if (!isFinite(value[valueIt])) { throw new TypeError('value[valueIt] must be a number'); }
            }
            var args = {
                value : value
            };
            var result = this._execute('colors', args);
            return result ? result.value : undefined;
        }
    });

    // Static method that creates a CustomGraphicsCoordinates object which can be used as input to
    // various custom graphics methods.
    // coordinates : An array of doubles where the values are the x, y, z components of each coordinate where
    // the unit of measure is centimeters.
    // Returns the created CustomGraphicsCoordinates object or null in the case of failure.
    adsk.fusion.CustomGraphicsCoordinates.create = function (coordinates) {
        if (!Array.isArray(coordinates)) { throw new TypeError('coordinates must be an array'); }
        var coordinatesLength = coordinates.length;
        var coordinatesIt;
        for (coordinatesIt = 0; coordinatesIt < coordinatesLength; ++coordinatesIt) {
            if (!isFinite(coordinates[coordinatesIt])) { throw new TypeError('coordinates[coordinatesIt] must be a number'); }
        }
        var args = {
            coordinates : coordinates
        };
        var result = adsk.core.Base._executeStatic('adsk.fusion.CustomGraphicsCoordinates', 'create', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsCoordinates) : null;
    };

    // Gets the coordinate at the specified index.
    // index : The index of the coordinate to return. The first coordinate has an index of 0.
    // Returns the coordinate as a Point3D object.
    adsk.fusion.CustomGraphicsCoordinates.prototype.getCoordinate = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('getCoordinate', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.core.Point3D) : null;
    };

    // Sets the coordinate at the specified index.
    // index : The index of the coordinate to set. The first coordinate has an index of 0.
    // coordinate : The coordinate value as a Point3D object.
    // Returns true if setting the coordinate was successful.
    adsk.fusion.CustomGraphicsCoordinates.prototype.setCoordinate = function (index, coordinate) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        if (coordinate !== null && !(coordinate instanceof adsk.core.Point3D)) { throw new TypeError('coordinate must be a adsk.core.Point3D'); }
        var args = {
            index : Number(index),
            coordinate : (coordinate === null ? coordinate : coordinate.handle)
        };
        var result = this._execute('setCoordinate', args);
        return result ? result.value : undefined;
    };

    // Gets the color assigned to the coordinate at the specified index.
    // index : The index of the color to return. The first color has an index of 0.
    // Returns the color associated with the index. Can also return null in the case
    // where there is no color assigned.
    adsk.fusion.CustomGraphicsCoordinates.prototype.getColor = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('getColor', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.core.Color) : null;
    };

    // Sets the color of the coordinate at the specified index.
    // index : The index of the coordinate to set. The first coordinate has an index of 0.
    // color : The color value as a Color object.
    // Returns true if setting the color was successful.
    adsk.fusion.CustomGraphicsCoordinates.prototype.setColor = function (index, color) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        if (color !== null && !(color instanceof adsk.core.Color)) { throw new TypeError('color must be a adsk.core.Color'); }
        var args = {
            index : Number(index),
            color : (color === null ? color : color.handle)
        };
        var result = this._execute('setColor', args);
        return result ? result.value : undefined;
    };

    //=========== CustomGraphicsCullModes ============
    // The various culling modes supported by custom graphics.
    adsk.fusion.CustomGraphicsCullModes = {
        CustomGraphicsCullFront : 0,
        CustomGraphicsCullBack : 1,
        CustomGraphicsCullNone : 2
    };

    //=========== CustomGraphicsEntity ============
    // The base class for all visible and selectable custom graphics objects.
    adsk.fusion.CustomGraphicsEntity = function CustomGraphicsEntity(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsEntity)) {
            return adsk.fusion.CustomGraphicsEntity.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsEntity.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsEntity.prototype.constructor = adsk.fusion.CustomGraphicsEntity;
    adsk.fusion.CustomGraphicsEntity.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsEntity';
    };
    adsk.fusion.CustomGraphicsEntity.interfaceId = 'adsk.fusion.CustomGraphicsEntity';
    adsk.objectTypes['adsk.fusion.CustomGraphicsEntity'] = adsk.fusion.CustomGraphicsEntity;
    adsk.fusion.CustomGraphicsEntity.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsEntity ? object : null;
    };

    // Gets and sets if the graphics entity is visible in the graphics window. By
    // default, when a new entity is created it is visible.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'isVisible', {
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

    // Gets and sets if the graphics entity is selectable within the graphics window. By
    // default, when a new entity is created it is selectable.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'isSelectable', {
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

    // Gets and sets the transform associated with the graphics entity. When a new graphics
    // entity is created its default transform is an identity matrix which results in the graphics entity
    // being displayed in model space using the original coordinate data used to define the entity.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'transform', {
        get : function () {
            var result = this._execute('transform');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Matrix3D) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Matrix3D)) { throw new TypeError('value must be a adsk.core.Matrix3D'); }
            var args = {
                value : value
            };
            var result = this._execute('transform', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the depth priority associated with the graphics entity. The depth priority defines
    // how one graphics entity will be drawn with respect to another entity. This is useful when there
    // are entities that lie in the same space so it's ambiguous which should be drawn on the other. For
    // example, if you draw a curve on a planar mesh and want the curve to be completely visible. You can
    // set the depth priority of the curve to be greater than the mesh so it will be drawn after the mesh
    // and will remain visible.
    // When a new graphics entity is created it's default depth priority is 0.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'depthPriority', {
        get : function () {
            var result = this._execute('depthPriority');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('depthPriority', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the culling model to use when rendering the entity. Culling is used when the entity contains
    // a mesh or B-Rep faces and defines which sides of the mesh or face are rendered. This is primarily used
    // for a watertight mesh or solid B-Rep so that the "inside" of the faces is not rendered since it's never
    // visible to the user.
    // When a new graphics entity is created its default cull mode is CustomGraphicsCullBack which will optimize
    // the rendering of "solid" meshes so the inside is not rendered.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'cullMode', {
        get : function () {
            var result = this._execute('cullMode');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('cullMode', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the current color definition for this entity. The color of custom graphics can
    // be defined in many ways; solid color, simple material, and appearance.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'color', {
        get : function () {
            var result = this._execute('color');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsColorEffect) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.fusion.CustomGraphicsColorEffect)) { throw new TypeError('value must be a adsk.fusion.CustomGraphicsColorEffect'); }
            var args = {
                value : value
            };
            var result = this._execute('color', args);
            return result ? result.value : undefined;
        }
    });

    // Returns the parent Component for a top-level group or the CustomGraphicsGroup object for
    // graphics entities and child groups.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'parent', {
        get : function () {
            var result = this._execute('parent');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Base) : null;
        }
    });

    // An id you can specify for the entity. By default, all new graphics entities do not have an id and
    // this property will return an empty string. But in cases where entities will be selected, assigning
    // an id can make understanding what was selected much easier.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'id', {
        get : function () {
            var result = this._execute('id');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (value === undefined || value === null || value.constructor !== String) { throw new TypeError('value must be a string'); }
            var args = {
                value : value
            };
            var result = this._execute('id', args);
            return result ? result.value : undefined;
        }
    });

    // Returns a box oriented parallel to the world x-y-x axes that contains the graphics entity.
    // Depending on whether the graphics are drawn in model space or screen space this will return
    // the bounding box in either centimeters (model) or pixels (screen). In the case where it
    // returns the bounding box in pixel space, the Z coordinates of the box will be 0 and can be ignored.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'boundingBox', {
        get : function () {
            var result = this._execute('boundingBox');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.BoundingBox3D) : null;
        }
    });

    // Gets and sets the billboarding behavior of this custom graphics entity. To define billboarding
    // you can set this property using a CustomGraphicsBillBoard objects that you statically create using
    // the create method of the CustomGraphicsBillBoard class. To remove billboarding from this entity
    // you can set this property to null.
    // Billboarding is used to specify that the orientation of custom graphics is defined relative to the
    // screen instead of model space. This is commonly used for legends and symbols that you want to
    // always face the user, even as the camera is rotated.
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'billBoarding', {
        get : function () {
            var result = this._execute('billBoarding');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsBillBoard) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.fusion.CustomGraphicsBillBoard)) { throw new TypeError('value must be a adsk.fusion.CustomGraphicsBillBoard'); }
            var args = {
                value : value
            };
            var result = this._execute('billBoarding', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the graphics view placement being applied to this graphics entity. A
    // CustomGraphicsViewPlacement object can be created using the static create method of the
    // class. When assigned to a graphics entity the position of the graphics is defined
    // relative to the view in 2D view space (pixels) rather than in 3D model space (centimeters).
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'viewPlacement', {
        get : function () {
            var result = this._execute('viewPlacement');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsViewPlacement) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.fusion.CustomGraphicsViewPlacement)) { throw new TypeError('value must be a adsk.fusion.CustomGraphicsViewPlacement'); }
            var args = {
                value : value
            };
            var result = this._execute('viewPlacement', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the graphics view scale being applied to this graphics entity. A
    // CustomGraphicsViewScale object can be created using the static create method of the
    // class. When assigned to a graphics entity the size of the graphics entity is defined
    // in view space (pixels) instead of model space (centimeters).
    Object.defineProperty(adsk.fusion.CustomGraphicsEntity.prototype, 'viewScale', {
        get : function () {
            var result = this._execute('viewScale');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsViewScale) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.fusion.CustomGraphicsViewScale)) { throw new TypeError('value must be a adsk.fusion.CustomGraphicsViewScale'); }
            var args = {
                value : value
            };
            var result = this._execute('viewScale', args);
            return result ? result.value : undefined;
        }
    });

    // Deletes the entity from the custom graphics group.
    // Returns true if the deletion was successful.
    adsk.fusion.CustomGraphicsEntity.prototype.deleteMe = function () {
        var result = this._execute('deleteMe');
        return result ? result.value : undefined;
    };

    // Sets the opacity of the graphics entity. By default, when a new entity is it is
    // completely opaque and does not override the opacity defined by the material.
    // opacity : The opacity value where 1.0 is completely opaque and 0.0 is completely transparent.
    // isOverride : Indicates if this entities opacity will override the opacity defined by the material.
    // If true, it will override the material opacity and if false the opacity values will
    // accumulate.
    // Returns true if setting the opacity information was successful.
    adsk.fusion.CustomGraphicsEntity.prototype.setOpacity = function (opacity, isOverride) {
        if (!isFinite(opacity)) { throw new TypeError('opacity must be a number'); }
        if (typeof isOverride !== 'boolean') { throw new TypeError('isOverride must be a boolean'); }
        var args = {
            opacity : Number(opacity),
            isOverride : isOverride
        };
        var result = this._execute('setOpacity', args);
        return result ? result.value : undefined;
    };

    // Gets the opacity of the graphics entity.
    // opacity : The opacity value where 1.0 is completely opaque and 0.0 is completely transparent.
    // isOverride : Indicates if this entities opacity will override the opacity defined by the material.
    // If true, it will override the material opacity and if false the opacity values will
    // accumulate.
    // Returns true if getting the opacity information was successful.
    adsk.fusion.CustomGraphicsEntity.prototype.getOpacity = function (opacity, isOverride) {
        if (typeof opacity !== 'object') { throw new TypeError('opacity must be an object'); }
        if (typeof isOverride !== 'object') { throw new TypeError('isOverride must be an object'); }
        var args = {
            opacity : null,
            isOverride : null
        };
        var result = this._execute('getOpacity', args);
        if (result && result.outargs) {
            opacity.value = (result.outargs.opacity !== undefined) ? result.outargs.opacity : undefined;
            isOverride.value = (result.outargs.isOverride !== undefined) ? result.outargs.isOverride : undefined;
        }
        return result ? result.value : undefined;
    };

    //=========== CustomGraphicsGroups ============
    // Provides access to a set of graphics groups that are either associated with a component or owned by another
    // CustomGraphicsGroup object. This object also supports the creation of new custom graphics groups.
    adsk.fusion.CustomGraphicsGroups = function CustomGraphicsGroups(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsGroups)) {
            return adsk.fusion.CustomGraphicsGroups.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsGroups.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsGroups.prototype.constructor = adsk.fusion.CustomGraphicsGroups;
    adsk.fusion.CustomGraphicsGroups.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsGroups';
    };
    adsk.fusion.CustomGraphicsGroups.interfaceId = 'adsk.fusion.CustomGraphicsGroups';
    adsk.objectTypes['adsk.fusion.CustomGraphicsGroups'] = adsk.fusion.CustomGraphicsGroups;
    adsk.fusion.CustomGraphicsGroups.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsGroups ? object : null;
    };

    // Returns the number of graphics groups in the collection.
    Object.defineProperty(adsk.fusion.CustomGraphicsGroups.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified graphics group using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.CustomGraphicsGroups.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsGroup) : null;
    };

    // Creates a new, empty CustomGraphicsGroup.
    // Returns the new CustomGraphicsGroup object or null in the case of a failure.
    adsk.fusion.CustomGraphicsGroups.prototype.add = function () {
        var result = this._execute('add');
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsGroup) : null;
    };

    //=========== CustomGraphicsPointTypes ============
    // A list of predefined point images that you can use for a CustomGraphicsPointSet.
    adsk.fusion.CustomGraphicsPointTypes = {
        UserDefinedCustomGraphicsPointType : 0,
        PointCloudCustomGraphicsPointType : 1
    };

    //=========== CustomGraphicsViewPlacement ============
    // Positions custom graphics relative to one of the four corners of the view. Graphics positioned
    // this way will always appear on top of the model graphics. This is typically used to display
    // legends are small interactive tools.
    adsk.fusion.CustomGraphicsViewPlacement = function CustomGraphicsViewPlacement(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsViewPlacement)) {
            return adsk.fusion.CustomGraphicsViewPlacement.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsViewPlacement.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsViewPlacement.prototype.constructor = adsk.fusion.CustomGraphicsViewPlacement;
    adsk.fusion.CustomGraphicsViewPlacement.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsViewPlacement';
    };
    adsk.fusion.CustomGraphicsViewPlacement.interfaceId = 'adsk.fusion.CustomGraphicsViewPlacement';
    adsk.objectTypes['adsk.fusion.CustomGraphicsViewPlacement'] = adsk.fusion.CustomGraphicsViewPlacement;
    adsk.fusion.CustomGraphicsViewPlacement.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsViewPlacement ? object : null;
    };

    // Gets and sets the position within the defined graphics that serves as the anchor. This is the location
    // on the graphics that is positioned at the specified view point.
    Object.defineProperty(adsk.fusion.CustomGraphicsViewPlacement.prototype, 'anchorPoint', {
        get : function () {
            var result = this._execute('anchorPoint');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Point3D) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Point3D)) { throw new TypeError('value must be a adsk.core.Point3D'); }
            var args = {
                value : value
            };
            var result = this._execute('anchorPoint', args);
            return result ? result.value : undefined;
        }
    });

    // A 2D point in the view that defines the position of the graphics. This is relative to the corner
    // and is in pixels. The x and y directions vary for each of the corners. These directions are only
    // used to position the 2D point and do not affect the standard coordinate system the graphics were
    // drawn in.
    // upperLeftViewCorner - The x direction is to the right and y is down.
    // upperRightViewCorner - The x direction is to the left and y is down.
    // lowerLeftViewCorner - The x direction is to the right and y is up.
    // lowerRightViewCorner - The x direction is to the left and y is up.
    Object.defineProperty(adsk.fusion.CustomGraphicsViewPlacement.prototype, 'viewPoint', {
        get : function () {
            var result = this._execute('viewPoint');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Point2D) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Point2D)) { throw new TypeError('value must be a adsk.core.Point2D'); }
            var args = {
                value : value
            };
            var result = this._execute('viewPoint', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets which corner the graphics are positioned relative to.
    Object.defineProperty(adsk.fusion.CustomGraphicsViewPlacement.prototype, 'viewCorner', {
        get : function () {
            var result = this._execute('viewCorner');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('viewCorner', args);
            return result ? result.value : undefined;
        }
    });

    // Creates a new CustomGraphicsViewPlacement object that can be used when setting the viewPlacement property
    // of a custom graphics entity to specify the billboarding behavior.
    // anchorPoint : The position within the defined graphics that will serve as the anchor. This is the location
    // on the graphics that will be positioned at the specified view point.
    // viewCorner : Defines which of the four corners of the view the graphics are drawn relative to.
    // viewPoint : A 2D point in the view that defines the position of the graphics. This is relative to the corner
    // and is in pixels. The x and y directions vary for each of the corners. These directions are only
    // used to position the 2D point and do not affect the standard coordinate system the graphics were
    // drawn in.
    // upperLeftViewCorner - The x direction is to the right and y is down.
    // upperRightViewCorner - The x direction is to the left and y is down.
    // lowerLeftViewCorner - The x direction is to the right and y is up.
    // lowerRightViewCorner - The x direction is to the left and y is up.
    // Returns the newly created CustomGraphicsViewPlacement object or null in the case of failure. This can then
    // be assigned to any custom graphics entity using its viewPlacement property.
    adsk.fusion.CustomGraphicsViewPlacement.create = function (anchorPoint, viewCorner, viewPoint) {
        if (anchorPoint !== null && !(anchorPoint instanceof adsk.core.Point3D)) { throw new TypeError('anchorPoint must be a adsk.core.Point3D'); }
        if (!isFinite(viewCorner)) { throw new TypeError('viewCorner must be a number'); }
        if (viewPoint !== null && !(viewPoint instanceof adsk.core.Point2D)) { throw new TypeError('viewPoint must be a adsk.core.Point2D'); }
        var args = {
            anchorPoint : (anchorPoint === null ? anchorPoint : anchorPoint.handle),
            viewCorner : Number(viewCorner),
            viewPoint : (viewPoint === null ? viewPoint : viewPoint.handle)
        };
        var result = adsk.core.Base._executeStatic('adsk.fusion.CustomGraphicsViewPlacement', 'create', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsViewPlacement) : null;
    };

    //=========== CustomGraphicsViewScale ============
    // Specifies that custom graphics are to be scaled relative to the view (pixels) and not model space.
    // If this is applied to some custom graphics then they will stat the same size on the screen regardless
    // of the user zooming in or out. This is commonly used for glyphs and other interactive widgets so they don't
    // don't get too large or too small.
    adsk.fusion.CustomGraphicsViewScale = function CustomGraphicsViewScale(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsViewScale)) {
            return adsk.fusion.CustomGraphicsViewScale.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.CustomGraphicsViewScale.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.CustomGraphicsViewScale.prototype.constructor = adsk.fusion.CustomGraphicsViewScale;
    adsk.fusion.CustomGraphicsViewScale.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsViewScale';
    };
    adsk.fusion.CustomGraphicsViewScale.interfaceId = 'adsk.fusion.CustomGraphicsViewScale';
    adsk.objectTypes['adsk.fusion.CustomGraphicsViewScale'] = adsk.fusion.CustomGraphicsViewScale;
    adsk.fusion.CustomGraphicsViewScale.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsViewScale ? object : null;
    };

    // Gets and sets the scale of the custom graphics relative to the view. If a custom graphics line is defined
    // to be 100 units long it would usually display as 100 cm long. When it is view scaled with a pixel scale of
    // 1 it will display as 100 pixels long.
    Object.defineProperty(adsk.fusion.CustomGraphicsViewScale.prototype, 'pixelScale', {
        get : function () {
            var result = this._execute('pixelScale');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('pixelScale', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the point in the graphics that defines the origin of the scaling. The graphics will be scaled
    // up or down relative to that point.
    Object.defineProperty(adsk.fusion.CustomGraphicsViewScale.prototype, 'anchorPoint', {
        get : function () {
            var result = this._execute('anchorPoint');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Point3D) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Point3D)) { throw new TypeError('value must be a adsk.core.Point3D'); }
            var args = {
                value : value
            };
            var result = this._execute('anchorPoint', args);
            return result ? result.value : undefined;
        }
    });

    // Creates a new CustomGraphicsViewScale object that can be used when setting the viewScale property
    // of a custom graphics entity to specify the scaling behavior.
    // pixelScale : Defines the scale of the custom graphics relative to the view. If a custom graphics line is defined
    // to be 100 units long it would usually display as 100 cm long. When it is view scaled with a pixel scale of
    // 1 it will display as 100 pixels long.
    // anchorPoint : Defines the point in the graphics that defines the origin of the scaling. The graphics will be scaled
    // up or down relative to that point.
    // Returns the newly created CustomGraphicsViewScale object or null in the case of failure. This can then
    // be assigned to any custom graphics entity using its viewScale property.
    adsk.fusion.CustomGraphicsViewScale.create = function (pixelScale, anchorPoint) {
        if (!isFinite(pixelScale)) { throw new TypeError('pixelScale must be a number'); }
        if (anchorPoint !== null && !(anchorPoint instanceof adsk.core.Point3D)) { throw new TypeError('anchorPoint must be a adsk.core.Point3D'); }
        var args = {
            pixelScale : Number(pixelScale),
            anchorPoint : (anchorPoint === null ? anchorPoint : anchorPoint.handle)
        };
        var result = adsk.core.Base._executeStatic('adsk.fusion.CustomGraphicsViewScale', 'create', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsViewScale) : null;
    };

    //=========== LineStylePatterns ============
    // Specifies the line styles that can be applied to custom graphics lines and curves.
    adsk.fusion.LineStylePatterns = {
        continuousLineStylePattern : 0,
        centerLineStylePattern : 1,
        dashedLineStylePattern : 2,
        dotLineStylePattern : 3,
        hiddenLineStylePattern : 4,
        phantomLineStylePattern : 5,
        tracksLineStylePattern : 6,
        zigzagLineStylePattern : 7
    };

    //=========== ViewCorners ============
    // Specifies which of the four view corners custom graphics will be drawn in relation to. The
    // notUsedViewCorner setting indicates the graphics are not positioned with respect to the view.
    adsk.fusion.ViewCorners = {
        upperLeftViewCorner : 0,
        upperRightViewCorner : 1,
        lowerLeftViewCorner : 2,
        lowerRightViewCorner : 3
    };

    //=========== CustomGraphicsAppearanceColorEffect ============
    // One of the types of color effects that can be applied to a custom graphics entity. With this
    // type of effect, the graphics entity will display using a Fusion appearance.
    adsk.fusion.CustomGraphicsAppearanceColorEffect = function CustomGraphicsAppearanceColorEffect(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsAppearanceColorEffect)) {
            return adsk.fusion.CustomGraphicsAppearanceColorEffect.cast(handle);
        }
        adsk.fusion.CustomGraphicsColorEffect.call(this, handle);
    };
    adsk.fusion.CustomGraphicsAppearanceColorEffect.prototype = Object.create(adsk.fusion.CustomGraphicsColorEffect.prototype);
    adsk.fusion.CustomGraphicsAppearanceColorEffect.prototype.constructor = adsk.fusion.CustomGraphicsAppearanceColorEffect;
    adsk.fusion.CustomGraphicsAppearanceColorEffect.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsAppearanceColorEffect';
    };
    adsk.fusion.CustomGraphicsAppearanceColorEffect.interfaceId = 'adsk.fusion.CustomGraphicsAppearanceColorEffect';
    adsk.objectTypes['adsk.fusion.CustomGraphicsAppearanceColorEffect'] = adsk.fusion.CustomGraphicsAppearanceColorEffect;
    adsk.fusion.CustomGraphicsAppearanceColorEffect.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsAppearanceColorEffect ? object : null;
    };

    // Gets and sets the appearance to use. The appearance assigned must be available in the
    // design where the graphics will be drawn.
    Object.defineProperty(adsk.fusion.CustomGraphicsAppearanceColorEffect.prototype, 'appearance', {
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

    // Statically creates a new CustomGraphicsAppearanceColorEffect object. This can be used when
    // setting the color property of the various custom graphics objects. With this coloring
    // effect, an existing appearance is used. The appearance must be avaialable in the
    // design where the graphics will be drawn.
    // appearance : The appearance to use. The appearance must be avaialable in the design where the
    // graphics will be drawn.
    // Returns the created CustomGraphicsAppearanceColorEffect or null in case of a failure.
    adsk.fusion.CustomGraphicsAppearanceColorEffect.create = function (appearance) {
        if (appearance !== null && !(appearance instanceof adsk.core.Appearance)) { throw new TypeError('appearance must be a adsk.core.Appearance'); }
        var args = {
            appearance : (appearance === null ? appearance : appearance.handle)
        };
        var result = adsk.core.Base._executeStatic('adsk.fusion.CustomGraphicsAppearanceColorEffect', 'create', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsAppearanceColorEffect) : null;
    };

    //=========== CustomGraphicsBasicMaterialColorEffect ============
    // One of the types of color effects that can be applied to a custom graphics entity. With this type
    // of effect, basic phong shading and lighting techniques are used so give the entity a 3-dimensional
    // appearance.
    adsk.fusion.CustomGraphicsBasicMaterialColorEffect = function CustomGraphicsBasicMaterialColorEffect(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsBasicMaterialColorEffect)) {
            return adsk.fusion.CustomGraphicsBasicMaterialColorEffect.cast(handle);
        }
        adsk.fusion.CustomGraphicsColorEffect.call(this, handle);
    };
    adsk.fusion.CustomGraphicsBasicMaterialColorEffect.prototype = Object.create(adsk.fusion.CustomGraphicsColorEffect.prototype);
    adsk.fusion.CustomGraphicsBasicMaterialColorEffect.prototype.constructor = adsk.fusion.CustomGraphicsBasicMaterialColorEffect;
    adsk.fusion.CustomGraphicsBasicMaterialColorEffect.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsBasicMaterialColorEffect';
    };
    adsk.fusion.CustomGraphicsBasicMaterialColorEffect.interfaceId = 'adsk.fusion.CustomGraphicsBasicMaterialColorEffect';
    adsk.objectTypes['adsk.fusion.CustomGraphicsBasicMaterialColorEffect'] = adsk.fusion.CustomGraphicsBasicMaterialColorEffect;
    adsk.fusion.CustomGraphicsBasicMaterialColorEffect.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsBasicMaterialColorEffect ? object : null;
    };

    // Gets and sets the emissiveColor associated with this CustomGraphicsBasicMaterialColorEffect object.
    // The emissive color is the primary color of the entity
    Object.defineProperty(adsk.fusion.CustomGraphicsBasicMaterialColorEffect.prototype, 'emissiveColor', {
        get : function () {
            var result = this._execute('emissiveColor');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Color) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Color)) { throw new TypeError('value must be a adsk.core.Color'); }
            var args = {
                value : value
            };
            var result = this._execute('emissiveColor', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the ambientColor associated with this CustomGraphicsBasicMaterialColorEffect object.
    // The ambient color is the color of the light anywhere there's not a specific light source.
    Object.defineProperty(adsk.fusion.CustomGraphicsBasicMaterialColorEffect.prototype, 'ambientColor', {
        get : function () {
            var result = this._execute('ambientColor');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Color) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Color)) { throw new TypeError('value must be a adsk.core.Color'); }
            var args = {
                value : value
            };
            var result = this._execute('ambientColor', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the diffuseColor associated with this CustomGraphicsBasicMaterialColorEffect object.
    // The diffuse color is the color of reflected light as it scatters off of a rough surface.
    Object.defineProperty(adsk.fusion.CustomGraphicsBasicMaterialColorEffect.prototype, 'diffuseColor', {
        get : function () {
            var result = this._execute('diffuseColor');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Color) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Color)) { throw new TypeError('value must be a adsk.core.Color'); }
            var args = {
                value : value
            };
            var result = this._execute('diffuseColor', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the specularColor associated with this CustomGraphicsBasicMaterialColorEffect object.
    // The specular color is the color of reflected light (highlights) as it is reflected off of a shiny surface. This is
    // commonly white or a lighter shade of the emissive color.
    Object.defineProperty(adsk.fusion.CustomGraphicsBasicMaterialColorEffect.prototype, 'specularColor', {
        get : function () {
            var result = this._execute('specularColor');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Color) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Color)) { throw new TypeError('value must be a adsk.core.Color'); }
            var args = {
                value : value
            };
            var result = this._execute('specularColor', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the glossiness associated with this CustomGraphicsBasicMaterialColorEffect object.
    // The glossiness determines the size of highlights, and thus the apparent shininess of the material.
    // A value of 0.0 will result in very large hightlights like you would see with a rough surface.
    // A maximum valaue of 128.0 will result in very small highlight as from a smooth surface.
    Object.defineProperty(adsk.fusion.CustomGraphicsBasicMaterialColorEffect.prototype, 'glossiness', {
        get : function () {
            var result = this._execute('glossiness');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('glossiness', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the opacity associated with this CustomGraphicsBasicMaterialColorEffect object.
    // A value of 1.0 is completely opaque and 0.0 is completely transparent.
    Object.defineProperty(adsk.fusion.CustomGraphicsBasicMaterialColorEffect.prototype, 'opacity', {
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

    // Statically creates a new basic CustomGraphicsBasicMaterialColorEffect object. This can be used to
    // color custom graphics entities. With this type of effect you define the basic phong shading
    // properties so that the entity can be rendered with basic shading and lighting effects applied
    // so that it appears 3-dimensional.
    // If only the emmissive coloris provided, the API will automatically create values for the
    // other colors to render the object as a single color.
    // diffuseColor : The diffuse color is the color of reflected light as it scatters off of a rough surface and is
    // the primary color of the entity. This color is always required.
    // ambientColor : The ambient color is the color of the light anywhere there's not a specific light source. If
    // not specified the same color as the diffuse color is used.
    // specularColor : The specular color is the color of reflected light (highlights) as it is reflected off of a shiny surface. This is
    // commonly white or a lighter shade of the diffuse color. If not specified, white is used.
    // emissiveColor : The emissive color is the color of light that entity emits, such as in a light bulb. If not specified,
    // black for no emissive light is used.
    // glossiness : This specifies how glossy the entity is. The glossiness determines the size of highlights, and thus
    // the apparent shininess of the material. A value of 0.0 will result in very large hightlights like you
    // would see with a rough surface. A maximum valaue of 128.0 will result in very small highlight as
    // from a smooth surface.
    // opacity : Specifies the opacity of the entity where a value of 1.0 is completely opaque and 0.0 is completely transparent.
    // Returns the created CustomGraphicsBasicMaterialColorEffect or null in case of a failure.
    adsk.fusion.CustomGraphicsBasicMaterialColorEffect.create = function (diffuseColor, ambientColor, specularColor, emissiveColor, glossiness, opacity) {
        if (diffuseColor !== null && !(diffuseColor instanceof adsk.core.Color)) { throw new TypeError('diffuseColor must be a adsk.core.Color'); }
        if (ambientColor === null || (ambientColor !== undefined && ambientColor !== null && !(ambientColor instanceof adsk.core.Color))) { throw new TypeError('ambientColor must be a adsk.core.Color'); }
        if (specularColor === null || (specularColor !== undefined && specularColor !== null && !(specularColor instanceof adsk.core.Color))) { throw new TypeError('specularColor must be a adsk.core.Color'); }
        if (emissiveColor === null || (emissiveColor !== undefined && emissiveColor !== null && !(emissiveColor instanceof adsk.core.Color))) { throw new TypeError('emissiveColor must be a adsk.core.Color'); }
        if (glossiness === null || (glossiness !== undefined && !isFinite(glossiness))) { throw new TypeError('glossiness must be a number'); }
        if (opacity === null || (opacity !== undefined && !isFinite(opacity))) { throw new TypeError('opacity must be a number'); }
        var args = {
            diffuseColor : (diffuseColor === null ? diffuseColor : diffuseColor.handle)
        };
        if (ambientColor !== undefined) {
            args.ambientColor = (ambientColor === null ? ambientColor : ambientColor.handle);
        }
        if (specularColor !== undefined) {
            args.specularColor = (specularColor === null ? specularColor : specularColor.handle);
        }
        if (emissiveColor !== undefined) {
            args.emissiveColor = (emissiveColor === null ? emissiveColor : emissiveColor.handle);
        }
        if (glossiness !== undefined) {
            args.glossiness = Number(glossiness);
        }
        if (opacity !== undefined) {
            args.opacity = Number(opacity);
        }
        var result = adsk.core.Base._executeStatic('adsk.fusion.CustomGraphicsBasicMaterialColorEffect', 'create', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsBasicMaterialColorEffect) : null;
    };

    //=========== CustomGraphicsBRepBody ============
    // This represents custom graphics that are based on a BRepBody.
    adsk.fusion.CustomGraphicsBRepBody = function CustomGraphicsBRepBody(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsBRepBody)) {
            return adsk.fusion.CustomGraphicsBRepBody.cast(handle);
        }
        adsk.fusion.CustomGraphicsEntity.call(this, handle);
    };
    adsk.fusion.CustomGraphicsBRepBody.prototype = Object.create(adsk.fusion.CustomGraphicsEntity.prototype);
    adsk.fusion.CustomGraphicsBRepBody.prototype.constructor = adsk.fusion.CustomGraphicsBRepBody;
    adsk.fusion.CustomGraphicsBRepBody.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsBRepBody';
    };
    adsk.fusion.CustomGraphicsBRepBody.interfaceId = 'adsk.fusion.CustomGraphicsBRepBody';
    adsk.objectTypes['adsk.fusion.CustomGraphicsBRepBody'] = adsk.fusion.CustomGraphicsBRepBody;
    adsk.fusion.CustomGraphicsBRepBody.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsBRepBody ? object : null;
    };

    // Returns the collection of CustomGraphicsBRepFace objects in the CustomGraphicsBRepBody.
    Object.defineProperty(adsk.fusion.CustomGraphicsBRepBody.prototype, 'faces', {
        get : function () {
            var result = this._execute('faces');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsBRepFaces) : null;
        }
    });

    // Returns the collection of CustomGraphicsBRepEdge objects in the CustomGraphicsBRepBody.
    Object.defineProperty(adsk.fusion.CustomGraphicsBRepBody.prototype, 'edges', {
        get : function () {
            var result = this._execute('edges');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsBRepEdges) : null;
        }
    });

    // Returns the collection of CustomGraphicsBRepVertex objects in the CustomGraphicsBRepBody.
    Object.defineProperty(adsk.fusion.CustomGraphicsBRepBody.prototype, 'vertices', {
        get : function () {
            var result = this._execute('vertices');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsBRepVertices) : null;
        }
    });

    // Returns a transient BRepBody that is being displayed as custom graphics.
    Object.defineProperty(adsk.fusion.CustomGraphicsBRepBody.prototype, 'bRepBody', {
        get : function () {
            var result = this._execute('bRepBody');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.BRepBody) : null;
        }
    });

    //=========== CustomGraphicsCurve ============
    // This represents custom graphics that are based on any object derived from Curve3D (except InfiniteLine3D).
    // This is useful when drawing curved geometry where the alternative is to stroke the smooth curve and draw
    // it as a series of lines. Using this you can directly use the curve and Fusion 360 will automatically take care
    // of creating the correct display for the current level of detail.
    adsk.fusion.CustomGraphicsCurve = function CustomGraphicsCurve(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsCurve)) {
            return adsk.fusion.CustomGraphicsCurve.cast(handle);
        }
        adsk.fusion.CustomGraphicsEntity.call(this, handle);
    };
    adsk.fusion.CustomGraphicsCurve.prototype = Object.create(adsk.fusion.CustomGraphicsEntity.prototype);
    adsk.fusion.CustomGraphicsCurve.prototype.constructor = adsk.fusion.CustomGraphicsCurve;
    adsk.fusion.CustomGraphicsCurve.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsCurve';
    };
    adsk.fusion.CustomGraphicsCurve.interfaceId = 'adsk.fusion.CustomGraphicsCurve';
    adsk.objectTypes['adsk.fusion.CustomGraphicsCurve'] = adsk.fusion.CustomGraphicsCurve;
    adsk.fusion.CustomGraphicsCurve.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsCurve ? object : null;
    };

    // Gets and sets the curve associated with this graphics entity. Any of the curve types derived from Curve3D
    // is valid except for InfiniteLine3D.
    Object.defineProperty(adsk.fusion.CustomGraphicsCurve.prototype, 'curve', {
        get : function () {
            var result = this._execute('curve');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Curve3D) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Curve3D)) { throw new TypeError('value must be a adsk.core.Curve3D'); }
            var args = {
                value : value
            };
            var result = this._execute('curve', args);
            return result ? result.value : undefined;
        }
    });

    // Defines the thickness of the curve in pixels.
    Object.defineProperty(adsk.fusion.CustomGraphicsCurve.prototype, 'weight', {
        get : function () {
            var result = this._execute('weight');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('weight', args);
            return result ? result.value : undefined;
        }
    });

    //=========== CustomGraphicsGroup ============
    // Represents of group of custom graphics entities. A group can also own other graphics groups.
    adsk.fusion.CustomGraphicsGroup = function CustomGraphicsGroup(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsGroup)) {
            return adsk.fusion.CustomGraphicsGroup.cast(handle);
        }
        adsk.fusion.CustomGraphicsEntity.call(this, handle);
    };
    adsk.fusion.CustomGraphicsGroup.prototype = Object.create(adsk.fusion.CustomGraphicsEntity.prototype);
    adsk.fusion.CustomGraphicsGroup.prototype.constructor = adsk.fusion.CustomGraphicsGroup;
    adsk.fusion.CustomGraphicsGroup.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsGroup';
    };
    adsk.fusion.CustomGraphicsGroup.interfaceId = 'adsk.fusion.CustomGraphicsGroup';
    adsk.objectTypes['adsk.fusion.CustomGraphicsGroup'] = adsk.fusion.CustomGraphicsGroup;
    adsk.fusion.CustomGraphicsGroup.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsGroup ? object : null;
    };

    // Returns the number of graphics entities within the group.
    Object.defineProperty(adsk.fusion.CustomGraphicsGroup.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified custom graphics entity within this group. This also includes
    // any child graphics groups.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.CustomGraphicsGroup.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsEntity) : null;
    };

    // Creates a new, empty CustomGraphicsGroup that is owned by this CustomGraphicsGroup.
    // Returns the new CustomGraphicsGroup object or null in the case of a failure.
    adsk.fusion.CustomGraphicsGroup.prototype.addGroup = function () {
        var result = this._execute('addGroup');
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsGroup) : null;
    };

    // Adds a new CustomGraphicsMesh entity to this group.
    // coordinates : The CustomGraphicsCoordinates object that defines the coordinates of the vertices of the mesh.
    // A CustomGrahpicsCoordinates object can be created using the static create method of the CustomGraphicsCoordinates class.
    // coordinateIndexList : An array of integers that represent indices into the coordinates to define the vertices of the triangles. If an empty
    // array is provided, then it's assumed that the first three coordinates defines the first triangle, the next three define
    // the second triangle, and so on.
    // normalVectors : An array of doubles that represent the x, y, z components of the normals at each coordinate. There should be a normal defined
    // for each coordinate. If an empty array is provided for the normal vectors, Fusion 360 will automatically calculate normal vectors
    // that are 90 degrees to the face of the triangle, making it appear flat.
    // normalIndexList : An array of integers that represent indices into the normal vectors to define the which vector corresponds to which vertex. This
    // should be the same size as the vertex index list. If an empty array is input and normal vectors are provided, it is assumed that
    // the normals match up one-to-one to each coordinate.
    // Returns the new CustomGraphicsMesh object or null in the case of a failure.
    adsk.fusion.CustomGraphicsGroup.prototype.addMesh = function (coordinates, coordinateIndexList, normalVectors, normalIndexList) {
        if (coordinates !== null && !(coordinates instanceof adsk.fusion.CustomGraphicsCoordinates)) { throw new TypeError('coordinates must be a adsk.fusion.CustomGraphicsCoordinates'); }
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
            coordinates : (coordinates === null ? coordinates : coordinates.handle),
            coordinateIndexList : coordinateIndexList,
            normalVectors : normalVectors,
            normalIndexList : normalIndexList
        };
        var result = this._execute('addMesh', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsMesh) : null;
    };

    // Adds a new CustomGraphicsLines entity to this group.
    // coordinates : The CustomGraphicsCoordinates object that defines the coordinates of the vertices of the lines.
    // A CustomGraphicsCoordinates object can be created using the static create method of the CustomGraphicsCoordinates class.
    // indexList : An array of integers that represent indices into the coordinates to define the order the coordinates are used to draw the lines.
    // If an empty array is provided, the coordinates are used in the order they're provided in the provided CustomGraphicsCoordinates object.
    // isLineStrip : A boolean indicating if a series of individual lines or a connected set of lines (a line strip) is to be drawn. If individual lines
    // are drawn, (this argument is false), each pair of coordinates defines a single line. If a line strip is drawn, (this argument is true),
    // the first pair of coordinates define the first line and the third coordinate defines a line that connects to the second coordinate.
    // The fourth coordinate creates a line connecting to the third coordinate, and so on.
    // lineStripLengths : If isLineStrip is true, this argument is used to define the number of coordinates to use in each line strip. It is an array of integers
    // that defines the number of coordinates for each line strip. For example, if the array [4,10] is input, 4 coordinates are connected for
    // the first line strip and 10 are used to create a second line strip. If an empty array is provided, a single line strip is created. If
    // isLineStrip is False, this argument is ignored.
    // Returns the new CustomGraphicsLines object or null in the case of a failure.
    adsk.fusion.CustomGraphicsGroup.prototype.addLines = function (coordinates, indexList, isLineStrip, lineStripLengths) {
        if (coordinates !== null && !(coordinates instanceof adsk.fusion.CustomGraphicsCoordinates)) { throw new TypeError('coordinates must be a adsk.fusion.CustomGraphicsCoordinates'); }
        if (!Array.isArray(indexList)) { throw new TypeError('indexList must be an array'); }
        var indexListLength = indexList.length;
        var indexListIt;
        for (indexListIt = 0; indexListIt < indexListLength; ++indexListIt) {
            if (!isFinite(indexList[indexListIt])) { throw new TypeError('indexList[indexListIt] must be a number'); }
        }
        if (typeof isLineStrip !== 'boolean') { throw new TypeError('isLineStrip must be a boolean'); }
        if (lineStripLengths) {
            if (!Array.isArray(lineStripLengths)) { throw new TypeError('lineStripLengths must be an array'); }
            var lineStripLengthsLength = lineStripLengths.length;
            var lineStripLengthsIt;
            for (lineStripLengthsIt = 0; lineStripLengthsIt < lineStripLengthsLength; ++lineStripLengthsIt) {
                if (!isFinite(lineStripLengths[lineStripLengthsIt])) { throw new TypeError('lineStripLengths[lineStripLengthsIt] must be a number'); }
            }
        }
        var args = {
            coordinates : (coordinates === null ? coordinates : coordinates.handle),
            indexList : indexList,
            isLineStrip : isLineStrip
        };
        if (lineStripLengths !== undefined) {
            args.lineStripLengths = lineStripLengths;
        }
        var result = this._execute('addLines', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsLines) : null;
    };

    // Adds a new CustomGraphicsCurve entity to this group. A CustomGraphicsCurve is a wireframe graphic
    // that is based on any object derived from Curve3D (except InfiniteLine3D). This is useful when
    // drawing curved geometry where the alternative is to stroke the smooth curve and draw it as a series
    // of lines. Using this you can directly use the curve and Fusion 360 will automatically take care of creating
    // the correct display for the current level of detail.
    // curve : The curve that defines the shape of the graphics entity. Any of the curve types derived from Curve3D
    // are valid except for InfiniteLine3D.
    // Returns the newly created CustomGraphicsCurve object or null in the case of failure.
    adsk.fusion.CustomGraphicsGroup.prototype.addCurve = function (curve) {
        if (curve !== null && !(curve instanceof adsk.core.Curve3D)) { throw new TypeError('curve must be a adsk.core.Curve3D'); }
        var args = {
            curve : (curve === null ? curve : curve.handle)
        };
        var result = this._execute('addCurve', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsCurve) : null;
    };

    // Adds a new CustomGraphicsPointSet entity to this group. This will be displayed as one or more points where
    // all of the points will display using the same image.
    // coordinates : The CustomGraphicsCoordinates object that defines the coordinates where the points will be displayed.
    // A CustomGraphicsCoordinates object can be created using the static create method of the CustomGraphicsCoordinates class.
    // indexList : An array of integers that represent indices into the coordinates to define which coordinates to use when drawing points.
    // If an empty array is provided, a point is drawn for every coordinate.
    // pointType : Specifies the type of point to display. Currently there are two choices; UserDefinedCustomGraphicsPointType and
    // PointCloudCustomGraphicsPointType. When set to PointCloudCustomGraphicsPointType, each point displays as a single pixel and is
    // the most efficient point display type for displaying sets that contain very large quantities of points. When
    // set to UserDefinedCustomGraphicsPointType, you specify the image to display as the point. This can be any png image and is
    // centered on the point.
    // pointImage : If the pointType is PointCloudCustomGraphicsPointType this argument is ignored and can be an empty string. This argument
    // must be specified if the pointType is UserDefinedCustomGraphicsPointType. This is the path to the png image file that will be
    // displayed as the point. It can be either a full path to the file or a relative path that is respect to the .py, dll, or dylib
    // file being run. There is no restriction on the size of the image, but generally very small images would be used for points.
    // Returns the newly created CustomGraphicsPointSet object or null in the case of failure.
    adsk.fusion.CustomGraphicsGroup.prototype.addPointSet = function (coordinates, indexList, pointType, pointImage) {
        if (coordinates !== null && !(coordinates instanceof adsk.fusion.CustomGraphicsCoordinates)) { throw new TypeError('coordinates must be a adsk.fusion.CustomGraphicsCoordinates'); }
        if (!Array.isArray(indexList)) { throw new TypeError('indexList must be an array'); }
        var indexListLength = indexList.length;
        var indexListIt;
        for (indexListIt = 0; indexListIt < indexListLength; ++indexListIt) {
            if (!isFinite(indexList[indexListIt])) { throw new TypeError('indexList[indexListIt] must be a number'); }
        }
        if (!isFinite(pointType)) { throw new TypeError('pointType must be a number'); }
        if (pointImage === undefined || pointImage === null || pointImage.constructor !== String) { throw new TypeError('pointImage must be a string'); }
        var args = {
            coordinates : (coordinates === null ? coordinates : coordinates.handle),
            indexList : indexList,
            pointType : Number(pointType),
            pointImage : pointImage
        };
        var result = this._execute('addPointSet', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsPointSet) : null;
    };

    // Adds a new CustomGraphicsText entity to this group. This will be displayed as a single line of text.
    // It is placed so that the upper-left corner is at the point defined and the text will be parallel
    // to the X-Y plane of the world coordinate system and in the X direction. To change it's position relative
    // to the input point you can change the horizontal and vertical justification on the returnsed CustomGrahicsText
    // object. You can also reorient the text by changing the transform of the returned CustomGraphicsText object.
    // formattedText : The text string to be displayed. Overall formatting can be defined using properties on the returned
    // CustomGraphicsText object. Formatting overrides can be defined within the string using formatting codes.
    // font : The name of the font to use when displaying the text.
    // size : The size of the text in centimeters.
    // transform : Transformation matrix that specifies the position and orientation of the text in model space.
    // Returns the newly created CustomGraphicsText object or null in the case of failure.
    adsk.fusion.CustomGraphicsGroup.prototype.addText = function (formattedText, font, size, transform) {
        if (formattedText === undefined || formattedText === null || formattedText.constructor !== String) { throw new TypeError('formattedText must be a string'); }
        if (font === undefined || font === null || font.constructor !== String) { throw new TypeError('font must be a string'); }
        if (!isFinite(size)) { throw new TypeError('size must be a number'); }
        if (transform !== null && !(transform instanceof adsk.core.Matrix3D)) { throw new TypeError('transform must be a adsk.core.Matrix3D'); }
        var args = {
            formattedText : formattedText,
            font : font,
            size : Number(size),
            transform : (transform === null ? transform : transform.handle)
        };
        var result = this._execute('addText', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsText) : null;
    };

    // Adds a new CustomGraphicsBRepBody object to this group. This displays a real or transient BRepBody
    // object as custom graphics. No relationship exists back to the original input body so if it is
    // changed, the custom graphics will not change.
    // The body associated with the CustomGraphicsBRep body is a copy of the original input body. Equivalent
    // Faces, Edges, and vertices can be found by using the indexes in the collection. For example if you have
    // a face of the original body and find that it is at index 24 in the BRepFaces collection of that body,
    // the equivalent face in the custom graphics body will also be at index 24. This works as long as the original
    // body is not modified in any way.
    // body : The real or transient BRepBody object to draw using custom graphics.
    // Returns the newly created CustomGraphicsBRepBody object or null in the case of failure.
    adsk.fusion.CustomGraphicsGroup.prototype.addBRepBody = function (body) {
        if (body !== null && !(body instanceof adsk.fusion.BRepBody)) { throw new TypeError('body must be a adsk.fusion.BRepBody'); }
        var args = {
            body : (body === null ? body : body.handle)
        };
        var result = this._execute('addBRepBody', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsBRepBody) : null;
    };

    //=========== CustomGraphicsLines ============
    // Represents lines drawn in the graphics window.
    adsk.fusion.CustomGraphicsLines = function CustomGraphicsLines(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsLines)) {
            return adsk.fusion.CustomGraphicsLines.cast(handle);
        }
        adsk.fusion.CustomGraphicsEntity.call(this, handle);
    };
    adsk.fusion.CustomGraphicsLines.prototype = Object.create(adsk.fusion.CustomGraphicsEntity.prototype);
    adsk.fusion.CustomGraphicsLines.prototype.constructor = adsk.fusion.CustomGraphicsLines;
    adsk.fusion.CustomGraphicsLines.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsLines';
    };
    adsk.fusion.CustomGraphicsLines.interfaceId = 'adsk.fusion.CustomGraphicsLines';
    adsk.objectTypes['adsk.fusion.CustomGraphicsLines'] = adsk.fusion.CustomGraphicsLines;
    adsk.fusion.CustomGraphicsLines.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsLines ? object : null;
    };

    // Gets and sets the CustomGraphicsCoordinates object that defines the coordinates of the vertices of the lines.
    // A CustomGraphicsCoordinates object can be created using the static create method of the CustomGraphicsCoordinates class.
    Object.defineProperty(adsk.fusion.CustomGraphicsLines.prototype, 'coordinates', {
        get : function () {
            var result = this._execute('coordinates');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsCoordinates) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.fusion.CustomGraphicsCoordinates)) { throw new TypeError('value must be a adsk.fusion.CustomGraphicsCoordinates'); }
            var args = {
                value : value
            };
            var result = this._execute('coordinates', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets an array of integers that represent indices into the coordinates to define the order the coordinates are used to draw the lines.
    // An empty array indicates that no index list is used and coordinates are used in the order they're provided in the provided CustomGraphicsCoordinates object.
    Object.defineProperty(adsk.fusion.CustomGraphicsLines.prototype, 'indexList', {
        get : function () {
            var result = this._execute('indexList');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!Array.isArray(value)) { throw new TypeError('value must be an array'); }
            var valueLength = value.length;
            var valueIt;
            for (valueIt = 0; valueIt < valueLength; ++valueIt) {
                if (!isFinite(value[valueIt])) { throw new TypeError('value[valueIt] must be a number'); }
            }
            var args = {
                value : value
            };
            var result = this._execute('indexList', args);
            return result ? result.value : undefined;
        }
    });

    // Defines if the coordinates are used to define a series of individual lines or a connected set of lines (line strip). If individual lines
    // are drawn (this property is false), each pair of coordinates define a single line. If a line strip is drawn (this property is true),
    // the first pair of coordinates define the first line and the third coordinate defines a line that connects to the second coordinate.
    // The fourth coordinate creates a line connecting to the third coordinate, and so on.
    Object.defineProperty(adsk.fusion.CustomGraphicsLines.prototype, 'isLineStrip', {
        get : function () {
            var result = this._execute('isLineStrip');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isLineStrip', args);
            return result ? result.value : undefined;
        }
    });

    // If isLineStrip is true, this property defines the number of coordinates to use in the line strips. It is an array of integers
    // that defines the number of coordinates for each line strip. An empty array indicates that a single line strip is to be drawn.
    Object.defineProperty(adsk.fusion.CustomGraphicsLines.prototype, 'lineStripLengths', {
        get : function () {
            var result = this._execute('lineStripLengths');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!Array.isArray(value)) { throw new TypeError('value must be an array'); }
            var valueLength = value.length;
            var valueIt;
            for (valueIt = 0; valueIt < valueLength; ++valueIt) {
                if (!isFinite(value[valueIt])) { throw new TypeError('value[valueIt] must be a number'); }
            }
            var args = {
                value : value
            };
            var result = this._execute('lineStripLengths', args);
            return result ? result.value : undefined;
        }
    });

    // Defines the thickness of the line in pixels.
    Object.defineProperty(adsk.fusion.CustomGraphicsLines.prototype, 'weight', {
        get : function () {
            var result = this._execute('weight');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('weight', args);
            return result ? result.value : undefined;
        }
    });

    // Defines the scale as it relates to how the line style is applied. The effect is to
    // shrink or expand the line style as it is applied to the line. This does not affect the line width.
    Object.defineProperty(adsk.fusion.CustomGraphicsLines.prototype, 'lineStyleScale', {
        get : function () {
            var result = this._execute('lineStyleScale');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('lineStyleScale', args);
            return result ? result.value : undefined;
        }
    });

    // Specifies if the line style is computed based on the screen or model space. The default is
    // based on the screen which means the style is drawn the same regardless of how you zoom in
    // or out of the view. That is the length of lines and spaces are based on pixels. If it
    // is drawn relative to model space then the lines and spaces are defined in centimeters and
    // will zooming in and out will change the apparent spacing.
    Object.defineProperty(adsk.fusion.CustomGraphicsLines.prototype, 'isScreenSpaceLineStyle', {
        get : function () {
            var result = this._execute('isScreenSpaceLineStyle');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isScreenSpaceLineStyle', args);
            return result ? result.value : undefined;
        }
    });

    // The line style to apply to the line. The default is to draw a continuous line.
    Object.defineProperty(adsk.fusion.CustomGraphicsLines.prototype, 'lineStylePattern', {
        get : function () {
            var result = this._execute('lineStylePattern');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('lineStylePattern', args);
            return result ? result.value : undefined;
        }
    });

    //=========== CustomGraphicsMesh ============
    // Represents a custom triangle mesh drawn in the graphics window.
    adsk.fusion.CustomGraphicsMesh = function CustomGraphicsMesh(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsMesh)) {
            return adsk.fusion.CustomGraphicsMesh.cast(handle);
        }
        adsk.fusion.CustomGraphicsEntity.call(this, handle);
    };
    adsk.fusion.CustomGraphicsMesh.prototype = Object.create(adsk.fusion.CustomGraphicsEntity.prototype);
    adsk.fusion.CustomGraphicsMesh.prototype.constructor = adsk.fusion.CustomGraphicsMesh;
    adsk.fusion.CustomGraphicsMesh.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsMesh';
    };
    adsk.fusion.CustomGraphicsMesh.interfaceId = 'adsk.fusion.CustomGraphicsMesh';
    adsk.objectTypes['adsk.fusion.CustomGraphicsMesh'] = adsk.fusion.CustomGraphicsMesh;
    adsk.fusion.CustomGraphicsMesh.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsMesh ? object : null;
    };

    // Gets and sets the coordinates associated with this CustomGraphicsMesh.
    Object.defineProperty(adsk.fusion.CustomGraphicsMesh.prototype, 'coordinates', {
        get : function () {
            var result = this._execute('coordinates');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsCoordinates) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.fusion.CustomGraphicsCoordinates)) { throw new TypeError('value must be a adsk.fusion.CustomGraphicsCoordinates'); }
            var args = {
                value : value
            };
            var result = this._execute('coordinates', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the normal vectors of the mesh where there is a normal
    // vector at each node. The normals are defined as an array
    // of floats where they are the x, y, z components of each vector.
    Object.defineProperty(adsk.fusion.CustomGraphicsMesh.prototype, 'normalVectors', {
        get : function () {
            var result = this._execute('normalVectors');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!Array.isArray(value)) { throw new TypeError('value must be an array'); }
            var valueLength = value.length;
            var valueIt;
            for (valueIt = 0; valueIt < valueLength; ++valueIt) {
                if (!isFinite(value[valueIt])) { throw new TypeError('value[valueIt] must be a number'); }
            }
            var args = {
                value : value
            };
            var result = this._execute('normalVectors', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets an array of indices that define which coordinate in the
    // coordinate list is used for each vertex in the mesh. Each set of three
    // indices defines a triagle. For example:
    // Indices 0, 1, and 2 define the coordinates to use for the first triangle and
    // indices 3, 4, and 5 define the coordinates for the second triangle, and so on.
    Object.defineProperty(adsk.fusion.CustomGraphicsMesh.prototype, 'vertexIndexList', {
        get : function () {
            var result = this._execute('vertexIndexList');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!Array.isArray(value)) { throw new TypeError('value must be an array'); }
            var valueLength = value.length;
            var valueIt;
            for (valueIt = 0; valueIt < valueLength; ++valueIt) {
                if (!isFinite(value[valueIt])) { throw new TypeError('value[valueIt] must be a number'); }
            }
            var args = {
                value : value
            };
            var result = this._execute('vertexIndexList', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets an array of indices that define which normal is associated
    // with each vertex in the mesh. This is used to look-up the normal in the
    // normalVectors array.
    Object.defineProperty(adsk.fusion.CustomGraphicsMesh.prototype, 'normalIndexList', {
        get : function () {
            var result = this._execute('normalIndexList');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!Array.isArray(value)) { throw new TypeError('value must be an array'); }
            var valueLength = value.length;
            var valueIt;
            for (valueIt = 0; valueIt < valueLength; ++valueIt) {
                if (!isFinite(value[valueIt])) { throw new TypeError('value[valueIt] must be a number'); }
            }
            var args = {
                value : value
            };
            var result = this._execute('normalIndexList', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the texture coordinates as an array of floats where
    // they are the u,v components at each node. They are defined as an
    // array of doubles where they are the u, v coordinates of each node.
    // Defining texture coordinates for a mesh is optional.
    Object.defineProperty(adsk.fusion.CustomGraphicsMesh.prototype, 'textureCoordinates', {
        get : function () {
            var result = this._execute('textureCoordinates');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!Array.isArray(value)) { throw new TypeError('value must be an array'); }
            var valueLength = value.length;
            var valueIt;
            for (valueIt = 0; valueIt < valueLength; ++valueIt) {
                if (!isFinite(value[valueIt])) { throw new TypeError('value[valueIt] must be a number'); }
            }
            var args = {
                value : value
            };
            var result = this._execute('textureCoordinates', args);
            return result ? result.value : undefined;
        }
    });

    //=========== CustomGraphicsPointSet ============
    // Represents a set of one or more custom graphics points all of the same style.
    adsk.fusion.CustomGraphicsPointSet = function CustomGraphicsPointSet(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsPointSet)) {
            return adsk.fusion.CustomGraphicsPointSet.cast(handle);
        }
        adsk.fusion.CustomGraphicsEntity.call(this, handle);
    };
    adsk.fusion.CustomGraphicsPointSet.prototype = Object.create(adsk.fusion.CustomGraphicsEntity.prototype);
    adsk.fusion.CustomGraphicsPointSet.prototype.constructor = adsk.fusion.CustomGraphicsPointSet;
    adsk.fusion.CustomGraphicsPointSet.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsPointSet';
    };
    adsk.fusion.CustomGraphicsPointSet.interfaceId = 'adsk.fusion.CustomGraphicsPointSet';
    adsk.objectTypes['adsk.fusion.CustomGraphicsPointSet'] = adsk.fusion.CustomGraphicsPointSet;
    adsk.fusion.CustomGraphicsPointSet.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsPointSet ? object : null;
    };

    // Gets and sets the coordinates used to define the position of the custom graphics points.
    // If no indexList is specified, every coordinate will be drawn using a custom graphics point,
    Object.defineProperty(adsk.fusion.CustomGraphicsPointSet.prototype, 'coordinates', {
        get : function () {
            var result = this._execute('coordinates');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsCoordinates) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.fusion.CustomGraphicsCoordinates)) { throw new TypeError('value must be a adsk.fusion.CustomGraphicsCoordinates'); }
            var args = {
                value : value
            };
            var result = this._execute('coordinates', args);
            return result ? result.value : undefined;
        }
    });

    // An list of indices that specify which coordinates from the coordinate list to draw points for.
    // If this is an empty array, then all of the coordinates are used.
    Object.defineProperty(adsk.fusion.CustomGraphicsPointSet.prototype, 'indexList', {
        get : function () {
            var result = this._execute('indexList');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!Array.isArray(value)) { throw new TypeError('value must be an array'); }
            var valueLength = value.length;
            var valueIt;
            for (valueIt = 0; valueIt < valueLength; ++valueIt) {
                if (!isFinite(value[valueIt])) { throw new TypeError('value[valueIt] must be a number'); }
            }
            var args = {
                value : value
            };
            var result = this._execute('indexList', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the image that will be used to display the point if the point type
    // is a custom image. The image will always be be billboarded. The file should be
    // a png image and can use transparency. The filename can be a full path or a
    // relative path that is relative to your runtime file. Setting this will automatically
    // set the pointType to UserDefinedCustomGraphicsPointType. This property can also
    // return an empty string in the case where a user defined image point is not being used.
    Object.defineProperty(adsk.fusion.CustomGraphicsPointSet.prototype, 'pointImage', {
        get : function () {
            var result = this._execute('pointImage');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (value === undefined || value === null || value.constructor !== String) { throw new TypeError('value must be a string'); }
            var args = {
                value : value
            };
            var result = this._execute('pointImage', args);
            return result ? result.value : undefined;
        }
    });

    // Specifies which of the pre-defined point images to use. Attempting to set this property
    // to UserDefinedCustomGraphicsPointType will fail. To change to a user defined point type
    // you must set use the pointImage property to specify the image to use and this will have
    // the side-effect of changing the value of this property to UserDefinedCustomGraphicsPointType.
    Object.defineProperty(adsk.fusion.CustomGraphicsPointSet.prototype, 'pointType', {
        get : function () {
            var result = this._execute('pointType');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('pointType', args);
            return result ? result.value : undefined;
        }
    });

    //=========== CustomGraphicsSolidColorEffect ============
    // One of the types of color effects that can be applied to a custom graphics entity. With this
    // type of effect, the graphics entity will display as the single color without any lighting
    // effects. For example, a sphere will display as a solid filled circle without any shading
    // indicating it is actually spherical.
    adsk.fusion.CustomGraphicsSolidColorEffect = function CustomGraphicsSolidColorEffect(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsSolidColorEffect)) {
            return adsk.fusion.CustomGraphicsSolidColorEffect.cast(handle);
        }
        adsk.fusion.CustomGraphicsColorEffect.call(this, handle);
    };
    adsk.fusion.CustomGraphicsSolidColorEffect.prototype = Object.create(adsk.fusion.CustomGraphicsColorEffect.prototype);
    adsk.fusion.CustomGraphicsSolidColorEffect.prototype.constructor = adsk.fusion.CustomGraphicsSolidColorEffect;
    adsk.fusion.CustomGraphicsSolidColorEffect.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsSolidColorEffect';
    };
    adsk.fusion.CustomGraphicsSolidColorEffect.interfaceId = 'adsk.fusion.CustomGraphicsSolidColorEffect';
    adsk.objectTypes['adsk.fusion.CustomGraphicsSolidColorEffect'] = adsk.fusion.CustomGraphicsSolidColorEffect;
    adsk.fusion.CustomGraphicsSolidColorEffect.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsSolidColorEffect ? object : null;
    };

    // The color to use for the solid color display. The opacity component of the color is ignored
    // because the opacity of custom graphics is controlled seperately using an opacity attribute.
    Object.defineProperty(adsk.fusion.CustomGraphicsSolidColorEffect.prototype, 'color', {
        get : function () {
            var result = this._execute('color');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Color) : null;
        },
        set : function (value) {
            if (value !== null && !(value instanceof adsk.core.Color)) { throw new TypeError('value must be a adsk.core.Color'); }
            var args = {
                value : value
            };
            var result = this._execute('color', args);
            return result ? result.value : undefined;
        }
    });

    // Statically creates a new CustomGraphicsSolidColorEffect object. This can be used as input
    // when creating various color related custom graphics attributes. A solid color effect,
    // colors the entity with a single color without any lighting effects. With this coloring
    // effect, a sphere will display as a solid filled circle.
    // color : The color to use for the solid color display. The opacity component of the color is ignored
    // because the opacity of custom graphics is controlled seperately using an opacity attribute.
    // Returns the created CustomGraphicsSolidColorEffect or null in case of a failure.
    adsk.fusion.CustomGraphicsSolidColorEffect.create = function (color) {
        if (color !== null && !(color instanceof adsk.core.Color)) { throw new TypeError('color must be a adsk.core.Color'); }
        var args = {
            color : (color === null ? color : color.handle)
        };
        var result = adsk.core.Base._executeStatic('adsk.fusion.CustomGraphicsSolidColorEffect', 'create', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsSolidColorEffect) : null;
    };

    //=========== CustomGraphicsText ============
    // Represents text drawn in the graphics window. The default position of the text is at (0,0,0) and
    // orientation is the text lying on the x-y plane. To reposition and reorient the text you can use
    // the transformation property.
    adsk.fusion.CustomGraphicsText = function CustomGraphicsText(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsText)) {
            return adsk.fusion.CustomGraphicsText.cast(handle);
        }
        adsk.fusion.CustomGraphicsEntity.call(this, handle);
    };
    adsk.fusion.CustomGraphicsText.prototype = Object.create(adsk.fusion.CustomGraphicsEntity.prototype);
    adsk.fusion.CustomGraphicsText.prototype.constructor = adsk.fusion.CustomGraphicsText;
    adsk.fusion.CustomGraphicsText.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsText';
    };
    adsk.fusion.CustomGraphicsText.interfaceId = 'adsk.fusion.CustomGraphicsText';
    adsk.objectTypes['adsk.fusion.CustomGraphicsText'] = adsk.fusion.CustomGraphicsText;
    adsk.fusion.CustomGraphicsText.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsText ? object : null;
    };

    // Gets and sets the formatted text definition. This is the full string, including the
    // formatting information, that's used to define the displayed text.
    Object.defineProperty(adsk.fusion.CustomGraphicsText.prototype, 'formattedText', {
        get : function () {
            var result = this._execute('formattedText');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (value === undefined || value === null || value.constructor !== String) { throw new TypeError('value must be a string'); }
            var args = {
                value : value
            };
            var result = this._execute('formattedText', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the font used to display the text. This is the default font and applies to
    // all of text unless there is a font override defined within the text.
    Object.defineProperty(adsk.fusion.CustomGraphicsText.prototype, 'font', {
        get : function () {
            var result = this._execute('font');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (value === undefined || value === null || value.constructor !== String) { throw new TypeError('value must be a string'); }
            var args = {
                value : value
            };
            var result = this._execute('font', args);
            return result ? result.value : undefined;
        }
    });

    // Specifies that the text displays using an italic style. This is the default italic style and applies to
    // all of text unless there is a style override defined within the text.
    Object.defineProperty(adsk.fusion.CustomGraphicsText.prototype, 'isItalic', {
        get : function () {
            var result = this._execute('isItalic');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isItalic', args);
            return result ? result.value : undefined;
        }
    });

    // Specifies that the text displays using a bold style. This is the default bold style and applies to
    // all of text unless there is a style override defined within the text.
    Object.defineProperty(adsk.fusion.CustomGraphicsText.prototype, 'isBold', {
        get : function () {
            var result = this._execute('isBold');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isBold', args);
            return result ? result.value : undefined;
        }
    });

    // Specifies that the text displays using an underline style. This is the default underline style and applies to
    // all of text unless there is a style override defined within the text.
    Object.defineProperty(adsk.fusion.CustomGraphicsText.prototype, 'isUnderline', {
        get : function () {
            var result = this._execute('isUnderline');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isUnderline', args);
            return result ? result.value : undefined;
        }
    });

    // Specifies that the text displays using a strike through style. This is the default strike through style and applies to
    // all of text unless there is a style override defined within the text.
    Object.defineProperty(adsk.fusion.CustomGraphicsText.prototype, 'isStrikeThrough', {
        get : function () {
            var result = this._execute('isStrikeThrough');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isStrikeThrough', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the size of the text in centimeters. This is the default size and applies to
    // all of text unless there is a size override defined within the text.
    Object.defineProperty(adsk.fusion.CustomGraphicsText.prototype, 'size', {
        get : function () {
            var result = this._execute('size');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (!isFinite(value)) { throw new TypeError('value must be a number'); }
            var args = {
                value : Number(value)
            };
            var result = this._execute('size', args);
            return result ? result.value : undefined;
        }
    });

    // The actual width of the text in centimeters. This is useful when you want to position several
    // GraphicsText objects together.
    Object.defineProperty(adsk.fusion.CustomGraphicsText.prototype, 'width', {
        get : function () {
            var result = this._execute('width');
            return result ? result.value : undefined;
        }
    });

    // The actual height of the text in centimeters. This is useful when you want to position several
    // GraphicsText objects together.
    Object.defineProperty(adsk.fusion.CustomGraphicsText.prototype, 'height', {
        get : function () {
            var result = this._execute('height');
            return result ? result.value : undefined;
        }
    });

    //=========== CustomGraphicsVertexColorEffect ============
    // One of the types of color effects that can be applied to a custom graphics entity. With this
    // type of effect, the graphics entity will display using the colors associated with the vertices
    // of the mesh in the CustomGraphicsCoordinates object.
    adsk.fusion.CustomGraphicsVertexColorEffect = function CustomGraphicsVertexColorEffect(handle) {
        if (!(this instanceof adsk.fusion.CustomGraphicsVertexColorEffect)) {
            return adsk.fusion.CustomGraphicsVertexColorEffect.cast(handle);
        }
        adsk.fusion.CustomGraphicsColorEffect.call(this, handle);
    };
    adsk.fusion.CustomGraphicsVertexColorEffect.prototype = Object.create(adsk.fusion.CustomGraphicsColorEffect.prototype);
    adsk.fusion.CustomGraphicsVertexColorEffect.prototype.constructor = adsk.fusion.CustomGraphicsVertexColorEffect;
    adsk.fusion.CustomGraphicsVertexColorEffect.classType = function classType () {
        return 'adsk::fusion::CustomGraphicsVertexColorEffect';
    };
    adsk.fusion.CustomGraphicsVertexColorEffect.interfaceId = 'adsk.fusion.CustomGraphicsVertexColorEffect';
    adsk.objectTypes['adsk.fusion.CustomGraphicsVertexColorEffect'] = adsk.fusion.CustomGraphicsVertexColorEffect;
    adsk.fusion.CustomGraphicsVertexColorEffect.cast = function (object) {
        return object instanceof adsk.fusion.CustomGraphicsVertexColorEffect ? object : null;
    };

    // Statically creates a new CustomGraphicsVertexColorEffect object.
    // Returns the created CustomGraphicsVertexColorEffect or null in case of a failure.
    adsk.fusion.CustomGraphicsVertexColorEffect.create = function () {
        var result = adsk.core.Base._executeStatic('adsk.fusion.CustomGraphicsVertexColorEffect', 'create');
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.CustomGraphicsVertexColorEffect) : null;
    };

    return adsk;
}));