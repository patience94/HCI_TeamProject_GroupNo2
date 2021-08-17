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
    if (adsk.cam === undefined) {
        adsk.cam = {};
    }

    //=========== CAMParameter ============
    // Base class for representing parameter of an operation.
    adsk.cam.CAMParameter = function CAMParameter(handle) {
        if (!(this instanceof adsk.cam.CAMParameter)) {
            return adsk.cam.CAMParameter.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.cam.CAMParameter.prototype = Object.create(adsk.core.Base.prototype);
    adsk.cam.CAMParameter.prototype.constructor = adsk.cam.CAMParameter;
    adsk.cam.CAMParameter.classType = function classType () {
        return 'adsk::cam::CAMParameter';
    };
    adsk.cam.CAMParameter.interfaceId = 'adsk.cam.CAMParameter';
    adsk.objectTypes['adsk.cam.CAMParameter'] = adsk.cam.CAMParameter;
    adsk.cam.CAMParameter.cast = function (object) {
        return object instanceof adsk.cam.CAMParameter ? object : null;
    };

    // Gets the name (internal name) of the parameter.
    Object.defineProperty(adsk.cam.CAMParameter.prototype, 'name', {
        get : function () {
            var result = this._execute('name');
            return result ? result.value : undefined;
        }
    });

    // Returns the title of this parameter as seen in the user interface.
    // This title is localized and can change based on the current language
    Object.defineProperty(adsk.cam.CAMParameter.prototype, 'title', {
        get : function () {
            var result = this._execute('title');
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the value expression of the parameter.
    Object.defineProperty(adsk.cam.CAMParameter.prototype, 'expression', {
        get : function () {
            var result = this._execute('expression');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (value === undefined || value === null || value.constructor !== String) { throw new TypeError('value must be a string'); }
            var args = {
                value : value
            };
            var result = this._execute('expression', args);
            return result ? result.value : undefined;
        }
    });

    // Gets if this parameter is enabled. Some parameters are enabled/disabled depending on the values
    // set for other parameters.
    Object.defineProperty(adsk.cam.CAMParameter.prototype, 'isEnabled', {
        get : function () {
            var result = this._execute('isEnabled');
            return result ? result.value : undefined;
        }
    });

    // Returns a message corresponding to any active error associated with the value of this parameter.
    Object.defineProperty(adsk.cam.CAMParameter.prototype, 'error', {
        get : function () {
            var result = this._execute('error');
            return result ? result.value : undefined;
        }
    });

    // Returns a message corresponding to any active warning associated with the value of this parameter.
    Object.defineProperty(adsk.cam.CAMParameter.prototype, 'warning', {
        get : function () {
            var result = this._execute('warning');
            return result ? result.value : undefined;
        }
    });

    //=========== CAMParameters ============
    // Collection that provides access to the parameters of an existing operation.
    adsk.cam.CAMParameters = function CAMParameters(handle) {
        if (!(this instanceof adsk.cam.CAMParameters)) {
            return adsk.cam.CAMParameters.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.cam.CAMParameters.prototype = Object.create(adsk.core.Base.prototype);
    adsk.cam.CAMParameters.prototype.constructor = adsk.cam.CAMParameters;
    adsk.cam.CAMParameters.classType = function classType () {
        return 'adsk::cam::CAMParameters';
    };
    adsk.cam.CAMParameters.interfaceId = 'adsk.cam.CAMParameters';
    adsk.objectTypes['adsk.cam.CAMParameters'] = adsk.cam.CAMParameters;
    adsk.cam.CAMParameters.cast = function (object) {
        return object instanceof adsk.cam.CAMParameters ? object : null;
    };

    // The number of items in the collection.
    Object.defineProperty(adsk.cam.CAMParameters.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified parameter using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.cam.CAMParameters.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.cam.CAMParameter) : null;
    };

    // Returns the parameter of the specified id (internal name).
    // internalName : The id (internal name) of the parameter.
    // Returns the specified parameter or null in the case where there is no parameter with the specified id.
    adsk.cam.CAMParameters.prototype.itemByName = function (internalName) {
        if (internalName === undefined || internalName === null || internalName.constructor !== String) { throw new TypeError('internalName must be a string'); }
        var args = {
            internalName : internalName
        };
        var result = this._execute('itemByName', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.cam.CAMParameter) : null;
    };

    //=========== OperationBase ============
    // Base class object representing all operations, folders, patterns and setups.
    adsk.cam.OperationBase = function OperationBase(handle) {
        if (!(this instanceof adsk.cam.OperationBase)) {
            return adsk.cam.OperationBase.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.cam.OperationBase.prototype = Object.create(adsk.core.Base.prototype);
    adsk.cam.OperationBase.prototype.constructor = adsk.cam.OperationBase;
    adsk.cam.OperationBase.classType = function classType () {
        return 'adsk::cam::OperationBase';
    };
    adsk.cam.OperationBase.interfaceId = 'adsk.cam.OperationBase';
    adsk.objectTypes['adsk.cam.OperationBase'] = adsk.cam.OperationBase;
    adsk.cam.OperationBase.cast = function (object) {
        return object instanceof adsk.cam.OperationBase ? object : null;
    };

    // Gets and sets the name of the operation as seen in the browser. This name is unique as compared
    // to the names of all other operations in the document.
    Object.defineProperty(adsk.cam.OperationBase.prototype, 'name', {
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

    // Gets and sets the "protected" property value of the operation.
    // Gets/sets true if the operation is protected.
    Object.defineProperty(adsk.cam.OperationBase.prototype, 'isProtected', {
        get : function () {
            var result = this._execute('isProtected');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isProtected', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the "Optional" property value of the operation.
    // Gets/sets true if the operation is optional.
    Object.defineProperty(adsk.cam.OperationBase.prototype, 'isOptional', {
        get : function () {
            var result = this._execute('isOptional');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isOptional', args);
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the "Suppressed" property value of the operation.
    // Gets/sets true if the operation is suppressed.
    Object.defineProperty(adsk.cam.OperationBase.prototype, 'isSuppressed', {
        get : function () {
            var result = this._execute('isSuppressed');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (typeof value !== 'boolean') { throw new TypeError('value must be a boolean'); }
            var args = {
                value : value
            };
            var result = this._execute('isSuppressed', args);
            return result ? result.value : undefined;
        }
    });

    // Gets the Setup this operation belongs to.
    Object.defineProperty(adsk.cam.OperationBase.prototype, 'parentSetup', {
        get : function () {
            var result = this._execute('parentSetup');
            return (result && result.value) ? adsk.createObject(result.value, adsk.cam.Setup) : null;
        }
    });

    // Gets if this operation is selected in the 'Setups' browser.
    Object.defineProperty(adsk.cam.OperationBase.prototype, 'isSelected', {
        get : function () {
            var result = this._execute('isSelected');
            return result ? result.value : undefined;
        }
    });

    // Gets and sets the notes of the operation.
    Object.defineProperty(adsk.cam.OperationBase.prototype, 'notes', {
        get : function () {
            var result = this._execute('notes');
            return result ? result.value : undefined;
        },
        set : function (value) {
            if (value === undefined || value === null || value.constructor !== String) { throw new TypeError('value must be a string'); }
            var args = {
                value : value
            };
            var result = this._execute('notes', args);
            return result ? result.value : undefined;
        }
    });

    // Returns the id of the operation. This id is unique as compared
    // to the ids of all other operations in the document.
    // This id will not change when changing the order or parent of the operation.
    // This id will remain valid when the document is saved and reloaded.
    Object.defineProperty(adsk.cam.OperationBase.prototype, 'operationId', {
        get : function () {
            var result = this._execute('operationId');
            return result ? result.value : undefined;
        }
    });

    // Gets the CAMParameters collection for this operation.
    Object.defineProperty(adsk.cam.OperationBase.prototype, 'parameters', {
        get : function () {
            var result = this._execute('parameters');
            return (result && result.value) ? adsk.createObject(result.value, adsk.cam.CAMParameters) : null;
        }
    });

    //=========== Operations ============
    // Collection that provides access to the individual operations within an existing setup, folder or pattern.
    adsk.cam.Operations = function Operations(handle) {
        if (!(this instanceof adsk.cam.Operations)) {
            return adsk.cam.Operations.cast(handle);
        }
        adsk.core.Base.call(this, handle);
    };
    adsk.cam.Operations.prototype = Object.create(adsk.core.Base.prototype);
    adsk.cam.Operations.prototype.constructor = adsk.cam.Operations;
    adsk.cam.Operations.classType = function classType () {
        return 'adsk::cam::Operations';
    };
    adsk.cam.Operations.interfaceId = 'adsk.cam.Operations';
    adsk.objectTypes['adsk.cam.Operations'] = adsk.cam.Operations;
    adsk.cam.Operations.cast = function (object) {
        return object instanceof adsk.cam.Operations ? object : null;
    };

    // The number of items in the collection.
    Object.defineProperty(adsk.cam.Operations.prototype, 'count', {
        get : function () {
            var result = this._execute('count');
            return result ? result.value : undefined;
        }
    });

    // Function that returns the specified operation using an index into the collection.
    // index : The index of the item within the collection to return. The first item in the collection has an index of 0.
    // Returns the specified item or null if an invalid index was specified.
    adsk.cam.Operations.prototype.item = function (index) {
        if (!isFinite(index)) { throw new TypeError('index must be a number'); }
        var args = {
            index : Number(index)
        };
        var result = this._execute('item', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.cam.Operation) : null;
    };

    // Returns the operation with the specified name (as appears in the browser).
    // name : The name (as it appears in the browser) of the operation.
    // Returns the specified operation or null in the case where there is no operation with the specified name.
    adsk.cam.Operations.prototype.itemByName = function (name) {
        if (name === undefined || name === null || name.constructor !== String) { throw new TypeError('name must be a string'); }
        var args = {
            name : name
        };
        var result = this._execute('itemByName', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.cam.Operation) : null;
    };

    // Returns the operation with the specified operation id.
    // id : The id of the operation.
    // Returns the specified operation or null in the case where there is no operation with the specified operation id.
    adsk.cam.Operations.prototype.itemByOperationId = function (id) {
        if (!isFinite(id)) { throw new TypeError('id must be a number'); }
        var args = {
            id : Number(id)
        };
        var result = this._execute('itemByOperationId', args);
        return (result && result.value) ? adsk.createObject(result.value, adsk.cam.Operation) : null;
    };

    //=========== OperationStates ============
    // The possible states of an operation
    adsk.cam.OperationStates = {
        IsValidOperationState : 0,
        IsInvalidOperationState : 1,
        SuppressedOperationState : 2,
        NoToolpathOperationState : 3
    };

    //=========== OperationStrategyTypes ============
    // The valid options for the Strategy Type of an operation.
    adsk.cam.OperationStrategyTypes = {
        AdaptiveClearing2D : 0,
        Pocket2D : 1,
        Face : 2,
        Contour2D : 3,
        Slot : 4,
        Trace : 5,
        Thread : 6,
        Bore : 7,
        Circular : 8,
        Engrave : 9,
        AdaptiveClearing : 10,
        PocketClearing : 11,
        Parallel : 12,
        Contour : 13,
        Ramp : 14,
        Horizontal : 15,
        Pencil : 16,
        Scallop : 17,
        Spiral : 18,
        Radial : 19,
        MorphedSpiral : 20,
        Projection : 21,
        Drilling : 22,
        Jet2D : 23,
        TurningChamfer : 24,
        TurningFace : 25,
        TurningGroove : 26,
        TurningPart : 27,
        TurningProfile : 28,
        TurningProfileGroove : 29,
        TurningStockTransfer : 30,
        TurningThread : 31
    };

    //=========== OperationTypes ============
    // The valid options for the Operation Type of a Setup.
    adsk.cam.OperationTypes = {
        MillingOperation : 0,
        TurningOperation : 1,
        JetOperation : 2
    };

    //=========== Operation ============
    // Object that represents an operation in an existing Setup, Folder or Pattern.
    adsk.cam.Operation = function Operation(handle) {
        if (!(this instanceof adsk.cam.Operation)) {
            return adsk.cam.Operation.cast(handle);
        }
        adsk.cam.OperationBase.call(this, handle);
    };
    adsk.cam.Operation.prototype = Object.create(adsk.cam.OperationBase.prototype);
    adsk.cam.Operation.prototype.constructor = adsk.cam.Operation;
    adsk.cam.Operation.classType = function classType () {
        return 'adsk::cam::Operation';
    };
    adsk.cam.Operation.interfaceId = 'adsk.cam.Operation';
    adsk.objectTypes['adsk.cam.Operation'] = adsk.cam.Operation;
    adsk.cam.Operation.cast = function (object) {
        return object instanceof adsk.cam.Operation ? object : null;
    };

    // Gets the strategy type for this operation.
    Object.defineProperty(adsk.cam.Operation.prototype, 'strategyType', {
        get : function () {
            var result = this._execute('strategyType');
            return result ? result.value : undefined;
        }
    });

    // Gets if the toolpath for this operation is currently valid. (has not become invalidated by model changes).
    Object.defineProperty(adsk.cam.Operation.prototype, 'isToolpathValid', {
        get : function () {
            var result = this._execute('isToolpathValid');
            return result ? result.value : undefined;
        }
    });

    // Gets if the toolpath is in the process of generating.
    Object.defineProperty(adsk.cam.Operation.prototype, 'isGenerating', {
        get : function () {
            var result = this._execute('isGenerating');
            return result ? result.value : undefined;
        }
    });

    // Gets if problems were encountered when generating the toolpath for this operation.
    Object.defineProperty(adsk.cam.Operation.prototype, 'hasWarning', {
        get : function () {
            var result = this._execute('hasWarning');
            return result ? result.value : undefined;
        }
    });

    // Returns the parent Setup, Folder or Pattern for this operation.
    Object.defineProperty(adsk.cam.Operation.prototype, 'parent', {
        get : function () {
            var result = this._execute('parent');
            return (result && result.value) ? adsk.createObject(result.value, adsk.core.Base) : null;
        }
    });

    // Gets if a toolpath currently exists (has been generated) for this operation.
    Object.defineProperty(adsk.cam.Operation.prototype, 'hasToolpath', {
        get : function () {
            var result = this._execute('hasToolpath');
            return result ? result.value : undefined;
        }
    });

    // Gets the current state of this operation.
    Object.defineProperty(adsk.cam.Operation.prototype, 'operationState', {
        get : function () {
            var result = this._execute('operationState');
            return result ? result.value : undefined;
        }
    });

    // Gets the toolpath generation progress value for this operation.
    Object.defineProperty(adsk.cam.Operation.prototype, 'generatingProgress', {
        get : function () {
            var result = this._execute('generatingProgress');
            return result ? result.value : undefined;
        }
    });

    return adsk;
}));