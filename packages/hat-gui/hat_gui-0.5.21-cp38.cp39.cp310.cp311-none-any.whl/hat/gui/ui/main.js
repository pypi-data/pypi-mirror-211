/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ([
/* 0 */,
/* 1 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Renderer": () => (/* binding */ Renderer),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var snabbdom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(3);
/* harmony import */ var snabbdom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(7);
/* harmony import */ var snabbdom__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(8);
/* harmony import */ var snabbdom__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(9);
/* harmony import */ var snabbdom__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(10);
/* harmony import */ var snabbdom__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(11);
/* harmony import */ var _hat_open_util__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(2);
/** @module @hat-open/renderer
 */






// patched version of snabbdom's modules/attributes.js
const snabbdomAttributesModule = (() => {
    function updateAttrs(oldVnode, vnode) {
        let key;
        const elm = vnode.elm;
        let oldAttrs = oldVnode.data.attrs;
        let attrs = vnode.data.attrs;
        if (!oldAttrs && !attrs)
            return;
        if (oldAttrs === attrs)
            return;
        oldAttrs = oldAttrs || {};
        attrs = attrs || {};
        for (key in attrs) {
            const cur = attrs[key];
            const old = oldAttrs[key];
            if (old !== cur) {
                if (cur === true) {
                    elm.setAttribute(key, "");
                }
                else if (cur === false) {
                    elm.removeAttribute(key);
                }
                else {
                    elm.setAttribute(key, cur);
                }
            }
        }
        for (key in oldAttrs) {
            if (!(key in attrs)) {
                elm.removeAttribute(key);
            }
        }
    }
    return { create: updateAttrs, update: updateAttrs };
})();


// patched version of snabbdom's modules/props.js
const snabbdomPropsModule = (() => {
    function updateProps(oldVnode, vnode) {
        let key;
        let cur;
        let old;
        const elm = vnode.elm;
        let oldProps = oldVnode.data.props;
        let props = vnode.data.props;
        if (!oldProps && !props)
            return;
        if (oldProps === props)
            return;
        oldProps = oldProps || {};
        props = props || {};
        for (key in oldProps) {
            if (!props[key]) {
                if (key === 'style') {
                    elm[key] = '';
                } else {
                    delete elm[key];
                }
            }
        }
        for (key in props) {
            cur = props[key];
            old = oldProps[key];
            if (old !== cur && (key !== 'value' || elm[key] !== cur)) {
                elm[key] = cur;
            }
        }
    }
    return { create: updateProps, update: updateProps };
})();


const patch = snabbdom__WEBPACK_IMPORTED_MODULE_1__.init([
    snabbdomAttributesModule,
    snabbdom__WEBPACK_IMPORTED_MODULE_2__.classModule,
    snabbdom__WEBPACK_IMPORTED_MODULE_3__.datasetModule,
    snabbdom__WEBPACK_IMPORTED_MODULE_4__.eventListenersModule,
    snabbdomPropsModule,
    snabbdom__WEBPACK_IMPORTED_MODULE_5__.styleModule
]);


function vhFromArray(node) {
    if (!node)
        return [];
    if (_hat_open_util__WEBPACK_IMPORTED_MODULE_0__.isString(node))
        return node;
    if (!_hat_open_util__WEBPACK_IMPORTED_MODULE_0__.isArray(node))
        throw 'Invalid node structure';
    if (node.length < 1)
        return [];
    if (typeof node[0] != 'string')
        return node.map(vhFromArray);
    const hasData = node.length > 1 && _hat_open_util__WEBPACK_IMPORTED_MODULE_0__.isObject(node[1]);
    const children = _hat_open_util__WEBPACK_IMPORTED_MODULE_0__.pipe(
        _hat_open_util__WEBPACK_IMPORTED_MODULE_0__.map(vhFromArray),
        _hat_open_util__WEBPACK_IMPORTED_MODULE_0__.flatten,
        Array.from
    )(node.slice(hasData ? 2 : 1));
    const result = hasData ?
        snabbdom__WEBPACK_IMPORTED_MODULE_6__.h(node[0], node[1], children) :
        snabbdom__WEBPACK_IMPORTED_MODULE_6__.h(node[0], children);
    return result;
}

/**
 * Virtual DOM renderer
 */
class Renderer extends EventTarget {

    /**
     * Calls `init` method
     * @param {HTMLElement} [el=document.body]
     * @param {Any} [initState=null]
     * @param {Function} [vtCb=null]
     * @param {Number} [maxFps=30]
     */
    constructor(el, initState, vtCb, maxFps) {
        super();
        this.init(el, initState, vtCb, maxFps);
    }

    /**
     * Initialize renderer
     * @param {HTMLElement} [el=document.body]
     * @param {Any} [initState=null]
     * @param {Function} [vtCb=null]
     * @param {Number} [maxFps=30]
     * @return {Promise}
     */
    init(el, initState, vtCb, maxFps) {
        this._state = null;
        this._changes = [];
        this._promise = null;
        this._timeout = null;
        this._lastRender = null;
        this._vtCb = vtCb;
        this._maxFps = _hat_open_util__WEBPACK_IMPORTED_MODULE_0__.isNumber(maxFps) ? maxFps : 30;
        this._vNode = el || document.querySelector('body');
        if (initState)
            return this.change(_ => initState);
        return new Promise(resolve => { resolve(); });
    }

    /**
      * Render
      */
    render() {
        if (!this._vtCb)
            return;
        this._lastRender = performance.now();
        const vNode = vhFromArray(this._vtCb(this));
        patch(this._vNode, vNode);
        this._vNode = vNode;
        this.dispatchEvent(new CustomEvent('render', {detail: this._state}));
    }

    /**
     * Get current state value referenced by `paths`
     * @param {...Path} paths
     * @return {Any}
     */
    get(...paths) {
        return _hat_open_util__WEBPACK_IMPORTED_MODULE_0__.get(paths, this._state);
    }

    /**
     * Change current state value referenced by `path`
     * @param {Path} path
     * @param {Any} value
     * @return {Promise}
     */
    set(path, value) {
        if (arguments.length < 2) {
            value = path;
            path = [];
        }
        return this.change(path, _ => value);
    }

    /**
     * Change current state value referenced by `path`
     * @param {Path} path
     * @param {Function} cb
     * @return {Promise}
     */
    change(path, cb) {
        if (arguments.length < 2) {
            cb = path;
            path = [];
        }
        this._changes.push([path, cb]);
        if (this._promise)
            return this._promise;
        this._promise = new Promise((resolve, reject) => {
            setTimeout(() => {
                try {
                    this._change();
                } catch(e) {
                    this._promise = null;
                    reject(e);
                    throw e;
                }
                this._promise = null;
                resolve();
            }, 0);
        });
        return this._promise;
    }

    _change() {
        while (this._changes.length > 0) {
            let change = false;
            while (this._changes.length > 0) {
                const [path, cb] = this._changes.shift();
                const view = _hat_open_util__WEBPACK_IMPORTED_MODULE_0__.get(path);
                const oldState = this._state;
                this._state = _hat_open_util__WEBPACK_IMPORTED_MODULE_0__.change(path, cb, this._state);
                if (this._state && _hat_open_util__WEBPACK_IMPORTED_MODULE_0__.equals(view(oldState),
                                            view(this._state)))
                    continue;
                change = true;
                if (!this._vtCb || this._timeout)
                    continue;
                const delay = (!this._lastRender || !this._maxFps ?
                    0 :
                    (1000 / this._maxFps) -
                    (performance.now() - this._lastRender));
                this._timeout = setTimeout(() => {
                    this._timeout = null;
                    this.render();
                }, (delay > 0 ? delay : 0));
            }
            if (change)
                this.dispatchEvent(
                    new CustomEvent('change', {detail: this._state}));
        }
    }
}
// Renderer.prototype.set = u.curry(Renderer.prototype.set);
// Renderer.prototype.change = u.curry(Renderer.prototype.change);


/**
 * Default renderer
 * @static
 * @type {Renderer}
 */
const defaultRenderer = (() => {
    const r = (window && window.__hat_default_renderer) || new Renderer();
    if (window)
        window.__hat_default_renderer = r;
    return r;
})();
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (defaultRenderer);


/***/ }),
/* 2 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "identity": () => (/* binding */ identity),
/* harmony export */   "isNil": () => (/* binding */ isNil),
/* harmony export */   "isBoolean": () => (/* binding */ isBoolean),
/* harmony export */   "isInteger": () => (/* binding */ isInteger),
/* harmony export */   "isNumber": () => (/* binding */ isNumber),
/* harmony export */   "isString": () => (/* binding */ isString),
/* harmony export */   "isArray": () => (/* binding */ isArray),
/* harmony export */   "isObject": () => (/* binding */ isObject),
/* harmony export */   "strictParseInt": () => (/* binding */ strictParseInt),
/* harmony export */   "strictParseFloat": () => (/* binding */ strictParseFloat),
/* harmony export */   "clone": () => (/* binding */ clone),
/* harmony export */   "zip": () => (/* binding */ zip),
/* harmony export */   "toPairs": () => (/* binding */ toPairs),
/* harmony export */   "fromPairs": () => (/* binding */ fromPairs),
/* harmony export */   "flatten": () => (/* binding */ flatten),
/* harmony export */   "pipe": () => (/* binding */ pipe),
/* harmony export */   "flap": () => (/* binding */ flap),
/* harmony export */   "curry": () => (/* binding */ curry),
/* harmony export */   "equals": () => (/* binding */ equals),
/* harmony export */   "repeat": () => (/* binding */ repeat),
/* harmony export */   "get": () => (/* binding */ get),
/* harmony export */   "change": () => (/* binding */ change),
/* harmony export */   "set": () => (/* binding */ set),
/* harmony export */   "omit": () => (/* binding */ omit),
/* harmony export */   "move": () => (/* binding */ move),
/* harmony export */   "sort": () => (/* binding */ sort),
/* harmony export */   "sortBy": () => (/* binding */ sortBy),
/* harmony export */   "pick": () => (/* binding */ pick),
/* harmony export */   "map": () => (/* binding */ map),
/* harmony export */   "filter": () => (/* binding */ filter),
/* harmony export */   "append": () => (/* binding */ append),
/* harmony export */   "reduce": () => (/* binding */ reduce),
/* harmony export */   "merge": () => (/* binding */ merge),
/* harmony export */   "mergeAll": () => (/* binding */ mergeAll),
/* harmony export */   "find": () => (/* binding */ find),
/* harmony export */   "findIndex": () => (/* binding */ findIndex),
/* harmony export */   "concat": () => (/* binding */ concat),
/* harmony export */   "union": () => (/* binding */ union),
/* harmony export */   "contains": () => (/* binding */ contains),
/* harmony export */   "insert": () => (/* binding */ insert),
/* harmony export */   "slice": () => (/* binding */ slice),
/* harmony export */   "reverse": () => (/* binding */ reverse),
/* harmony export */   "length": () => (/* binding */ length),
/* harmony export */   "inc": () => (/* binding */ inc),
/* harmony export */   "dec": () => (/* binding */ dec),
/* harmony export */   "not": () => (/* binding */ not),
/* harmony export */   "sleep": () => (/* binding */ sleep),
/* harmony export */   "delay": () => (/* binding */ delay),
/* harmony export */   "timestampToLocalString": () => (/* binding */ timestampToLocalString)
/* harmony export */ });
/**
 * Utility library for manipulation of JSON data.
 *
 * Main characteristics:
 *   - input/output data types are limited to JSON data, functions and
 *     `undefined` (sparse arrays and complex objects with prototype chain are
 *     not supported)
 *   - functional API with curried functions (similar to ramdajs)
 *   - implementation based on natively supported browser JS API
 *   - scope limited to most used functions in hat projects
 *   - usage of `paths` instead of `lenses`
 *
 * TODO: define convetion for naming arguments based on their type and
 *       semantics
 *
 * @module @hat-open/util
 */

/**
 * Path can be an object property name, array index, or array of Paths
 *
 * TODO: explain paths and path compositions (include examples)
 *
 * @typedef {(String|Number|Path[])} module:@hat-open/util.Path
 */

/**
 * Identity function returning same value provided as argument.
 *
 * @function
 * @sig a -> a
 * @param {*} x input value
 * @return {*} same value as input
 */
const identity = x => x;

/**
 * Check if value is `null` or `undefined`.
 *
 * For same argument, if this function returns `true`, functions `isBoolean`,
 * `isInteger`, `isNumber`, `isString`, `isArray` and `isObject` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isNil = x => x == null;

/**
 * Check if value is Boolean.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isInteger`, `isNumber`, `isString`, `isArray` and `isObject` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isBoolean = x => typeof(x) == 'boolean';

/**
 * Check if value is Integer.
 *
 * For same argument, if this function returns `true`, function `isNumber` will
 * also return `true`.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isString`, `isArray` and `isObject` will return `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @type {Boolean}
 */
const isInteger = Number.isInteger;

/**
 * Check if value is Number.
 *
 * For same argument, if this function returns `true`, function `isInteger` may
 * also return `true` if argument is integer number.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isString`, `isArray` and `isObject` will return `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isNumber = x => typeof(x) == 'number';

/**
 * Check if value is String.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isInteger`, `isNumber`, `isArray`, and `isObject` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {Any} x input value
 * @type {Boolean}
 */
const isString = x => typeof(x) == 'string';

/**
 * Check if value is Array.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isInteger`, `isNumber`, `isString`, and `isObject` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isArray = Array.isArray;

/**
 * Check if value is Object.
 *
 * For same argument, if this function returns `true`, functions `isNil`,
 * `isBoolean`, `isInteger`, `isNumber`, `isString`, and `isArray` will return
 * `false`.
 *
 * @function
 * @sig * -> Boolean
 * @param {*} x input value
 * @return {Boolean}
 */
const isObject = x => typeof(x) == 'object' &&
                             !isArray(x) &&
                             !isNil(x);

/**
 * Strictly parse integer from string
 *
 * If provided string doesn't represent integer value, `NaN` is returned.
 *
 * @function
 * @sig String -> Number
 * @param {String} value
 * @return {Number}
 */
function strictParseInt(value) {
    if (/^(-|\+)?([0-9]+)$/.test(value))
        return Number(value);
    return NaN;
}

/**
 * Strictly parse floating point number from string
 *
 * If provided string doesn't represent valid number, `NaN` is returned.
 *
 * @function
 * @sig String -> Number
 * @param {String} value
 * @return {Number}
 */
function strictParseFloat(value) {
    if (/^(-|\+)?([0-9]+(\.[0-9]+)?)$/.test(value))
        return Number(value);
    return NaN;
}

/**
 * Create new deep copy of input value.
 *
 * In case of Objects or Arrays, new instances are created with elements
 * obtained by recursivly calling `clone` in input argument values.
 *
 * @function
 * @sig * -> *
 * @param {*} x value
 * @return {*} copy of value
 */
function clone(x) {
    if (isArray(x))
        return Array.from(x, clone);
    if (isObject(x)) {
        let ret = {};
        for (let i in x)
            ret[i] = clone(x[i]);
        return ret;
    }
    return x;
}

/**
 * Combine two arrays in single array of pairs
 *
 * The returned array is truncated to the length of the shorter of the two
 * input arrays.
 *
 * @function
 * @sig [a] -> [b] -> [[a,b]]
 * @param {Array} arr1
 * @param {Array} arr2
 * @return {Array}
 */
function zip(arr1, arr2) {
    return Array.from((function*() {
        for (let i = 0; i < arr1.length || i < arr2.length; ++i)
            yield [arr1[i], arr2[i]];
    })());
}

/**
 * Convert object to array of key, value pairs
 *
 * @function
 * @sig Object -> [[String,*]]
 * @param {Object} obj
 * @return {Array}
 */
function toPairs(obj) {
    return Object.entries(obj);
}

/**
 * Convert array of key, value pairs to object
 *
 * @function
 * @sig [[String,*]] -> Object
 * @param {Array} arr
 * @return {Object}
 */
function fromPairs(arr) {
    let ret = {};
    for (let [k, v] of arr)
        ret[k] = v;
    return ret;
}

/**
 * Flatten nested arrays.
 *
 * Create array with same elements as in input array where all elements which
 * are also arrays are replaced with elements of resulting recursive
 * application of flatten function.
 *
 * If argument is not an array, function returns the argument encapsulated in
 * an array.
 *
 * @function
 * @sig [a] -> [b]
 * @param {*} arr
 * @return {Array}
 */
function flatten(arr) {
    return isArray(arr) ? arr.flat(Infinity) : [arr];
}

/**
 * Pipe function calls
 *
 * Pipe provides functional composition with reversed order. First function
 * may have any arity and all other functions are called with only single
 * argument (result from previous function application).
 *
 * In case when no function is provided, pipe returns identity function.
 *
 * @function
 * @sig (((a1, a2, ..., an) -> b1), (b1 -> b2), ..., (bm1 -> bm)) -> ((a1, a2, ..., an) -> bm)
 * @param {...Function} fns functions
 * @return {Function}
 */
function pipe(...fns) {
    if (fns.length < 1)
        return identity;
    return function (...args) {
        let ret = fns[0].apply(this, args);
        for (let fn of fns.slice(1))
            ret = fn(ret);
        return ret;
    };
}

/**
 * Apply list of functions to same arguments and return list of results
 *
 * @function
 * @sig ((a1 -> ... -> an -> b1), ..., (a1 -> ... -> an -> bm)) -> (a1 -> ... -> an -> [b1,...,bm])
 * @param {...Function} fns functions
 * @return {Function}
 */
function flap(...fns) {
    return (...args) => fns.map(fn => fn.apply(this, args));
}

/**
 * Curry function with fixed arguments lenth
 *
 * Function arity is determined based on function's length property.
 *
 * @function
 * @sig (* -> a) -> (* -> a)
 * @param {Function} fn
 * @return {Function}
 */
function curry(fn) {
    let wrapper = function(oldArgs) {
        return function(...args) {
            args = oldArgs.concat(args);
            if (args.length >= fn.length)
                return fn(...args);
            return wrapper(args);
        };
    };
    return wrapper([]);
}

/**
 * Deep object equality
 * (curried function)
 *
 * @function
 * @sig a -> b -> Boolean
 * @param {*} x
 * @param {*} y
 * @return {Boolean}
 */
const equals = curry((x, y) => {
    if (x === y)
        return true;
    if (typeof(x) != 'object' ||
        typeof(y) != 'object' ||
        x === null ||
        y === null)
        return false;
    if (Array.isArray(x) && Array.isArray(y)) {
        if (x.length != y.length)
            return false;
        for (let [a, b] of zip(x, y)) {
            if (!equals(a, b))
                return false;
        }
        return true;
    } else if (!Array.isArray(x) && !Array.isArray(y)) {
        if (Object.keys(x).length != Object.keys(y).length)
            return false;
        for (let key in x) {
            if (!(key in y))
                return false;
        }
        for (let key in x) {
            if (!equals(x[key], y[key]))
                return false;
        }
        return true;
    }
    return false;
});


/**
 * Create array by repeating same value
 * (curried function)
 *
 * @function
 * @sig a -> Number -> [a]
 * @param {*} x
 * @param {Number} n
 * @return {Array}
 */
const repeat = curry((x, n) => Array.from({length: n}, _ => x));

/**
 * Get value referenced by path
 * (curried function)
 *
 * If input value doesn't contain provided path value, `undefined` is returned.
 *
 * @function
 * @sig Path -> a -> b
 * @param {Path} path
 * @param {*} x
 * @return {*}
 */
const get = curry((path, x) => {
    let ret = x;
    for (let i of flatten(path)) {
        if (ret === null || typeof(ret) != 'object')
            return undefined;
        ret = ret[i];
    }
    return ret;
});

/**
 * Change value referenced with path by appling function
 * (curried function)
 *
 * @function
 * @sig Path -> (a -> b) -> c -> c
 * @param {Path} path
 * @param {Function} fn
 * @param {*} x
 * @return {*}
 */
const change = curry((path, fn, x) => {
    return (function change(path, x) {
        if (path.length < 1)
            return fn(x);
        const [first, ...rest] = path;
        if (isInteger(first)) {
            x = (isArray(x) ? Array.from(x) : repeat(undefined, first));
        } else if (isString(first)) {
            x = (isObject(x) ? Object.assign({}, x) : {});
        } else {
            throw 'invalid path';
        }
        x[first] = change(rest, x[first]);
        return x;
    })(flatten(path), x);
});

/**
 * Replace value referenced with path with another value
 * (curried function)
 *
 * @function
 * @sig Path -> (a -> b) -> c -> c
 * @param {Path} path
 * @param {*} val
 * @param {*} x
 * @return {*}
 */
const set = curry((path, val, x) => change(path, _ => val, x));

/**
 * Omitting value referenced by path
 * (curried function)
 *
 * @function
 * @sig Path -> a -> a
 * @param {Path} path
 * @param {*} x
 * @return {*}
 */
const omit = curry((path, x) => {
    function _omit(path, x) {
        if (isInteger(path[0])) {
            x = (isArray(x) ? Array.from(x) : []);
        } else if (isString(path[0])) {
            x = (isObject(x) ? Object.assign({}, x) : {});
        } else {
            throw 'invalid path';
        }
        if (path.length > 1) {
            x[path[0]] = _omit(path.slice(1), x[path[0]]);
        } else if (isInteger(path[0])) {
            x.splice(path[0], 1);
        } else {
            delete x[path[0]];
        }
        return x;
    }
    path = flatten(path);
    if (path.length < 1)
        return undefined;
    return _omit(path, x);
});

/**
 * Change by moving value from source path to destination path
 * (curried function)
 *
 * @function
 * @sig Path -> Path -> a -> a
 * @param {Path} srcPath
 * @param {Path} dstPath
 * @param {*} x
 * @return {*}
 */
const move = curry((srcPath, dstPath, x) => pipe(
    set(dstPath, get(srcPath, x)),
    omit(srcPath)
)(x));

/**
 * Sort array
 * (curried function)
 *
 * Comparison function receives two arguments representing array elements and
 * should return:
 *   - negative number in case first argument is more significant then second
 *   - zero in case first argument is equaly significant as second
 *   - positive number in case first argument is less significant then second
 *
 * @function
 * @sig ((a, a) -> Number) -> [a] -> [a]
 * @param {Function} fn
 * @param {Array} arr
 * @return {Array}
 */
const sort = curry((fn, arr) => Array.from(arr).sort(fn));

/**
 * Sort array based on results of appling function to it's elements
 * (curried function)
 *
 * Resulting order is determined by comparring function application results
 * with greater then and lesser then operators.
 *
 * @function
 * @sig (a -> b) -> [a] -> [a]
 * @param {Function} fn
 * @param {Array} arr
 * @return {Array}
 */
const sortBy = curry((fn, arr) => sort((x, y) => {
    const xVal = fn(x);
    const yVal = fn(y);
    if (xVal < yVal)
        return -1;
    if (xVal > yVal)
        return 1;
    return 0;
}, arr));

/**
 * Create object containing only subset of selected properties
 * (curried function)
 *
 * @function
 * @sig [String] -> a -> a
 * @param {Array} arr
 * @param {Object} obj
 * @return {Object}
 */
const pick = curry((arr, obj) => {
    const ret = {};
    for (let i of arr)
        if (i in obj)
            ret[i] = obj[i];
    return ret;
});

/**
 * Change array or object by appling function to it's elements
 * (curried function)
 *
 * For each element, provided function is called with element value,
 * index/key and original container.
 *
 * @function
 * @sig ((a, Number, [a]) -> b) -> [a] -> [b]
 * @sig ((a, String, {String: a}) -> b) -> {String: a} -> {String: b}
 * @param {Function} fn
 * @param {Array|Object} x
 * @return {Array|Object}
 */
const map = curry((fn, x) => {
    if (isArray(x))
        return x.map(fn);
    const res = {};
    for (let k in x)
        res[k] = fn(x[k], k, x);
    return res;
});

/**
 * Change array to contain only elements for which function returns `true`
 * (curried function)
 *
 * @function
 * @sig (a -> Boolean) -> [a] -> [a]
 * @param {Function} fn
 * @param {Array} arr
 * @return {Array}
 */
const filter = curry((fn, arr) => arr.filter(fn));

/**
 * Append value to end of array
 * (curried function)
 *
 * @function
 * @sig a -> [a] -> [a]
 * @param {*} val
 * @param {Array} arr
 * @return {Array}
 */
const append = curry((val, arr) => arr.concat([val]));

/**
 * Reduce array or object by appling function
 * (curried function)
 *
 * For each element, provided function is called with accumulator,
 * elements value, element index/key and original container.
 *
 * @function
 * @sig ((b, a, Number, [a]) -> b) -> b -> [a] -> b
 * @sig ((b, a, String, {String: a}) -> b) -> b -> {String: a} -> b
 * @param {Function} fn
 * @param {*} val initial accumulator value
 * @param {Array|Object} x
 * @return {*} reduced value
 */
const reduce = curry((fn, val, x) => {
    if (isArray(x))
        return x.reduce(fn, val);
    let acc = val;
    for (let k in x)
        acc = fn(acc, x[k], k, x);
    return acc;
});

/**
 * Merge two objects
 * (curried function)
 *
 * If same property exist in both arguments, second argument's value is used
 * as resulting value
 *
 * @function
 * @sig a -> a -> a
 * @param {Object} x
 * @param {Object} y
 * @return {Object}
 */
const merge = curry((x, y) => Object.assign({}, x, y));

/**
 * Merge multiple objects
 * (curried function)
 *
 * If same property exist in multiple arguments, value from the last argument
 * containing that property is used
 *
 * @function
 * @sig [a] -> a
 * @param {Object[]}
 * @return {Object}
 */
const mergeAll = reduce(merge, {});

/**
 * Find element in array or object for which provided function returns `true`
 * (curried function)
 *
 * Until element is found, provided function is called for each element with
 * arguments: current element, current index/key and initial container.
 *
 * If searched element is not found, `undefined` is returned.
 *
 * @function
 * @sig ((a, Number, [a]) -> Boolean) -> [a] -> a
 * @sig ((a, String, {String: a}) -> Boolean) -> {String: a} -> a
 * @param {Function} fn
 * @param {Array|Object} x
 * @return {*}
 */
const find = curry((fn, x) => {
    if (isArray(x))
        return x.find(fn);
    for (let k in x)
        if (fn(x[k], k, x))
            return x[k];
});

/**
 * Find element's index/key in array or object for which provided function
 * returns `true`
 * (curried function)
 *
 * Until element is found, provided function is called for each element with
 * arguments: current element, current index/key and initial container.
 *
 * If searched element is not found, `undefined` is returned.
 *
 * @function
 * @sig ((a, Number, [a]) -> Boolean) -> [a] -> a
 * @sig ((a, String, {String: a}) -> Boolean) -> {String: a} -> a
 * @param {Function} fn
 * @param {Array|Object} x
 * @return {*}
 */
const findIndex = curry((fn, x) => {
    if (isArray(x))
        return x.findIndex(fn);
    for (let k in x)
        if (fn(x[k], k, x))
            return k;
});

/**
 * Concatenate two arrays
 * (curried function)
 *
 * @function
 * @sig [a] -> [a] -> [a]
 * @param {Array} x
 * @param {Array} y
 * @return {Array}
 */
const concat = curry((x, y) => x.concat(y));

/**
 * Create union of two arrays using `equals` to check equality
 * (curried function)
 *
 * @function
 * @sig [a] -> [a] -> [a]
 * @param {Array} x
 * @param {Array} y
 * @return {Array}
 */
const union = curry((x, y) => {
    return reduce((acc, val) => {
        if (!find(equals(val), x))
            acc = append(val, acc);
        return acc;
    }, x, y);
});

/**
 * Check if array contains value
 * (curried function)
 *
 * TODO: add support for objects (should we check for keys or values?)
 *
 * @function
 * @sig a -> [a] -> Boolean
 * @param {*} val
 * @param {Array|Object} x
 * @return {Boolean}
 */
const contains = curry((val, arr) => arr.includes(val));

/**
 * Insert value into array on specified index
 * (curried function)
 *
 * @function
 * @sig Number -> a -> [a] -> [a]
 * @param {Number} idx
 * @param {*} val
 * @param {Array} arr
 * @return {Array}
 */
const insert = curry((idx, val, arr) =>
    arr.slice(0, idx).concat([val], arr.slice(idx)));

/**
 * Get array slice
 * (curried function)
 *
 * @function
 * @sig Number -> Number -> [a] -> [a]
 * @param {Number} begin
 * @param {Number} end
 * @param {Array} arr
 * @return {Array}
 */
const slice = curry((begin, end, arr) => arr.slice(begin, end));

/**
 * Reverse array
 *
 * @function
 * @sig [a] -> [a]
 * @param  {Array} arr
 * @return {Array}
 */
function reverse(arr) {
    return Array.from(arr).reverse();
}

/**
 * Array length
 *
 * @function
 * @sig [a] -> Number
 * @param  {Array} arr
 * @return {Number}
 */
function length(arr) {
    return arr.length;
}

/**
 * Increment value
 * @param  {Number} val
 * @return {Number}
 */
function inc(val) {
    return val + 1;
}

/**
 * Decrement value
 * @param  {Number} val
 * @return {Number}
 */
function dec(val) {
    return val - 1;
}

/**
 * Logical not
 * @param  {Any} val
 * @return {Boolean}
 */
function not(val) {
    return !val;
}

/**
 * Create promise that resolves in `t` milliseconds
 *
 * TODO: move to other module
 *
 * @function
 * @sig Number -> Promise
 * @param {Number} t
 * @return {Promise}
 */
function sleep(t) {
    return new Promise(resolve => {
        setTimeout(() => { resolve(); }, t);
    });
}

/**
 * Delay function call `fn(...args)` for `t` milliseconds
 *
 * TODO: move to other module
 *
 * @function
 * @sig (((a1, a2, ..., an) -> _), Number, a1, a2, ..., an) -> Promise
 * @param {Function} fn
 * @param {Number} [t=0]
 * @param {*} args
 * @return {Promise}
 */
function delay(fn, t, ...args) {
    return new Promise(resolve => {
        setTimeout(() => { resolve(fn(...args)); }, t || 0);
    });
}

/**
 * Format timestamp (in seconds) as "YYYY-mm-dd HH:MM:SS.fff" in local time
 *
 * TODO: move to other module
 *
 * @function
 * @sig Number -> String
 * @param {Number} timestamp
 * @return {String}
 */
function timestampToLocalString(timestamp) {
    const date = new Date(timestamp * 1000);
    const YYYY = String(date.getFullYear()).padStart(4, '0');
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    const HH = String(date.getHours()).padStart(2, '0');
    const MM = String(date.getMinutes()).padStart(2, '0');
    const SS = String(date.getSeconds()).padStart(2, '0');
    const fff = String(date.getMilliseconds()).padStart(3, '0');
    return `${YYYY}-${mm}-${dd} ${HH}:${MM}:${SS}.${fff}`;
}


/***/ }),
/* 3 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "init": () => (/* binding */ init)
/* harmony export */ });
/* harmony import */ var _vnode__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(4);
/* harmony import */ var _is__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(6);
/* harmony import */ var _htmldomapi__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(5);



function isUndef(s) {
    return s === undefined;
}
function isDef(s) {
    return s !== undefined;
}
const emptyNode = (0,_vnode__WEBPACK_IMPORTED_MODULE_0__.vnode)("", {}, [], undefined, undefined);
function sameVnode(vnode1, vnode2) {
    var _a, _b;
    const isSameKey = vnode1.key === vnode2.key;
    const isSameIs = ((_a = vnode1.data) === null || _a === void 0 ? void 0 : _a.is) === ((_b = vnode2.data) === null || _b === void 0 ? void 0 : _b.is);
    const isSameSel = vnode1.sel === vnode2.sel;
    const isSameTextOrFragment = !vnode1.sel && vnode1.sel === vnode2.sel
        ? typeof vnode1.text === typeof vnode2.text
        : true;
    return isSameSel && isSameKey && isSameIs && isSameTextOrFragment;
}
/**
 * @todo Remove this function when the document fragment is considered stable.
 */
function documentFragmentIsNotSupported() {
    throw new Error("The document fragment is not supported on this platform.");
}
function isElement(api, vnode) {
    return api.isElement(vnode);
}
function isDocumentFragment(api, vnode) {
    return api.isDocumentFragment(vnode);
}
function createKeyToOldIdx(children, beginIdx, endIdx) {
    var _a;
    const map = {};
    for (let i = beginIdx; i <= endIdx; ++i) {
        const key = (_a = children[i]) === null || _a === void 0 ? void 0 : _a.key;
        if (key !== undefined) {
            map[key] = i;
        }
    }
    return map;
}
const hooks = [
    "create",
    "update",
    "remove",
    "destroy",
    "pre",
    "post",
];
function init(modules, domApi, options) {
    const cbs = {
        create: [],
        update: [],
        remove: [],
        destroy: [],
        pre: [],
        post: [],
    };
    const api = domApi !== undefined ? domApi : _htmldomapi__WEBPACK_IMPORTED_MODULE_1__.htmlDomApi;
    for (const hook of hooks) {
        for (const module of modules) {
            const currentHook = module[hook];
            if (currentHook !== undefined) {
                cbs[hook].push(currentHook);
            }
        }
    }
    function emptyNodeAt(elm) {
        const id = elm.id ? "#" + elm.id : "";
        // elm.className doesn't return a string when elm is an SVG element inside a shadowRoot.
        // https://stackoverflow.com/questions/29454340/detecting-classname-of-svganimatedstring
        const classes = elm.getAttribute("class");
        const c = classes ? "." + classes.split(" ").join(".") : "";
        return (0,_vnode__WEBPACK_IMPORTED_MODULE_0__.vnode)(api.tagName(elm).toLowerCase() + id + c, {}, [], undefined, elm);
    }
    function emptyDocumentFragmentAt(frag) {
        return (0,_vnode__WEBPACK_IMPORTED_MODULE_0__.vnode)(undefined, {}, [], undefined, frag);
    }
    function createRmCb(childElm, listeners) {
        return function rmCb() {
            if (--listeners === 0) {
                const parent = api.parentNode(childElm);
                api.removeChild(parent, childElm);
            }
        };
    }
    function createElm(vnode, insertedVnodeQueue) {
        var _a, _b, _c, _d;
        let i;
        let data = vnode.data;
        if (data !== undefined) {
            const init = (_a = data.hook) === null || _a === void 0 ? void 0 : _a.init;
            if (isDef(init)) {
                init(vnode);
                data = vnode.data;
            }
        }
        const children = vnode.children;
        const sel = vnode.sel;
        if (sel === "!") {
            if (isUndef(vnode.text)) {
                vnode.text = "";
            }
            vnode.elm = api.createComment(vnode.text);
        }
        else if (sel !== undefined) {
            // Parse selector
            const hashIdx = sel.indexOf("#");
            const dotIdx = sel.indexOf(".", hashIdx);
            const hash = hashIdx > 0 ? hashIdx : sel.length;
            const dot = dotIdx > 0 ? dotIdx : sel.length;
            const tag = hashIdx !== -1 || dotIdx !== -1
                ? sel.slice(0, Math.min(hash, dot))
                : sel;
            const elm = (vnode.elm =
                isDef(data) && isDef((i = data.ns))
                    ? api.createElementNS(i, tag, data)
                    : api.createElement(tag, data));
            if (hash < dot)
                elm.setAttribute("id", sel.slice(hash + 1, dot));
            if (dotIdx > 0)
                elm.setAttribute("class", sel.slice(dot + 1).replace(/\./g, " "));
            for (i = 0; i < cbs.create.length; ++i)
                cbs.create[i](emptyNode, vnode);
            if (_is__WEBPACK_IMPORTED_MODULE_2__.array(children)) {
                for (i = 0; i < children.length; ++i) {
                    const ch = children[i];
                    if (ch != null) {
                        api.appendChild(elm, createElm(ch, insertedVnodeQueue));
                    }
                }
            }
            else if (_is__WEBPACK_IMPORTED_MODULE_2__.primitive(vnode.text)) {
                api.appendChild(elm, api.createTextNode(vnode.text));
            }
            const hook = vnode.data.hook;
            if (isDef(hook)) {
                (_b = hook.create) === null || _b === void 0 ? void 0 : _b.call(hook, emptyNode, vnode);
                if (hook.insert) {
                    insertedVnodeQueue.push(vnode);
                }
            }
        }
        else if (((_c = options === null || options === void 0 ? void 0 : options.experimental) === null || _c === void 0 ? void 0 : _c.fragments) && vnode.children) {
            vnode.elm = ((_d = api.createDocumentFragment) !== null && _d !== void 0 ? _d : documentFragmentIsNotSupported)();
            for (i = 0; i < cbs.create.length; ++i)
                cbs.create[i](emptyNode, vnode);
            for (i = 0; i < vnode.children.length; ++i) {
                const ch = vnode.children[i];
                if (ch != null) {
                    api.appendChild(vnode.elm, createElm(ch, insertedVnodeQueue));
                }
            }
        }
        else {
            vnode.elm = api.createTextNode(vnode.text);
        }
        return vnode.elm;
    }
    function addVnodes(parentElm, before, vnodes, startIdx, endIdx, insertedVnodeQueue) {
        for (; startIdx <= endIdx; ++startIdx) {
            const ch = vnodes[startIdx];
            if (ch != null) {
                api.insertBefore(parentElm, createElm(ch, insertedVnodeQueue), before);
            }
        }
    }
    function invokeDestroyHook(vnode) {
        var _a, _b;
        const data = vnode.data;
        if (data !== undefined) {
            (_b = (_a = data === null || data === void 0 ? void 0 : data.hook) === null || _a === void 0 ? void 0 : _a.destroy) === null || _b === void 0 ? void 0 : _b.call(_a, vnode);
            for (let i = 0; i < cbs.destroy.length; ++i)
                cbs.destroy[i](vnode);
            if (vnode.children !== undefined) {
                for (let j = 0; j < vnode.children.length; ++j) {
                    const child = vnode.children[j];
                    if (child != null && typeof child !== "string") {
                        invokeDestroyHook(child);
                    }
                }
            }
        }
    }
    function removeVnodes(parentElm, vnodes, startIdx, endIdx) {
        var _a, _b;
        for (; startIdx <= endIdx; ++startIdx) {
            let listeners;
            let rm;
            const ch = vnodes[startIdx];
            if (ch != null) {
                if (isDef(ch.sel)) {
                    invokeDestroyHook(ch);
                    listeners = cbs.remove.length + 1;
                    rm = createRmCb(ch.elm, listeners);
                    for (let i = 0; i < cbs.remove.length; ++i)
                        cbs.remove[i](ch, rm);
                    const removeHook = (_b = (_a = ch === null || ch === void 0 ? void 0 : ch.data) === null || _a === void 0 ? void 0 : _a.hook) === null || _b === void 0 ? void 0 : _b.remove;
                    if (isDef(removeHook)) {
                        removeHook(ch, rm);
                    }
                    else {
                        rm();
                    }
                }
                else if (ch.children) {
                    // Fragment node
                    invokeDestroyHook(ch);
                    removeVnodes(parentElm, ch.children, 0, ch.children.length - 1);
                }
                else {
                    // Text node
                    api.removeChild(parentElm, ch.elm);
                }
            }
        }
    }
    function updateChildren(parentElm, oldCh, newCh, insertedVnodeQueue) {
        let oldStartIdx = 0;
        let newStartIdx = 0;
        let oldEndIdx = oldCh.length - 1;
        let oldStartVnode = oldCh[0];
        let oldEndVnode = oldCh[oldEndIdx];
        let newEndIdx = newCh.length - 1;
        let newStartVnode = newCh[0];
        let newEndVnode = newCh[newEndIdx];
        let oldKeyToIdx;
        let idxInOld;
        let elmToMove;
        let before;
        while (oldStartIdx <= oldEndIdx && newStartIdx <= newEndIdx) {
            if (oldStartVnode == null) {
                oldStartVnode = oldCh[++oldStartIdx]; // Vnode might have been moved left
            }
            else if (oldEndVnode == null) {
                oldEndVnode = oldCh[--oldEndIdx];
            }
            else if (newStartVnode == null) {
                newStartVnode = newCh[++newStartIdx];
            }
            else if (newEndVnode == null) {
                newEndVnode = newCh[--newEndIdx];
            }
            else if (sameVnode(oldStartVnode, newStartVnode)) {
                patchVnode(oldStartVnode, newStartVnode, insertedVnodeQueue);
                oldStartVnode = oldCh[++oldStartIdx];
                newStartVnode = newCh[++newStartIdx];
            }
            else if (sameVnode(oldEndVnode, newEndVnode)) {
                patchVnode(oldEndVnode, newEndVnode, insertedVnodeQueue);
                oldEndVnode = oldCh[--oldEndIdx];
                newEndVnode = newCh[--newEndIdx];
            }
            else if (sameVnode(oldStartVnode, newEndVnode)) {
                // Vnode moved right
                patchVnode(oldStartVnode, newEndVnode, insertedVnodeQueue);
                api.insertBefore(parentElm, oldStartVnode.elm, api.nextSibling(oldEndVnode.elm));
                oldStartVnode = oldCh[++oldStartIdx];
                newEndVnode = newCh[--newEndIdx];
            }
            else if (sameVnode(oldEndVnode, newStartVnode)) {
                // Vnode moved left
                patchVnode(oldEndVnode, newStartVnode, insertedVnodeQueue);
                api.insertBefore(parentElm, oldEndVnode.elm, oldStartVnode.elm);
                oldEndVnode = oldCh[--oldEndIdx];
                newStartVnode = newCh[++newStartIdx];
            }
            else {
                if (oldKeyToIdx === undefined) {
                    oldKeyToIdx = createKeyToOldIdx(oldCh, oldStartIdx, oldEndIdx);
                }
                idxInOld = oldKeyToIdx[newStartVnode.key];
                if (isUndef(idxInOld)) {
                    // New element
                    api.insertBefore(parentElm, createElm(newStartVnode, insertedVnodeQueue), oldStartVnode.elm);
                }
                else {
                    elmToMove = oldCh[idxInOld];
                    if (elmToMove.sel !== newStartVnode.sel) {
                        api.insertBefore(parentElm, createElm(newStartVnode, insertedVnodeQueue), oldStartVnode.elm);
                    }
                    else {
                        patchVnode(elmToMove, newStartVnode, insertedVnodeQueue);
                        oldCh[idxInOld] = undefined;
                        api.insertBefore(parentElm, elmToMove.elm, oldStartVnode.elm);
                    }
                }
                newStartVnode = newCh[++newStartIdx];
            }
        }
        if (newStartIdx <= newEndIdx) {
            before = newCh[newEndIdx + 1] == null ? null : newCh[newEndIdx + 1].elm;
            addVnodes(parentElm, before, newCh, newStartIdx, newEndIdx, insertedVnodeQueue);
        }
        if (oldStartIdx <= oldEndIdx) {
            removeVnodes(parentElm, oldCh, oldStartIdx, oldEndIdx);
        }
    }
    function patchVnode(oldVnode, vnode, insertedVnodeQueue) {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        const hook = (_a = vnode.data) === null || _a === void 0 ? void 0 : _a.hook;
        (_b = hook === null || hook === void 0 ? void 0 : hook.prepatch) === null || _b === void 0 ? void 0 : _b.call(hook, oldVnode, vnode);
        const elm = (vnode.elm = oldVnode.elm);
        if (oldVnode === vnode)
            return;
        if (vnode.data !== undefined ||
            (isDef(vnode.text) && vnode.text !== oldVnode.text)) {
            (_c = vnode.data) !== null && _c !== void 0 ? _c : (vnode.data = {});
            (_d = oldVnode.data) !== null && _d !== void 0 ? _d : (oldVnode.data = {});
            for (let i = 0; i < cbs.update.length; ++i)
                cbs.update[i](oldVnode, vnode);
            (_g = (_f = (_e = vnode.data) === null || _e === void 0 ? void 0 : _e.hook) === null || _f === void 0 ? void 0 : _f.update) === null || _g === void 0 ? void 0 : _g.call(_f, oldVnode, vnode);
        }
        const oldCh = oldVnode.children;
        const ch = vnode.children;
        if (isUndef(vnode.text)) {
            if (isDef(oldCh) && isDef(ch)) {
                if (oldCh !== ch)
                    updateChildren(elm, oldCh, ch, insertedVnodeQueue);
            }
            else if (isDef(ch)) {
                if (isDef(oldVnode.text))
                    api.setTextContent(elm, "");
                addVnodes(elm, null, ch, 0, ch.length - 1, insertedVnodeQueue);
            }
            else if (isDef(oldCh)) {
                removeVnodes(elm, oldCh, 0, oldCh.length - 1);
            }
            else if (isDef(oldVnode.text)) {
                api.setTextContent(elm, "");
            }
        }
        else if (oldVnode.text !== vnode.text) {
            if (isDef(oldCh)) {
                removeVnodes(elm, oldCh, 0, oldCh.length - 1);
            }
            api.setTextContent(elm, vnode.text);
        }
        (_h = hook === null || hook === void 0 ? void 0 : hook.postpatch) === null || _h === void 0 ? void 0 : _h.call(hook, oldVnode, vnode);
    }
    return function patch(oldVnode, vnode) {
        let i, elm, parent;
        const insertedVnodeQueue = [];
        for (i = 0; i < cbs.pre.length; ++i)
            cbs.pre[i]();
        if (isElement(api, oldVnode)) {
            oldVnode = emptyNodeAt(oldVnode);
        }
        else if (isDocumentFragment(api, oldVnode)) {
            oldVnode = emptyDocumentFragmentAt(oldVnode);
        }
        if (sameVnode(oldVnode, vnode)) {
            patchVnode(oldVnode, vnode, insertedVnodeQueue);
        }
        else {
            elm = oldVnode.elm;
            parent = api.parentNode(elm);
            createElm(vnode, insertedVnodeQueue);
            if (parent !== null) {
                api.insertBefore(parent, vnode.elm, api.nextSibling(elm));
                removeVnodes(parent, [oldVnode], 0, 0);
            }
        }
        for (i = 0; i < insertedVnodeQueue.length; ++i) {
            insertedVnodeQueue[i].data.hook.insert(insertedVnodeQueue[i]);
        }
        for (i = 0; i < cbs.post.length; ++i)
            cbs.post[i]();
        return vnode;
    };
}
//# sourceMappingURL=init.js.map

/***/ }),
/* 4 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "vnode": () => (/* binding */ vnode)
/* harmony export */ });
function vnode(sel, data, children, text, elm) {
    const key = data === undefined ? undefined : data.key;
    return { sel, data, children, text, elm, key };
}
//# sourceMappingURL=vnode.js.map

/***/ }),
/* 5 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "htmlDomApi": () => (/* binding */ htmlDomApi)
/* harmony export */ });
function createElement(tagName, options) {
    return document.createElement(tagName, options);
}
function createElementNS(namespaceURI, qualifiedName, options) {
    return document.createElementNS(namespaceURI, qualifiedName, options);
}
function createDocumentFragment() {
    return parseFragment(document.createDocumentFragment());
}
function createTextNode(text) {
    return document.createTextNode(text);
}
function createComment(text) {
    return document.createComment(text);
}
function insertBefore(parentNode, newNode, referenceNode) {
    if (isDocumentFragment(parentNode)) {
        let node = parentNode;
        while (node && isDocumentFragment(node)) {
            const fragment = parseFragment(node);
            node = fragment.parent;
        }
        parentNode = node !== null && node !== void 0 ? node : parentNode;
    }
    if (isDocumentFragment(newNode)) {
        newNode = parseFragment(newNode, parentNode);
    }
    if (referenceNode && isDocumentFragment(referenceNode)) {
        referenceNode = parseFragment(referenceNode).firstChildNode;
    }
    parentNode.insertBefore(newNode, referenceNode);
}
function removeChild(node, child) {
    node.removeChild(child);
}
function appendChild(node, child) {
    if (isDocumentFragment(child)) {
        child = parseFragment(child, node);
    }
    node.appendChild(child);
}
function parentNode(node) {
    if (isDocumentFragment(node)) {
        while (node && isDocumentFragment(node)) {
            const fragment = parseFragment(node);
            node = fragment.parent;
        }
        return node !== null && node !== void 0 ? node : null;
    }
    return node.parentNode;
}
function nextSibling(node) {
    var _a;
    if (isDocumentFragment(node)) {
        const fragment = parseFragment(node);
        const parent = parentNode(fragment);
        if (parent && fragment.lastChildNode) {
            const children = Array.from(parent.childNodes);
            const index = children.indexOf(fragment.lastChildNode);
            return (_a = children[index + 1]) !== null && _a !== void 0 ? _a : null;
        }
        return null;
    }
    return node.nextSibling;
}
function tagName(elm) {
    return elm.tagName;
}
function setTextContent(node, text) {
    node.textContent = text;
}
function getTextContent(node) {
    return node.textContent;
}
function isElement(node) {
    return node.nodeType === 1;
}
function isText(node) {
    return node.nodeType === 3;
}
function isComment(node) {
    return node.nodeType === 8;
}
function isDocumentFragment(node) {
    return node.nodeType === 11;
}
function parseFragment(fragmentNode, parentNode) {
    var _a, _b, _c;
    const fragment = fragmentNode;
    (_a = fragment.parent) !== null && _a !== void 0 ? _a : (fragment.parent = parentNode !== null && parentNode !== void 0 ? parentNode : null);
    (_b = fragment.firstChildNode) !== null && _b !== void 0 ? _b : (fragment.firstChildNode = fragmentNode.firstChild);
    (_c = fragment.lastChildNode) !== null && _c !== void 0 ? _c : (fragment.lastChildNode = fragmentNode.lastChild);
    return fragment;
}
const htmlDomApi = {
    createElement,
    createElementNS,
    createTextNode,
    createDocumentFragment,
    createComment,
    insertBefore,
    removeChild,
    appendChild,
    parentNode,
    nextSibling,
    tagName,
    setTextContent,
    getTextContent,
    isElement,
    isText,
    isComment,
    isDocumentFragment,
};
//# sourceMappingURL=htmldomapi.js.map

/***/ }),
/* 6 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "array": () => (/* binding */ array),
/* harmony export */   "primitive": () => (/* binding */ primitive)
/* harmony export */ });
const array = Array.isArray;
function primitive(s) {
    return (typeof s === "string" ||
        typeof s === "number" ||
        s instanceof String ||
        s instanceof Number);
}
//# sourceMappingURL=is.js.map

/***/ }),
/* 7 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "classModule": () => (/* binding */ classModule)
/* harmony export */ });
function updateClass(oldVnode, vnode) {
    let cur;
    let name;
    const elm = vnode.elm;
    let oldClass = oldVnode.data.class;
    let klass = vnode.data.class;
    if (!oldClass && !klass)
        return;
    if (oldClass === klass)
        return;
    oldClass = oldClass || {};
    klass = klass || {};
    for (name in oldClass) {
        if (oldClass[name] && !Object.prototype.hasOwnProperty.call(klass, name)) {
            // was `true` and now not provided
            elm.classList.remove(name);
        }
    }
    for (name in klass) {
        cur = klass[name];
        if (cur !== oldClass[name]) {
            elm.classList[cur ? "add" : "remove"](name);
        }
    }
}
const classModule = { create: updateClass, update: updateClass };
//# sourceMappingURL=class.js.map

/***/ }),
/* 8 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "datasetModule": () => (/* binding */ datasetModule)
/* harmony export */ });
const CAPS_REGEX = /[A-Z]/g;
function updateDataset(oldVnode, vnode) {
    const elm = vnode.elm;
    let oldDataset = oldVnode.data.dataset;
    let dataset = vnode.data.dataset;
    let key;
    if (!oldDataset && !dataset)
        return;
    if (oldDataset === dataset)
        return;
    oldDataset = oldDataset || {};
    dataset = dataset || {};
    const d = elm.dataset;
    for (key in oldDataset) {
        if (!dataset[key]) {
            if (d) {
                if (key in d) {
                    delete d[key];
                }
            }
            else {
                elm.removeAttribute("data-" + key.replace(CAPS_REGEX, "-$&").toLowerCase());
            }
        }
    }
    for (key in dataset) {
        if (oldDataset[key] !== dataset[key]) {
            if (d) {
                d[key] = dataset[key];
            }
            else {
                elm.setAttribute("data-" + key.replace(CAPS_REGEX, "-$&").toLowerCase(), dataset[key]);
            }
        }
    }
}
const datasetModule = {
    create: updateDataset,
    update: updateDataset,
};
//# sourceMappingURL=dataset.js.map

/***/ }),
/* 9 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "eventListenersModule": () => (/* binding */ eventListenersModule)
/* harmony export */ });
function invokeHandler(handler, vnode, event) {
    if (typeof handler === "function") {
        // call function handler
        handler.call(vnode, event, vnode);
    }
    else if (typeof handler === "object") {
        // call multiple handlers
        for (let i = 0; i < handler.length; i++) {
            invokeHandler(handler[i], vnode, event);
        }
    }
}
function handleEvent(event, vnode) {
    const name = event.type;
    const on = vnode.data.on;
    // call event handler(s) if exists
    if (on && on[name]) {
        invokeHandler(on[name], vnode, event);
    }
}
function createListener() {
    return function handler(event) {
        handleEvent(event, handler.vnode);
    };
}
function updateEventListeners(oldVnode, vnode) {
    const oldOn = oldVnode.data.on;
    const oldListener = oldVnode.listener;
    const oldElm = oldVnode.elm;
    const on = vnode && vnode.data.on;
    const elm = (vnode && vnode.elm);
    let name;
    // optimization for reused immutable handlers
    if (oldOn === on) {
        return;
    }
    // remove existing listeners which no longer used
    if (oldOn && oldListener) {
        // if element changed or deleted we remove all existing listeners unconditionally
        if (!on) {
            for (name in oldOn) {
                // remove listener if element was changed or existing listeners removed
                oldElm.removeEventListener(name, oldListener, false);
            }
        }
        else {
            for (name in oldOn) {
                // remove listener if existing listener removed
                if (!on[name]) {
                    oldElm.removeEventListener(name, oldListener, false);
                }
            }
        }
    }
    // add new listeners which has not already attached
    if (on) {
        // reuse existing listener or create new
        const listener = (vnode.listener =
            oldVnode.listener || createListener());
        // update vnode for listener
        listener.vnode = vnode;
        // if element changed or added we add all needed listeners unconditionally
        if (!oldOn) {
            for (name in on) {
                // add listener if element was changed or new listeners added
                elm.addEventListener(name, listener, false);
            }
        }
        else {
            for (name in on) {
                // add listener if new listener added
                if (!oldOn[name]) {
                    elm.addEventListener(name, listener, false);
                }
            }
        }
    }
}
const eventListenersModule = {
    create: updateEventListeners,
    update: updateEventListeners,
    destroy: updateEventListeners,
};
//# sourceMappingURL=eventlisteners.js.map

/***/ }),
/* 10 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "styleModule": () => (/* binding */ styleModule)
/* harmony export */ });
// Bindig `requestAnimationFrame` like this fixes a bug in IE/Edge. See #360 and #409.
const raf = (typeof window !== "undefined" &&
    window.requestAnimationFrame.bind(window)) ||
    setTimeout;
const nextFrame = function (fn) {
    raf(function () {
        raf(fn);
    });
};
let reflowForced = false;
function setNextFrame(obj, prop, val) {
    nextFrame(function () {
        obj[prop] = val;
    });
}
function updateStyle(oldVnode, vnode) {
    let cur;
    let name;
    const elm = vnode.elm;
    let oldStyle = oldVnode.data.style;
    let style = vnode.data.style;
    if (!oldStyle && !style)
        return;
    if (oldStyle === style)
        return;
    oldStyle = oldStyle || {};
    style = style || {};
    const oldHasDel = "delayed" in oldStyle;
    for (name in oldStyle) {
        if (!style[name]) {
            if (name[0] === "-" && name[1] === "-") {
                elm.style.removeProperty(name);
            }
            else {
                elm.style[name] = "";
            }
        }
    }
    for (name in style) {
        cur = style[name];
        if (name === "delayed" && style.delayed) {
            for (const name2 in style.delayed) {
                cur = style.delayed[name2];
                if (!oldHasDel || cur !== oldStyle.delayed[name2]) {
                    setNextFrame(elm.style, name2, cur);
                }
            }
        }
        else if (name !== "remove" && cur !== oldStyle[name]) {
            if (name[0] === "-" && name[1] === "-") {
                elm.style.setProperty(name, cur);
            }
            else {
                elm.style[name] = cur;
            }
        }
    }
}
function applyDestroyStyle(vnode) {
    let style;
    let name;
    const elm = vnode.elm;
    const s = vnode.data.style;
    if (!s || !(style = s.destroy))
        return;
    for (name in style) {
        elm.style[name] = style[name];
    }
}
function applyRemoveStyle(vnode, rm) {
    const s = vnode.data.style;
    if (!s || !s.remove) {
        rm();
        return;
    }
    if (!reflowForced) {
        // eslint-disable-next-line @typescript-eslint/no-unused-expressions
        vnode.elm.offsetLeft;
        reflowForced = true;
    }
    let name;
    const elm = vnode.elm;
    let i = 0;
    const style = s.remove;
    let amount = 0;
    const applied = [];
    for (name in style) {
        applied.push(name);
        elm.style[name] = style[name];
    }
    const compStyle = getComputedStyle(elm);
    const props = compStyle["transition-property"].split(", ");
    for (; i < props.length; ++i) {
        if (applied.indexOf(props[i]) !== -1)
            amount++;
    }
    elm.addEventListener("transitionend", function (ev) {
        if (ev.target === elm)
            --amount;
        if (amount === 0)
            rm();
    });
}
function forceReflow() {
    reflowForced = false;
}
const styleModule = {
    pre: forceReflow,
    create: updateStyle,
    update: updateStyle,
    destroy: applyDestroyStyle,
    remove: applyRemoveStyle,
};
//# sourceMappingURL=style.js.map

/***/ }),
/* 11 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "addNS": () => (/* binding */ addNS),
/* harmony export */   "h": () => (/* binding */ h),
/* harmony export */   "fragment": () => (/* binding */ fragment)
/* harmony export */ });
/* harmony import */ var _vnode__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4);
/* harmony import */ var _is__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(6);


function addNS(data, children, sel) {
    data.ns = "http://www.w3.org/2000/svg";
    if (sel !== "foreignObject" && children !== undefined) {
        for (let i = 0; i < children.length; ++i) {
            const child = children[i];
            if (typeof child === "string")
                continue;
            const childData = child.data;
            if (childData !== undefined) {
                addNS(childData, child.children, child.sel);
            }
        }
    }
}
function h(sel, b, c) {
    let data = {};
    let children;
    let text;
    let i;
    if (c !== undefined) {
        if (b !== null) {
            data = b;
        }
        if (_is__WEBPACK_IMPORTED_MODULE_0__.array(c)) {
            children = c;
        }
        else if (_is__WEBPACK_IMPORTED_MODULE_0__.primitive(c)) {
            text = c.toString();
        }
        else if (c && c.sel) {
            children = [c];
        }
    }
    else if (b !== undefined && b !== null) {
        if (_is__WEBPACK_IMPORTED_MODULE_0__.array(b)) {
            children = b;
        }
        else if (_is__WEBPACK_IMPORTED_MODULE_0__.primitive(b)) {
            text = b.toString();
        }
        else if (b && b.sel) {
            children = [b];
        }
        else {
            data = b;
        }
    }
    if (children !== undefined) {
        for (i = 0; i < children.length; ++i) {
            if (_is__WEBPACK_IMPORTED_MODULE_0__.primitive(children[i]))
                children[i] = (0,_vnode__WEBPACK_IMPORTED_MODULE_1__.vnode)(undefined, undefined, undefined, children[i], undefined);
        }
    }
    if (sel[0] === "s" &&
        sel[1] === "v" &&
        sel[2] === "g" &&
        (sel.length === 3 || sel[3] === "." || sel[3] === "#")) {
        addNS(data, children, sel);
    }
    return (0,_vnode__WEBPACK_IMPORTED_MODULE_1__.vnode)(sel, data, children, text, undefined);
}
/**
 * @experimental
 */
function fragment(children) {
    let c;
    let text;
    if (_is__WEBPACK_IMPORTED_MODULE_0__.array(children)) {
        c = children;
    }
    else if (_is__WEBPACK_IMPORTED_MODULE_0__.primitive(c)) {
        text = children;
    }
    else if (c && c.sel) {
        c = [children];
    }
    if (c !== undefined) {
        for (let i = 0; i < c.length; ++i) {
            if (_is__WEBPACK_IMPORTED_MODULE_0__.primitive(c[i]))
                c[i] = (0,_vnode__WEBPACK_IMPORTED_MODULE_1__.vnode)(undefined, undefined, undefined, c[i], undefined);
        }
    }
    return (0,_vnode__WEBPACK_IMPORTED_MODULE_1__.vnode)(undefined, {}, c, text, undefined);
}
//# sourceMappingURL=h.js.map

/***/ }),
/* 12 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getDefaultAddress": () => (/* binding */ getDefaultAddress),
/* harmony export */   "Connection": () => (/* binding */ Connection),
/* harmony export */   "Application": () => (/* binding */ Application)
/* harmony export */ });
/* harmony import */ var jiff__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(13);
/* harmony import */ var _hat_open_renderer__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(1);
/* harmony import */ var _hat_open_util__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(2);
/* harmony import */ var _hat_open_future__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(27);
/** @module @hat-open/juggler
 */








function getDefaultAddress() {
    const protocol = window.location.protocol == 'https:' ? 'wss' : 'ws';
    const hostname = window.location.hostname || 'localhost';
    const port = window.location.port;
    return `${protocol}://${hostname}` + (port ? `:${port}` : '') + '/ws';
}


/**
 * Juggler client connection
 *
 * Available events:
 *  - open - connection is opened (detail is undefined)
 *  - close - connection is closed (detail is undefined)
 *  - message - received new message (detail is received message)
 *  - change - remote data changed (detail is new remote data)
 */
class Connection extends EventTarget {

    /**
     * Create connection
     * @param {string} address Juggler server address, formatted as
     *     ``ws[s]://<host>[:<port>][/<path>]``. If not provided, hostname
     *     and port obtained from ``widow.location`` are used instead, with
     *     ``ws`` as a path.
     * @param {number} syncDelay sync delay in ms
     * @param {number} pingInterval ping interval in ms
     * @param {number} pongTimeout pong timeout in ms
     */
    constructor(address=getDefaultAddress(), syncDelay=100, pingInterval=5000, pongTimeout=5000) {
        super();
        this._syncDelay = syncDelay;
        this._pingInterval = pingInterval;
        this._pongTimeout = pongTimeout;
        this._localData = null;
        this._remoteData = null;
        this._delayedSyncID = null;
        this._syncedLocalData = null;
        this._pingID = null;
        this._pongID = null;
        this._ws = new WebSocket(address);
        this._ws.addEventListener('open', () => this._onOpen());
        this._ws.addEventListener('close', () => this._onClose());
        this._ws.addEventListener('message', evt => this._onMessage(evt.data));
    }

    /**
     * Local data
     * @type {*}
     */
    get localData() {
        return this._localData;
    }

    /**
     * Remote data
     * @type {*}
     */
    get remoteData() {
        return this._remoteData;
    }

    /**
     * WebSocket ready state
     * @type {number}
     */
    get readyState() {
        return this._ws.readyState;
    }

    /**
     * Close connection
     */
    close() {
        this._ws.close(1000);
    }

    /**
     * Send message
     * @param {*} msg
     */
    send(msg) {
        if (this.readyState != WebSocket.OPEN) {
            throw new Error("connection not open");
        }
        this._ws.send(JSON.stringify({
            type: 'MESSAGE',
            payload: msg
        }));
    }

    /**
     * Set local data
     * @param {*} data
     */
    setLocalData(data) {
        if (this.readyState != WebSocket.OPEN) {
            throw new Error("connection not open");
        }
        this._localData = data;
        if (this._delayedSyncID != null)
            return;
        this._delayedSyncID = setTimeout(
            () => { this._onSync(); },
            this._syncDelay);
    }

    _onOpen() {
        this._pingID = setInterval(() => {
            if (this._pongID != null)
                return;
            this._pongID = setTimeout(() => {
                this.close();
            }, this._pongTimeout);
            this._ws.send(JSON.stringify({
                type: 'PING',
                payload: {}
            }));
        }, this._pingInterval);
        this.dispatchEvent(new CustomEvent('open'));
    }

    _onClose() {
        if (this._delayedSyncID != null) {
            clearTimeout(this._delayedSyncID);
            this._delayedSyncID = null;
        }
        if (this._pingID != null) {
            clearInterval(this._pingID);
            this._pingID = null;
        }
        if (this._pongID != null) {
            clearTimeout(this._pongID);
            this._pongID = null;
        }
        this.dispatchEvent(new CustomEvent('close'));
    }

    _onMessage(data) {
        try {
            const msg = JSON.parse(data);
            if (msg.type == 'DATA') {
                this._remoteData = jiff__WEBPACK_IMPORTED_MODULE_0__.patch(msg.payload, this._remoteData);
                this.dispatchEvent(new CustomEvent('change', {detail: this._remoteData}));
            } else if (msg.type == 'MESSAGE') {
                this.dispatchEvent(new CustomEvent('message', {detail: msg.payload}));
            } else if (msg.type == 'PING') {
                this._ws.send(JSON.stringify({
                    type: 'PONG',
                    payload: {}
                }));
            } else if (msg.type == 'PONG') {
                if (this._pongID != null) {
                    clearTimeout(this._pongID);
                    this._pongID = null;
                }
            } else {
                throw new Error('unsupported message type');
            }
        } catch (e) {
            this._ws.close();
            throw e;
        }
    }

    _onSync() {
        const patch = jiff__WEBPACK_IMPORTED_MODULE_0__.diff(this._syncedLocalData, this._localData);
        if (patch.length > 0) {
            this._ws.send(JSON.stringify({
                type: 'DATA',
                payload: patch
            }));
            this._syncedLocalData = this._localData;
        }
        this._delayedSyncID = null;
    }

}


/**
 * Juggler based application
 *
 * Available events:
 *  - connected - connected to server (detail is undefined)
 *  - disconnected - disconnected from server (detail is undefined)
 *  - message - received new message (detail is received message)
 */
class Application extends EventTarget {

    /**
     * Create application
     * @param {?module:@hat-open/util.Path} localPath local data state path
     * @param {?module:@hat-open/util.Path} remotePath remote data state path
     * @param {object} localRpcCbs local RPC function callbacs
     * @param {module:@hat-open/renderer.Renderer} renderer renderer
     * @param {string} address juggler server address, see
     *     {@link module:@hat-open/juggler.Connection}
     * @param {number} syncDelay sync delay in ms
     * @param {?number} retryDelay connection retry delay in ms, does not
     *     retry if null
     */
    constructor(
        localPath=null,
        remotePath=null,
        localRpcCbs={},
        renderer=_hat_open_renderer__WEBPACK_IMPORTED_MODULE_1__.default,
        address=getDefaultAddress(),
        syncDelay=100,
        pingInterval=5000,
        pongTimeout=5000,
        retryDelay=5000) {

        super();
        this._localPath = localPath;
        this._remotePath = remotePath;
        this._localRpcCbs = localRpcCbs;
        this._renderer = renderer;
        this._address = address;
        this._syncDelay = syncDelay;
        this._pingInterval = pingInterval;
        this._pongTimeout = pongTimeout;
        this._retryDelay = retryDelay;
        this._conn = null;
        this._lastRpcId = 0;
        this._rpcFutures = new Map();
        this._rpc = new Proxy({}, {
            get: (_, action) => (...args) => this._rpcCall(action, args)
        });

        if (localPath != null)
            renderer.addEventListener('change', () => this._onRendererChange());

        _hat_open_util__WEBPACK_IMPORTED_MODULE_2__.delay(() => this._connectLoop());
    }

    /**
     * RPC proxy
     * @type {*}
     */
    get rpc() {
        return this._rpc;
    }

    /**
     * Send message
     * @param {*} msg
     */
    send(msg) {
        if (!this._conn)
            throw new Error("connection closed");
        this._conn.send(msg);
    }

    _onOpen() {
        if (this._localPath)
            this._conn.setLocalData(this._renderer.get(this._localPath));
        this.dispatchEvent(new CustomEvent('connected'));
    }

    _onClose() {
        if (this._remotePath)
            this._renderer.set(this._remotePath, null);
        this.dispatchEvent(new CustomEvent('disconnected'));
    }

    _onMessage(msg) {
        if (_hat_open_util__WEBPACK_IMPORTED_MODULE_2__.isObject(msg) && msg.type == 'rpc') {
            this._onRpcMessage(msg);
        } else {
            this.dispatchEvent(new CustomEvent('message', {detail: msg}));
        }
    }

    _onRpcMessage(msg) {
        if (msg.direction == 'request') {
            this._onRpcReqMessage(msg);
        } else if (msg.direction == 'response') {
            this._onRpcResMessage(msg);
        }
    }

    _onRpcReqMessage(msg) {
        let success;
        let result;
        try {
            result = this._localRpcCbs[msg.action](...msg.args);
            success = true;
        } catch (e) {
            result = String(e);
            success = false;
        }
        this.send({
            type: 'rpc',
            id: msg.id,
            direction: 'response',
            success: success,
            result: result
        });
    }

    _onRpcResMessage(msg) {
        const f = this._rpcFutures.get(msg.id);
        this._rpcFutures.delete(msg.id);
        if (msg.success) {
            f.setResult(msg.result);
        } else {
            f.setError(msg.result);
        }
    }

    _onConnectionChange(data) {
        if (this._remotePath == null)
            return;
        this._renderer.set(this._remotePath, data);
    }

    _onRendererChange() {
        if (!this._conn || this._conn.readyState != WebSocket.OPEN)
            return;
        this._conn.setLocalData(this._renderer.get(this._localPath));
    }

    _rpcCall(action, args) {
        this._lastRpcId += 1;
        this.send({
            type: 'rpc',
            id: this._lastRpcId,
            direction: 'request',
            action: action,
            args: args});
        const f = _hat_open_future__WEBPACK_IMPORTED_MODULE_3__.create();
        this._rpcFutures.set(this._lastRpcId, f);
        return f;
    }

    async _connectLoop() {
        while (true) {
            this._conn = new Connection(this._address, this._syncDelay, this._pingInterval, this._pongTimeout);
            this._conn.addEventListener('open', () => this._onOpen());
            this._conn.addEventListener('close', () => this._onClose());
            this._conn.addEventListener('message', evt => this._onMessage(evt.detail));
            this._conn.addEventListener('change', evt => this._onConnectionChange(evt.detail));

            const closeFuture = _hat_open_future__WEBPACK_IMPORTED_MODULE_3__.create();
            this._conn.addEventListener('close', () => closeFuture.setResult());
            await closeFuture;
            this._conn = null;
            if (this._retryDelay == null) {
                break;
            }
            await _hat_open_util__WEBPACK_IMPORTED_MODULE_2__.sleep(this._retryDelay);
        }
    }

}


/***/ }),
/* 13 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

var lcs = __webpack_require__(14);
var array = __webpack_require__(15);
var patch = __webpack_require__(16);
var inverse = __webpack_require__(26);
var jsonPointer = __webpack_require__(18);
var encodeSegment = jsonPointer.encodeSegment;

exports.diff = diff;
exports.patch = patch.apply;
exports.patchInPlace = patch.applyInPlace;
exports.inverse = inverse;
exports.clone = patch.clone;

// Errors
exports.InvalidPatchOperationError = __webpack_require__(24);
exports.TestFailedError = __webpack_require__(23);
exports.PatchNotInvertibleError = __webpack_require__(25);

var isValidObject = patch.isValidObject;
var defaultHash = patch.defaultHash;

/**
 * Compute a JSON Patch representing the differences between a and b.
 * @param {object|array|string|number|null} a
 * @param {object|array|string|number|null} b
 * @param {?function|?object} options if a function, see options.hash
 * @param {?function(x:*):String|Number} options.hash used to hash array items
 *  in order to recognize identical objects, defaults to JSON.stringify
 * @param {?function(index:Number, array:Array):object} options.makeContext
 *  used to generate patch context. If not provided, context will not be generated
 * @returns {array} JSON Patch such that patch(diff(a, b), a) ~ b
 */
function diff(a, b, options) {
	return appendChanges(a, b, '', initState(options, [])).patch;
}

/**
 * Create initial diff state from the provided options
 * @param {?function|?object} options @see diff options above
 * @param {array} patch an empty or existing JSON Patch array into which
 *  the diff should generate new patch operations
 * @returns {object} initialized diff state
 */
function initState(options, patch) {
	if(typeof options === 'object') {
		return {
			patch: patch,
			hash: orElse(isFunction, options.hash, defaultHash),
			makeContext: orElse(isFunction, options.makeContext, defaultContext),
			invertible: !(options.invertible === false)
		};
	} else {
		return {
			patch: patch,
			hash: orElse(isFunction, options, defaultHash),
			makeContext: defaultContext,
			invertible: true
		};
	}
}

/**
 * Given two JSON values (object, array, number, string, etc.), find their
 * differences and append them to the diff state
 * @param {object|array|string|number|null} a
 * @param {object|array|string|number|null} b
 * @param {string} path
 * @param {object} state
 * @returns {Object} updated diff state
 */
function appendChanges(a, b, path, state) {
	if(Array.isArray(a) && Array.isArray(b)) {
		return appendArrayChanges(a, b, path, state);
	}

	if(isValidObject(a) && isValidObject(b)) {
		return appendObjectChanges(a, b, path, state);
	}

	return appendValueChanges(a, b, path, state);
}

/**
 * Given two objects, find their differences and append them to the diff state
 * @param {object} o1
 * @param {object} o2
 * @param {string} path
 * @param {object} state
 * @returns {Object} updated diff state
 */
function appendObjectChanges(o1, o2, path, state) {
	var keys = Object.keys(o2);
	var patch = state.patch;
	var i, key;

	for(i=keys.length-1; i>=0; --i) {
		key = keys[i];
		var keyPath = path + '/' + encodeSegment(key);
		if(o1[key] !== void 0) {
			appendChanges(o1[key], o2[key], keyPath, state);
		} else {
			patch.push({ op: 'add', path: keyPath, value: o2[key] });
		}
	}

	keys = Object.keys(o1);
	for(i=keys.length-1; i>=0; --i) {
		key = keys[i];
		if(o2[key] === void 0) {
			var p = path + '/' + encodeSegment(key);
			if(state.invertible) {
				patch.push({ op: 'test', path: p, value: o1[key] });
			}
			patch.push({ op: 'remove', path: p });
		}
	}

	return state;
}

/**
 * Given two arrays, find their differences and append them to the diff state
 * @param {array} a1
 * @param {array} a2
 * @param {string} path
 * @param {object} state
 * @returns {Object} updated diff state
 */
function appendArrayChanges(a1, a2, path, state) {
	var a1hash = array.map(state.hash, a1);
	var a2hash = array.map(state.hash, a2);

	var lcsMatrix = lcs.compare(a1hash, a2hash);

	return lcsToJsonPatch(a1, a2, path, state, lcsMatrix);
}

/**
 * Transform an lcsMatrix into JSON Patch operations and append
 * them to state.patch, recursing into array elements as necessary
 * @param {array} a1
 * @param {array} a2
 * @param {string} path
 * @param {object} state
 * @param {object} lcsMatrix
 * @returns {object} new state with JSON Patch operations added based
 *  on the provided lcsMatrix
 */
function lcsToJsonPatch(a1, a2, path, state, lcsMatrix) {
	var offset = 0;
	return lcs.reduce(function(state, op, i, j) {
		var last, context;
		var patch = state.patch;
		var p = path + '/' + (j + offset);

		if (op === lcs.REMOVE) {
			// Coalesce adjacent remove + add into replace
			last = patch[patch.length-1];
			context = state.makeContext(j, a1);

			if(state.invertible) {
				patch.push({ op: 'test', path: p, value: a1[j], context: context });
			}

			if(last !== void 0 && last.op === 'add' && last.path === p) {
				last.op = 'replace';
				last.context = context;
			} else {
				patch.push({ op: 'remove', path: p, context: context });
			}

			offset -= 1;

		} else if (op === lcs.ADD) {
			// See https://tools.ietf.org/html/rfc6902#section-4.1
			// May use either index===length *or* '-' to indicate appending to array
			patch.push({ op: 'add', path: p, value: a2[i],
				context: state.makeContext(j, a1)
			});

			offset += 1;

		} else {
			appendChanges(a1[j], a2[i], p, state);
		}

		return state;

	}, state, lcsMatrix);
}

/**
 * Given two number|string|null values, if they differ, append to diff state
 * @param {string|number|null} a
 * @param {string|number|null} b
 * @param {string} path
 * @param {object} state
 * @returns {object} updated diff state
 */
function appendValueChanges(a, b, path, state) {
	if(a !== b) {
		if(state.invertible) {
			state.patch.push({ op: 'test', path: path, value: a });
		}

		state.patch.push({ op: 'replace', path: path, value: b });
	}

	return state;
}

/**
 * @param {function} predicate
 * @param {*} x
 * @param {*} y
 * @returns {*} x if predicate(x) is truthy, otherwise y
 */
function orElse(predicate, x, y) {
	return predicate(x) ? x : y;
}

/**
 * Default patch context generator
 * @returns {undefined} undefined context
 */
function defaultContext() {
	return void 0;
}

/**
 * @param {*} x
 * @returns {boolean} true if x is a function, false otherwise
 */
function isFunction(x) {
	return typeof x === 'function';
}


/***/ }),
/* 14 */
/***/ ((__unused_webpack_module, exports) => {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

exports.compare = compare;
exports.reduce = reduce;

var REMOVE, RIGHT, ADD, DOWN, SKIP;

exports.REMOVE = REMOVE = RIGHT = -1;
exports.ADD    = ADD    = DOWN  =  1;
exports.EQUAL  = SKIP   = 0;

/**
 * Create an lcs comparison matrix describing the differences
 * between two array-like sequences
 * @param {array} a array-like
 * @param {array} b array-like
 * @returns {object} lcs descriptor, suitable for passing to reduce()
 */
function compare(a, b) {
	var cols = a.length;
	var rows = b.length;

	var prefix = findPrefix(a, b);
	var suffix = prefix < cols && prefix < rows
		? findSuffix(a, b, prefix)
		: 0;

	var remove = suffix + prefix - 1;
	cols -= remove;
	rows -= remove;
	var matrix = createMatrix(cols, rows);

	for (var j = cols - 1; j >= 0; --j) {
		for (var i = rows - 1; i >= 0; --i) {
			matrix[i][j] = backtrack(matrix, a, b, prefix, j, i);
		}
	}

	return {
		prefix: prefix,
		matrix: matrix,
		suffix: suffix
	};
}

/**
 * Reduce a set of lcs changes previously created using compare
 * @param {function(result:*, type:number, i:number, j:number)} f
 *  reducer function, where:
 *  - result is the current reduce value,
 *  - type is the type of change: ADD, REMOVE, or SKIP
 *  - i is the index of the change location in b
 *  - j is the index of the change location in a
 * @param {*} r initial value
 * @param {object} lcs results returned by compare()
 * @returns {*} the final reduced value
 */
function reduce(f, r, lcs) {
	var i, j, k, op;

	var m = lcs.matrix;

	// Reduce shared prefix
	var l = lcs.prefix;
	for(i = 0;i < l; ++i) {
		r = f(r, SKIP, i, i);
	}

	// Reduce longest change span
	k = i;
	l = m.length;
	i = 0;
	j = 0;
	while(i < l) {
		op = m[i][j].type;
		r = f(r, op, i+k, j+k);

		switch(op) {
			case SKIP:  ++i; ++j; break;
			case RIGHT: ++j; break;
			case DOWN:  ++i; break;
		}
	}

	// Reduce shared suffix
	i += k;
	j += k;
	l = lcs.suffix;
	for(k = 0;k < l; ++k) {
		r = f(r, SKIP, i+k, j+k);
	}

	return r;
}

function findPrefix(a, b) {
	var i = 0;
	var l = Math.min(a.length, b.length);
	while(i < l && a[i] === b[i]) {
		++i;
	}
	return i;
}

function findSuffix(a, b) {
	var al = a.length - 1;
	var bl = b.length - 1;
	var l = Math.min(al, bl);
	var i = 0;
	while(i < l && a[al-i] === b[bl-i]) {
		++i;
	}
	return i;
}

function backtrack(matrix, a, b, start, j, i) {
	if (a[j+start] === b[i+start]) {
		return { value: matrix[i + 1][j + 1].value, type: SKIP };
	}
	if (matrix[i][j + 1].value < matrix[i + 1][j].value) {
		return { value: matrix[i][j + 1].value + 1, type: RIGHT };
	}

	return { value: matrix[i + 1][j].value + 1, type: DOWN };
}

function createMatrix (cols, rows) {
	var m = [], i, j, lastrow;

	// Fill the last row
	lastrow = m[rows] = [];
	for (j = 0; j<cols; ++j) {
		lastrow[j] = { value: cols - j, type: RIGHT };
	}

	// Fill the last col
	for (i = 0; i<rows; ++i) {
		m[i] = [];
		m[i][cols] = { value: rows - i, type: DOWN };
	}

	// Fill the last cell
	m[rows][cols] = { value: 0, type: SKIP };

	return m;
}


/***/ }),
/* 15 */
/***/ ((__unused_webpack_module, exports) => {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

exports.cons = cons;
exports.tail = tail;
exports.map = map;

/**
 * Prepend x to a, without mutating a. Faster than a.unshift(x)
 * @param {*} x
 * @param {Array} a array-like
 * @returns {Array} new Array with x prepended
 */
function cons(x, a) {
	var l = a.length;
	var b = new Array(l+1);
	b[0] = x;
	for(var i=0; i<l; ++i) {
		b[i+1] = a[i];
	}

	return b;
}

/**
 * Create a new Array containing all elements in a, except the first.
 *  Faster than a.slice(1)
 * @param {Array} a array-like
 * @returns {Array} new Array, the equivalent of a.slice(1)
 */
function tail(a) {
	var l = a.length-1;
	var b = new Array(l);
	for(var i=0; i<l; ++i) {
		b[i] = a[i+1];
	}

	return b;
}

/**
 * Map any array-like. Faster than Array.prototype.map
 * @param {function} f
 * @param {Array} a array-like
 * @returns {Array} new Array mapped by f
 */
function map(f, a) {
	var b = new Array(a.length);
	for(var i=0; i< a.length; ++i) {
		b[i] = f(a[i]);
	}
	return b;
}

/***/ }),
/* 16 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

var patches = __webpack_require__(17);
var clone = __webpack_require__(20);
var InvalidPatchOperationError = __webpack_require__(24);

exports.apply = patch;
exports.applyInPlace = patchInPlace;
exports.clone = clone;
exports.isValidObject = isValidObject;
exports.defaultHash = defaultHash;

var defaultOptions = {};

/**
 * Apply the supplied JSON Patch to x
 * @param {array} changes JSON Patch
 * @param {object|array|string|number} x object/array/value to patch
 * @param {object} options
 * @param {function(index:Number, array:Array, context:object):Number} options.findContext
 *  function used adjust array indexes for smarty/fuzzy patching, for
 *  patches containing context
 * @returns {object|array|string|number} patched version of x. If x is
 *  an array or object, it will be mutated and returned. Otherwise, if
 *  x is a value, the new value will be returned.
 */
function patch(changes, x, options) {
	return patchInPlace(changes, clone(x), options);
}

function patchInPlace(changes, x, options) {
	if(!options) {
		options = defaultOptions;
	}

	// TODO: Consider throwing if changes is not an array
	if(!Array.isArray(changes)) {
		return x;
	}

	var patch, p;
	for(var i=0; i<changes.length; ++i) {
		p = changes[i];
		patch = patches[p.op];

		if(patch === void 0) {
			throw new InvalidPatchOperationError('invalid op ' + JSON.stringify(p));
		}

		x = patch.apply(x, p, options);
	}

	return x;
}

function defaultHash(x) {
	return isValidObject(x) || isArray(x) ? JSON.stringify(x) : x;
}

function isValidObject (x) {
	return x !== null && Object.prototype.toString.call(x) === '[object Object]';
}

function isArray (x) {
	return Object.prototype.toString.call(x) === '[object Array]';
}


/***/ }),
/* 17 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var jsonPointer = __webpack_require__(18);
var clone = __webpack_require__(20);
var deepEquals = __webpack_require__(21);
var commutePaths = __webpack_require__(22);

var array = __webpack_require__(15);

var TestFailedError = __webpack_require__(23);
var InvalidPatchOperationError = __webpack_require__(24);
var PatchNotInvertibleError = __webpack_require__(25);

var find = jsonPointer.find;
var parseArrayIndex = jsonPointer.parseArrayIndex;

exports.test = {
	apply: applyTest,
	inverse: invertTest,
	commute: commuteTest
};

exports.add = {
	apply: applyAdd,
	inverse: invertAdd,
	commute: commuteAddOrCopy
};

exports.remove = {
	apply: applyRemove,
	inverse: invertRemove,
	commute: commuteRemove
};

exports.replace = {
	apply: applyReplace,
	inverse: invertReplace,
	commute: commuteReplace
};

exports.move = {
	apply: applyMove,
	inverse: invertMove,
	commute: commuteMove
};

exports.copy = {
	apply: applyCopy,
	inverse: notInvertible,
	commute: commuteAddOrCopy
};

/**
 * Apply a test operation to x
 * @param {object|array} x
 * @param {object} test test operation
 * @throws {TestFailedError} if the test operation fails
 */

function applyTest(x, test, options) {
	var pointer = find(x, test.path, options.findContext, test.context);
	var target = pointer.target;
	var index, value;

	if(Array.isArray(target)) {
		index = parseArrayIndex(pointer.key);
		//index = findIndex(options.findContext, index, target, test.context);
		value = target[index];
	} else {
		value = pointer.key === void 0 ? pointer.target : pointer.target[pointer.key];
	}

	if(!deepEquals(value, test.value)) {
		throw new TestFailedError('test failed ' + JSON.stringify(test));
	}

	return x;
}

/**
 * Invert the provided test and add it to the inverted patch sequence
 * @param pr
 * @param test
 * @returns {number}
 */
function invertTest(pr, test) {
	pr.push(test);
	return 1;
}

function commuteTest(test, b) {
	if(test.path === b.path && b.op === 'remove') {
		throw new TypeError('Can\'t commute test,remove -> remove,test for same path');
	}

	if(b.op === 'test' || b.op === 'replace') {
		return [b, test];
	}

	return commutePaths(test, b);
}

/**
 * Apply an add operation to x
 * @param {object|array} x
 * @param {object} change add operation
 */
function applyAdd(x, change, options) {
	var pointer = find(x, change.path, options.findContext, change.context);

	if(notFound(pointer)) {
		throw new InvalidPatchOperationError('path does not exist ' + change.path);
	}

	if(change.value === void 0) {
		throw new InvalidPatchOperationError('missing value');
	}

	var val = clone(change.value);

	// If pointer refers to whole document, replace whole document
	if(pointer.key === void 0) {
		return val;
	}

	_add(pointer, val);
	return x;
}

function _add(pointer, value) {
	var target = pointer.target;

	if(Array.isArray(target)) {
		// '-' indicates 'append' to array
		if(pointer.key === '-') {
			target.push(value);
		} else if (pointer.key > target.length) {
			throw new InvalidPatchOperationError('target of add outside of array bounds')
		} else {
			target.splice(pointer.key, 0, value);
		}
	} else if(isValidObject(target)) {
		target[pointer.key] = value;
	} else {
		throw new InvalidPatchOperationError('target of add must be an object or array ' + pointer.key);
	}
}

function invertAdd(pr, add) {
	var context = add.context;
	if(context !== void 0) {
		context = {
			before: context.before,
			after: array.cons(add.value, context.after)
		}
	}
	pr.push({ op: 'test', path: add.path, value: add.value, context: context });
	pr.push({ op: 'remove', path: add.path, context: context });
	return 1;
}

function commuteAddOrCopy(add, b) {
	if(add.path === b.path && b.op === 'remove') {
		throw new TypeError('Can\'t commute add,remove -> remove,add for same path');
	}

	return commutePaths(add, b);
}

/**
 * Apply a replace operation to x
 * @param {object|array} x
 * @param {object} change replace operation
 */
function applyReplace(x, change, options) {
	var pointer = find(x, change.path, options.findContext, change.context);

	if(notFound(pointer) || missingValue(pointer)) {
		throw new InvalidPatchOperationError('path does not exist ' + change.path);
	}

	if(change.value === void 0) {
		throw new InvalidPatchOperationError('missing value');
	}

	var value = clone(change.value);

	// If pointer refers to whole document, replace whole document
	if(pointer.key === void 0) {
		return value;
	}

	var target = pointer.target;

	if(Array.isArray(target)) {
		target[parseArrayIndex(pointer.key)] = value;
	} else {
		target[pointer.key] = value;
	}

	return x;
}

function invertReplace(pr, c, i, patch) {
	var prev = patch[i-1];
	if(prev === void 0 || prev.op !== 'test' || prev.path !== c.path) {
		throw new PatchNotInvertibleError('cannot invert replace w/o test');
	}

	var context = prev.context;
	if(context !== void 0) {
		context = {
			before: context.before,
			after: array.cons(prev.value, array.tail(context.after))
		}
	}

	pr.push({ op: 'test', path: prev.path, value: c.value });
	pr.push({ op: 'replace', path: prev.path, value: prev.value });
	return 2;
}

function commuteReplace(replace, b) {
	if(replace.path === b.path && b.op === 'remove') {
		throw new TypeError('Can\'t commute replace,remove -> remove,replace for same path');
	}

	if(b.op === 'test' || b.op === 'replace') {
		return [b, replace];
	}

	return commutePaths(replace, b);
}

/**
 * Apply a remove operation to x
 * @param {object|array} x
 * @param {object} change remove operation
 */
function applyRemove(x, change, options) {
	var pointer = find(x, change.path, options.findContext, change.context);

	// key must exist for remove
	if(notFound(pointer) || pointer.target[pointer.key] === void 0) {
		throw new InvalidPatchOperationError('path does not exist ' + change.path);
	}

	_remove(pointer);
	return x;
}

function _remove (pointer) {
	var target = pointer.target;

	var removed;
	if (Array.isArray(target)) {
		removed = target.splice(parseArrayIndex(pointer.key), 1);
		return removed[0];

	} else if (isValidObject(target)) {
		removed = target[pointer.key];
		delete target[pointer.key];
		return removed;

	} else {
		throw new InvalidPatchOperationError('target of remove must be an object or array');
	}
}

function invertRemove(pr, c, i, patch) {
	var prev = patch[i-1];
	if(prev === void 0 || prev.op !== 'test' || prev.path !== c.path) {
		throw new PatchNotInvertibleError('cannot invert remove w/o test');
	}

	var context = prev.context;
	if(context !== void 0) {
		context = {
			before: context.before,
			after: array.tail(context.after)
		}
	}

	pr.push({ op: 'add', path: prev.path, value: prev.value, context: context });
	return 2;
}

function commuteRemove(remove, b) {
	if(remove.path === b.path && b.op === 'remove') {
		return [b, remove];
	}

	return commutePaths(remove, b);
}

/**
 * Apply a move operation to x
 * @param {object|array} x
 * @param {object} change move operation
 */
function applyMove(x, change, options) {
	if(jsonPointer.contains(change.path, change.from)) {
		throw new InvalidPatchOperationError('move.from cannot be ancestor of move.path');
	}

	var pto = find(x, change.path, options.findContext, change.context);
	var pfrom = find(x, change.from, options.findContext, change.fromContext);

	_add(pto, _remove(pfrom));
	return x;
}

function invertMove(pr, c) {
	pr.push({ op: 'move',
		path: c.from, context: c.fromContext,
		from: c.path, fromContext: c.context });
	return 1;
}

function commuteMove(move, b) {
	if(move.path === b.path && b.op === 'remove') {
		throw new TypeError('Can\'t commute move,remove -> move,replace for same path');
	}

	return commutePaths(move, b);
}

/**
 * Apply a copy operation to x
 * @param {object|array} x
 * @param {object} change copy operation
 */
function applyCopy(x, change, options) {
	var pto = find(x, change.path, options.findContext, change.context);
	var pfrom = find(x, change.from, options.findContext, change.fromContext);

	if(notFound(pfrom) || missingValue(pfrom)) {
		throw new InvalidPatchOperationError('copy.from must exist');
	}

	var target = pfrom.target;
	var value;

	if(Array.isArray(target)) {
		value = target[parseArrayIndex(pfrom.key)];
	} else {
		value = target[pfrom.key];
	}

	_add(pto, clone(value));
	return x;
}

// NOTE: Copy is not invertible
// See https://github.com/cujojs/jiff/issues/9
// This needs more thought. We may have to extend/amend JSON Patch.
// At first glance, this seems like it should just be a remove.
// However, that's not correct.  It violates the involution:
// invert(invert(p)) ~= p.  For example:
// invert(copy) -> remove
// invert(remove) -> add
// thus: invert(invert(copy)) -> add (DOH! this should be copy!)

function notInvertible(_, c) {
	throw new PatchNotInvertibleError('cannot invert ' + c.op);
}

function notFound (pointer) {
	return pointer === void 0 || (pointer.target == null && pointer.key !== void 0);
}

function missingValue(pointer) {
	return pointer.key !== void 0 && pointer.target[pointer.key] === void 0;
}

/**
 * Return true if x is a non-null object
 * @param {*} x
 * @returns {boolean}
 */
function isValidObject (x) {
	return x !== null && typeof x === 'object';
}


/***/ }),
/* 18 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

var _parse = __webpack_require__(19);

exports.find = find;
exports.join = join;
exports.absolute = absolute;
exports.parse = parse;
exports.contains = contains;
exports.encodeSegment = encodeSegment;
exports.decodeSegment = decodeSegment;
exports.parseArrayIndex = parseArrayIndex;
exports.isValidArrayIndex = isValidArrayIndex;

// http://tools.ietf.org/html/rfc6901#page-2
var separator = '/';
var separatorRx = /\//g;
var encodedSeparator = '~1';
var encodedSeparatorRx = /~1/g;

var escapeChar = '~';
var escapeRx = /~/g;
var encodedEscape = '~0';
var encodedEscapeRx = /~0/g;

/**
 * Find the parent of the specified path in x and return a descriptor
 * containing the parent and a key.  If the parent does not exist in x,
 * return undefined, instead.
 * @param {object|array} x object or array in which to search
 * @param {string} path JSON Pointer string (encoded)
 * @param {?function(index:Number, array:Array, context:object):Number} findContext
 *  optional function used adjust array indexes for smarty/fuzzy patching, for
 *  patches containing context.  If provided, context MUST also be provided.
 * @param {?{before:Array, after:Array}} context optional patch context for
 *  findContext to use to adjust array indices.  If provided, findContext MUST
 *  also be provided.
 * @returns {{target:object|array|number|string, key:string}|undefined}
 */
function find(x, path, findContext, context) {
	if(typeof path !== 'string') {
		return;
	}

	if(path === '') {
		// whole document
		return { target: x, key: void 0 };
	}

	if(path === separator) {
		return { target: x, key: '' };
	}

	var parent = x, key;
	var hasContext = context !== void 0;

	_parse(path, function(segment) {
		// hm... this seems like it should be if(typeof x === 'undefined')
		if(x == null) {
			// Signal that we prematurely hit the end of the path hierarchy.
			parent = null;
			return false;
		}

		if(Array.isArray(x)) {
			key = hasContext
				? findIndex(findContext, parseArrayIndex(segment), x, context)
				: segment === '-' ? segment : parseArrayIndex(segment);
		} else {
			key = segment;
		}

		parent = x;
		x = x[key];
	});

	return parent === null
		? void 0
		: { target: parent, key: key };
}

function absolute(path) {
	return path[0] === separator ? path : separator + path;
}

function join(segments) {
	return segments.join(separator);
}

function parse(path) {
	var segments = [];
	_parse(path, segments.push.bind(segments));
	return segments;
}

function contains(a, b) {
	return b.indexOf(a) === 0 && b[a.length] === separator;
}

/**
 * Decode a JSON Pointer path segment
 * @see http://tools.ietf.org/html/rfc6901#page-3
 * @param {string} s encoded segment
 * @returns {string} decoded segment
 */
function decodeSegment(s) {
	// See: http://tools.ietf.org/html/rfc6901#page-3
	return s.replace(encodedSeparatorRx, separator).replace(encodedEscapeRx, escapeChar);
}

/**
 * Encode a JSON Pointer path segment
 * @see http://tools.ietf.org/html/rfc6901#page-3
 * @param {string} s decoded segment
 * @returns {string} encoded segment
 */
function encodeSegment(s) {
	return s.replace(escapeRx, encodedEscape).replace(separatorRx, encodedSeparator);
}

var arrayIndexRx = /^(0|[1-9]\d*)$/;

/**
 * Return true if s is a valid JSON Pointer array index
 * @param {String} s
 * @returns {boolean}
 */
function isValidArrayIndex(s) {
	return arrayIndexRx.test(s);
}

/**
 * Safely parse a string into a number >= 0. Does not check for decimal numbers
 * @param {string} s numeric string
 * @returns {number} number >= 0
 */
function parseArrayIndex (s) {
	if(isValidArrayIndex(s)) {
		return +s;
	}

	throw new SyntaxError('invalid array index ' + s);
}

function findIndex (findContext, start, array, context) {
	var index = start;

	if(index < 0) {
		throw new Error('array index out of bounds ' + index);
	}

	if(context !== void 0 && typeof findContext === 'function') {
		index = findContext(start, array, context);
		if(index < 0) {
			throw new Error('could not find patch context ' + context);
		}
	}

	return index;
}

/***/ }),
/* 19 */
/***/ ((module) => {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

module.exports = jsonPointerParse;

var parseRx = /\/|~1|~0/g;
var separator = '/';
var escapeChar = '~';
var encodedSeparator = '~1';

/**
 * Parse through an encoded JSON Pointer string, decoding each path segment
 * and passing it to an onSegment callback function.
 * @see https://tools.ietf.org/html/rfc6901#section-4
 * @param {string} path encoded JSON Pointer string
 * @param {{function(segment:string):boolean}} onSegment callback function
 * @returns {string} original path
 */
function jsonPointerParse(path, onSegment) {
	var pos, accum, matches, match;

	pos = path.charAt(0) === separator ? 1 : 0;
	accum = '';
	parseRx.lastIndex = pos;

	while(matches = parseRx.exec(path)) {

		match = matches[0];
		accum += path.slice(pos, parseRx.lastIndex - match.length);
		pos = parseRx.lastIndex;

		if(match === separator) {
			if (onSegment(accum) === false) return path;
			accum = '';
		} else {
			accum += match === encodedSeparator ? separator : escapeChar;
		}
	}

	accum += path.slice(pos);
	onSegment(accum);

	return path;
}


/***/ }),
/* 20 */
/***/ ((module) => {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

/**
 * Create a deep copy of x which must be a legal JSON object/array/value
 * @param {object|array|string|number|null} x object/array/value to clone
 * @returns {object|array|string|number|null} clone of x
 */
module.exports = clone;

function clone(x) {
	if(x == null || typeof x !== 'object') {
		return x;
	}

	if(Array.isArray(x)) {
		return cloneArray(x);
	}

	return cloneObject(x);
}

function cloneArray (x) {
	var l = x.length;
	var y = new Array(l);

	for (var i = 0; i < l; ++i) {
		y[i] = clone(x[i]);
	}

	return y;
}

function cloneObject (x) {
	var keys = Object.keys(x);
	var y = {};

	for (var k, i = 0, l = keys.length; i < l; ++i) {
		k = keys[i];
		y[k] = clone(x[k]);
	}

	return y;
}


/***/ }),
/* 21 */
/***/ ((module) => {

module.exports = deepEquals;

/**
 * Compare 2 JSON values, or recursively compare 2 JSON objects or arrays
 * @param {object|array|string|number|boolean|null} a
 * @param {object|array|string|number|boolean|null} b
 * @returns {boolean} true iff a and b are recursively equal
 */
function deepEquals(a, b) {
	if(a === b) {
		return true;
	}

	if(Array.isArray(a) && Array.isArray(b)) {
		return compareArrays(a, b);
	}

	if(typeof a === 'object' && typeof b === 'object') {
		return compareObjects(a, b);
	}

	return false;
}

function compareArrays(a, b) {
	if(a.length !== b.length) {
		return false;
	}

	for(var i = 0; i<a.length; ++i) {
		if(!deepEquals(a[i], b[i])) {
			return false;
		}
	}

	return true;
}

function compareObjects(a, b) {
	if((a === null && b !== null) || (a !== null && b === null)) {
		return false;
	}

	var akeys = Object.keys(a);
	var bkeys = Object.keys(b);

	if(akeys.length !== bkeys.length) {
		return false;
	}

	for(var i = 0, k; i<akeys.length; ++i) {
		k = akeys[i];
		if(!(k in b && deepEquals(a[k], b[k]))) {
			return false;
		}
	}

	return true;
}

/***/ }),
/* 22 */
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var jsonPointer = __webpack_require__(18);

/**
 * commute the patch sequence a,b to b,a
 * @param {object} a patch operation
 * @param {object} b patch operation
 */
module.exports = function commutePaths(a, b) {
	// TODO: cases for special paths: '' and '/'
	var left = jsonPointer.parse(a.path);
	var right = jsonPointer.parse(b.path);
	var prefix = getCommonPathPrefix(left, right);
	var isArray = isArrayPath(left, right, prefix.length);

	// Never mutate the originals
	var ac = copyPatch(a);
	var bc = copyPatch(b);

	if(prefix.length === 0 && !isArray) {
		// Paths share no common ancestor, simple swap
		return [bc, ac];
	}

	if(isArray) {
		return commuteArrayPaths(ac, left, bc, right);
	} else {
		return commuteTreePaths(ac, left, bc, right);
	}
};

function commuteTreePaths(a, left, b, right) {
	if(a.path === b.path) {
		throw new TypeError('cannot commute ' + a.op + ',' + b.op + ' with identical object paths');
	}
	// FIXME: Implement tree path commutation
	return [b, a];
}

/**
 * Commute two patches whose common ancestor (which may be the immediate parent)
 * is an array
 * @param a
 * @param left
 * @param b
 * @param right
 * @returns {*}
 */
function commuteArrayPaths(a, left, b, right) {
	if(left.length === right.length) {
		return commuteArraySiblings(a, left, b, right);
	}

	if (left.length > right.length) {
		// left is longer, commute by "moving" it to the right
		left = commuteArrayAncestor(b, right, a, left, -1);
		a.path = jsonPointer.absolute(jsonPointer.join(left));
	} else {
		// right is longer, commute by "moving" it to the left
		right = commuteArrayAncestor(a, left, b, right, 1);
		b.path = jsonPointer.absolute(jsonPointer.join(right));
	}

	return [b, a];
}

function isArrayPath(left, right, index) {
	return jsonPointer.isValidArrayIndex(left[index])
		&& jsonPointer.isValidArrayIndex(right[index]);
}

/**
 * Commute two patches referring to items in the same array
 * @param l
 * @param lpath
 * @param r
 * @param rpath
 * @returns {*[]}
 */
function commuteArraySiblings(l, lpath, r, rpath) {

	var target = lpath.length-1;
	var lindex = +lpath[target];
	var rindex = +rpath[target];

	var commuted;

	if(lindex < rindex) {
		// Adjust right path
		if(l.op === 'add' || l.op === 'copy') {
			commuted = rpath.slice();
			commuted[target] = Math.max(0, rindex - 1);
			r.path = jsonPointer.absolute(jsonPointer.join(commuted));
		} else if(l.op === 'remove') {
			commuted = rpath.slice();
			commuted[target] = rindex + 1;
			r.path = jsonPointer.absolute(jsonPointer.join(commuted));
		}
	} else if(r.op === 'add' || r.op === 'copy') {
		// Adjust left path
		commuted = lpath.slice();
		commuted[target] = lindex + 1;
		l.path = jsonPointer.absolute(jsonPointer.join(commuted));
	} else if (lindex > rindex && r.op === 'remove') {
		// Adjust left path only if remove was at a (strictly) lower index
		commuted = lpath.slice();
		commuted[target] = Math.max(0, lindex - 1);
		l.path = jsonPointer.absolute(jsonPointer.join(commuted));
	}

	return [r, l];
}

/**
 * Commute two patches with a common array ancestor
 * @param l
 * @param lpath
 * @param r
 * @param rpath
 * @param direction
 * @returns {*}
 */
function commuteArrayAncestor(l, lpath, r, rpath, direction) {
	// rpath is longer or same length

	var target = lpath.length-1;
	var lindex = +lpath[target];
	var rindex = +rpath[target];

	// Copy rpath, then adjust its array index
	var rc = rpath.slice();

	if(lindex > rindex) {
		return rc;
	}

	if(l.op === 'add' || l.op === 'copy') {
		rc[target] = Math.max(0, rindex - direction);
	} else if(l.op === 'remove') {
		rc[target] = Math.max(0, rindex + direction);
	}

	return rc;
}

function getCommonPathPrefix(p1, p2) {
	var p1l = p1.length;
	var p2l = p2.length;
	if(p1l === 0 || p2l === 0 || (p1l < 2 && p2l < 2)) {
		return [];
	}

	// If paths are same length, the last segment cannot be part
	// of a common prefix.  If not the same length, the prefix cannot
	// be longer than the shorter path.
	var l = p1l === p2l
		? p1l - 1
		: Math.min(p1l, p2l);

	var i = 0;
	while(i < l && p1[i] === p2[i]) {
		++i
	}

	return p1.slice(0, i);
}

function copyPatch(p) {
	if(p.op === 'remove') {
		return { op: p.op, path: p.path };
	}

	if(p.op === 'copy' || p.op === 'move') {
		return { op: p.op, path: p.path, from: p.from };
	}

	// test, add, replace
	return { op: p.op, path: p.path, value: p.value };
}

/***/ }),
/* 23 */
/***/ ((module) => {

module.exports = TestFailedError;

function TestFailedError(message) {
	Error.call(this);
	this.name = this.constructor.name;
	this.message = message;
	if(typeof Error.captureStackTrace === 'function') {
		Error.captureStackTrace(this, this.constructor);
	}
}

TestFailedError.prototype = Object.create(Error.prototype);
TestFailedError.prototype.constructor = TestFailedError;

/***/ }),
/* 24 */
/***/ ((module) => {

module.exports = InvalidPatchOperationError;

function InvalidPatchOperationError(message) {
	Error.call(this);
	this.name = this.constructor.name;
	this.message = message;
	if(typeof Error.captureStackTrace === 'function') {
		Error.captureStackTrace(this, this.constructor);
	}
}

InvalidPatchOperationError.prototype = Object.create(Error.prototype);
InvalidPatchOperationError.prototype.constructor = InvalidPatchOperationError;

/***/ }),
/* 25 */
/***/ ((module) => {

module.exports = PatchNotInvertibleError;

function PatchNotInvertibleError(message) {
	Error.call(this);
	this.name = this.constructor.name;
	this.message = message;
	if(typeof Error.captureStackTrace === 'function') {
		Error.captureStackTrace(this, this.constructor);
	}
}

PatchNotInvertibleError.prototype = Object.create(Error.prototype);
PatchNotInvertibleError.prototype.constructor = PatchNotInvertibleError;

/***/ }),
/* 26 */
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var patches = __webpack_require__(17);

module.exports = function inverse(p) {
	var pr = [];
	var i, skip;
	for(i = p.length-1; i>= 0; i -= skip) {
		skip = invertOp(pr, p[i], i, p);
	}

	return pr;
};

function invertOp(patch, c, i, context) {
	var op = patches[c.op];
	return op !== void 0 && typeof op.inverse === 'function'
		? op.inverse(patch, c, i, context)
		: 1;
}


/***/ }),
/* 27 */
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "create": () => (/* binding */ create)
/* harmony export */ });
/** @module @hat-open/future
 */


function create() {
    const data = {
        done: false,
        error: false,
        result: undefined,
        resolve: null,
        reject: null
    };

    const future = new Promise((resolve, reject) => {
        data.resolve = resolve;
        data.reject = reject;
        if (data.error) {
            reject(data.result);
        } else if (data.done) {
            resolve(data.resolve);
        }
    });

    future.done = () => data.done;

    future.result = () => {
        if (!data.done)
            throw new Error('future is not done');
        if (data.error)
            throw data.error;
        return data.result;
    };

    future.setResult = result => {
        if (data.done)
            throw new Error('result already set');
        data.result = result;
        data.done = true;
        if (data.resolve)
            data.resolve(data.result);
    };

    future.setError = error => {
        if (data.done)
            throw new Error('result already set');
        data.error = true;
        data.result = error;
        data.done = true;
        if (data.reject)
            data.reject(error);
    };

    return future;
}


/***/ })
/******/ 	]);
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		if(__webpack_module_cache__[moduleId]) {
/******/ 			return __webpack_module_cache__[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be in strict mode.
(() => {
"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _hat_open_renderer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1);
/* harmony import */ var _hat_open_util__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(2);
/* harmony import */ var _hat_open_juggler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(12);





let viewManager = null;


const defaultState = {
    local: {},
    remote: null
};


function main() {
    viewManager = new ViewManager();
    const root = document.body.appendChild(document.createElement('div'));
    _hat_open_renderer__WEBPACK_IMPORTED_MODULE_0__.default.init(root, defaultState, () => viewManager.vt());
    viewManager.app = new _hat_open_juggler__WEBPACK_IMPORTED_MODULE_2__.Application('local', 'remote', {}, _hat_open_renderer__WEBPACK_IMPORTED_MODULE_0__.default,
                                              _hat_open_juggler__WEBPACK_IMPORTED_MODULE_2__.getDefaultAddress(),
                                              100, 5000, 10000, 5000);
    window.viewManager = viewManager;
}


class ViewManager {

    constructor() {
        this._app = null;
        this._view = null;
        this._hat = null;
    }

    get app() {
        return this._app;
    }

    get view() {
        return this._view;
    }

    get hat() {
        return this._hat;
    }

    set app(app) {
        this._app = app;
        if (app) {
            app.addEventListener('message', evt => this._onMessage(evt.detail));
            app.addEventListener('disconnected', _ => this._destroyView());
        }
    }

    vt() {
        if (!this.view)
            return ['div'];
        return this.view.vt();
    }

    _onMessage(msg) {
        if (msg.type == 'state') {
            this._initView(msg);
        } else if (msg.type == 'adapter') {
            if (this.hat) {
                this.hat.conn.addMessage(msg.name, msg.data);
            }
        } else {
            throw new Error(`received invalid message type: ${msg.type}`);
        }
    }

    async _initView(msg) {
        await this._destroyView();
        this._hat = {
            conf: msg.conf,
            reason: msg.reason,
            user: msg.user,
            roles: msg.roles,
            view: msg.view,
            conn: new ViewConnection(this.app)
        };
        const src = _hat_open_util__WEBPACK_IMPORTED_MODULE_1__.get('index.js', msg.view);
        if (!src)
            return;
        const fn = new Function(
            'hat', `var exports = {};\n${src}\nreturn exports;`);
        const view = fn(this.hat);
        if (view.init)
            await view.init();
        this._view = view;
    }

    async _destroyView() {
        if (this.view) {
            if (this.view.destroy)
                await this.view.destroy();
            this._view = null;
            this._hat = null;
        }
        await _hat_open_renderer__WEBPACK_IMPORTED_MODULE_0__.default.set(defaultState);
        _hat_open_renderer__WEBPACK_IMPORTED_MODULE_0__.default.render();
        document.head.querySelectorAll('style').forEach(
            node => node.parentNode.removeChild(node));
    }
}


class ViewConnection {

    constructor(conn) {
        this._conn = conn;
        this._onMessage = null;
    }

    addMessage(adapter, msg) {
        if (this._onMessage) {
            this._onMessage(adapter, msg);
        }
    }

    /**
     * Set on adapter message callback
     * @type {function(string, *)}
     */
    set onMessage(cb) {
        this._onMessage = cb;
    }

    /**
     * Login
     * @param {string} name
     * @param {string} password
     */
    login(name, password) {
        this._conn.send({
            type: 'login',
            name: name,
            password: password
        });
    }

    /**
     * Logout
     */
    logout() {
        this._conn.send({ type: 'logout' });
    }

    /**
     * Send adapter message
     * @param {string} adapter adapter name
     * @param {*} msg message
     */
    send(adapter, msg) {
        this._conn.send({
            type: 'adapter',
            name: adapter,
            data: msg
        });
    }
}


window.addEventListener('load', main);
window.r = _hat_open_renderer__WEBPACK_IMPORTED_MODULE_0__.default;
window.u = _hat_open_util__WEBPACK_IMPORTED_MODULE_1__;

})();

/******/ })()
;
//# sourceMappingURL=main.js.map