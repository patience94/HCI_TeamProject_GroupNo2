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

    //=========== TSplineBodies ============
    // A collection of TSpline bodies.
    adsk.fusion.TSplineBodies = function TSplineBodies(handle) {
        if (!(this instanceof adsk.fusion.TSplineBodies)) {
            return adsk.fusion.TSplineBodies.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.TSplineBodies.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.TSplineBodies.prototype.constructor = adsk.fusion.TSplineBodies;
    adsk.fusion.TSplineBodies.classType = function classType () {
        return 'adsk::fusion::TSplineBodies';
    };
    adsk.fusion.TSplineBodies.interfaceId = 'adsk.fusion.TSplineBodies';
    adsk.objectTypes['adsk.fusion.TSplineBodies'] = adsk.fusion.TSplineBodies;
    adsk.fusion.TSplineBodies.cast = function (object) {
        return object instanceof adsk.fusion.TSplineBodies ? object : null;
    };

    // The number of bodies in the collection.
    Object.defineProperty(adsk.fusion.TSplineBodies.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified T-Spline body using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.fusion.TSplineBodies.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.TSplineBody) : null;
    };

    // Returns a TSplineBody by specifying the name of the body as seen in the browser.
    // name : The name of the body, as seen in the browser. This is case sensitive.
    // Returns the specified item or null if a body with that name was not found.
    adsk.fusion.TSplineBodies.prototype.itemByName = function (name) {
        if (name === undefined || name === null || name.constructor !== String) { throw new TypeError('name must be a string'); }
        var args = {
            name : name
        };
        var result = this._execute('itemByName', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.TSplineBody) : null;
    };

    // Creates a new TSplineBody by reading in a TSM file from disk.
    // tsmFilename : The full filename of the TSM file on disk.
    // Returns the newly created TSplineBody if successful or null in the case of failure.
    adsk.fusion.TSplineBodies.prototype.addByTSMFile = function (tsmFilename) {
        if (tsmFilename === undefined || tsmFilename === null || tsmFilename.constructor !== String) { throw new TypeError('tsmFilename must be a string'); }
        var args = {
            tsmFilename : tsmFilename
        };
        var result = this._execute('addByTSMFile', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.TSplineBody) : null;
    };

    // Creates a new TSplineBody using the T-Spline description provided by the input
    // string which contains TSM formatted text.
    // tsmDescription : A string that contains a T-Spline description in TSM form.
    // Returns the newly created TSplineBody if successful or null in the case of failure.
    adsk.fusion.TSplineBodies.prototype.addByTSMDescription = function (tsmDescription) {
        if (tsmDescription === undefined || tsmDescription === null || tsmDescription.constructor !== String) { throw new TypeError('tsmDescription must be a string'); }
        var args = {
            tsmDescription : tsmDescription
        };
        var result = this._execute('addByTSMDescription', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.TSplineBody) : null;
    };

    //=========== TSplineBody ============
    // A TSpline body.
    adsk.fusion.TSplineBody = function TSplineBody(handle) {
        if (!(this instanceof adsk.fusion.TSplineBody)) {
            return adsk.fusion.TSplineBody.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.fusion.TSplineBody.prototype = Object.create(adsk.core.Base.prototype);
    adsk.fusion.TSplineBody.prototype.constructor = adsk.fusion.TSplineBody;
    adsk.fusion.TSplineBody.classType = function classType () {
        return 'adsk::fusion::TSplineBody';
    };
    adsk.fusion.TSplineBody.interfaceId = 'adsk.fusion.TSplineBody';
    adsk.objectTypes['adsk.fusion.TSplineBody'] = adsk.fusion.TSplineBody;
    adsk.fusion.TSplineBody.cast = function (object) {
        return object instanceof adsk.fusion.TSplineBody ? object : null;
    };

    // Gets and sets the name of the body. If setting this property, there is the side-effect
    // that the B-Rep body created from this T-Spline body is also renamed.
    Object.defineProperty(adsk.fusion.TSplineBody.prototype, 'name', {
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

    // Returns the owning form feature.
    Object.defineProperty(adsk.fusion.TSplineBody.prototype, 'parentFormFeature', {
        get : function () {
            var result = this._execute('parentFormFeature');
            return (result && result.value) ? adsk.createObject(result.value, adsk.fusion.FormFeature) : null;
        }
    });

    // Returns the T-Spline body as a string in the form of a TSM description.
    // Returns the string formatted using the TSM format.
    adsk.fusion.TSplineBody.prototype.getTSMDescription = function () {
        var result = this._execute('getTSMDescription');
        return result ? result.value : undefined;
    };

    // Saves the body as a TSM file.
    // filename : The full filename of the file to save the body to. If the file already exists,
    // it will be overwritten.
    // Returns true if the file was successfully created.
    adsk.fusion.TSplineBody.prototype.saveAsTSMFile = function (filename) {
        if (filename === undefined || filename === null || filename.constructor !== String) { throw new TypeError('filename must be a string'); }
        var args = {
            filename : filename
        };
        var result = this._execute('saveAsTSMFile', args);
        return result ? result.value : undefined;
    };

    return adsk;
}));