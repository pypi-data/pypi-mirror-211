"use strict";
(self["webpackChunkjupyterview"] = self["webpackChunkjupyterview"] || []).push([[169],{

/***/ 8169:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  ICollaborativeDrive: () => (/* reexport */ ICollaborativeDrive),
  WebSocketProvider: () => (/* reexport */ WebSocketProvider),
  YDrive: () => (/* reexport */ YDrive)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@^4.0.0 (singleton)
var apputils_4_0_singleton_ = __webpack_require__(8501);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@^6.0.0 (singleton)
var coreutils_6_0_singleton_ = __webpack_require__(9406);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@^7.0.0 (singleton)
var services_7_0_singleton_ = __webpack_require__(3067);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton)
var coreutils_2_0_singleton_ = __webpack_require__(7930);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton)
var signaling_2_0_singleton_ = __webpack_require__(4901);
// EXTERNAL MODULE: consume shared module (default) yjs@^13.5.40 (singleton)
var consume_shared_module_default_yjs_13_5_singleton_ = __webpack_require__(981);
;// CONCATENATED MODULE: ./node_modules/lib0/map.js
/**
 * Utility module to work with key-value stores.
 *
 * @module map
 */

/**
 * Creates a new Map instance.
 *
 * @function
 * @return {Map<any, any>}
 *
 * @function
 */
const create = () => new Map()

/**
 * Copy a Map object into a fresh Map object.
 *
 * @function
 * @template X,Y
 * @param {Map<X,Y>} m
 * @return {Map<X,Y>}
 */
const copy = m => {
  const r = create()
  m.forEach((v, k) => { r.set(k, v) })
  return r
}

/**
 * Get map property. Create T if property is undefined and set T on map.
 *
 * ```js
 * const listeners = map.setIfUndefined(events, 'eventName', set.create)
 * listeners.add(listener)
 * ```
 *
 * @function
 * @template V,K
 * @template {Map<K,V>} MAP
 * @param {MAP} map
 * @param {K} key
 * @param {function():V} createT
 * @return {V}
 */
const setIfUndefined = (map, key, createT) => {
  let set = map.get(key)
  if (set === undefined) {
    map.set(key, set = createT())
  }
  return set
}

/**
 * Creates an Array and populates it with the content of all key-value pairs using the `f(value, key)` function.
 *
 * @function
 * @template K
 * @template V
 * @template R
 * @param {Map<K,V>} m
 * @param {function(V,K):R} f
 * @return {Array<R>}
 */
const map = (m, f) => {
  const res = []
  for (const [key, value] of m) {
    res.push(f(value, key))
  }
  return res
}

/**
 * Tests whether any key-value pairs pass the test implemented by `f(value, key)`.
 *
 * @todo should rename to some - similarly to Array.some
 *
 * @function
 * @template K
 * @template V
 * @param {Map<K,V>} m
 * @param {function(V,K):boolean} f
 * @return {boolean}
 */
const any = (m, f) => {
  for (const [key, value] of m) {
    if (f(value, key)) {
      return true
    }
  }
  return false
}

/**
 * Tests whether all key-value pairs pass the test implemented by `f(value, key)`.
 *
 * @function
 * @template K
 * @template V
 * @param {Map<K,V>} m
 * @param {function(V,K):boolean} f
 * @return {boolean}
 */
const map_all = (m, f) => {
  for (const [key, value] of m) {
    if (!f(value, key)) {
      return false
    }
  }
  return true
}

;// CONCATENATED MODULE: ./node_modules/lib0/set.js
/**
 * Utility module to work with sets.
 *
 * @module set
 */

const set_create = () => new Set()

/**
 * @template T
 * @param {Set<T>} set
 * @return {Array<T>}
 */
const toArray = set => Array.from(set)

/**
 * @template T
 * @param {Set<T>} set
 * @return {T}
 */
const first = set =>
  set.values().next().value || undefined

/**
 * @template T
 * @param {Iterable<T>} entries
 * @return {Set<T>}
 */
const from = entries => new Set(entries)

;// CONCATENATED MODULE: ./node_modules/lib0/string.js


/**
 * Utility module to work with strings.
 *
 * @module string
 */

const fromCharCode = String.fromCharCode
const fromCodePoint = String.fromCodePoint

/**
 * The largest utf16 character.
 * Corresponds to Uint8Array([255, 255]) or charcodeof(2x2^8)
 */
const MAX_UTF16_CHARACTER = fromCharCode(65535)

/**
 * @param {string} s
 * @return {string}
 */
const toLowerCase = s => s.toLowerCase()

const trimLeftRegex = /^\s*/g

/**
 * @param {string} s
 * @return {string}
 */
const trimLeft = s => s.replace(trimLeftRegex, '')

const fromCamelCaseRegex = /([A-Z])/g

/**
 * @param {string} s
 * @param {string} separator
 * @return {string}
 */
const fromCamelCase = (s, separator) => trimLeft(s.replace(fromCamelCaseRegex, match => `${separator}${toLowerCase(match)}`))

/**
 * Compute the utf8ByteLength
 * @param {string} str
 * @return {number}
 */
const utf8ByteLength = str => unescape(encodeURIComponent(str)).length

/**
 * @param {string} str
 * @return {Uint8Array}
 */
const _encodeUtf8Polyfill = str => {
  const encodedString = unescape(encodeURIComponent(str))
  const len = encodedString.length
  const buf = new Uint8Array(len)
  for (let i = 0; i < len; i++) {
    buf[i] = /** @type {number} */ (encodedString.codePointAt(i))
  }
  return buf
}

/* c8 ignore next */
const utf8TextEncoder = /** @type {TextEncoder} */ (typeof TextEncoder !== 'undefined' ? new TextEncoder() : null)

/**
 * @param {string} str
 * @return {Uint8Array}
 */
const _encodeUtf8Native = str => utf8TextEncoder.encode(str)

/**
 * @param {string} str
 * @return {Uint8Array}
 */
/* c8 ignore next */
const encodeUtf8 = utf8TextEncoder ? _encodeUtf8Native : _encodeUtf8Polyfill

/**
 * @param {Uint8Array} buf
 * @return {string}
 */
const _decodeUtf8Polyfill = buf => {
  let remainingLen = buf.length
  let encodedString = ''
  let bufPos = 0
  while (remainingLen > 0) {
    const nextLen = remainingLen < 10000 ? remainingLen : 10000
    const bytes = buf.subarray(bufPos, bufPos + nextLen)
    bufPos += nextLen
    // Starting with ES5.1 we can supply a generic array-like object as arguments
    encodedString += String.fromCodePoint.apply(null, /** @type {any} */ (bytes))
    remainingLen -= nextLen
  }
  return decodeURIComponent(escape(encodedString))
}

/* c8 ignore next */
let utf8TextDecoder = typeof TextDecoder === 'undefined' ? null : new TextDecoder('utf-8', { fatal: true, ignoreBOM: true })

/* c8 ignore start */
if (utf8TextDecoder && utf8TextDecoder.decode(new Uint8Array()).length === 1) {
  // Safari doesn't handle BOM correctly.
  // This fixes a bug in Safari 13.0.5 where it produces a BOM the first time it is called.
  // utf8TextDecoder.decode(new Uint8Array()).length === 1 on the first call and
  // utf8TextDecoder.decode(new Uint8Array()).length === 1 on the second call
  // Another issue is that from then on no BOM chars are recognized anymore
  /* c8 ignore next */
  utf8TextDecoder = null
}
/* c8 ignore stop */

/**
 * @param {Uint8Array} buf
 * @return {string}
 */
const _decodeUtf8Native = buf => /** @type {TextDecoder} */ (utf8TextDecoder).decode(buf)

/**
 * @param {Uint8Array} buf
 * @return {string}
 */
/* c8 ignore next */
const decodeUtf8 = (/* unused pure expression or super */ null && (utf8TextDecoder ? _decodeUtf8Native : _decodeUtf8Polyfill))

/**
 * @param {string} str The initial string
 * @param {number} index Starting position
 * @param {number} remove Number of characters to remove
 * @param {string} insert New content to insert
 */
const splice = (str, index, remove, insert = '') => str.slice(0, index) + insert + str.slice(index + remove)

/**
 * @param {string} source
 * @param {number} n
 */
const repeat = (source, n) => array.unfold(n, () => source).join('')

;// CONCATENATED MODULE: ./node_modules/lib0/conditions.js
/**
 * Often used conditions.
 *
 * @module conditions
 */

/**
 * @template T
 * @param {T|null|undefined} v
 * @return {T|null}
 */
/* c8 ignore next */
const undefinedToNull = v => v === undefined ? null : v

;// CONCATENATED MODULE: ./node_modules/lib0/storage.js
/* eslint-env browser */

/**
 * Isomorphic variable storage.
 *
 * Uses LocalStorage in the browser and falls back to in-memory storage.
 *
 * @module storage
 */

/* c8 ignore start */
class VarStoragePolyfill {
  constructor () {
    this.map = new Map()
  }

  /**
   * @param {string} key
   * @param {any} newValue
   */
  setItem (key, newValue) {
    this.map.set(key, newValue)
  }

  /**
   * @param {string} key
   */
  getItem (key) {
    return this.map.get(key)
  }
}
/* c8 ignore stop */

/**
 * @type {any}
 */
let _localStorage = new VarStoragePolyfill()
let usePolyfill = true

/* c8 ignore start */
try {
  // if the same-origin rule is violated, accessing localStorage might thrown an error
  if (typeof localStorage !== 'undefined') {
    _localStorage = localStorage
    usePolyfill = false
  }
} catch (e) { }
/* c8 ignore stop */

/**
 * This is basically localStorage in browser, or a polyfill in nodejs
 */
/* c8 ignore next */
const varStorage = _localStorage

/**
 * A polyfill for `addEventListener('storage', event => {..})` that does nothing if the polyfill is being used.
 *
 * @param {function({ key: string, newValue: string, oldValue: string }): void} eventHandler
 * @function
 */
/* c8 ignore next */
const onChange = eventHandler => usePolyfill || addEventListener('storage', /** @type {any} */ (eventHandler))

/**
 * A polyfill for `removeEventListener('storage', event => {..})` that does nothing if the polyfill is being used.
 *
 * @param {function({ key: string, newValue: string, oldValue: string }): void} eventHandler
 * @function
 */
/* c8 ignore next */
const offChange = eventHandler => usePolyfill || removeEventListener('storage', /** @type {any} */ (eventHandler))

;// CONCATENATED MODULE: ./node_modules/lib0/array.js
/**
 * Utility module to work with Arrays.
 *
 * @module array
 */



/**
 * Return the last element of an array. The element must exist
 *
 * @template L
 * @param {ArrayLike<L>} arr
 * @return {L}
 */
const last = arr => arr[arr.length - 1]

/**
 * @template C
 * @return {Array<C>}
 */
const array_create = () => /** @type {Array<C>} */ ([])

/**
 * @template D
 * @param {Array<D>} a
 * @return {Array<D>}
 */
const array_copy = a => /** @type {Array<D>} */ (a.slice())

/**
 * Append elements from src to dest
 *
 * @template M
 * @param {Array<M>} dest
 * @param {Array<M>} src
 */
const appendTo = (dest, src) => {
  for (let i = 0; i < src.length; i++) {
    dest.push(src[i])
  }
}

/**
 * Transforms something array-like to an actual Array.
 *
 * @function
 * @template T
 * @param {ArrayLike<T>|Iterable<T>} arraylike
 * @return {T}
 */
const array_from = Array.from

/**
 * True iff condition holds on every element in the Array.
 *
 * @function
 * @template ITEM
 * @template {ArrayLike<ITEM>} ARR
 *
 * @param {ARR} arr
 * @param {function(ITEM, number, ARR):boolean} f
 * @return {boolean}
 */
const every = (arr, f) => {
  for (let i = 0; i < arr.length; i++) {
    if (!f(arr[i], i, arr)) {
      return false
    }
  }
  return true
}

/**
 * True iff condition holds on some element in the Array.
 *
 * @function
 * @template S
 * @template {ArrayLike<S>} ARR
 * @param {ARR} arr
 * @param {function(S, number, ARR):boolean} f
 * @return {boolean}
 */
const some = (arr, f) => {
  for (let i = 0; i < arr.length; i++) {
    if (f(arr[i], i, arr)) {
      return true
    }
  }
  return false
}

/**
 * @template ELEM
 *
 * @param {ArrayLike<ELEM>} a
 * @param {ArrayLike<ELEM>} b
 * @return {boolean}
 */
const equalFlat = (a, b) => a.length === b.length && every(a, (item, index) => item === b[index])

/**
 * @template ELEM
 * @param {Array<Array<ELEM>>} arr
 * @return {Array<ELEM>}
 */
const flatten = arr => fold(arr, /** @type {Array<ELEM>} */ ([]), (acc, val) => acc.concat(val))

/**
 * @template T
 * @param {number} len
 * @param {function(number, Array<T>):T} f
 * @return {Array<T>}
 */
const unfold = (len, f) => {
  const array = new Array(len)
  for (let i = 0; i < len; i++) {
    array[i] = f(i, array)
  }
  return array
}

/**
 * @template T
 * @template RESULT
 * @param {Array<T>} arr
 * @param {RESULT} seed
 * @param {function(RESULT, T, number):RESULT} folder
 */
const fold = (arr, seed, folder) => arr.reduce(folder, seed)

const isArray = Array.isArray

/**
 * @template T
 * @param {Array<T>} arr
 * @return {Array<T>}
 */
const unique = arr => array_from(set.from(arr))

/**
 * @template T
 * @template M
 * @param {ArrayLike<T>} arr
 * @param {function(T):M} mapper
 * @return {Array<T>}
 */
const uniqueBy = (arr, mapper) => {
  /**
   * @type {Set<M>}
   */
  const happened = set.create()
  /**
   * @type {Array<T>}
   */
  const result = []
  for (let i = 0; i < arr.length; i++) {
    const el = arr[i]
    const mapped = mapper(el)
    if (!happened.has(mapped)) {
      happened.add(mapped)
      result.push(el)
    }
  }
  return result
}

;// CONCATENATED MODULE: ./node_modules/lib0/function.js
/**
 * Common functions and function call helpers.
 *
 * @module function
 */




/**
 * Calls all functions in `fs` with args. Only throws after all functions were called.
 *
 * @param {Array<function>} fs
 * @param {Array<any>} args
 */
const callAll = (fs, args, i = 0) => {
  try {
    for (; i < fs.length; i++) {
      fs[i](...args)
    }
  } finally {
    if (i < fs.length) {
      callAll(fs, args, i + 1)
    }
  }
}

const nop = () => {}

/**
 * @template T
 * @param {function():T} f
 * @return {T}
 */
const apply = f => f()

/**
 * @template A
 *
 * @param {A} a
 * @return {A}
 */
const id = a => a

/**
 * @template T
 *
 * @param {T} a
 * @param {T} b
 * @return {boolean}
 */
const equalityStrict = (a, b) => a === b

/**
 * @template T
 *
 * @param {Array<T>|object} a
 * @param {Array<T>|object} b
 * @return {boolean}
 */
const equalityFlat = (a, b) => a === b || (a != null && b != null && a.constructor === b.constructor && ((array.isArray(a) && array.equalFlat(a, /** @type {Array<T>} */ (b))) || (typeof a === 'object' && object.equalFlat(a, b))))

/* c8 ignore start */

/**
 * @param {any} a
 * @param {any} b
 * @return {boolean}
 */
const equalityDeep = (a, b) => {
  if (a == null || b == null) {
    return equalityStrict(a, b)
  }
  if (a.constructor !== b.constructor) {
    return false
  }
  if (a === b) {
    return true
  }
  switch (a.constructor) {
    case ArrayBuffer:
      a = new Uint8Array(a)
      b = new Uint8Array(b)
    // eslint-disable-next-line no-fallthrough
    case Uint8Array: {
      if (a.byteLength !== b.byteLength) {
        return false
      }
      for (let i = 0; i < a.length; i++) {
        if (a[i] !== b[i]) {
          return false
        }
      }
      break
    }
    case Set: {
      if (a.size !== b.size) {
        return false
      }
      for (const value of a) {
        if (!b.has(value)) {
          return false
        }
      }
      break
    }
    case Map: {
      if (a.size !== b.size) {
        return false
      }
      for (const key of a.keys()) {
        if (!b.has(key) || !equalityDeep(a.get(key), b.get(key))) {
          return false
        }
      }
      break
    }
    case Object:
      if (object.length(a) !== object.length(b)) {
        return false
      }
      for (const key in a) {
        if (!object.hasProperty(a, key) || !equalityDeep(a[key], b[key])) {
          return false
        }
      }
      break
    case Array:
      if (a.length !== b.length) {
        return false
      }
      for (let i = 0; i < a.length; i++) {
        if (!equalityDeep(a[i], b[i])) {
          return false
        }
      }
      break
    default:
      return false
  }
  return true
}

/**
 * @template V
 * @template {V} OPTS
 *
 * @param {V} value
 * @param {Array<OPTS>} options
 */
// @ts-ignore
const isOneOf = (value, options) => options.includes(value)
/* c8 ignore stop */

const function_isArray = isArray

/**
 * @param {any} s
 * @return {s is String}
 */
const isString = (s) => s && s.constructor === String

/**
 * @param {any} n
 * @return {n is Number}
 */
const isNumber = n => n != null && n.constructor === Number

/**
 * @template {abstract new (...args: any) => any} TYPE
 * @param {any} n
 * @param {TYPE} T
 * @return {n is InstanceType<TYPE>}
 */
const is = (n, T) => n && n.constructor === T

/**
 * @template {abstract new (...args: any) => any} TYPE
 * @param {TYPE} T
 */
const isTemplate = (T) =>
  /**
   * @param {any} n
   * @return {n is InstanceType<TYPE>}
   **/
  n => n && n.constructor === T

;// CONCATENATED MODULE: ./node_modules/lib0/environment.js
/* provided dependency */ var process = __webpack_require__(4155);
/**
 * Isomorphic module to work access the environment (query params, env variables).
 *
 * @module map
 */







/* c8 ignore next */
// @ts-ignore
const isNode = typeof process !== 'undefined' && process.release &&
  /node|io\.js/.test(process.release.name)
/* c8 ignore next */
const isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined' && !isNode
/* c8 ignore next 3 */
const isMac = typeof navigator !== 'undefined'
  ? /Mac/.test(navigator.platform)
  : false

/**
 * @type {Map<string,string>}
 */
let params
const args = []

/* c8 ignore start */
const computeParams = () => {
  if (params === undefined) {
    if (isNode) {
      params = create()
      const pargs = process.argv
      let currParamName = null
      for (let i = 0; i < pargs.length; i++) {
        const parg = pargs[i]
        if (parg[0] === '-') {
          if (currParamName !== null) {
            params.set(currParamName, '')
          }
          currParamName = parg
        } else {
          if (currParamName !== null) {
            params.set(currParamName, parg)
            currParamName = null
          } else {
            args.push(parg)
          }
        }
      }
      if (currParamName !== null) {
        params.set(currParamName, '')
      }
      // in ReactNative for example this would not be true (unless connected to the Remote Debugger)
    } else if (typeof location === 'object') {
      params = create(); // eslint-disable-next-line no-undef
      (location.search || '?').slice(1).split('&').forEach((kv) => {
        if (kv.length !== 0) {
          const [key, value] = kv.split('=')
          params.set(`--${fromCamelCase(key, '-')}`, value)
          params.set(`-${fromCamelCase(key, '-')}`, value)
        }
      })
    } else {
      params = create()
    }
  }
  return params
}
/* c8 ignore stop */

/**
 * @param {string} name
 * @return {boolean}
 */
/* c8 ignore next */
const hasParam = (name) => computeParams().has(name)

/**
 * @param {string} name
 * @param {string} defaultVal
 * @return {string}
 */
/* c8 ignore next 2 */
const getParam = (name, defaultVal) =>
  computeParams().get(name) || defaultVal

/**
 * @param {string} name
 * @return {string|null}
 */
/* c8 ignore next 4 */
const getVariable = (name) =>
  isNode
    ? undefinedToNull(process.env[name.toUpperCase()])
    : undefinedToNull(varStorage.getItem(name))

/**
 * @param {string} name
 * @return {string|null}
 */
/* c8 ignore next 2 */
const getConf = (name) =>
  computeParams().get('--' + name) || getVariable(name)

/**
 * @param {string} name
 * @return {boolean}
 */
/* c8 ignore next 2 */
const hasConf = (name) =>
  hasParam('--' + name) || getVariable(name) !== null

/* c8 ignore next */
const production = hasConf('production')

/* c8 ignore next 2 */
const forceColor = isNode &&
  isOneOf(process.env.FORCE_COLOR, ['true', '1', '2'])

/* c8 ignore start */
const supportsColor = !hasParam('no-colors') &&
  (!isNode || process.stdout.isTTY || forceColor) && (
  !isNode || hasParam('color') || forceColor ||
    getVariable('COLORTERM') !== null ||
    (getVariable('TERM') || '').includes('color')
)
/* c8 ignore stop */

;// CONCATENATED MODULE: ./node_modules/lib0/buffer.js
/**
 * Utility functions to work with buffers (Uint8Array).
 *
 * @module buffer
 */






/**
 * @param {number} len
 */
const createUint8ArrayFromLen = len => new Uint8Array(len)

/**
 * Create Uint8Array with initial content from buffer
 *
 * @param {ArrayBuffer} buffer
 * @param {number} byteOffset
 * @param {number} length
 */
const createUint8ArrayViewFromArrayBuffer = (buffer, byteOffset, length) => new Uint8Array(buffer, byteOffset, length)

/**
 * Create Uint8Array with initial content from buffer
 *
 * @param {ArrayBuffer} buffer
 */
const createUint8ArrayFromArrayBuffer = buffer => new Uint8Array(buffer)

/* c8 ignore start */
/**
 * @param {Uint8Array} bytes
 * @return {string}
 */
const toBase64Browser = bytes => {
  let s = ''
  for (let i = 0; i < bytes.byteLength; i++) {
    s += fromCharCode(bytes[i])
  }
  // eslint-disable-next-line no-undef
  return btoa(s)
}
/* c8 ignore stop */

/**
 * @param {Uint8Array} bytes
 * @return {string}
 */
const toBase64Node = bytes => Buffer.from(bytes.buffer, bytes.byteOffset, bytes.byteLength).toString('base64')

/* c8 ignore start */
/**
 * @param {string} s
 * @return {Uint8Array}
 */
const fromBase64Browser = s => {
  // eslint-disable-next-line no-undef
  const a = atob(s)
  const bytes = createUint8ArrayFromLen(a.length)
  for (let i = 0; i < a.length; i++) {
    bytes[i] = a.charCodeAt(i)
  }
  return bytes
}
/* c8 ignore stop */

/**
 * @param {string} s
 */
const fromBase64Node = s => {
  const buf = Buffer.from(s, 'base64')
  return new Uint8Array(buf.buffer, buf.byteOffset, buf.byteLength)
}

/* c8 ignore next */
const toBase64 = isBrowser ? toBase64Browser : toBase64Node

/* c8 ignore next */
const fromBase64 = isBrowser ? fromBase64Browser : fromBase64Node

/**
 * Copy the content of an Uint8Array view to a new ArrayBuffer.
 *
 * @param {Uint8Array} uint8Array
 * @return {Uint8Array}
 */
const copyUint8Array = uint8Array => {
  const newBuf = createUint8ArrayFromLen(uint8Array.byteLength)
  newBuf.set(uint8Array)
  return newBuf
}

/**
 * Encode anything as a UInt8Array. It's a pun on typescripts's `any` type.
 * See encoding.writeAny for more information.
 *
 * @param {any} data
 * @return {Uint8Array}
 */
const encodeAny = data => {
  const encoder = encoding.createEncoder()
  encoding.writeAny(encoder, data)
  return encoding.toUint8Array(encoder)
}

/**
 * Decode an any-encoded value.
 *
 * @param {Uint8Array} buf
 * @return {any}
 */
const decodeAny = buf => decoding.readAny(decoding.createDecoder(buf))

;// CONCATENATED MODULE: ./node_modules/lib0/broadcastchannel.js
/* eslint-env browser */

/**
 * Helpers for cross-tab communication using broadcastchannel with LocalStorage fallback.
 *
 * ```js
 * // In browser window A:
 * broadcastchannel.subscribe('my events', data => console.log(data))
 * broadcastchannel.publish('my events', 'Hello world!') // => A: 'Hello world!' fires synchronously in same tab
 *
 * // In browser window B:
 * broadcastchannel.publish('my events', 'hello from tab B') // => A: 'hello from tab B'
 * ```
 *
 * @module broadcastchannel
 */

// @todo before next major: use Uint8Array instead as buffer object






/**
 * @typedef {Object} Channel
 * @property {Set<function(any, any):any>} Channel.subs
 * @property {any} Channel.bc
 */

/**
 * @type {Map<string, Channel>}
 */
const channels = new Map()

/* c8 ignore start */
class LocalStoragePolyfill {
  /**
   * @param {string} room
   */
  constructor (room) {
    this.room = room
    /**
     * @type {null|function({data:ArrayBuffer}):void}
     */
    this.onmessage = null
    /**
     * @param {any} e
     */
    this._onChange = e => e.key === room && this.onmessage !== null && this.onmessage({ data: fromBase64(e.newValue || '') })
    onChange(this._onChange)
  }

  /**
   * @param {ArrayBuffer} buf
   */
  postMessage (buf) {
    varStorage.setItem(this.room, toBase64(createUint8ArrayFromArrayBuffer(buf)))
  }

  close () {
    offChange(this._onChange)
  }
}
/* c8 ignore stop */

// Use BroadcastChannel or Polyfill
/* c8 ignore next */
const BC = typeof BroadcastChannel === 'undefined' ? LocalStoragePolyfill : BroadcastChannel

/**
 * @param {string} room
 * @return {Channel}
 */
const getChannel = room =>
  setIfUndefined(channels, room, () => {
    const subs = set_create()
    const bc = new BC(room)
    /**
     * @param {{data:ArrayBuffer}} e
     */
    /* c8 ignore next */
    bc.onmessage = e => subs.forEach(sub => sub(e.data, 'broadcastchannel'))
    return {
      bc, subs
    }
  })

/**
 * Subscribe to global `publish` events.
 *
 * @function
 * @param {string} room
 * @param {function(any, any):any} f
 */
const subscribe = (room, f) => {
  getChannel(room).subs.add(f)
  return f
}

/**
 * Unsubscribe from `publish` global events.
 *
 * @function
 * @param {string} room
 * @param {function(any, any):any} f
 */
const unsubscribe = (room, f) => {
  const channel = getChannel(room)
  const unsubscribed = channel.subs.delete(f)
  if (unsubscribed && channel.subs.size === 0) {
    channel.bc.close()
    channels.delete(room)
  }
  return unsubscribed
}

/**
 * Publish data to all subscribers (including subscribers on this tab)
 *
 * @function
 * @param {string} room
 * @param {any} data
 * @param {any} [origin]
 */
const publish = (room, data, origin = null) => {
  const c = getChannel(room)
  c.bc.postMessage(data)
  c.subs.forEach(sub => sub(data, origin))
}

;// CONCATENATED MODULE: ./node_modules/lib0/time.js
/**
 * Utility module to work with time.
 *
 * @module time
 */




/**
 * Return current time.
 *
 * @return {Date}
 */
const getDate = () => new Date()

/**
 * Return current unix time.
 *
 * @return {number}
 */
const getUnixTime = Date.now

/**
 * Transform time (in ms) to a human readable format. E.g. 1100 => 1.1s. 60s => 1min. .001 => 10μs.
 *
 * @param {number} d duration in milliseconds
 * @return {string} humanized approximation of time
 */
const humanizeDuration = d => {
  if (d < 60000) {
    const p = metric.prefix(d, -1)
    return math.round(p.n * 100) / 100 + p.prefix + 's'
  }
  d = math.floor(d / 1000)
  const seconds = d % 60
  const minutes = math.floor(d / 60) % 60
  const hours = math.floor(d / 3600) % 24
  const days = math.floor(d / 86400)
  if (days > 0) {
    return days + 'd' + ((hours > 0 || minutes > 30) ? ' ' + (minutes > 30 ? hours + 1 : hours) + 'h' : '')
  }
  if (hours > 0) {
    /* c8 ignore next */
    return hours + 'h' + ((minutes > 0 || seconds > 30) ? ' ' + (seconds > 30 ? minutes + 1 : minutes) + 'min' : '')
  }
  return minutes + 'min' + (seconds > 0 ? ' ' + seconds + 's' : '')
}

;// CONCATENATED MODULE: ./node_modules/lib0/math.js
/**
 * Common Math expressions.
 *
 * @module math
 */

const floor = Math.floor
const ceil = Math.ceil
const abs = Math.abs
const imul = Math.imul
const round = Math.round
const log10 = Math.log10
const log2 = Math.log2
const log = Math.log
const sqrt = Math.sqrt

/**
 * @function
 * @param {number} a
 * @param {number} b
 * @return {number} The sum of a and b
 */
const add = (a, b) => a + b

/**
 * @function
 * @param {number} a
 * @param {number} b
 * @return {number} The smaller element of a and b
 */
const min = (a, b) => a < b ? a : b

/**
 * @function
 * @param {number} a
 * @param {number} b
 * @return {number} The bigger element of a and b
 */
const max = (a, b) => a > b ? a : b

const math_isNaN = Number.isNaN

const pow = Math.pow
/**
 * Base 10 exponential function. Returns the value of 10 raised to the power of pow.
 *
 * @param {number} exp
 * @return {number}
 */
const exp10 = exp => Math.pow(10, exp)

const sign = Math.sign

/**
 * @param {number} n
 * @return {boolean} Wether n is negative. This function also differentiates between -0 and +0
 */
const isNegativeZero = n => n !== 0 ? n < 0 : 1 / n < 0

;// CONCATENATED MODULE: ./node_modules/lib0/binary.js
/* eslint-env browser */

/**
 * Binary data constants.
 *
 * @module binary
 */

/**
 * n-th bit activated.
 *
 * @type {number}
 */
const BIT1 = 1
const BIT2 = 2
const BIT3 = 4
const BIT4 = 8
const BIT5 = 16
const BIT6 = 32
const BIT7 = 64
const BIT8 = 128
const BIT9 = 256
const BIT10 = 512
const BIT11 = 1024
const BIT12 = 2048
const BIT13 = 4096
const BIT14 = 8192
const BIT15 = 16384
const BIT16 = 32768
const BIT17 = 65536
const BIT18 = 1 << 17
const BIT19 = 1 << 18
const BIT20 = 1 << 19
const BIT21 = 1 << 20
const BIT22 = 1 << 21
const BIT23 = 1 << 22
const BIT24 = 1 << 23
const BIT25 = 1 << 24
const BIT26 = 1 << 25
const BIT27 = 1 << 26
const BIT28 = 1 << 27
const BIT29 = 1 << 28
const BIT30 = 1 << 29
const BIT31 = 1 << 30
const BIT32 = (/* unused pure expression or super */ null && (1 << 31))

/**
 * First n bits activated.
 *
 * @type {number}
 */
const BITS0 = 0
const BITS1 = 1
const BITS2 = 3
const BITS3 = 7
const BITS4 = 15
const BITS5 = 31
const BITS6 = 63
const BITS7 = 127
const BITS8 = 255
const BITS9 = 511
const BITS10 = 1023
const BITS11 = 2047
const BITS12 = 4095
const BITS13 = 8191
const BITS14 = 16383
const BITS15 = 32767
const BITS16 = 65535
const BITS17 = BIT18 - 1
const BITS18 = BIT19 - 1
const BITS19 = BIT20 - 1
const BITS20 = BIT21 - 1
const BITS21 = BIT22 - 1
const BITS22 = BIT23 - 1
const BITS23 = BIT24 - 1
const BITS24 = BIT25 - 1
const BITS25 = BIT26 - 1
const BITS26 = BIT27 - 1
const BITS27 = BIT28 - 1
const BITS28 = BIT29 - 1
const BITS29 = BIT30 - 1
const BITS30 = BIT31 - 1
/**
 * @type {number}
 */
const BITS31 = 0x7FFFFFFF
/**
 * @type {number}
 */
const BITS32 = 0xFFFFFFFF

;// CONCATENATED MODULE: ./node_modules/lib0/encoding.js
/**
 * Efficient schema-less binary encoding with support for variable length encoding.
 *
 * Use [lib0/encoding] with [lib0/decoding]. Every encoding function has a corresponding decoding function.
 *
 * Encodes numbers in little-endian order (least to most significant byte order)
 * and is compatible with Golang's binary encoding (https://golang.org/pkg/encoding/binary/)
 * which is also used in Protocol Buffers.
 *
 * ```js
 * // encoding step
 * const encoder = encoding.createEncoder()
 * encoding.writeVarUint(encoder, 256)
 * encoding.writeVarString(encoder, 'Hello world!')
 * const buf = encoding.toUint8Array(encoder)
 * ```
 *
 * ```js
 * // decoding step
 * const decoder = decoding.createDecoder(buf)
 * decoding.readVarUint(decoder) // => 256
 * decoding.readVarString(decoder) // => 'Hello world!'
 * decoding.hasContent(decoder) // => false - all data is read
 * ```
 *
 * @module encoding
 */








/**
 * A BinaryEncoder handles the encoding to an Uint8Array.
 */
class Encoder {
  constructor () {
    this.cpos = 0
    this.cbuf = new Uint8Array(100)
    /**
     * @type {Array<Uint8Array>}
     */
    this.bufs = []
  }
}

/**
 * @function
 * @return {Encoder}
 */
const createEncoder = () => new Encoder()

/**
 * @param {function(Encoder):void} f
 */
const encode = (f) => {
  const encoder = createEncoder()
  f(encoder)
  return toUint8Array(encoder)
}

/**
 * The current length of the encoded data.
 *
 * @function
 * @param {Encoder} encoder
 * @return {number}
 */
const encoding_length = encoder => {
  let len = encoder.cpos
  for (let i = 0; i < encoder.bufs.length; i++) {
    len += encoder.bufs[i].length
  }
  return len
}

/**
 * Check whether encoder is empty.
 *
 * @function
 * @param {Encoder} encoder
 * @return {boolean}
 */
const hasContent = encoder => encoder.cpos > 0 || encoder.bufs.length > 0

/**
 * Transform to Uint8Array.
 *
 * @function
 * @param {Encoder} encoder
 * @return {Uint8Array} The created ArrayBuffer.
 */
const toUint8Array = encoder => {
  const uint8arr = new Uint8Array(encoding_length(encoder))
  let curPos = 0
  for (let i = 0; i < encoder.bufs.length; i++) {
    const d = encoder.bufs[i]
    uint8arr.set(d, curPos)
    curPos += d.length
  }
  uint8arr.set(createUint8ArrayViewFromArrayBuffer(encoder.cbuf.buffer, 0, encoder.cpos), curPos)
  return uint8arr
}

/**
 * Verify that it is possible to write `len` bytes wtihout checking. If
 * necessary, a new Buffer with the required length is attached.
 *
 * @param {Encoder} encoder
 * @param {number} len
 */
const verifyLen = (encoder, len) => {
  const bufferLen = encoder.cbuf.length
  if (bufferLen - encoder.cpos < len) {
    encoder.bufs.push(buffer.createUint8ArrayViewFromArrayBuffer(encoder.cbuf.buffer, 0, encoder.cpos))
    encoder.cbuf = new Uint8Array(math.max(bufferLen, len) * 2)
    encoder.cpos = 0
  }
}

/**
 * Write one byte to the encoder.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The byte that is to be encoded.
 */
const write = (encoder, num) => {
  const bufferLen = encoder.cbuf.length
  if (encoder.cpos === bufferLen) {
    encoder.bufs.push(encoder.cbuf)
    encoder.cbuf = new Uint8Array(bufferLen * 2)
    encoder.cpos = 0
  }
  encoder.cbuf[encoder.cpos++] = num
}

/**
 * Write one byte at a specific position.
 * Position must already be written (i.e. encoder.length > pos)
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} pos Position to which to write data
 * @param {number} num Unsigned 8-bit integer
 */
const encoding_set = (encoder, pos, num) => {
  let buffer = null
  // iterate all buffers and adjust position
  for (let i = 0; i < encoder.bufs.length && buffer === null; i++) {
    const b = encoder.bufs[i]
    if (pos < b.length) {
      buffer = b // found buffer
    } else {
      pos -= b.length
    }
  }
  if (buffer === null) {
    // use current buffer
    buffer = encoder.cbuf
  }
  buffer[pos] = num
}

/**
 * Write one byte as an unsigned integer.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const writeUint8 = (/* unused pure expression or super */ null && (write))

/**
 * Write one byte as an unsigned Integer at a specific location.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} pos The location where the data will be written.
 * @param {number} num The number that is to be encoded.
 */
const setUint8 = (/* unused pure expression or super */ null && (encoding_set))

/**
 * Write two bytes as an unsigned integer.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const writeUint16 = (encoder, num) => {
  write(encoder, num & binary.BITS8)
  write(encoder, (num >>> 8) & binary.BITS8)
}
/**
 * Write two bytes as an unsigned integer at a specific location.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} pos The location where the data will be written.
 * @param {number} num The number that is to be encoded.
 */
const setUint16 = (encoder, pos, num) => {
  encoding_set(encoder, pos, num & binary.BITS8)
  encoding_set(encoder, pos + 1, (num >>> 8) & binary.BITS8)
}

/**
 * Write two bytes as an unsigned integer
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const writeUint32 = (encoder, num) => {
  for (let i = 0; i < 4; i++) {
    write(encoder, num & binary.BITS8)
    num >>>= 8
  }
}

/**
 * Write two bytes as an unsigned integer in big endian order.
 * (most significant byte first)
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const writeUint32BigEndian = (encoder, num) => {
  for (let i = 3; i >= 0; i--) {
    write(encoder, (num >>> (8 * i)) & binary.BITS8)
  }
}

/**
 * Write two bytes as an unsigned integer at a specific location.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} pos The location where the data will be written.
 * @param {number} num The number that is to be encoded.
 */
const setUint32 = (encoder, pos, num) => {
  for (let i = 0; i < 4; i++) {
    encoding_set(encoder, pos + i, num & binary.BITS8)
    num >>>= 8
  }
}

/**
 * Write a variable length unsigned integer. Max encodable integer is 2^53.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const writeVarUint = (encoder, num) => {
  while (num > BITS7) {
    write(encoder, BIT8 | (BITS7 & num))
    num = floor(num / 128) // shift >>> 7
  }
  write(encoder, BITS7 & num)
}

/**
 * Write a variable length integer.
 *
 * We use the 7th bit instead for signaling that this is a negative number.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const writeVarInt = (encoder, num) => {
  const isNegative = math.isNegativeZero(num)
  if (isNegative) {
    num = -num
  }
  //             |- whether to continue reading         |- whether is negative     |- number
  write(encoder, (num > binary.BITS6 ? binary.BIT8 : 0) | (isNegative ? binary.BIT7 : 0) | (binary.BITS6 & num))
  num = math.floor(num / 64) // shift >>> 6
  // We don't need to consider the case of num === 0 so we can use a different
  // pattern here than above.
  while (num > 0) {
    write(encoder, (num > binary.BITS7 ? binary.BIT8 : 0) | (binary.BITS7 & num))
    num = math.floor(num / 128) // shift >>> 7
  }
}

/**
 * A cache to store strings temporarily
 */
const _strBuffer = new Uint8Array(30000)
const _maxStrBSize = _strBuffer.length / 3

/**
 * Write a variable length string.
 *
 * @function
 * @param {Encoder} encoder
 * @param {String} str The string that is to be encoded.
 */
const _writeVarStringNative = (encoder, str) => {
  if (str.length < _maxStrBSize) {
    // We can encode the string into the existing buffer
    /* c8 ignore next */
    const written = utf8TextEncoder.encodeInto(str, _strBuffer).written || 0
    writeVarUint(encoder, written)
    for (let i = 0; i < written; i++) {
      write(encoder, _strBuffer[i])
    }
  } else {
    writeVarUint8Array(encoder, encodeUtf8(str))
  }
}

/**
 * Write a variable length string.
 *
 * @function
 * @param {Encoder} encoder
 * @param {String} str The string that is to be encoded.
 */
const _writeVarStringPolyfill = (encoder, str) => {
  const encodedString = unescape(encodeURIComponent(str))
  const len = encodedString.length
  writeVarUint(encoder, len)
  for (let i = 0; i < len; i++) {
    write(encoder, /** @type {number} */ (encodedString.codePointAt(i)))
  }
}

/**
 * Write a variable length string.
 *
 * @function
 * @param {Encoder} encoder
 * @param {String} str The string that is to be encoded.
 */
/* c8 ignore next */
const writeVarString = (utf8TextEncoder && /** @type {any} */ utf8TextEncoder.encodeInto) ? _writeVarStringNative : _writeVarStringPolyfill

/**
 * Write a string terminated by a special byte sequence. This is not very performant and is
 * generally discouraged. However, the resulting byte arrays are lexiographically ordered which
 * makes this a nice feature for databases.
 *
 * The string will be encoded using utf8 and then terminated and escaped using writeTerminatingUint8Array.
 *
 * @function
 * @param {Encoder} encoder
 * @param {String} str The string that is to be encoded.
 */
const writeTerminatedString = (encoder, str) =>
  writeTerminatedUint8Array(encoder, string.encodeUtf8(str))

/**
 * Write a terminating Uint8Array. Note that this is not performant and is generally
 * discouraged. There are few situations when this is needed.
 *
 * We use 0x0 as a terminating character. 0x1 serves as an escape character for 0x0 and 0x1.
 *
 * Example: [0,1,2] is encoded to [1,0,1,1,2,0]. 0x0, and 0x1 needed to be escaped using 0x1. Then
 * the result is terminated using the 0x0 character.
 *
 * This is basically how many systems implement null terminated strings. However, we use an escape
 * character 0x1 to avoid issues and potenial attacks on our database (if this is used as a key
 * encoder for NoSql databases).
 *
 * @function
 * @param {Encoder} encoder
 * @param {Uint8Array} buf The string that is to be encoded.
 */
const writeTerminatedUint8Array = (encoder, buf) => {
  for (let i = 0; i < buf.length; i++) {
    const b = buf[i]
    if (b === 0 || b === 1) {
      write(encoder, 1)
    }
    write(encoder, buf[i])
  }
  write(encoder, 0)
}

/**
 * Write the content of another Encoder.
 *
 * @TODO: can be improved!
 *        - Note: Should consider that when appending a lot of small Encoders, we should rather clone than referencing the old structure.
 *                Encoders start with a rather big initial buffer.
 *
 * @function
 * @param {Encoder} encoder The enUint8Arr
 * @param {Encoder} append The BinaryEncoder to be written.
 */
const writeBinaryEncoder = (encoder, append) => writeUint8Array(encoder, toUint8Array(append))

/**
 * Append fixed-length Uint8Array to the encoder.
 *
 * @function
 * @param {Encoder} encoder
 * @param {Uint8Array} uint8Array
 */
const writeUint8Array = (encoder, uint8Array) => {
  const bufferLen = encoder.cbuf.length
  const cpos = encoder.cpos
  const leftCopyLen = min(bufferLen - cpos, uint8Array.length)
  const rightCopyLen = uint8Array.length - leftCopyLen
  encoder.cbuf.set(uint8Array.subarray(0, leftCopyLen), cpos)
  encoder.cpos += leftCopyLen
  if (rightCopyLen > 0) {
    // Still something to write, write right half..
    // Append new buffer
    encoder.bufs.push(encoder.cbuf)
    // must have at least size of remaining buffer
    encoder.cbuf = new Uint8Array(max(bufferLen * 2, rightCopyLen))
    // copy array
    encoder.cbuf.set(uint8Array.subarray(leftCopyLen))
    encoder.cpos = rightCopyLen
  }
}

/**
 * Append an Uint8Array to Encoder.
 *
 * @function
 * @param {Encoder} encoder
 * @param {Uint8Array} uint8Array
 */
const writeVarUint8Array = (encoder, uint8Array) => {
  writeVarUint(encoder, uint8Array.byteLength)
  writeUint8Array(encoder, uint8Array)
}

/**
 * Create an DataView of the next `len` bytes. Use it to write data after
 * calling this function.
 *
 * ```js
 * // write float32 using DataView
 * const dv = writeOnDataView(encoder, 4)
 * dv.setFloat32(0, 1.1)
 * // read float32 using DataView
 * const dv = readFromDataView(encoder, 4)
 * dv.getFloat32(0) // => 1.100000023841858 (leaving it to the reader to find out why this is the correct result)
 * ```
 *
 * @param {Encoder} encoder
 * @param {number} len
 * @return {DataView}
 */
const writeOnDataView = (encoder, len) => {
  verifyLen(encoder, len)
  const dview = new DataView(encoder.cbuf.buffer, encoder.cpos, len)
  encoder.cpos += len
  return dview
}

/**
 * @param {Encoder} encoder
 * @param {number} num
 */
const writeFloat32 = (encoder, num) => writeOnDataView(encoder, 4).setFloat32(0, num, false)

/**
 * @param {Encoder} encoder
 * @param {number} num
 */
const writeFloat64 = (encoder, num) => writeOnDataView(encoder, 8).setFloat64(0, num, false)

/**
 * @param {Encoder} encoder
 * @param {bigint} num
 */
const writeBigInt64 = (encoder, num) => /** @type {any} */ (writeOnDataView(encoder, 8)).setBigInt64(0, num, false)

/**
 * @param {Encoder} encoder
 * @param {bigint} num
 */
const writeBigUint64 = (encoder, num) => /** @type {any} */ (writeOnDataView(encoder, 8)).setBigUint64(0, num, false)

const floatTestBed = new DataView(new ArrayBuffer(4))
/**
 * Check if a number can be encoded as a 32 bit float.
 *
 * @param {number} num
 * @return {boolean}
 */
const isFloat32 = num => {
  floatTestBed.setFloat32(0, num)
  return floatTestBed.getFloat32(0) === num
}

/**
 * Encode data with efficient binary format.
 *
 * Differences to JSON:
 * • Transforms data to a binary format (not to a string)
 * • Encodes undefined, NaN, and ArrayBuffer (these can't be represented in JSON)
 * • Numbers are efficiently encoded either as a variable length integer, as a
 *   32 bit float, as a 64 bit float, or as a 64 bit bigint.
 *
 * Encoding table:
 *
 * | Data Type           | Prefix   | Encoding Method    | Comment |
 * | ------------------- | -------- | ------------------ | ------- |
 * | undefined           | 127      |                    | Functions, symbol, and everything that cannot be identified is encoded as undefined |
 * | null                | 126      |                    | |
 * | integer             | 125      | writeVarInt        | Only encodes 32 bit signed integers |
 * | float32             | 124      | writeFloat32       | |
 * | float64             | 123      | writeFloat64       | |
 * | bigint              | 122      | writeBigInt64      | |
 * | boolean (false)     | 121      |                    | True and false are different data types so we save the following byte |
 * | boolean (true)      | 120      |                    | - 0b01111000 so the last bit determines whether true or false |
 * | string              | 119      | writeVarString     | |
 * | object<string,any>  | 118      | custom             | Writes {length} then {length} key-value pairs |
 * | array<any>          | 117      | custom             | Writes {length} then {length} json values |
 * | Uint8Array          | 116      | writeVarUint8Array | We use Uint8Array for any kind of binary data |
 *
 * Reasons for the decreasing prefix:
 * We need the first bit for extendability (later we may want to encode the
 * prefix with writeVarUint). The remaining 7 bits are divided as follows:
 * [0-30]   the beginning of the data range is used for custom purposes
 *          (defined by the function that uses this library)
 * [31-127] the end of the data range is used for data encoding by
 *          lib0/encoding.js
 *
 * @param {Encoder} encoder
 * @param {undefined|null|number|bigint|boolean|string|Object<string,any>|Array<any>|Uint8Array} data
 */
const writeAny = (encoder, data) => {
  switch (typeof data) {
    case 'string':
      // TYPE 119: STRING
      write(encoder, 119)
      writeVarString(encoder, data)
      break
    case 'number':
      if (number.isInteger(data) && math.abs(data) <= binary.BITS31) {
        // TYPE 125: INTEGER
        write(encoder, 125)
        writeVarInt(encoder, data)
      } else if (isFloat32(data)) {
        // TYPE 124: FLOAT32
        write(encoder, 124)
        writeFloat32(encoder, data)
      } else {
        // TYPE 123: FLOAT64
        write(encoder, 123)
        writeFloat64(encoder, data)
      }
      break
    case 'bigint':
      // TYPE 122: BigInt
      write(encoder, 122)
      writeBigInt64(encoder, data)
      break
    case 'object':
      if (data === null) {
        // TYPE 126: null
        write(encoder, 126)
      } else if (array.isArray(data)) {
        // TYPE 117: Array
        write(encoder, 117)
        writeVarUint(encoder, data.length)
        for (let i = 0; i < data.length; i++) {
          writeAny(encoder, data[i])
        }
      } else if (data instanceof Uint8Array) {
        // TYPE 116: ArrayBuffer
        write(encoder, 116)
        writeVarUint8Array(encoder, data)
      } else {
        // TYPE 118: Object
        write(encoder, 118)
        const keys = Object.keys(data)
        writeVarUint(encoder, keys.length)
        for (let i = 0; i < keys.length; i++) {
          const key = keys[i]
          writeVarString(encoder, key)
          writeAny(encoder, data[key])
        }
      }
      break
    case 'boolean':
      // TYPE 120/121: boolean (true/false)
      write(encoder, data ? 120 : 121)
      break
    default:
      // TYPE 127: undefined
      write(encoder, 127)
  }
}

/**
 * Now come a few stateful encoder that have their own classes.
 */

/**
 * Basic Run Length Encoder - a basic compression implementation.
 *
 * Encodes [1,1,1,7] to [1,3,7,1] (3 times 1, 1 time 7). This encoder might do more harm than good if there are a lot of values that are not repeated.
 *
 * It was originally used for image compression. Cool .. article http://csbruce.com/cbm/transactor/pdfs/trans_v7_i06.pdf
 *
 * @note T must not be null!
 *
 * @template T
 */
class RleEncoder extends (/* unused pure expression or super */ null && (Encoder)) {
  /**
   * @param {function(Encoder, T):void} writer
   */
  constructor (writer) {
    super()
    /**
     * The writer
     */
    this.w = writer
    /**
     * Current state
     * @type {T|null}
     */
    this.s = null
    this.count = 0
  }

  /**
   * @param {T} v
   */
  write (v) {
    if (this.s === v) {
      this.count++
    } else {
      if (this.count > 0) {
        // flush counter, unless this is the first value (count = 0)
        writeVarUint(this, this.count - 1) // since count is always > 0, we can decrement by one. non-standard encoding ftw
      }
      this.count = 1
      // write first value
      this.w(this, v)
      this.s = v
    }
  }
}

/**
 * Basic diff decoder using variable length encoding.
 *
 * Encodes the values [3, 1100, 1101, 1050, 0] to [3, 1097, 1, -51, -1050] using writeVarInt.
 */
class IntDiffEncoder extends (/* unused pure expression or super */ null && (Encoder)) {
  /**
   * @param {number} start
   */
  constructor (start) {
    super()
    /**
     * Current state
     * @type {number}
     */
    this.s = start
  }

  /**
   * @param {number} v
   */
  write (v) {
    writeVarInt(this, v - this.s)
    this.s = v
  }
}

/**
 * A combination of IntDiffEncoder and RleEncoder.
 *
 * Basically first writes the IntDiffEncoder and then counts duplicate diffs using RleEncoding.
 *
 * Encodes the values [1,1,1,2,3,4,5,6] as [1,1,0,2,1,5] (RLE([1,0,0,1,1,1,1,1]) ⇒ RleIntDiff[1,1,0,2,1,5])
 */
class RleIntDiffEncoder extends (/* unused pure expression or super */ null && (Encoder)) {
  /**
   * @param {number} start
   */
  constructor (start) {
    super()
    /**
     * Current state
     * @type {number}
     */
    this.s = start
    this.count = 0
  }

  /**
   * @param {number} v
   */
  write (v) {
    if (this.s === v && this.count > 0) {
      this.count++
    } else {
      if (this.count > 0) {
        // flush counter, unless this is the first value (count = 0)
        writeVarUint(this, this.count - 1) // since count is always > 0, we can decrement by one. non-standard encoding ftw
      }
      this.count = 1
      // write first value
      writeVarInt(this, v - this.s)
      this.s = v
    }
  }
}

/**
 * @param {UintOptRleEncoder} encoder
 */
const flushUintOptRleEncoder = encoder => {
  if (encoder.count > 0) {
    // flush counter, unless this is the first value (count = 0)
    // case 1: just a single value. set sign to positive
    // case 2: write several values. set sign to negative to indicate that there is a length coming
    writeVarInt(encoder.encoder, encoder.count === 1 ? encoder.s : -encoder.s)
    if (encoder.count > 1) {
      writeVarUint(encoder.encoder, encoder.count - 2) // since count is always > 1, we can decrement by one. non-standard encoding ftw
    }
  }
}

/**
 * Optimized Rle encoder that does not suffer from the mentioned problem of the basic Rle encoder.
 *
 * Internally uses VarInt encoder to write unsigned integers. If the input occurs multiple times, we write
 * write it as a negative number. The UintOptRleDecoder then understands that it needs to read a count.
 *
 * Encodes [1,2,3,3,3] as [1,2,-3,3] (once 1, once 2, three times 3)
 */
class UintOptRleEncoder {
  constructor () {
    this.encoder = new Encoder()
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
  }

  /**
   * @param {number} v
   */
  write (v) {
    if (this.s === v) {
      this.count++
    } else {
      flushUintOptRleEncoder(this)
      this.count = 1
      this.s = v
    }
  }

  toUint8Array () {
    flushUintOptRleEncoder(this)
    return toUint8Array(this.encoder)
  }
}

/**
 * Increasing Uint Optimized RLE Encoder
 *
 * The RLE encoder counts the number of same occurences of the same value.
 * The IncUintOptRle encoder counts if the value increases.
 * I.e. 7, 8, 9, 10 will be encoded as [-7, 4]. 1, 3, 5 will be encoded
 * as [1, 3, 5].
 */
class IncUintOptRleEncoder {
  constructor () {
    this.encoder = new Encoder()
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
  }

  /**
   * @param {number} v
   */
  write (v) {
    if (this.s + this.count === v) {
      this.count++
    } else {
      flushUintOptRleEncoder(this)
      this.count = 1
      this.s = v
    }
  }

  toUint8Array () {
    flushUintOptRleEncoder(this)
    return toUint8Array(this.encoder)
  }
}

/**
 * @param {IntDiffOptRleEncoder} encoder
 */
const flushIntDiffOptRleEncoder = encoder => {
  if (encoder.count > 0) {
    //          31 bit making up the diff | wether to write the counter
    // const encodedDiff = encoder.diff << 1 | (encoder.count === 1 ? 0 : 1)
    const encodedDiff = encoder.diff * 2 + (encoder.count === 1 ? 0 : 1)
    // flush counter, unless this is the first value (count = 0)
    // case 1: just a single value. set first bit to positive
    // case 2: write several values. set first bit to negative to indicate that there is a length coming
    writeVarInt(encoder.encoder, encodedDiff)
    if (encoder.count > 1) {
      writeVarUint(encoder.encoder, encoder.count - 2) // since count is always > 1, we can decrement by one. non-standard encoding ftw
    }
  }
}

/**
 * A combination of the IntDiffEncoder and the UintOptRleEncoder.
 *
 * The count approach is similar to the UintDiffOptRleEncoder, but instead of using the negative bitflag, it encodes
 * in the LSB whether a count is to be read. Therefore this Encoder only supports 31 bit integers!
 *
 * Encodes [1, 2, 3, 2] as [3, 1, 6, -1] (more specifically [(1 << 1) | 1, (3 << 0) | 0, -1])
 *
 * Internally uses variable length encoding. Contrary to normal UintVar encoding, the first byte contains:
 * * 1 bit that denotes whether the next value is a count (LSB)
 * * 1 bit that denotes whether this value is negative (MSB - 1)
 * * 1 bit that denotes whether to continue reading the variable length integer (MSB)
 *
 * Therefore, only five bits remain to encode diff ranges.
 *
 * Use this Encoder only when appropriate. In most cases, this is probably a bad idea.
 */
class IntDiffOptRleEncoder {
  constructor () {
    this.encoder = new Encoder()
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
    this.diff = 0
  }

  /**
   * @param {number} v
   */
  write (v) {
    if (this.diff === v - this.s) {
      this.s = v
      this.count++
    } else {
      flushIntDiffOptRleEncoder(this)
      this.count = 1
      this.diff = v - this.s
      this.s = v
    }
  }

  toUint8Array () {
    flushIntDiffOptRleEncoder(this)
    return toUint8Array(this.encoder)
  }
}

/**
 * Optimized String Encoder.
 *
 * Encoding many small strings in a simple Encoder is not very efficient. The function call to decode a string takes some time and creates references that must be eventually deleted.
 * In practice, when decoding several million small strings, the GC will kick in more and more often to collect orphaned string objects (or maybe there is another reason?).
 *
 * This string encoder solves the above problem. All strings are concatenated and written as a single string using a single encoding call.
 *
 * The lengths are encoded using a UintOptRleEncoder.
 */
class StringEncoder {
  constructor () {
    /**
     * @type {Array<string>}
     */
    this.sarr = []
    this.s = ''
    this.lensE = new UintOptRleEncoder()
  }

  /**
   * @param {string} string
   */
  write (string) {
    this.s += string
    if (this.s.length > 19) {
      this.sarr.push(this.s)
      this.s = ''
    }
    this.lensE.write(string.length)
  }

  toUint8Array () {
    const encoder = new Encoder()
    this.sarr.push(this.s)
    this.s = ''
    writeVarString(encoder, this.sarr.join(''))
    writeUint8Array(encoder, this.lensE.toUint8Array())
    return toUint8Array(encoder)
  }
}

;// CONCATENATED MODULE: ./node_modules/lib0/number.js
/**
 * Utility helpers for working with numbers.
 *
 * @module number
 */




const MAX_SAFE_INTEGER = Number.MAX_SAFE_INTEGER
const MIN_SAFE_INTEGER = Number.MIN_SAFE_INTEGER

const LOWEST_INT32 = (/* unused pure expression or super */ null && (1 << 31))
const HIGHEST_INT32 = BITS31
const HIGHEST_UINT32 = BITS32

/* c8 ignore next */
const isInteger = Number.isInteger || (num => typeof num === 'number' && isFinite(num) && floor(num) === num)
const number_isNaN = Number.isNaN
const number_parseInt = Number.parseInt

;// CONCATENATED MODULE: ./node_modules/lib0/error.js
/**
 * Error helpers.
 *
 * @module error
 */

/**
 * @param {string} s
 * @return {Error}
 */
/* c8 ignore next */
const error_create = s => new Error(s)

/**
 * @throws {Error}
 * @return {never}
 */
/* c8 ignore next 3 */
const methodUnimplemented = () => {
  throw error_create('Method unimplemented')
}

/**
 * @throws {Error}
 * @return {never}
 */
/* c8 ignore next 3 */
const unexpectedCase = () => {
  throw error_create('Unexpected case')
}

;// CONCATENATED MODULE: ./node_modules/lib0/decoding.js
/**
 * Efficient schema-less binary decoding with support for variable length encoding.
 *
 * Use [lib0/decoding] with [lib0/encoding]. Every encoding function has a corresponding decoding function.
 *
 * Encodes numbers in little-endian order (least to most significant byte order)
 * and is compatible with Golang's binary encoding (https://golang.org/pkg/encoding/binary/)
 * which is also used in Protocol Buffers.
 *
 * ```js
 * // encoding step
 * const encoder = encoding.createEncoder()
 * encoding.writeVarUint(encoder, 256)
 * encoding.writeVarString(encoder, 'Hello world!')
 * const buf = encoding.toUint8Array(encoder)
 * ```
 *
 * ```js
 * // decoding step
 * const decoder = decoding.createDecoder(buf)
 * decoding.readVarUint(decoder) // => 256
 * decoding.readVarString(decoder) // => 'Hello world!'
 * decoding.hasContent(decoder) // => false - all data is read
 * ```
 *
 * @module decoding
 */









const errorUnexpectedEndOfArray = error_create('Unexpected end of array')
const errorIntegerOutOfRange = error_create('Integer out of Range')

/**
 * A Decoder handles the decoding of an Uint8Array.
 */
class Decoder {
  /**
   * @param {Uint8Array} uint8Array Binary data to decode
   */
  constructor (uint8Array) {
    /**
     * Decoding target.
     *
     * @type {Uint8Array}
     */
    this.arr = uint8Array
    /**
     * Current decoding position.
     *
     * @type {number}
     */
    this.pos = 0
  }
}

/**
 * @function
 * @param {Uint8Array} uint8Array
 * @return {Decoder}
 */
const createDecoder = uint8Array => new Decoder(uint8Array)

/**
 * @function
 * @param {Decoder} decoder
 * @return {boolean}
 */
const decoding_hasContent = decoder => decoder.pos !== decoder.arr.length

/**
 * Clone a decoder instance.
 * Optionally set a new position parameter.
 *
 * @function
 * @param {Decoder} decoder The decoder instance
 * @param {number} [newPos] Defaults to current position
 * @return {Decoder} A clone of `decoder`
 */
const clone = (decoder, newPos = decoder.pos) => {
  const _decoder = createDecoder(decoder.arr)
  _decoder.pos = newPos
  return _decoder
}

/**
 * Create an Uint8Array view of the next `len` bytes and advance the position by `len`.
 *
 * Important: The Uint8Array still points to the underlying ArrayBuffer. Make sure to discard the result as soon as possible to prevent any memory leaks.
 *            Use `buffer.copyUint8Array` to copy the result into a new Uint8Array.
 *
 * @function
 * @param {Decoder} decoder The decoder instance
 * @param {number} len The length of bytes to read
 * @return {Uint8Array}
 */
const readUint8Array = (decoder, len) => {
  const view = createUint8ArrayViewFromArrayBuffer(decoder.arr.buffer, decoder.pos + decoder.arr.byteOffset, len)
  decoder.pos += len
  return view
}

/**
 * Read variable length Uint8Array.
 *
 * Important: The Uint8Array still points to the underlying ArrayBuffer. Make sure to discard the result as soon as possible to prevent any memory leaks.
 *            Use `buffer.copyUint8Array` to copy the result into a new Uint8Array.
 *
 * @function
 * @param {Decoder} decoder
 * @return {Uint8Array}
 */
const readVarUint8Array = decoder => readUint8Array(decoder, readVarUint(decoder))

/**
 * Read the rest of the content as an ArrayBuffer
 * @function
 * @param {Decoder} decoder
 * @return {Uint8Array}
 */
const readTailAsUint8Array = decoder => readUint8Array(decoder, decoder.arr.length - decoder.pos)

/**
 * Skip one byte, jump to the next position.
 * @function
 * @param {Decoder} decoder The decoder instance
 * @return {number} The next position
 */
const skip8 = decoder => decoder.pos++

/**
 * Read one byte as unsigned integer.
 * @function
 * @param {Decoder} decoder The decoder instance
 * @return {number} Unsigned 8-bit integer
 */
const readUint8 = decoder => decoder.arr[decoder.pos++]

/**
 * Read 2 bytes as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const readUint16 = decoder => {
  const uint =
    decoder.arr[decoder.pos] +
    (decoder.arr[decoder.pos + 1] << 8)
  decoder.pos += 2
  return uint
}

/**
 * Read 4 bytes as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const readUint32 = decoder => {
  const uint =
    (decoder.arr[decoder.pos] +
    (decoder.arr[decoder.pos + 1] << 8) +
    (decoder.arr[decoder.pos + 2] << 16) +
    (decoder.arr[decoder.pos + 3] << 24)) >>> 0
  decoder.pos += 4
  return uint
}

/**
 * Read 4 bytes as unsigned integer in big endian order.
 * (most significant byte first)
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const readUint32BigEndian = decoder => {
  const uint =
    (decoder.arr[decoder.pos + 3] +
    (decoder.arr[decoder.pos + 2] << 8) +
    (decoder.arr[decoder.pos + 1] << 16) +
    (decoder.arr[decoder.pos] << 24)) >>> 0
  decoder.pos += 4
  return uint
}

/**
 * Look ahead without incrementing the position
 * to the next byte and read it as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const peekUint8 = decoder => decoder.arr[decoder.pos]

/**
 * Look ahead without incrementing the position
 * to the next byte and read it as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const peekUint16 = decoder =>
  decoder.arr[decoder.pos] +
  (decoder.arr[decoder.pos + 1] << 8)

/**
 * Look ahead without incrementing the position
 * to the next byte and read it as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const peekUint32 = decoder => (
  decoder.arr[decoder.pos] +
  (decoder.arr[decoder.pos + 1] << 8) +
  (decoder.arr[decoder.pos + 2] << 16) +
  (decoder.arr[decoder.pos + 3] << 24)
) >>> 0

/**
 * Read unsigned integer (32bit) with variable length.
 * 1/8th of the storage is used as encoding overhead.
 *  * numbers < 2^7 is stored in one bytlength
 *  * numbers < 2^14 is stored in two bylength
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.length
 */
const readVarUint = decoder => {
  let num = 0
  let mult = 1
  const len = decoder.arr.length
  while (decoder.pos < len) {
    const r = decoder.arr[decoder.pos++]
    // num = num | ((r & binary.BITS7) << len)
    num = num + (r & BITS7) * mult // shift $r << (7*#iterations) and add it to num
    mult *= 128 // next iteration, shift 7 "more" to the left
    if (r < BIT8) {
      return num
    }
    /* c8 ignore start */
    if (num > MAX_SAFE_INTEGER) {
      throw errorIntegerOutOfRange
    }
    /* c8 ignore stop */
  }
  throw errorUnexpectedEndOfArray
}

/**
 * Read signed integer (32bit) with variable length.
 * 1/8th of the storage is used as encoding overhead.
 *  * numbers < 2^7 is stored in one bytlength
 *  * numbers < 2^14 is stored in two bylength
 * @todo This should probably create the inverse ~num if number is negative - but this would be a breaking change.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.length
 */
const readVarInt = decoder => {
  let r = decoder.arr[decoder.pos++]
  let num = r & BITS6
  let mult = 64
  const sign = (r & BIT7) > 0 ? -1 : 1
  if ((r & BIT8) === 0) {
    // don't continue reading
    return sign * num
  }
  const len = decoder.arr.length
  while (decoder.pos < len) {
    r = decoder.arr[decoder.pos++]
    // num = num | ((r & binary.BITS7) << len)
    num = num + (r & BITS7) * mult
    mult *= 128
    if (r < BIT8) {
      return sign * num
    }
    /* c8 ignore start */
    if (num > MAX_SAFE_INTEGER) {
      throw errorIntegerOutOfRange
    }
    /* c8 ignore stop */
  }
  throw errorUnexpectedEndOfArray
}

/**
 * Look ahead and read varUint without incrementing position
 *
 * @function
 * @param {Decoder} decoder
 * @return {number}
 */
const peekVarUint = decoder => {
  const pos = decoder.pos
  const s = readVarUint(decoder)
  decoder.pos = pos
  return s
}

/**
 * Look ahead and read varUint without incrementing position
 *
 * @function
 * @param {Decoder} decoder
 * @return {number}
 */
const peekVarInt = decoder => {
  const pos = decoder.pos
  const s = readVarInt(decoder)
  decoder.pos = pos
  return s
}

/**
 * We don't test this function anymore as we use native decoding/encoding by default now.
 * Better not modify this anymore..
 *
 * Transforming utf8 to a string is pretty expensive. The code performs 10x better
 * when String.fromCodePoint is fed with all characters as arguments.
 * But most environments have a maximum number of arguments per functions.
 * For effiency reasons we apply a maximum of 10000 characters at once.
 *
 * @function
 * @param {Decoder} decoder
 * @return {String} The read String.
 */
/* c8 ignore start */
const _readVarStringPolyfill = decoder => {
  let remainingLen = readVarUint(decoder)
  if (remainingLen === 0) {
    return ''
  } else {
    let encodedString = String.fromCodePoint(readUint8(decoder)) // remember to decrease remainingLen
    if (--remainingLen < 100) { // do not create a Uint8Array for small strings
      while (remainingLen--) {
        encodedString += String.fromCodePoint(readUint8(decoder))
      }
    } else {
      while (remainingLen > 0) {
        const nextLen = remainingLen < 10000 ? remainingLen : 10000
        // this is dangerous, we create a fresh array view from the existing buffer
        const bytes = decoder.arr.subarray(decoder.pos, decoder.pos + nextLen)
        decoder.pos += nextLen
        // Starting with ES5.1 we can supply a generic array-like object as arguments
        encodedString += String.fromCodePoint.apply(null, /** @type {any} */ (bytes))
        remainingLen -= nextLen
      }
    }
    return decodeURIComponent(escape(encodedString))
  }
}
/* c8 ignore stop */

/**
 * @function
 * @param {Decoder} decoder
 * @return {String} The read String
 */
const _readVarStringNative = decoder =>
  /** @type any */ utf8TextDecoder.decode(readVarUint8Array(decoder))

/**
 * Read string of variable length
 * * varUint is used to store the length of the string
 *
 * @function
 * @param {Decoder} decoder
 * @return {String} The read String
 *
 */
/* c8 ignore next */
const readVarString = utf8TextDecoder ? _readVarStringNative : _readVarStringPolyfill

/**
 * @param {Decoder} decoder
 * @return {Uint8Array}
 */
const readTerminatedUint8Array = decoder => {
  const encoder = encoding.createEncoder()
  let b
  while (true) {
    b = readUint8(decoder)
    if (b === 0) {
      return encoding.toUint8Array(encoder)
    }
    if (b === 1) {
      b = readUint8(decoder)
    }
    encoding.write(encoder, b)
  }
}

/**
 * @param {Decoder} decoder
 * @return {string}
 */
const readTerminatedString = decoder => string.decodeUtf8(readTerminatedUint8Array(decoder))

/**
 * Look ahead and read varString without incrementing position
 *
 * @function
 * @param {Decoder} decoder
 * @return {string}
 */
const peekVarString = decoder => {
  const pos = decoder.pos
  const s = readVarString(decoder)
  decoder.pos = pos
  return s
}

/**
 * @param {Decoder} decoder
 * @param {number} len
 * @return {DataView}
 */
const readFromDataView = (decoder, len) => {
  const dv = new DataView(decoder.arr.buffer, decoder.arr.byteOffset + decoder.pos, len)
  decoder.pos += len
  return dv
}

/**
 * @param {Decoder} decoder
 */
const readFloat32 = decoder => readFromDataView(decoder, 4).getFloat32(0, false)

/**
 * @param {Decoder} decoder
 */
const readFloat64 = decoder => readFromDataView(decoder, 8).getFloat64(0, false)

/**
 * @param {Decoder} decoder
 */
const readBigInt64 = decoder => /** @type {any} */ (readFromDataView(decoder, 8)).getBigInt64(0, false)

/**
 * @param {Decoder} decoder
 */
const readBigUint64 = decoder => /** @type {any} */ (readFromDataView(decoder, 8)).getBigUint64(0, false)

/**
 * @type {Array<function(Decoder):any>}
 */
const readAnyLookupTable = [
  decoder => undefined, // CASE 127: undefined
  decoder => null, // CASE 126: null
  readVarInt, // CASE 125: integer
  readFloat32, // CASE 124: float32
  readFloat64, // CASE 123: float64
  readBigInt64, // CASE 122: bigint
  decoder => false, // CASE 121: boolean (false)
  decoder => true, // CASE 120: boolean (true)
  readVarString, // CASE 119: string
  decoder => { // CASE 118: object<string,any>
    const len = readVarUint(decoder)
    /**
     * @type {Object<string,any>}
     */
    const obj = {}
    for (let i = 0; i < len; i++) {
      const key = readVarString(decoder)
      obj[key] = readAny(decoder)
    }
    return obj
  },
  decoder => { // CASE 117: array<any>
    const len = readVarUint(decoder)
    const arr = []
    for (let i = 0; i < len; i++) {
      arr.push(readAny(decoder))
    }
    return arr
  },
  readVarUint8Array // CASE 116: Uint8Array
]

/**
 * @param {Decoder} decoder
 */
const readAny = decoder => readAnyLookupTable[127 - readUint8(decoder)](decoder)

/**
 * T must not be null.
 *
 * @template T
 */
class RleDecoder extends (/* unused pure expression or super */ null && (Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   * @param {function(Decoder):T} reader
   */
  constructor (uint8Array, reader) {
    super(uint8Array)
    /**
     * The reader
     */
    this.reader = reader
    /**
     * Current state
     * @type {T|null}
     */
    this.s = null
    this.count = 0
  }

  read () {
    if (this.count === 0) {
      this.s = this.reader(this)
      if (decoding_hasContent(this)) {
        this.count = readVarUint(this) + 1 // see encoder implementation for the reason why this is incremented
      } else {
        this.count = -1 // read the current value forever
      }
    }
    this.count--
    return /** @type {T} */ (this.s)
  }
}

class IntDiffDecoder extends (/* unused pure expression or super */ null && (Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   * @param {number} start
   */
  constructor (uint8Array, start) {
    super(uint8Array)
    /**
     * Current state
     * @type {number}
     */
    this.s = start
  }

  /**
   * @return {number}
   */
  read () {
    this.s += readVarInt(this)
    return this.s
  }
}

class RleIntDiffDecoder extends (/* unused pure expression or super */ null && (Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   * @param {number} start
   */
  constructor (uint8Array, start) {
    super(uint8Array)
    /**
     * Current state
     * @type {number}
     */
    this.s = start
    this.count = 0
  }

  /**
   * @return {number}
   */
  read () {
    if (this.count === 0) {
      this.s += readVarInt(this)
      if (decoding_hasContent(this)) {
        this.count = readVarUint(this) + 1 // see encoder implementation for the reason why this is incremented
      } else {
        this.count = -1 // read the current value forever
      }
    }
    this.count--
    return /** @type {number} */ (this.s)
  }
}

class UintOptRleDecoder extends (/* unused pure expression or super */ null && (Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   */
  constructor (uint8Array) {
    super(uint8Array)
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
  }

  read () {
    if (this.count === 0) {
      this.s = readVarInt(this)
      // if the sign is negative, we read the count too, otherwise count is 1
      const isNegative = math.isNegativeZero(this.s)
      this.count = 1
      if (isNegative) {
        this.s = -this.s
        this.count = readVarUint(this) + 2
      }
    }
    this.count--
    return /** @type {number} */ (this.s)
  }
}

class IncUintOptRleDecoder extends (/* unused pure expression or super */ null && (Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   */
  constructor (uint8Array) {
    super(uint8Array)
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
  }

  read () {
    if (this.count === 0) {
      this.s = readVarInt(this)
      // if the sign is negative, we read the count too, otherwise count is 1
      const isNegative = math.isNegativeZero(this.s)
      this.count = 1
      if (isNegative) {
        this.s = -this.s
        this.count = readVarUint(this) + 2
      }
    }
    this.count--
    return /** @type {number} */ (this.s++)
  }
}

class IntDiffOptRleDecoder extends (/* unused pure expression or super */ null && (Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   */
  constructor (uint8Array) {
    super(uint8Array)
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
    this.diff = 0
  }

  /**
   * @return {number}
   */
  read () {
    if (this.count === 0) {
      const diff = readVarInt(this)
      // if the first bit is set, we read more data
      const hasCount = diff & 1
      this.diff = math.floor(diff / 2) // shift >> 1
      this.count = 1
      if (hasCount) {
        this.count = readVarUint(this) + 2
      }
    }
    this.s += this.diff
    this.count--
    return this.s
  }
}

class StringDecoder {
  /**
   * @param {Uint8Array} uint8Array
   */
  constructor (uint8Array) {
    this.decoder = new UintOptRleDecoder(uint8Array)
    this.str = readVarString(this.decoder)
    /**
     * @type {number}
     */
    this.spos = 0
  }

  /**
   * @return {string}
   */
  read () {
    const end = this.spos + this.decoder.read()
    const res = this.str.slice(this.spos, end)
    this.spos = end
    return res
  }
}

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/string.js
/**
 * Utility module to work with strings.
 *
 * @module string
 */

const string_fromCharCode = String.fromCharCode
const string_fromCodePoint = String.fromCodePoint

/**
 * @param {string} s
 * @return {string}
 */
const string_toLowerCase = s => s.toLowerCase()

const string_trimLeftRegex = /^\s*/g

/**
 * @param {string} s
 * @return {string}
 */
const string_trimLeft = s => s.replace(string_trimLeftRegex, '')

const string_fromCamelCaseRegex = /([A-Z])/g

/**
 * @param {string} s
 * @param {string} separator
 * @return {string}
 */
const string_fromCamelCase = (s, separator) => string_trimLeft(s.replace(string_fromCamelCaseRegex, match => `${separator}${string_toLowerCase(match)}`))

/**
 * Compute the utf8ByteLength
 * @param {string} str
 * @return {number}
 */
const string_utf8ByteLength = str => unescape(encodeURIComponent(str)).length

/**
 * @param {string} str
 * @return {Uint8Array}
 */
const string_encodeUtf8Polyfill = str => {
  const encodedString = unescape(encodeURIComponent(str))
  const len = encodedString.length
  const buf = new Uint8Array(len)
  for (let i = 0; i < len; i++) {
    buf[i] = /** @type {number} */ (encodedString.codePointAt(i))
  }
  return buf
}

/* istanbul ignore next */
const string_utf8TextEncoder = /** @type {TextEncoder} */ (typeof TextEncoder !== 'undefined' ? new TextEncoder() : null)

/**
 * @param {string} str
 * @return {Uint8Array}
 */
const string_encodeUtf8Native = str => string_utf8TextEncoder.encode(str)

/**
 * @param {string} str
 * @return {Uint8Array}
 */
/* istanbul ignore next */
const string_encodeUtf8 = (/* unused pure expression or super */ null && (string_utf8TextEncoder ? string_encodeUtf8Native : string_encodeUtf8Polyfill))

/**
 * @param {Uint8Array} buf
 * @return {string}
 */
const string_decodeUtf8Polyfill = buf => {
  let remainingLen = buf.length
  let encodedString = ''
  let bufPos = 0
  while (remainingLen > 0) {
    const nextLen = remainingLen < 10000 ? remainingLen : 10000
    const bytes = buf.subarray(bufPos, bufPos + nextLen)
    bufPos += nextLen
    // Starting with ES5.1 we can supply a generic array-like object as arguments
    encodedString += String.fromCodePoint.apply(null, /** @type {any} */ (bytes))
    remainingLen -= nextLen
  }
  return decodeURIComponent(escape(encodedString))
}

/* istanbul ignore next */
let string_utf8TextDecoder = typeof TextDecoder === 'undefined' ? null : new TextDecoder('utf-8', { fatal: true, ignoreBOM: true })

/* istanbul ignore next */
if (string_utf8TextDecoder && string_utf8TextDecoder.decode(new Uint8Array()).length === 1) {
  // Safari doesn't handle BOM correctly.
  // This fixes a bug in Safari 13.0.5 where it produces a BOM the first time it is called.
  // utf8TextDecoder.decode(new Uint8Array()).length === 1 on the first call and
  // utf8TextDecoder.decode(new Uint8Array()).length === 1 on the second call
  // Another issue is that from then on no BOM chars are recognized anymore
  /* istanbul ignore next */
  string_utf8TextDecoder = null
}

/**
 * @param {Uint8Array} buf
 * @return {string}
 */
const string_decodeUtf8Native = buf => /** @type {TextDecoder} */ (string_utf8TextDecoder).decode(buf)

/**
 * @param {Uint8Array} buf
 * @return {string}
 */
/* istanbul ignore next */
const string_decodeUtf8 = (/* unused pure expression or super */ null && (string_utf8TextDecoder ? string_decodeUtf8Native : string_decodeUtf8Polyfill))

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/map.js
/**
 * Utility module to work with key-value stores.
 *
 * @module map
 */

/**
 * Creates a new Map instance.
 *
 * @function
 * @return {Map<any, any>}
 *
 * @function
 */
const map_create = () => new Map()

/**
 * Copy a Map object into a fresh Map object.
 *
 * @function
 * @template X,Y
 * @param {Map<X,Y>} m
 * @return {Map<X,Y>}
 */
const map_copy = m => {
  const r = map_create()
  m.forEach((v, k) => { r.set(k, v) })
  return r
}

/**
 * Get map property. Create T if property is undefined and set T on map.
 *
 * ```js
 * const listeners = map.setIfUndefined(events, 'eventName', set.create)
 * listeners.add(listener)
 * ```
 *
 * @function
 * @template T,K
 * @param {Map<K, T>} map
 * @param {K} key
 * @param {function():T} createT
 * @return {T}
 */
const map_setIfUndefined = (map, key, createT) => {
  let set = map.get(key)
  if (set === undefined) {
    map.set(key, set = createT())
  }
  return set
}

/**
 * Creates an Array and populates it with the content of all key-value pairs using the `f(value, key)` function.
 *
 * @function
 * @template K
 * @template V
 * @template R
 * @param {Map<K,V>} m
 * @param {function(V,K):R} f
 * @return {Array<R>}
 */
const map_map = (m, f) => {
  const res = []
  for (const [key, value] of m) {
    res.push(f(value, key))
  }
  return res
}

/**
 * Tests whether any key-value pairs pass the test implemented by `f(value, key)`.
 *
 * @todo should rename to some - similarly to Array.some
 *
 * @function
 * @template K
 * @template V
 * @param {Map<K,V>} m
 * @param {function(V,K):boolean} f
 * @return {boolean}
 */
const map_any = (m, f) => {
  for (const [key, value] of m) {
    if (f(value, key)) {
      return true
    }
  }
  return false
}

/**
 * Tests whether all key-value pairs pass the test implemented by `f(value, key)`.
 *
 * @function
 * @template K
 * @template V
 * @param {Map<K,V>} m
 * @param {function(V,K):boolean} f
 * @return {boolean}
 */
const lib0_map_all = (m, f) => {
  for (const [key, value] of m) {
    if (!f(value, key)) {
      return false
    }
  }
  return true
}

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/conditions.js
/**
 * Often used conditions.
 *
 * @module conditions
 */

/**
 * @template T
 * @param {T|null|undefined} v
 * @return {T|null}
 */
/* istanbul ignore next */
const conditions_undefinedToNull = v => v === undefined ? null : v

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/storage.js
/* global localStorage, addEventListener */

/**
 * Isomorphic variable storage.
 *
 * Uses LocalStorage in the browser and falls back to in-memory storage.
 *
 * @module storage
 */

/* istanbul ignore next */
class storage_VarStoragePolyfill {
  constructor () {
    this.map = new Map()
  }

  /**
   * @param {string} key
   * @param {any} newValue
   */
  setItem (key, newValue) {
    this.map.set(key, newValue)
  }

  /**
   * @param {string} key
   */
  getItem (key) {
    return this.map.get(key)
  }
}

/* istanbul ignore next */
/**
 * @type {any}
 */
let storage_localStorage = new storage_VarStoragePolyfill()
let storage_usePolyfill = true

try {
  // if the same-origin rule is violated, accessing localStorage might thrown an error
  /* istanbul ignore next */
  if (typeof localStorage !== 'undefined') {
    storage_localStorage = localStorage
    storage_usePolyfill = false
  }
} catch (e) { }

/* istanbul ignore next */
/**
 * This is basically localStorage in browser, or a polyfill in nodejs
 */
const storage_varStorage = storage_localStorage

/* istanbul ignore next */
/**
 * A polyfill for `addEventListener('storage', event => {..})` that does nothing if the polyfill is being used.
 *
 * @param {function({ key: string, newValue: string, oldValue: string }): void} eventHandler
 * @function
 */
const storage_onChange = eventHandler => storage_usePolyfill || addEventListener('storage', /** @type {any} */ (eventHandler))

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/environment.js
/* provided dependency */ var environment_process = __webpack_require__(4155);
/**
 * Isomorphic module to work access the environment (query params, env variables).
 *
 * @module map
 */






/* istanbul ignore next */
// @ts-ignore
const environment_isNode = typeof environment_process !== 'undefined' && environment_process.release && /node|io\.js/.test(environment_process.release.name)
/* istanbul ignore next */
const environment_isBrowser = typeof window !== 'undefined' && !environment_isNode
/* istanbul ignore next */
const environment_isMac = typeof navigator !== 'undefined' ? /Mac/.test(navigator.platform) : false

/**
 * @type {Map<string,string>}
 */
let environment_params
const environment_args = []

/* istanbul ignore next */
const environment_computeParams = () => {
  if (environment_params === undefined) {
    if (environment_isNode) {
      environment_params = map_create()
      const pargs = environment_process.argv
      let currParamName = null
      /* istanbul ignore next */
      for (let i = 0; i < pargs.length; i++) {
        const parg = pargs[i]
        if (parg[0] === '-') {
          if (currParamName !== null) {
            environment_params.set(currParamName, '')
          }
          currParamName = parg
        } else {
          if (currParamName !== null) {
            environment_params.set(currParamName, parg)
            currParamName = null
          } else {
            environment_args.push(parg)
          }
        }
      }
      if (currParamName !== null) {
        environment_params.set(currParamName, '')
      }
    // in ReactNative for example this would not be true (unless connected to the Remote Debugger)
    } else if (typeof location === 'object') {
      environment_params = map_create()
      // eslint-disable-next-line no-undef
      ;(location.search || '?').slice(1).split('&').forEach(kv => {
        if (kv.length !== 0) {
          const [key, value] = kv.split('=')
          environment_params.set(`--${string_fromCamelCase(key, '-')}`, value)
          environment_params.set(`-${string_fromCamelCase(key, '-')}`, value)
        }
      })
    } else {
      environment_params = map_create()
    }
  }
  return environment_params
}

/**
 * @param {string} name
 * @return {boolean}
 */
/* istanbul ignore next */
const environment_hasParam = name => environment_computeParams().has(name)

/**
 * @param {string} name
 * @param {string} defaultVal
 * @return {string}
 */
/* istanbul ignore next */
const environment_getParam = (name, defaultVal) => environment_computeParams().get(name) || defaultVal
// export const getArgs = name => computeParams() && args

/**
 * @param {string} name
 * @return {string|null}
 */
/* istanbul ignore next */
const environment_getVariable = name => environment_isNode ? conditions_undefinedToNull(environment_process.env[name.toUpperCase()]) : conditions_undefinedToNull(storage_varStorage.getItem(name))

/**
 * @param {string} name
 * @return {string|null}
 */
const environment_getConf = name => environment_computeParams().get('--' + name) || environment_getVariable(name)

/**
 * @param {string} name
 * @return {boolean}
 */
/* istanbul ignore next */
const environment_hasConf = name => environment_hasParam('--' + name) || environment_getVariable(name) !== null

/* istanbul ignore next */
const environment_production = environment_hasConf('production')

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/buffer.js
/**
 * Utility functions to work with buffers (Uint8Array).
 *
 * @module buffer
 */






/**
 * @param {number} len
 */
const buffer_createUint8ArrayFromLen = len => new Uint8Array(len)

/**
 * Create Uint8Array with initial content from buffer
 *
 * @param {ArrayBuffer} buffer
 * @param {number} byteOffset
 * @param {number} length
 */
const buffer_createUint8ArrayViewFromArrayBuffer = (buffer, byteOffset, length) => new Uint8Array(buffer, byteOffset, length)

/**
 * Create Uint8Array with initial content from buffer
 *
 * @param {ArrayBuffer} buffer
 */
const buffer_createUint8ArrayFromArrayBuffer = buffer => new Uint8Array(buffer)

/* istanbul ignore next */
/**
 * @param {Uint8Array} bytes
 * @return {string}
 */
const buffer_toBase64Browser = bytes => {
  let s = ''
  for (let i = 0; i < bytes.byteLength; i++) {
    s += string_fromCharCode(bytes[i])
  }
  // eslint-disable-next-line no-undef
  return btoa(s)
}

/**
 * @param {Uint8Array} bytes
 * @return {string}
 */
const buffer_toBase64Node = bytes => Buffer.from(bytes.buffer, bytes.byteOffset, bytes.byteLength).toString('base64')

/* istanbul ignore next */
/**
 * @param {string} s
 * @return {Uint8Array}
 */
const buffer_fromBase64Browser = s => {
  // eslint-disable-next-line no-undef
  const a = atob(s)
  const bytes = buffer_createUint8ArrayFromLen(a.length)
  for (let i = 0; i < a.length; i++) {
    bytes[i] = a.charCodeAt(i)
  }
  return bytes
}

/**
 * @param {string} s
 */
const buffer_fromBase64Node = s => {
  const buf = Buffer.from(s, 'base64')
  return new Uint8Array(buf.buffer, buf.byteOffset, buf.byteLength)
}

/* istanbul ignore next */
const buffer_toBase64 = environment_isBrowser ? buffer_toBase64Browser : buffer_toBase64Node

/* istanbul ignore next */
const buffer_fromBase64 = environment_isBrowser ? buffer_fromBase64Browser : buffer_fromBase64Node

/**
 * Copy the content of an Uint8Array view to a new ArrayBuffer.
 *
 * @param {Uint8Array} uint8Array
 * @return {Uint8Array}
 */
const buffer_copyUint8Array = uint8Array => {
  const newBuf = buffer_createUint8ArrayFromLen(uint8Array.byteLength)
  newBuf.set(uint8Array)
  return newBuf
}

/**
 * Encode anything as a UInt8Array. It's a pun on typescripts's `any` type.
 * See encoding.writeAny for more information.
 *
 * @param {any} data
 * @return {Uint8Array}
 */
const buffer_encodeAny = data => {
  const encoder = encoding.createEncoder()
  encoding.writeAny(encoder, data)
  return encoding.toUint8Array(encoder)
}

/**
 * Decode an any-encoded value.
 *
 * @param {Uint8Array} buf
 * @return {any}
 */
const buffer_decodeAny = buf => decoding.readAny(decoding.createDecoder(buf))

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/math.js
/**
 * Common Math expressions.
 *
 * @module math
 */

const math_floor = Math.floor
const math_ceil = Math.ceil
const math_abs = Math.abs
const math_imul = Math.imul
const math_round = Math.round
const math_log10 = Math.log10
const math_log2 = Math.log2
const math_log = Math.log
const math_sqrt = Math.sqrt

/**
 * @function
 * @param {number} a
 * @param {number} b
 * @return {number} The sum of a and b
 */
const math_add = (a, b) => a + b

/**
 * @function
 * @param {number} a
 * @param {number} b
 * @return {number} The smaller element of a and b
 */
const math_min = (a, b) => a < b ? a : b

/**
 * @function
 * @param {number} a
 * @param {number} b
 * @return {number} The bigger element of a and b
 */
const math_max = (a, b) => a > b ? a : b

const lib0_math_isNaN = Number.isNaN

const math_pow = Math.pow
/**
 * Base 10 exponential function. Returns the value of 10 raised to the power of pow.
 *
 * @param {number} exp
 * @return {number}
 */
const math_exp10 = exp => Math.pow(10, exp)

const math_sign = Math.sign

/**
 * @param {number} n
 * @return {boolean} Wether n is negative. This function also differentiates between -0 and +0
 */
const math_isNegativeZero = n => n !== 0 ? n < 0 : 1 / n < 0

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/binary.js
/* eslint-env browser */

/**
 * Binary data constants.
 *
 * @module binary
 */

/**
 * n-th bit activated.
 *
 * @type {number}
 */
const binary_BIT1 = 1
const binary_BIT2 = 2
const binary_BIT3 = 4
const binary_BIT4 = 8
const binary_BIT5 = 16
const binary_BIT6 = 32
const binary_BIT7 = 64
const binary_BIT8 = 128
const binary_BIT9 = 256
const binary_BIT10 = 512
const binary_BIT11 = 1024
const binary_BIT12 = 2048
const binary_BIT13 = 4096
const binary_BIT14 = 8192
const binary_BIT15 = 16384
const binary_BIT16 = 32768
const binary_BIT17 = 65536
const binary_BIT18 = 1 << 17
const binary_BIT19 = 1 << 18
const binary_BIT20 = 1 << 19
const binary_BIT21 = 1 << 20
const binary_BIT22 = 1 << 21
const binary_BIT23 = 1 << 22
const binary_BIT24 = 1 << 23
const binary_BIT25 = 1 << 24
const binary_BIT26 = 1 << 25
const binary_BIT27 = 1 << 26
const binary_BIT28 = 1 << 27
const binary_BIT29 = 1 << 28
const binary_BIT30 = 1 << 29
const binary_BIT31 = 1 << 30
const binary_BIT32 = (/* unused pure expression or super */ null && (1 << 31))

/**
 * First n bits activated.
 *
 * @type {number}
 */
const binary_BITS0 = 0
const binary_BITS1 = 1
const binary_BITS2 = 3
const binary_BITS3 = 7
const binary_BITS4 = 15
const binary_BITS5 = 31
const binary_BITS6 = 63
const binary_BITS7 = 127
const binary_BITS8 = 255
const binary_BITS9 = 511
const binary_BITS10 = 1023
const binary_BITS11 = 2047
const binary_BITS12 = 4095
const binary_BITS13 = 8191
const binary_BITS14 = 16383
const binary_BITS15 = 32767
const binary_BITS16 = 65535
const binary_BITS17 = binary_BIT18 - 1
const binary_BITS18 = binary_BIT19 - 1
const binary_BITS19 = binary_BIT20 - 1
const binary_BITS20 = binary_BIT21 - 1
const binary_BITS21 = binary_BIT22 - 1
const binary_BITS22 = binary_BIT23 - 1
const binary_BITS23 = binary_BIT24 - 1
const binary_BITS24 = binary_BIT25 - 1
const binary_BITS25 = binary_BIT26 - 1
const binary_BITS26 = binary_BIT27 - 1
const binary_BITS27 = binary_BIT28 - 1
const binary_BITS28 = binary_BIT29 - 1
const binary_BITS29 = binary_BIT30 - 1
const binary_BITS30 = binary_BIT31 - 1
/**
 * @type {number}
 */
const binary_BITS31 = 0x7FFFFFFF
/**
 * @type {number}
 */
const binary_BITS32 = 0xFFFFFFFF

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/encoding.js
/**
 * Efficient schema-less binary encoding with support for variable length encoding.
 *
 * Use [lib0/encoding] with [lib0/decoding]. Every encoding function has a corresponding decoding function.
 *
 * Encodes numbers in little-endian order (least to most significant byte order)
 * and is compatible with Golang's binary encoding (https://golang.org/pkg/encoding/binary/)
 * which is also used in Protocol Buffers.
 *
 * ```js
 * // encoding step
 * const encoder = new encoding.createEncoder()
 * encoding.writeVarUint(encoder, 256)
 * encoding.writeVarString(encoder, 'Hello world!')
 * const buf = encoding.toUint8Array(encoder)
 * ```
 *
 * ```js
 * // decoding step
 * const decoder = new decoding.createDecoder(buf)
 * decoding.readVarUint(decoder) // => 256
 * decoding.readVarString(decoder) // => 'Hello world!'
 * decoding.hasContent(decoder) // => false - all data is read
 * ```
 *
 * @module encoding
 */






/**
 * A BinaryEncoder handles the encoding to an Uint8Array.
 */
class encoding_Encoder {
  constructor () {
    this.cpos = 0
    this.cbuf = new Uint8Array(100)
    /**
     * @type {Array<Uint8Array>}
     */
    this.bufs = []
  }
}

/**
 * @function
 * @return {Encoder}
 */
const encoding_createEncoder = () => new encoding_Encoder()

/**
 * The current length of the encoded data.
 *
 * @function
 * @param {Encoder} encoder
 * @return {number}
 */
const lib0_encoding_length = encoder => {
  let len = encoder.cpos
  for (let i = 0; i < encoder.bufs.length; i++) {
    len += encoder.bufs[i].length
  }
  return len
}

/**
 * Transform to Uint8Array.
 *
 * @function
 * @param {Encoder} encoder
 * @return {Uint8Array} The created ArrayBuffer.
 */
const encoding_toUint8Array = encoder => {
  const uint8arr = new Uint8Array(lib0_encoding_length(encoder))
  let curPos = 0
  for (let i = 0; i < encoder.bufs.length; i++) {
    const d = encoder.bufs[i]
    uint8arr.set(d, curPos)
    curPos += d.length
  }
  uint8arr.set(buffer_createUint8ArrayViewFromArrayBuffer(encoder.cbuf.buffer, 0, encoder.cpos), curPos)
  return uint8arr
}

/**
 * Verify that it is possible to write `len` bytes wtihout checking. If
 * necessary, a new Buffer with the required length is attached.
 *
 * @param {Encoder} encoder
 * @param {number} len
 */
const encoding_verifyLen = (encoder, len) => {
  const bufferLen = encoder.cbuf.length
  if (bufferLen - encoder.cpos < len) {
    encoder.bufs.push(buffer.createUint8ArrayViewFromArrayBuffer(encoder.cbuf.buffer, 0, encoder.cpos))
    encoder.cbuf = new Uint8Array(math.max(bufferLen, len) * 2)
    encoder.cpos = 0
  }
}

/**
 * Write one byte to the encoder.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The byte that is to be encoded.
 */
const encoding_write = (encoder, num) => {
  const bufferLen = encoder.cbuf.length
  if (encoder.cpos === bufferLen) {
    encoder.bufs.push(encoder.cbuf)
    encoder.cbuf = new Uint8Array(bufferLen * 2)
    encoder.cpos = 0
  }
  encoder.cbuf[encoder.cpos++] = num
}

/**
 * Write one byte at a specific position.
 * Position must already be written (i.e. encoder.length > pos)
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} pos Position to which to write data
 * @param {number} num Unsigned 8-bit integer
 */
const lib0_encoding_set = (encoder, pos, num) => {
  let buffer = null
  // iterate all buffers and adjust position
  for (let i = 0; i < encoder.bufs.length && buffer === null; i++) {
    const b = encoder.bufs[i]
    if (pos < b.length) {
      buffer = b // found buffer
    } else {
      pos -= b.length
    }
  }
  if (buffer === null) {
    // use current buffer
    buffer = encoder.cbuf
  }
  buffer[pos] = num
}

/**
 * Write one byte as an unsigned integer.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const encoding_writeUint8 = (/* unused pure expression or super */ null && (encoding_write))

/**
 * Write one byte as an unsigned Integer at a specific location.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} pos The location where the data will be written.
 * @param {number} num The number that is to be encoded.
 */
const encoding_setUint8 = (/* unused pure expression or super */ null && (lib0_encoding_set))

/**
 * Write two bytes as an unsigned integer.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const encoding_writeUint16 = (encoder, num) => {
  encoding_write(encoder, num & binary.BITS8)
  encoding_write(encoder, (num >>> 8) & binary.BITS8)
}
/**
 * Write two bytes as an unsigned integer at a specific location.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} pos The location where the data will be written.
 * @param {number} num The number that is to be encoded.
 */
const encoding_setUint16 = (encoder, pos, num) => {
  lib0_encoding_set(encoder, pos, num & binary.BITS8)
  lib0_encoding_set(encoder, pos + 1, (num >>> 8) & binary.BITS8)
}

/**
 * Write two bytes as an unsigned integer
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const encoding_writeUint32 = (encoder, num) => {
  for (let i = 0; i < 4; i++) {
    encoding_write(encoder, num & binary.BITS8)
    num >>>= 8
  }
}

/**
 * Write two bytes as an unsigned integer in big endian order.
 * (most significant byte first)
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const encoding_writeUint32BigEndian = (encoder, num) => {
  for (let i = 3; i >= 0; i--) {
    encoding_write(encoder, (num >>> (8 * i)) & binary.BITS8)
  }
}

/**
 * Write two bytes as an unsigned integer at a specific location.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} pos The location where the data will be written.
 * @param {number} num The number that is to be encoded.
 */
const encoding_setUint32 = (encoder, pos, num) => {
  for (let i = 0; i < 4; i++) {
    lib0_encoding_set(encoder, pos + i, num & binary.BITS8)
    num >>>= 8
  }
}

/**
 * Write a variable length unsigned integer.
 *
 * Encodes integers in the range from [0, 4294967295] / [0, 0xffffffff]. (max 32 bit unsigned integer)
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const encoding_writeVarUint = (encoder, num) => {
  while (num > binary_BITS7) {
    encoding_write(encoder, binary_BIT8 | (binary_BITS7 & num))
    num >>>= 7
  }
  encoding_write(encoder, binary_BITS7 & num)
}

/**
 * Write a variable length integer.
 *
 * Encodes integers in the range from [-2147483648, -2147483647].
 *
 * We don't use zig-zag encoding because we want to keep the option open
 * to use the same function for BigInt and 53bit integers (doubles).
 *
 * We use the 7th bit instead for signaling that this is a negative number.
 *
 * @function
 * @param {Encoder} encoder
 * @param {number} num The number that is to be encoded.
 */
const encoding_writeVarInt = (encoder, num) => {
  const isNegative = math.isNegativeZero(num)
  if (isNegative) {
    num = -num
  }
  //             |- whether to continue reading         |- whether is negative     |- number
  encoding_write(encoder, (num > binary.BITS6 ? binary.BIT8 : 0) | (isNegative ? binary.BIT7 : 0) | (binary.BITS6 & num))
  num >>>= 6
  // We don't need to consider the case of num === 0 so we can use a different
  // pattern here than above.
  while (num > 0) {
    encoding_write(encoder, (num > binary.BITS7 ? binary.BIT8 : 0) | (binary.BITS7 & num))
    num >>>= 7
  }
}

/**
 * Write a variable length string.
 *
 * @function
 * @param {Encoder} encoder
 * @param {String} str The string that is to be encoded.
 */
const encoding_writeVarString = (encoder, str) => {
  const encodedString = unescape(encodeURIComponent(str))
  const len = encodedString.length
  encoding_writeVarUint(encoder, len)
  for (let i = 0; i < len; i++) {
    encoding_write(encoder, /** @type {number} */ (encodedString.codePointAt(i)))
  }
}

/**
 * Write the content of another Encoder.
 *
 * @TODO: can be improved!
 *        - Note: Should consider that when appending a lot of small Encoders, we should rather clone than referencing the old structure.
 *                Encoders start with a rather big initial buffer.
 *
 * @function
 * @param {Encoder} encoder The enUint8Arr
 * @param {Encoder} append The BinaryEncoder to be written.
 */
const encoding_writeBinaryEncoder = (encoder, append) => encoding_writeUint8Array(encoder, encoding_toUint8Array(append))

/**
 * Append fixed-length Uint8Array to the encoder.
 *
 * @function
 * @param {Encoder} encoder
 * @param {Uint8Array} uint8Array
 */
const encoding_writeUint8Array = (encoder, uint8Array) => {
  const bufferLen = encoder.cbuf.length
  const cpos = encoder.cpos
  const leftCopyLen = math_min(bufferLen - cpos, uint8Array.length)
  const rightCopyLen = uint8Array.length - leftCopyLen
  encoder.cbuf.set(uint8Array.subarray(0, leftCopyLen), cpos)
  encoder.cpos += leftCopyLen
  if (rightCopyLen > 0) {
    // Still something to write, write right half..
    // Append new buffer
    encoder.bufs.push(encoder.cbuf)
    // must have at least size of remaining buffer
    encoder.cbuf = new Uint8Array(math_max(bufferLen * 2, rightCopyLen))
    // copy array
    encoder.cbuf.set(uint8Array.subarray(leftCopyLen))
    encoder.cpos = rightCopyLen
  }
}

/**
 * Append an Uint8Array to Encoder.
 *
 * @function
 * @param {Encoder} encoder
 * @param {Uint8Array} uint8Array
 */
const encoding_writeVarUint8Array = (encoder, uint8Array) => {
  encoding_writeVarUint(encoder, uint8Array.byteLength)
  encoding_writeUint8Array(encoder, uint8Array)
}

/**
 * Create an DataView of the next `len` bytes. Use it to write data after
 * calling this function.
 *
 * ```js
 * // write float32 using DataView
 * const dv = writeOnDataView(encoder, 4)
 * dv.setFloat32(0, 1.1)
 * // read float32 using DataView
 * const dv = readFromDataView(encoder, 4)
 * dv.getFloat32(0) // => 1.100000023841858 (leaving it to the reader to find out why this is the correct result)
 * ```
 *
 * @param {Encoder} encoder
 * @param {number} len
 * @return {DataView}
 */
const encoding_writeOnDataView = (encoder, len) => {
  encoding_verifyLen(encoder, len)
  const dview = new DataView(encoder.cbuf.buffer, encoder.cpos, len)
  encoder.cpos += len
  return dview
}

/**
 * @param {Encoder} encoder
 * @param {number} num
 */
const encoding_writeFloat32 = (encoder, num) => encoding_writeOnDataView(encoder, 4).setFloat32(0, num, false)

/**
 * @param {Encoder} encoder
 * @param {number} num
 */
const encoding_writeFloat64 = (encoder, num) => encoding_writeOnDataView(encoder, 8).setFloat64(0, num, false)

/**
 * @param {Encoder} encoder
 * @param {bigint} num
 */
const encoding_writeBigInt64 = (encoder, num) => /** @type {any} */ (encoding_writeOnDataView(encoder, 8)).setBigInt64(0, num, false)

/**
 * @param {Encoder} encoder
 * @param {bigint} num
 */
const encoding_writeBigUint64 = (encoder, num) => /** @type {any} */ (encoding_writeOnDataView(encoder, 8)).setBigUint64(0, num, false)

const encoding_floatTestBed = new DataView(new ArrayBuffer(4))
/**
 * Check if a number can be encoded as a 32 bit float.
 *
 * @param {number} num
 * @return {boolean}
 */
const encoding_isFloat32 = num => {
  encoding_floatTestBed.setFloat32(0, num)
  return encoding_floatTestBed.getFloat32(0) === num
}

/**
 * Encode data with efficient binary format.
 *
 * Differences to JSON:
 * • Transforms data to a binary format (not to a string)
 * • Encodes undefined, NaN, and ArrayBuffer (these can't be represented in JSON)
 * • Numbers are efficiently encoded either as a variable length integer, as a
 *   32 bit float, as a 64 bit float, or as a 64 bit bigint.
 *
 * Encoding table:
 *
 * | Data Type           | Prefix   | Encoding Method    | Comment |
 * | ------------------- | -------- | ------------------ | ------- |
 * | undefined           | 127      |                    | Functions, symbol, and everything that cannot be identified is encoded as undefined |
 * | null                | 126      |                    | |
 * | integer             | 125      | writeVarInt        | Only encodes 32 bit signed integers |
 * | float32             | 124      | writeFloat32       | |
 * | float64             | 123      | writeFloat64       | |
 * | bigint              | 122      | writeBigInt64      | |
 * | boolean (false)     | 121      |                    | True and false are different data types so we save the following byte |
 * | boolean (true)      | 120      |                    | - 0b01111000 so the last bit determines whether true or false |
 * | string              | 119      | writeVarString     | |
 * | object<string,any>  | 118      | custom             | Writes {length} then {length} key-value pairs |
 * | array<any>          | 117      | custom             | Writes {length} then {length} json values |
 * | Uint8Array          | 116      | writeVarUint8Array | We use Uint8Array for any kind of binary data |
 *
 * Reasons for the decreasing prefix:
 * We need the first bit for extendability (later we may want to encode the
 * prefix with writeVarUint). The remaining 7 bits are divided as follows:
 * [0-30]   the beginning of the data range is used for custom purposes
 *          (defined by the function that uses this library)
 * [31-127] the end of the data range is used for data encoding by
 *          lib0/encoding.js
 *
 * @param {Encoder} encoder
 * @param {undefined|null|number|bigint|boolean|string|Object<string,any>|Array<any>|Uint8Array} data
 */
const encoding_writeAny = (encoder, data) => {
  switch (typeof data) {
    case 'string':
      // TYPE 119: STRING
      encoding_write(encoder, 119)
      encoding_writeVarString(encoder, data)
      break
    case 'number':
      if (number.isInteger(data) && data <= binary.BITS31) {
        // TYPE 125: INTEGER
        encoding_write(encoder, 125)
        encoding_writeVarInt(encoder, data)
      } else if (encoding_isFloat32(data)) {
        // TYPE 124: FLOAT32
        encoding_write(encoder, 124)
        encoding_writeFloat32(encoder, data)
      } else {
        // TYPE 123: FLOAT64
        encoding_write(encoder, 123)
        encoding_writeFloat64(encoder, data)
      }
      break
    case 'bigint':
      // TYPE 122: BigInt
      encoding_write(encoder, 122)
      encoding_writeBigInt64(encoder, data)
      break
    case 'object':
      if (data === null) {
        // TYPE 126: null
        encoding_write(encoder, 126)
      } else if (data instanceof Array) {
        // TYPE 117: Array
        encoding_write(encoder, 117)
        encoding_writeVarUint(encoder, data.length)
        for (let i = 0; i < data.length; i++) {
          encoding_writeAny(encoder, data[i])
        }
      } else if (data instanceof Uint8Array) {
        // TYPE 116: ArrayBuffer
        encoding_write(encoder, 116)
        encoding_writeVarUint8Array(encoder, data)
      } else {
        // TYPE 118: Object
        encoding_write(encoder, 118)
        const keys = Object.keys(data)
        encoding_writeVarUint(encoder, keys.length)
        for (let i = 0; i < keys.length; i++) {
          const key = keys[i]
          encoding_writeVarString(encoder, key)
          encoding_writeAny(encoder, data[key])
        }
      }
      break
    case 'boolean':
      // TYPE 120/121: boolean (true/false)
      encoding_write(encoder, data ? 120 : 121)
      break
    default:
      // TYPE 127: undefined
      encoding_write(encoder, 127)
  }
}

/**
 * Now come a few stateful encoder that have their own classes.
 */

/**
 * Basic Run Length Encoder - a basic compression implementation.
 *
 * Encodes [1,1,1,7] to [1,3,7,1] (3 times 1, 1 time 7). This encoder might do more harm than good if there are a lot of values that are not repeated.
 *
 * It was originally used for image compression. Cool .. article http://csbruce.com/cbm/transactor/pdfs/trans_v7_i06.pdf
 *
 * @note T must not be null!
 *
 * @template T
 */
class encoding_RleEncoder extends (/* unused pure expression or super */ null && (encoding_Encoder)) {
  /**
   * @param {function(Encoder, T):void} writer
   */
  constructor (writer) {
    super()
    /**
     * The writer
     */
    this.w = writer
    /**
     * Current state
     * @type {T|null}
     */
    this.s = null
    this.count = 0
  }

  /**
   * @param {T} v
   */
  write (v) {
    if (this.s === v) {
      this.count++
    } else {
      if (this.count > 0) {
        // flush counter, unless this is the first value (count = 0)
        encoding_writeVarUint(this, this.count - 1) // since count is always > 0, we can decrement by one. non-standard encoding ftw
      }
      this.count = 1
      // write first value
      this.w(this, v)
      this.s = v
    }
  }
}

/**
 * Basic diff decoder using variable length encoding.
 *
 * Encodes the values [3, 1100, 1101, 1050, 0] to [3, 1097, 1, -51, -1050] using writeVarInt.
 */
class encoding_IntDiffEncoder extends (/* unused pure expression or super */ null && (encoding_Encoder)) {
  /**
   * @param {number} start
   */
  constructor (start) {
    super()
    /**
     * Current state
     * @type {number}
     */
    this.s = start
  }

  /**
   * @param {number} v
   */
  write (v) {
    encoding_writeVarInt(this, v - this.s)
    this.s = v
  }
}

/**
 * A combination of IntDiffEncoder and RleEncoder.
 *
 * Basically first writes the IntDiffEncoder and then counts duplicate diffs using RleEncoding.
 *
 * Encodes the values [1,1,1,2,3,4,5,6] as [1,1,0,2,1,5] (RLE([1,0,0,1,1,1,1,1]) ⇒ RleIntDiff[1,1,0,2,1,5])
 */
class encoding_RleIntDiffEncoder extends (/* unused pure expression or super */ null && (encoding_Encoder)) {
  /**
   * @param {number} start
   */
  constructor (start) {
    super()
    /**
     * Current state
     * @type {number}
     */
    this.s = start
    this.count = 0
  }

  /**
   * @param {number} v
   */
  write (v) {
    if (this.s === v && this.count > 0) {
      this.count++
    } else {
      if (this.count > 0) {
        // flush counter, unless this is the first value (count = 0)
        encoding_writeVarUint(this, this.count - 1) // since count is always > 0, we can decrement by one. non-standard encoding ftw
      }
      this.count = 1
      // write first value
      encoding_writeVarInt(this, v - this.s)
      this.s = v
    }
  }
}

/**
 * @param {UintOptRleEncoder} encoder
 */
const encoding_flushUintOptRleEncoder = encoder => {
  /* istanbul ignore else */
  if (encoder.count > 0) {
    // flush counter, unless this is the first value (count = 0)
    // case 1: just a single value. set sign to positive
    // case 2: write several values. set sign to negative to indicate that there is a length coming
    encoding_writeVarInt(encoder.encoder, encoder.count === 1 ? encoder.s : -encoder.s)
    if (encoder.count > 1) {
      encoding_writeVarUint(encoder.encoder, encoder.count - 2) // since count is always > 1, we can decrement by one. non-standard encoding ftw
    }
  }
}

/**
 * Optimized Rle encoder that does not suffer from the mentioned problem of the basic Rle encoder.
 *
 * Internally uses VarInt encoder to write unsigned integers. If the input occurs multiple times, we write
 * write it as a negative number. The UintOptRleDecoder then understands that it needs to read a count.
 *
 * Encodes [1,2,3,3,3] as [1,2,-3,3] (once 1, once 2, three times 3)
 */
class encoding_UintOptRleEncoder {
  constructor () {
    this.encoder = new encoding_Encoder()
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
  }

  /**
   * @param {number} v
   */
  write (v) {
    if (this.s === v) {
      this.count++
    } else {
      encoding_flushUintOptRleEncoder(this)
      this.count = 1
      this.s = v
    }
  }

  toUint8Array () {
    encoding_flushUintOptRleEncoder(this)
    return encoding_toUint8Array(this.encoder)
  }
}

/**
 * Increasing Uint Optimized RLE Encoder
 *
 * The RLE encoder counts the number of same occurences of the same value.
 * The IncUintOptRle encoder counts if the value increases.
 * I.e. 7, 8, 9, 10 will be encoded as [-7, 4]. 1, 3, 5 will be encoded
 * as [1, 3, 5].
 */
class encoding_IncUintOptRleEncoder {
  constructor () {
    this.encoder = new encoding_Encoder()
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
  }

  /**
   * @param {number} v
   */
  write (v) {
    if (this.s + this.count === v) {
      this.count++
    } else {
      encoding_flushUintOptRleEncoder(this)
      this.count = 1
      this.s = v
    }
  }

  toUint8Array () {
    encoding_flushUintOptRleEncoder(this)
    return encoding_toUint8Array(this.encoder)
  }
}

/**
 * @param {IntDiffOptRleEncoder} encoder
 */
const encoding_flushIntDiffOptRleEncoder = encoder => {
  if (encoder.count > 0) {
    //          31 bit making up the diff | wether to write the counter
    const encodedDiff = encoder.diff << 1 | (encoder.count === 1 ? 0 : 1)
    // flush counter, unless this is the first value (count = 0)
    // case 1: just a single value. set first bit to positive
    // case 2: write several values. set first bit to negative to indicate that there is a length coming
    encoding_writeVarInt(encoder.encoder, encodedDiff)
    if (encoder.count > 1) {
      encoding_writeVarUint(encoder.encoder, encoder.count - 2) // since count is always > 1, we can decrement by one. non-standard encoding ftw
    }
  }
}

/**
 * A combination of the IntDiffEncoder and the UintOptRleEncoder.
 *
 * The count approach is similar to the UintDiffOptRleEncoder, but instead of using the negative bitflag, it encodes
 * in the LSB whether a count is to be read. Therefore this Encoder only supports 31 bit integers!
 *
 * Encodes [1, 2, 3, 2] as [3, 1, 6, -1] (more specifically [(1 << 1) | 1, (3 << 0) | 0, -1])
 *
 * Internally uses variable length encoding. Contrary to normal UintVar encoding, the first byte contains:
 * * 1 bit that denotes whether the next value is a count (LSB)
 * * 1 bit that denotes whether this value is negative (MSB - 1)
 * * 1 bit that denotes whether to continue reading the variable length integer (MSB)
 *
 * Therefore, only five bits remain to encode diff ranges.
 *
 * Use this Encoder only when appropriate. In most cases, this is probably a bad idea.
 */
class encoding_IntDiffOptRleEncoder {
  constructor () {
    this.encoder = new encoding_Encoder()
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
    this.diff = 0
  }

  /**
   * @param {number} v
   */
  write (v) {
    if (this.diff === v - this.s) {
      this.s = v
      this.count++
    } else {
      encoding_flushIntDiffOptRleEncoder(this)
      this.count = 1
      this.diff = v - this.s
      this.s = v
    }
  }

  toUint8Array () {
    encoding_flushIntDiffOptRleEncoder(this)
    return encoding_toUint8Array(this.encoder)
  }
}

/**
 * Optimized String Encoder.
 *
 * Encoding many small strings in a simple Encoder is not very efficient. The function call to decode a string takes some time and creates references that must be eventually deleted.
 * In practice, when decoding several million small strings, the GC will kick in more and more often to collect orphaned string objects (or maybe there is another reason?).
 *
 * This string encoder solves the above problem. All strings are concatenated and written as a single string using a single encoding call.
 *
 * The lengths are encoded using a UintOptRleEncoder.
 */
class encoding_StringEncoder {
  constructor () {
    /**
     * @type {Array<string>}
     */
    this.sarr = []
    this.s = ''
    this.lensE = new encoding_UintOptRleEncoder()
  }

  /**
   * @param {string} string
   */
  write (string) {
    this.s += string
    if (this.s.length > 19) {
      this.sarr.push(this.s)
      this.s = ''
    }
    this.lensE.write(string.length)
  }

  toUint8Array () {
    const encoder = new encoding_Encoder()
    this.sarr.push(this.s)
    this.s = ''
    encoding_writeVarString(encoder, this.sarr.join(''))
    encoding_writeUint8Array(encoder, this.lensE.toUint8Array())
    return encoding_toUint8Array(encoder)
  }
}

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/decoding.js
/**
 * Efficient schema-less binary decoding with support for variable length encoding.
 *
 * Use [lib0/decoding] with [lib0/encoding]. Every encoding function has a corresponding decoding function.
 *
 * Encodes numbers in little-endian order (least to most significant byte order)
 * and is compatible with Golang's binary encoding (https://golang.org/pkg/encoding/binary/)
 * which is also used in Protocol Buffers.
 *
 * ```js
 * // encoding step
 * const encoder = new encoding.createEncoder()
 * encoding.writeVarUint(encoder, 256)
 * encoding.writeVarString(encoder, 'Hello world!')
 * const buf = encoding.toUint8Array(encoder)
 * ```
 *
 * ```js
 * // decoding step
 * const decoder = new decoding.createDecoder(buf)
 * decoding.readVarUint(decoder) // => 256
 * decoding.readVarString(decoder) // => 'Hello world!'
 * decoding.hasContent(decoder) // => false - all data is read
 * ```
 *
 * @module decoding
 */





/**
 * A Decoder handles the decoding of an Uint8Array.
 */
class decoding_Decoder {
  /**
   * @param {Uint8Array} uint8Array Binary data to decode
   */
  constructor (uint8Array) {
    /**
     * Decoding target.
     *
     * @type {Uint8Array}
     */
    this.arr = uint8Array
    /**
     * Current decoding position.
     *
     * @type {number}
     */
    this.pos = 0
  }
}

/**
 * @function
 * @param {Uint8Array} uint8Array
 * @return {Decoder}
 */
const decoding_createDecoder = uint8Array => new decoding_Decoder(uint8Array)

/**
 * @function
 * @param {Decoder} decoder
 * @return {boolean}
 */
const lib0_decoding_hasContent = decoder => decoder.pos !== decoder.arr.length

/**
 * Clone a decoder instance.
 * Optionally set a new position parameter.
 *
 * @function
 * @param {Decoder} decoder The decoder instance
 * @param {number} [newPos] Defaults to current position
 * @return {Decoder} A clone of `decoder`
 */
const decoding_clone = (decoder, newPos = decoder.pos) => {
  const _decoder = decoding_createDecoder(decoder.arr)
  _decoder.pos = newPos
  return _decoder
}

/**
 * Create an Uint8Array view of the next `len` bytes and advance the position by `len`.
 *
 * Important: The Uint8Array still points to the underlying ArrayBuffer. Make sure to discard the result as soon as possible to prevent any memory leaks.
 *            Use `buffer.copyUint8Array` to copy the result into a new Uint8Array.
 *
 * @function
 * @param {Decoder} decoder The decoder instance
 * @param {number} len The length of bytes to read
 * @return {Uint8Array}
 */
const decoding_readUint8Array = (decoder, len) => {
  const view = buffer_createUint8ArrayViewFromArrayBuffer(decoder.arr.buffer, decoder.pos + decoder.arr.byteOffset, len)
  decoder.pos += len
  return view
}

/**
 * Read variable length Uint8Array.
 *
 * Important: The Uint8Array still points to the underlying ArrayBuffer. Make sure to discard the result as soon as possible to prevent any memory leaks.
 *            Use `buffer.copyUint8Array` to copy the result into a new Uint8Array.
 *
 * @function
 * @param {Decoder} decoder
 * @return {Uint8Array}
 */
const decoding_readVarUint8Array = decoder => decoding_readUint8Array(decoder, decoding_readVarUint(decoder))

/**
 * Read the rest of the content as an ArrayBuffer
 * @function
 * @param {Decoder} decoder
 * @return {Uint8Array}
 */
const decoding_readTailAsUint8Array = decoder => decoding_readUint8Array(decoder, decoder.arr.length - decoder.pos)

/**
 * Skip one byte, jump to the next position.
 * @function
 * @param {Decoder} decoder The decoder instance
 * @return {number} The next position
 */
const decoding_skip8 = decoder => decoder.pos++

/**
 * Read one byte as unsigned integer.
 * @function
 * @param {Decoder} decoder The decoder instance
 * @return {number} Unsigned 8-bit integer
 */
const decoding_readUint8 = decoder => decoder.arr[decoder.pos++]

/**
 * Read 2 bytes as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const decoding_readUint16 = decoder => {
  const uint =
    decoder.arr[decoder.pos] +
    (decoder.arr[decoder.pos + 1] << 8)
  decoder.pos += 2
  return uint
}

/**
 * Read 4 bytes as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const decoding_readUint32 = decoder => {
  const uint =
    (decoder.arr[decoder.pos] +
    (decoder.arr[decoder.pos + 1] << 8) +
    (decoder.arr[decoder.pos + 2] << 16) +
    (decoder.arr[decoder.pos + 3] << 24)) >>> 0
  decoder.pos += 4
  return uint
}

/**
 * Read 4 bytes as unsigned integer in big endian order.
 * (most significant byte first)
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const decoding_readUint32BigEndian = decoder => {
  const uint =
    (decoder.arr[decoder.pos + 3] +
    (decoder.arr[decoder.pos + 2] << 8) +
    (decoder.arr[decoder.pos + 1] << 16) +
    (decoder.arr[decoder.pos] << 24)) >>> 0
  decoder.pos += 4
  return uint
}

/**
 * Look ahead without incrementing the position
 * to the next byte and read it as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const decoding_peekUint8 = decoder => decoder.arr[decoder.pos]

/**
 * Look ahead without incrementing the position
 * to the next byte and read it as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const decoding_peekUint16 = decoder =>
  decoder.arr[decoder.pos] +
  (decoder.arr[decoder.pos + 1] << 8)

/**
 * Look ahead without incrementing the position
 * to the next byte and read it as unsigned integer.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.
 */
const decoding_peekUint32 = decoder => (
  decoder.arr[decoder.pos] +
  (decoder.arr[decoder.pos + 1] << 8) +
  (decoder.arr[decoder.pos + 2] << 16) +
  (decoder.arr[decoder.pos + 3] << 24)
) >>> 0

/**
 * Read unsigned integer (32bit) with variable length.
 * 1/8th of the storage is used as encoding overhead.
 *  * numbers < 2^7 is stored in one bytlength
 *  * numbers < 2^14 is stored in two bylength
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.length
 */
const decoding_readVarUint = decoder => {
  let num = 0
  let len = 0
  while (true) {
    const r = decoder.arr[decoder.pos++]
    num = num | ((r & binary_BITS7) << len)
    len += 7
    if (r < binary_BIT8) {
      return num >>> 0 // return unsigned number!
    }
    /* istanbul ignore if */
    if (len > 35) {
      throw new Error('Integer out of range!')
    }
  }
}

/**
 * Read signed integer (32bit) with variable length.
 * 1/8th of the storage is used as encoding overhead.
 *  * numbers < 2^7 is stored in one bytlength
 *  * numbers < 2^14 is stored in two bylength
 * @todo This should probably create the inverse ~num if number is negative - but this would be a breaking change.
 *
 * @function
 * @param {Decoder} decoder
 * @return {number} An unsigned integer.length
 */
const decoding_readVarInt = decoder => {
  let r = decoder.arr[decoder.pos++]
  let num = r & binary_BITS6
  let len = 6
  const sign = (r & binary_BIT7) > 0 ? -1 : 1
  if ((r & binary_BIT8) === 0) {
    // don't continue reading
    return sign * num
  }
  while (true) {
    r = decoder.arr[decoder.pos++]
    num = num | ((r & binary_BITS7) << len)
    len += 7
    if (r < binary_BIT8) {
      return sign * (num >>> 0)
    }
    /* istanbul ignore if */
    if (len > 41) {
      throw new Error('Integer out of range!')
    }
  }
}

/**
 * Look ahead and read varUint without incrementing position
 *
 * @function
 * @param {Decoder} decoder
 * @return {number}
 */
const decoding_peekVarUint = decoder => {
  const pos = decoder.pos
  const s = decoding_readVarUint(decoder)
  decoder.pos = pos
  return s
}

/**
 * Look ahead and read varUint without incrementing position
 *
 * @function
 * @param {Decoder} decoder
 * @return {number}
 */
const decoding_peekVarInt = decoder => {
  const pos = decoder.pos
  const s = decoding_readVarInt(decoder)
  decoder.pos = pos
  return s
}

/**
 * Read string of variable length
 * * varUint is used to store the length of the string
 *
 * Transforming utf8 to a string is pretty expensive. The code performs 10x better
 * when String.fromCodePoint is fed with all characters as arguments.
 * But most environments have a maximum number of arguments per functions.
 * For effiency reasons we apply a maximum of 10000 characters at once.
 *
 * @function
 * @param {Decoder} decoder
 * @return {String} The read String.
 */
const decoding_readVarString = decoder => {
  let remainingLen = decoding_readVarUint(decoder)
  if (remainingLen === 0) {
    return ''
  } else {
    let encodedString = String.fromCodePoint(decoding_readUint8(decoder)) // remember to decrease remainingLen
    if (--remainingLen < 100) { // do not create a Uint8Array for small strings
      while (remainingLen--) {
        encodedString += String.fromCodePoint(decoding_readUint8(decoder))
      }
    } else {
      while (remainingLen > 0) {
        const nextLen = remainingLen < 10000 ? remainingLen : 10000
        // this is dangerous, we create a fresh array view from the existing buffer
        const bytes = decoder.arr.subarray(decoder.pos, decoder.pos + nextLen)
        decoder.pos += nextLen
        // Starting with ES5.1 we can supply a generic array-like object as arguments
        encodedString += String.fromCodePoint.apply(null, /** @type {any} */ (bytes))
        remainingLen -= nextLen
      }
    }
    return decodeURIComponent(escape(encodedString))
  }
}

/**
 * Look ahead and read varString without incrementing position
 *
 * @function
 * @param {Decoder} decoder
 * @return {string}
 */
const decoding_peekVarString = decoder => {
  const pos = decoder.pos
  const s = decoding_readVarString(decoder)
  decoder.pos = pos
  return s
}

/**
 * @param {Decoder} decoder
 * @param {number} len
 * @return {DataView}
 */
const decoding_readFromDataView = (decoder, len) => {
  const dv = new DataView(decoder.arr.buffer, decoder.arr.byteOffset + decoder.pos, len)
  decoder.pos += len
  return dv
}

/**
 * @param {Decoder} decoder
 */
const decoding_readFloat32 = decoder => decoding_readFromDataView(decoder, 4).getFloat32(0, false)

/**
 * @param {Decoder} decoder
 */
const decoding_readFloat64 = decoder => decoding_readFromDataView(decoder, 8).getFloat64(0, false)

/**
 * @param {Decoder} decoder
 */
const decoding_readBigInt64 = decoder => /** @type {any} */ (decoding_readFromDataView(decoder, 8)).getBigInt64(0, false)

/**
 * @param {Decoder} decoder
 */
const decoding_readBigUint64 = decoder => /** @type {any} */ (decoding_readFromDataView(decoder, 8)).getBigUint64(0, false)

/**
 * @type {Array<function(Decoder):any>}
 */
const decoding_readAnyLookupTable = [
  decoder => undefined, // CASE 127: undefined
  decoder => null, // CASE 126: null
  decoding_readVarInt, // CASE 125: integer
  decoding_readFloat32, // CASE 124: float32
  decoding_readFloat64, // CASE 123: float64
  decoding_readBigInt64, // CASE 122: bigint
  decoder => false, // CASE 121: boolean (false)
  decoder => true, // CASE 120: boolean (true)
  decoding_readVarString, // CASE 119: string
  decoder => { // CASE 118: object<string,any>
    const len = decoding_readVarUint(decoder)
    /**
     * @type {Object<string,any>}
     */
    const obj = {}
    for (let i = 0; i < len; i++) {
      const key = decoding_readVarString(decoder)
      obj[key] = decoding_readAny(decoder)
    }
    return obj
  },
  decoder => { // CASE 117: array<any>
    const len = decoding_readVarUint(decoder)
    const arr = []
    for (let i = 0; i < len; i++) {
      arr.push(decoding_readAny(decoder))
    }
    return arr
  },
  decoding_readVarUint8Array // CASE 116: Uint8Array
]

/**
 * @param {Decoder} decoder
 */
const decoding_readAny = decoder => decoding_readAnyLookupTable[127 - decoding_readUint8(decoder)](decoder)

/**
 * T must not be null.
 *
 * @template T
 */
class decoding_RleDecoder extends (/* unused pure expression or super */ null && (decoding_Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   * @param {function(Decoder):T} reader
   */
  constructor (uint8Array, reader) {
    super(uint8Array)
    /**
     * The reader
     */
    this.reader = reader
    /**
     * Current state
     * @type {T|null}
     */
    this.s = null
    this.count = 0
  }

  read () {
    if (this.count === 0) {
      this.s = this.reader(this)
      if (lib0_decoding_hasContent(this)) {
        this.count = decoding_readVarUint(this) + 1 // see encoder implementation for the reason why this is incremented
      } else {
        this.count = -1 // read the current value forever
      }
    }
    this.count--
    return /** @type {T} */ (this.s)
  }
}

class decoding_IntDiffDecoder extends (/* unused pure expression or super */ null && (decoding_Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   * @param {number} start
   */
  constructor (uint8Array, start) {
    super(uint8Array)
    /**
     * Current state
     * @type {number}
     */
    this.s = start
  }

  /**
   * @return {number}
   */
  read () {
    this.s += decoding_readVarInt(this)
    return this.s
  }
}

class decoding_RleIntDiffDecoder extends (/* unused pure expression or super */ null && (decoding_Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   * @param {number} start
   */
  constructor (uint8Array, start) {
    super(uint8Array)
    /**
     * Current state
     * @type {number}
     */
    this.s = start
    this.count = 0
  }

  /**
   * @return {number}
   */
  read () {
    if (this.count === 0) {
      this.s += decoding_readVarInt(this)
      if (lib0_decoding_hasContent(this)) {
        this.count = decoding_readVarUint(this) + 1 // see encoder implementation for the reason why this is incremented
      } else {
        this.count = -1 // read the current value forever
      }
    }
    this.count--
    return /** @type {number} */ (this.s)
  }
}

class decoding_UintOptRleDecoder extends (/* unused pure expression or super */ null && (decoding_Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   */
  constructor (uint8Array) {
    super(uint8Array)
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
  }

  read () {
    if (this.count === 0) {
      this.s = decoding_readVarInt(this)
      // if the sign is negative, we read the count too, otherwise count is 1
      const isNegative = math.isNegativeZero(this.s)
      this.count = 1
      if (isNegative) {
        this.s = -this.s
        this.count = decoding_readVarUint(this) + 2
      }
    }
    this.count--
    return /** @type {number} */ (this.s)
  }
}

class decoding_IncUintOptRleDecoder extends (/* unused pure expression or super */ null && (decoding_Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   */
  constructor (uint8Array) {
    super(uint8Array)
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
  }

  read () {
    if (this.count === 0) {
      this.s = decoding_readVarInt(this)
      // if the sign is negative, we read the count too, otherwise count is 1
      const isNegative = math.isNegativeZero(this.s)
      this.count = 1
      if (isNegative) {
        this.s = -this.s
        this.count = decoding_readVarUint(this) + 2
      }
    }
    this.count--
    return /** @type {number} */ (this.s++)
  }
}

class decoding_IntDiffOptRleDecoder extends (/* unused pure expression or super */ null && (decoding_Decoder)) {
  /**
   * @param {Uint8Array} uint8Array
   */
  constructor (uint8Array) {
    super(uint8Array)
    /**
     * @type {number}
     */
    this.s = 0
    this.count = 0
    this.diff = 0
  }

  /**
   * @return {number}
   */
  read () {
    if (this.count === 0) {
      const diff = decoding_readVarInt(this)
      // if the first bit is set, we read more data
      const hasCount = diff & 1
      this.diff = diff >> 1
      this.count = 1
      if (hasCount) {
        this.count = decoding_readVarUint(this) + 2
      }
    }
    this.s += this.diff
    this.count--
    return this.s
  }
}

class decoding_StringDecoder {
  /**
   * @param {Uint8Array} uint8Array
   */
  constructor (uint8Array) {
    this.decoder = new decoding_UintOptRleDecoder(uint8Array)
    this.str = decoding_readVarString(this.decoder)
    /**
     * @type {number}
     */
    this.spos = 0
  }

  /**
   * @return {string}
   */
  read () {
    const end = this.spos + this.decoder.read()
    const res = this.str.slice(this.spos, end)
    this.spos = end
    return res
  }
}

;// CONCATENATED MODULE: ./node_modules/y-protocols/sync.js
/**
 * @module sync-protocol
 */





/**
 * @typedef {Map<number, number>} StateMap
 */

/**
 * Core Yjs defines two message types:
 * • YjsSyncStep1: Includes the State Set of the sending client. When received, the client should reply with YjsSyncStep2.
 * • YjsSyncStep2: Includes all missing structs and the complete delete set. When received, the client is assured that it
 *   received all information from the remote client.
 *
 * In a peer-to-peer network, you may want to introduce a SyncDone message type. Both parties should initiate the connection
 * with SyncStep1. When a client received SyncStep2, it should reply with SyncDone. When the local client received both
 * SyncStep2 and SyncDone, it is assured that it is synced to the remote client.
 *
 * In a client-server model, you want to handle this differently: The client should initiate the connection with SyncStep1.
 * When the server receives SyncStep1, it should reply with SyncStep2 immediately followed by SyncStep1. The client replies
 * with SyncStep2 when it receives SyncStep1. Optionally the server may send a SyncDone after it received SyncStep2, so the
 * client knows that the sync is finished.  There are two reasons for this more elaborated sync model: 1. This protocol can
 * easily be implemented on top of http and websockets. 2. The server shoul only reply to requests, and not initiate them.
 * Therefore it is necesarry that the client initiates the sync.
 *
 * Construction of a message:
 * [messageType : varUint, message definition..]
 *
 * Note: A message does not include information about the room name. This must to be handled by the upper layer protocol!
 *
 * stringify[messageType] stringifies a message definition (messageType is already read from the bufffer)
 */

const messageYjsSyncStep1 = 0
const messageYjsSyncStep2 = 1
const messageYjsUpdate = 2

/**
 * Create a sync step 1 message based on the state of the current shared document.
 *
 * @param {encoding.Encoder} encoder
 * @param {Y.Doc} doc
 */
const writeSyncStep1 = (encoder, doc) => {
  encoding_writeVarUint(encoder, messageYjsSyncStep1)
  const sv = consume_shared_module_default_yjs_13_5_singleton_.encodeStateVector(doc)
  encoding_writeVarUint8Array(encoder, sv)
}

/**
 * @param {encoding.Encoder} encoder
 * @param {Y.Doc} doc
 * @param {Uint8Array} [encodedStateVector]
 */
const writeSyncStep2 = (encoder, doc, encodedStateVector) => {
  encoding_writeVarUint(encoder, messageYjsSyncStep2)
  encoding_writeVarUint8Array(encoder, consume_shared_module_default_yjs_13_5_singleton_.encodeStateAsUpdate(doc, encodedStateVector))
}

/**
 * Read SyncStep1 message and reply with SyncStep2.
 *
 * @param {decoding.Decoder} decoder The reply to the received message
 * @param {encoding.Encoder} encoder The received message
 * @param {Y.Doc} doc
 */
const readSyncStep1 = (decoder, encoder, doc) =>
  writeSyncStep2(encoder, doc, decoding_readVarUint8Array(decoder))

/**
 * Read and apply Structs and then DeleteStore to a y instance.
 *
 * @param {decoding.Decoder} decoder
 * @param {Y.Doc} doc
 * @param {any} transactionOrigin
 */
const readSyncStep2 = (decoder, doc, transactionOrigin) => {
  try {
    consume_shared_module_default_yjs_13_5_singleton_.applyUpdate(doc, decoding_readVarUint8Array(decoder), transactionOrigin)
  } catch (error) {
    // This catches errors that are thrown by event handlers
    console.error('Caught error while handling a Yjs update', error)
  }
}

/**
 * @param {encoding.Encoder} encoder
 * @param {Uint8Array} update
 */
const writeUpdate = (encoder, update) => {
  encoding_writeVarUint(encoder, messageYjsUpdate)
  encoding_writeVarUint8Array(encoder, update)
}

/**
 * Read and apply Structs and then DeleteStore to a y instance.
 *
 * @param {decoding.Decoder} decoder
 * @param {Y.Doc} doc
 * @param {any} transactionOrigin
 */
const readUpdate = readSyncStep2

/**
 * @param {decoding.Decoder} decoder A message received from another client
 * @param {encoding.Encoder} encoder The reply message. Will not be sent if empty.
 * @param {Y.Doc} doc
 * @param {any} transactionOrigin
 */
const readSyncMessage = (decoder, encoder, doc, transactionOrigin) => {
  const messageType = decoding_readVarUint(decoder)
  switch (messageType) {
    case messageYjsSyncStep1:
      readSyncStep1(decoder, encoder, doc)
      break
    case messageYjsSyncStep2:
      readSyncStep2(decoder, doc, transactionOrigin)
      break
    case messageYjsUpdate:
      readUpdate(decoder, doc, transactionOrigin)
      break
    default:
      throw new Error('Unknown message type')
  }
  return messageType
}

;// CONCATENATED MODULE: ./node_modules/y-protocols/auth.js

 // eslint-disable-line



const messagePermissionDenied = 0

/**
 * @param {encoding.Encoder} encoder
 * @param {string} reason
 */
const writePermissionDenied = (encoder, reason) => {
  encoding.writeVarUint(encoder, messagePermissionDenied)
  encoding.writeVarString(encoder, reason)
}

/**
 * @callback PermissionDeniedHandler
 * @param {any} y
 * @param {string} reason
 */

/**
 *
 * @param {decoding.Decoder} decoder
 * @param {Y.Doc} y
 * @param {PermissionDeniedHandler} permissionDeniedHandler
 */
const readAuthMessage = (decoder, y, permissionDeniedHandler) => {
  switch (decoding_readVarUint(decoder)) {
    case messagePermissionDenied: permissionDeniedHandler(y, decoding_readVarString(decoder))
  }
}

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/time.js
/**
 * Utility module to work with time.
 *
 * @module time
 */




/**
 * Return current time.
 *
 * @return {Date}
 */
const time_getDate = () => new Date()

/**
 * Return current unix time.
 *
 * @return {number}
 */
const time_getUnixTime = Date.now

/**
 * Transform time (in ms) to a human readable format. E.g. 1100 => 1.1s. 60s => 1min. .001 => 10μs.
 *
 * @param {number} d duration in milliseconds
 * @return {string} humanized approximation of time
 */
const time_humanizeDuration = d => {
  if (d < 60000) {
    const p = metric.prefix(d, -1)
    return math.round(p.n * 100) / 100 + p.prefix + 's'
  }
  d = math.floor(d / 1000)
  const seconds = d % 60
  const minutes = math.floor(d / 60) % 60
  const hours = math.floor(d / 3600) % 24
  const days = math.floor(d / 86400)
  if (days > 0) {
    return days + 'd' + ((hours > 0 || minutes > 30) ? ' ' + (minutes > 30 ? hours + 1 : hours) + 'h' : '')
  }
  if (hours > 0) {
    /* istanbul ignore next */
    return hours + 'h' + ((minutes > 0 || seconds > 30) ? ' ' + (seconds > 30 ? minutes + 1 : minutes) + 'min' : '')
  }
  return minutes + 'min' + (seconds > 0 ? ' ' + seconds + 's' : '')
}

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/set.js
/**
 * Utility module to work with sets.
 *
 * @module set
 */

const lib0_set_create = () => new Set()

/**
 * @template T
 * @param {Set<T>} set
 * @return {Array<T>}
 */
const set_toArray = set => Array.from(set)

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/array.js
/**
 * Utility module to work with Arrays.
 *
 * @module array
 */

/**
 * Return the last element of an array. The element must exist
 *
 * @template L
 * @param {Array<L>} arr
 * @return {L}
 */
const array_last = arr => arr[arr.length - 1]

/**
 * @template C
 * @return {Array<C>}
 */
const lib0_array_create = () => /** @type {Array<C>} */ ([])

/**
 * @template D
 * @param {Array<D>} a
 * @return {Array<D>}
 */
const lib0_array_copy = a => /** @type {Array<D>} */ (a.slice())

/**
 * Append elements from src to dest
 *
 * @template M
 * @param {Array<M>} dest
 * @param {Array<M>} src
 */
const array_appendTo = (dest, src) => {
  for (let i = 0; i < src.length; i++) {
    dest.push(src[i])
  }
}

/**
 * Transforms something array-like to an actual Array.
 *
 * @function
 * @template T
 * @param {ArrayLike<T>|Iterable<T>} arraylike
 * @return {T}
 */
const lib0_array_from = Array.from

/**
 * True iff condition holds on every element in the Array.
 *
 * @function
 * @template ITEM
 *
 * @param {Array<ITEM>} arr
 * @param {function(ITEM, number, Array<ITEM>):boolean} f
 * @return {boolean}
 */
const array_every = (arr, f) => arr.every(f)

/**
 * True iff condition holds on some element in the Array.
 *
 * @function
 * @template S
 * @param {Array<S>} arr
 * @param {function(S, number, Array<S>):boolean} f
 * @return {boolean}
 */
const array_some = (arr, f) => arr.some(f)

/**
 * @template ELEM
 *
 * @param {Array<ELEM>} a
 * @param {Array<ELEM>} b
 * @return {boolean}
 */
const array_equalFlat = (a, b) => a.length === b.length && array_every(a, (item, index) => item === b[index])

/**
 * @template ELEM
 * @param {Array<Array<ELEM>>} arr
 * @return {Array<ELEM>}
 */
const array_flatten = arr => arr.reduce((acc, val) => acc.concat(val), [])

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/observable.js
/**
 * Observable class prototype.
 *
 * @module observable
 */





/**
 * Handles named events.
 *
 * @template N
 */
class Observable {
  constructor () {
    /**
     * Some desc.
     * @type {Map<N, any>}
     */
    this._observers = map_create()
  }

  /**
   * @param {N} name
   * @param {function} f
   */
  on (name, f) {
    map_setIfUndefined(this._observers, name, lib0_set_create).add(f)
  }

  /**
   * @param {N} name
   * @param {function} f
   */
  once (name, f) {
    /**
     * @param  {...any} args
     */
    const _f = (...args) => {
      this.off(name, _f)
      f(...args)
    }
    this.on(name, _f)
  }

  /**
   * @param {N} name
   * @param {function} f
   */
  off (name, f) {
    const observers = this._observers.get(name)
    if (observers !== undefined) {
      observers.delete(f)
      if (observers.size === 0) {
        this._observers.delete(name)
      }
    }
  }

  /**
   * Emit a named event. All registered event listeners that listen to the
   * specified name will receive the event.
   *
   * @todo This should catch exceptions
   *
   * @param {N} name The event name.
   * @param {Array<any>} args The arguments that are applied to the event listener.
   */
  emit (name, args) {
    // copy all listeners to an array first to make sure that no event is emitted to listeners that are subscribed while the event handler is called.
    return lib0_array_from((this._observers.get(name) || map_create()).values()).forEach(f => f(...args))
  }

  destroy () {
    this._observers = map_create()
  }
}

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/object.js
/**
 * Utility functions for working with EcmaScript objects.
 *
 * @module object
 */

/**
 * @return {Object<string,any>} obj
 */
const object_create = () => Object.create(null)

/**
 * Object.assign
 */
const object_assign = Object.assign

/**
 * @param {Object<string,any>} obj
 */
const keys = Object.keys

/**
 * @param {Object<string,any>} obj
 * @param {function(any,string):any} f
 */
const forEach = (obj, f) => {
  for (const key in obj) {
    f(obj[key], key)
  }
}

/**
 * @template R
 * @param {Object<string,any>} obj
 * @param {function(any,string):R} f
 * @return {Array<R>}
 */
const object_map = (obj, f) => {
  const results = []
  for (const key in obj) {
    results.push(f(obj[key], key))
  }
  return results
}

/**
 * @param {Object<string,any>} obj
 * @return {number}
 */
const object_length = obj => keys(obj).length

/**
 * @param {Object<string,any>} obj
 * @param {function(any,string):boolean} f
 * @return {boolean}
 */
const object_some = (obj, f) => {
  for (const key in obj) {
    if (f(obj[key], key)) {
      return true
    }
  }
  return false
}

/**
 * @param {Object<string,any>} obj
 * @param {function(any,string):boolean} f
 * @return {boolean}
 */
const object_every = (obj, f) => {
  for (const key in obj) {
    if (!f(obj[key], key)) {
      return false
    }
  }
  return true
}

/**
 * Calls `Object.prototype.hasOwnProperty`.
 *
 * @param {any} obj
 * @param {string|symbol} key
 * @return {boolean}
 */
const hasProperty = (obj, key) => Object.prototype.hasOwnProperty.call(obj, key)

/**
 * @param {Object<string,any>} a
 * @param {Object<string,any>} b
 * @return {boolean}
 */
const object_equalFlat = (a, b) => a === b || (object_length(a) === object_length(b) && object_every(a, (val, key) => (val !== undefined || hasProperty(b, key)) && b[key] === val))

;// CONCATENATED MODULE: ./node_modules/y-protocols/node_modules/lib0/function.js
/**
 * Common functions and function call helpers.
 *
 * @module function
 */




/**
 * Calls all functions in `fs` with args. Only throws after all functions were called.
 *
 * @param {Array<function>} fs
 * @param {Array<any>} args
 */
const function_callAll = (fs, args, i = 0) => {
  try {
    for (; i < fs.length; i++) {
      fs[i](...args)
    }
  } finally {
    if (i < fs.length) {
      function_callAll(fs, args, i + 1)
    }
  }
}

const function_nop = () => {}

/**
 * @template T
 * @param {function():T} f
 * @return {T}
 */
const function_apply = f => f()

/**
 * @template A
 *
 * @param {A} a
 * @return {A}
 */
const function_id = a => a

/**
 * @template T
 *
 * @param {T} a
 * @param {T} b
 * @return {boolean}
 */
const function_equalityStrict = (a, b) => a === b

/**
 * @template T
 *
 * @param {Array<T>|object} a
 * @param {Array<T>|object} b
 * @return {boolean}
 */
const function_equalityFlat = (a, b) => a === b || (a != null && b != null && a.constructor === b.constructor && ((a instanceof Array && array.equalFlat(a, /** @type {Array<T>} */ (b))) || (typeof a === 'object' && object.equalFlat(a, b))))

/**
 * @param {any} a
 * @param {any} b
 * @return {boolean}
 */
const function_equalityDeep = (a, b) => {
  if (a == null || b == null) {
    return function_equalityStrict(a, b)
  }
  if (a.constructor !== b.constructor) {
    return false
  }
  if (a === b) {
    return true
  }
  switch (a.constructor) {
    case ArrayBuffer:
      a = new Uint8Array(a)
      b = new Uint8Array(b)
    // eslint-disable-next-line no-fallthrough
    case Uint8Array: {
      if (a.byteLength !== b.byteLength) {
        return false
      }
      for (let i = 0; i < a.length; i++) {
        if (a[i] !== b[i]) {
          return false
        }
      }
      break
    }
    case Set: {
      if (a.size !== b.size) {
        return false
      }
      for (const value of a) {
        if (!b.has(value)) {
          return false
        }
      }
      break
    }
    case Map: {
      if (a.size !== b.size) {
        return false
      }
      for (const key of a.keys()) {
        if (!b.has(key) || !function_equalityDeep(a.get(key), b.get(key))) {
          return false
        }
      }
      break
    }
    case Object:
      if (object_length(a) !== object_length(b)) {
        return false
      }
      for (const key in a) {
        if (!hasProperty(a, key) || !function_equalityDeep(a[key], b[key])) {
          return false
        }
      }
      break
    case Array:
      if (a.length !== b.length) {
        return false
      }
      for (let i = 0; i < a.length; i++) {
        if (!function_equalityDeep(a[i], b[i])) {
          return false
        }
      }
      break
    default:
      return false
  }
  return true
}

;// CONCATENATED MODULE: ./node_modules/y-protocols/awareness.js
/**
 * @module awareness-protocol
 */







 // eslint-disable-line

const outdatedTimeout = 30000

/**
 * @typedef {Object} MetaClientState
 * @property {number} MetaClientState.clock
 * @property {number} MetaClientState.lastUpdated unix timestamp
 */

/**
 * The Awareness class implements a simple shared state protocol that can be used for non-persistent data like awareness information
 * (cursor, username, status, ..). Each client can update its own local state and listen to state changes of
 * remote clients. Every client may set a state of a remote peer to `null` to mark the client as offline.
 *
 * Each client is identified by a unique client id (something we borrow from `doc.clientID`). A client can override
 * its own state by propagating a message with an increasing timestamp (`clock`). If such a message is received, it is
 * applied if the known state of that client is older than the new state (`clock < newClock`). If a client thinks that
 * a remote client is offline, it may propagate a message with
 * `{ clock: currentClientClock, state: null, client: remoteClient }`. If such a
 * message is received, and the known clock of that client equals the received clock, it will override the state with `null`.
 *
 * Before a client disconnects, it should propagate a `null` state with an updated clock.
 *
 * Awareness states must be updated every 30 seconds. Otherwise the Awareness instance will delete the client state.
 *
 * @extends {Observable<string>}
 */
class Awareness extends Observable {
  /**
   * @param {Y.Doc} doc
   */
  constructor (doc) {
    super()
    this.doc = doc
    /**
     * @type {number}
     */
    this.clientID = doc.clientID
    /**
     * Maps from client id to client state
     * @type {Map<number, Object<string, any>>}
     */
    this.states = new Map()
    /**
     * @type {Map<number, MetaClientState>}
     */
    this.meta = new Map()
    this._checkInterval = /** @type {any} */ (setInterval(() => {
      const now = time_getUnixTime()
      if (this.getLocalState() !== null && (outdatedTimeout / 2 <= now - /** @type {{lastUpdated:number}} */ (this.meta.get(this.clientID)).lastUpdated)) {
        // renew local clock
        this.setLocalState(this.getLocalState())
      }
      /**
       * @type {Array<number>}
       */
      const remove = []
      this.meta.forEach((meta, clientid) => {
        if (clientid !== this.clientID && outdatedTimeout <= now - meta.lastUpdated && this.states.has(clientid)) {
          remove.push(clientid)
        }
      })
      if (remove.length > 0) {
        removeAwarenessStates(this, remove, 'timeout')
      }
    }, math_floor(outdatedTimeout / 10)))
    doc.on('destroy', () => {
      this.destroy()
    })
    this.setLocalState({})
  }

  destroy () {
    this.emit('destroy', [this])
    this.setLocalState(null)
    super.destroy()
    clearInterval(this._checkInterval)
  }

  /**
   * @return {Object<string,any>|null}
   */
  getLocalState () {
    return this.states.get(this.clientID) || null
  }

  /**
   * @param {Object<string,any>|null} state
   */
  setLocalState (state) {
    const clientID = this.clientID
    const currLocalMeta = this.meta.get(clientID)
    const clock = currLocalMeta === undefined ? 0 : currLocalMeta.clock + 1
    const prevState = this.states.get(clientID)
    if (state === null) {
      this.states.delete(clientID)
    } else {
      this.states.set(clientID, state)
    }
    this.meta.set(clientID, {
      clock,
      lastUpdated: time_getUnixTime()
    })
    const added = []
    const updated = []
    const filteredUpdated = []
    const removed = []
    if (state === null) {
      removed.push(clientID)
    } else if (prevState == null) {
      if (state != null) {
        added.push(clientID)
      }
    } else {
      updated.push(clientID)
      if (!function_equalityDeep(prevState, state)) {
        filteredUpdated.push(clientID)
      }
    }
    if (added.length > 0 || filteredUpdated.length > 0 || removed.length > 0) {
      this.emit('change', [{ added, updated: filteredUpdated, removed }, 'local'])
    }
    this.emit('update', [{ added, updated, removed }, 'local'])
  }

  /**
   * @param {string} field
   * @param {any} value
   */
  setLocalStateField (field, value) {
    const state = this.getLocalState()
    if (state !== null) {
      this.setLocalState({
        ...state,
        [field]: value
      })
    }
  }

  /**
   * @return {Map<number,Object<string,any>>}
   */
  getStates () {
    return this.states
  }
}

/**
 * Mark (remote) clients as inactive and remove them from the list of active peers.
 * This change will be propagated to remote clients.
 *
 * @param {Awareness} awareness
 * @param {Array<number>} clients
 * @param {any} origin
 */
const removeAwarenessStates = (awareness, clients, origin) => {
  const removed = []
  for (let i = 0; i < clients.length; i++) {
    const clientID = clients[i]
    if (awareness.states.has(clientID)) {
      awareness.states.delete(clientID)
      if (clientID === awareness.clientID) {
        const curMeta = /** @type {MetaClientState} */ (awareness.meta.get(clientID))
        awareness.meta.set(clientID, {
          clock: curMeta.clock + 1,
          lastUpdated: time_getUnixTime()
        })
      }
      removed.push(clientID)
    }
  }
  if (removed.length > 0) {
    awareness.emit('change', [{ added: [], updated: [], removed }, origin])
    awareness.emit('update', [{ added: [], updated: [], removed }, origin])
  }
}

/**
 * @param {Awareness} awareness
 * @param {Array<number>} clients
 * @return {Uint8Array}
 */
const encodeAwarenessUpdate = (awareness, clients, states = awareness.states) => {
  const len = clients.length
  const encoder = encoding_createEncoder()
  encoding_writeVarUint(encoder, len)
  for (let i = 0; i < len; i++) {
    const clientID = clients[i]
    const state = states.get(clientID) || null
    const clock = /** @type {MetaClientState} */ (awareness.meta.get(clientID)).clock
    encoding_writeVarUint(encoder, clientID)
    encoding_writeVarUint(encoder, clock)
    encoding_writeVarString(encoder, JSON.stringify(state))
  }
  return encoding_toUint8Array(encoder)
}

/**
 * Modify the content of an awareness update before re-encoding it to an awareness update.
 *
 * This might be useful when you have a central server that wants to ensure that clients
 * cant hijack somebody elses identity.
 *
 * @param {Uint8Array} update
 * @param {function(any):any} modify
 * @return {Uint8Array}
 */
const modifyAwarenessUpdate = (update, modify) => {
  const decoder = decoding.createDecoder(update)
  const encoder = encoding.createEncoder()
  const len = decoding.readVarUint(decoder)
  encoding.writeVarUint(encoder, len)
  for (let i = 0; i < len; i++) {
    const clientID = decoding.readVarUint(decoder)
    const clock = decoding.readVarUint(decoder)
    const state = JSON.parse(decoding.readVarString(decoder))
    const modifiedState = modify(state)
    encoding.writeVarUint(encoder, clientID)
    encoding.writeVarUint(encoder, clock)
    encoding.writeVarString(encoder, JSON.stringify(modifiedState))
  }
  return encoding.toUint8Array(encoder)
}

/**
 * @param {Awareness} awareness
 * @param {Uint8Array} update
 * @param {any} origin This will be added to the emitted change event
 */
const applyAwarenessUpdate = (awareness, update, origin) => {
  const decoder = decoding_createDecoder(update)
  const timestamp = time_getUnixTime()
  const added = []
  const updated = []
  const filteredUpdated = []
  const removed = []
  const len = decoding_readVarUint(decoder)
  for (let i = 0; i < len; i++) {
    const clientID = decoding_readVarUint(decoder)
    let clock = decoding_readVarUint(decoder)
    const state = JSON.parse(decoding_readVarString(decoder))
    const clientMeta = awareness.meta.get(clientID)
    const prevState = awareness.states.get(clientID)
    const currClock = clientMeta === undefined ? 0 : clientMeta.clock
    if (currClock < clock || (currClock === clock && state === null && awareness.states.has(clientID))) {
      if (state === null) {
        // never let a remote client remove this local state
        if (clientID === awareness.clientID && awareness.getLocalState() != null) {
          // remote client removed the local state. Do not remote state. Broadcast a message indicating
          // that this client still exists by increasing the clock
          clock++
        } else {
          awareness.states.delete(clientID)
        }
      } else {
        awareness.states.set(clientID, state)
      }
      awareness.meta.set(clientID, {
        clock,
        lastUpdated: timestamp
      })
      if (clientMeta === undefined && state !== null) {
        added.push(clientID)
      } else if (clientMeta !== undefined && state === null) {
        removed.push(clientID)
      } else if (state !== null) {
        if (!function_equalityDeep(state, prevState)) {
          filteredUpdated.push(clientID)
        }
        updated.push(clientID)
      }
    }
  }
  if (added.length > 0 || filteredUpdated.length > 0 || removed.length > 0) {
    awareness.emit('change', [{
      added, updated: filteredUpdated, removed
    }, origin])
  }
  if (added.length > 0 || updated.length > 0 || removed.length > 0) {
    awareness.emit('update', [{
      added, updated, removed
    }, origin])
  }
}

;// CONCATENATED MODULE: ./node_modules/lib0/observable.js
/**
 * Observable class prototype.
 *
 * @module observable
 */





/**
 * Handles named events.
 *
 * @template N
 */
class observable_Observable {
  constructor () {
    /**
     * Some desc.
     * @type {Map<N, any>}
     */
    this._observers = create()
  }

  /**
   * @param {N} name
   * @param {function} f
   */
  on (name, f) {
    setIfUndefined(this._observers, name, set_create).add(f)
  }

  /**
   * @param {N} name
   * @param {function} f
   */
  once (name, f) {
    /**
     * @param  {...any} args
     */
    const _f = (...args) => {
      this.off(name, _f)
      f(...args)
    }
    this.on(name, _f)
  }

  /**
   * @param {N} name
   * @param {function} f
   */
  off (name, f) {
    const observers = this._observers.get(name)
    if (observers !== undefined) {
      observers.delete(f)
      if (observers.size === 0) {
        this._observers.delete(name)
      }
    }
  }

  /**
   * Emit a named event. All registered event listeners that listen to the
   * specified name will receive the event.
   *
   * @todo This should catch exceptions
   *
   * @param {N} name The event name.
   * @param {Array<any>} args The arguments that are applied to the event listener.
   */
  emit (name, args) {
    // copy all listeners to an array first to make sure that no event is emitted to listeners that are subscribed while the event handler is called.
    return array_from((this._observers.get(name) || create()).values()).forEach(f => f(...args))
  }

  destroy () {
    this._observers = create()
  }
}

;// CONCATENATED MODULE: ./node_modules/lib0/object.js
/**
 * Utility functions for working with EcmaScript objects.
 *
 * @module object
 */

/**
 * @return {Object<string,any>} obj
 */
const lib0_object_create = () => Object.create(null)

/**
 * Object.assign
 */
const lib0_object_assign = Object.assign

/**
 * @param {Object<string,any>} obj
 */
const object_keys = Object.keys

/**
 * @template V
 * @param {{[k:string]:V}} obj
 * @param {function(V,string):any} f
 */
const object_forEach = (obj, f) => {
  for (const key in obj) {
    f(obj[key], key)
  }
}

/**
 * @todo implement mapToArray & map
 *
 * @template R
 * @param {Object<string,any>} obj
 * @param {function(any,string):R} f
 * @return {Array<R>}
 */
const lib0_object_map = (obj, f) => {
  const results = []
  for (const key in obj) {
    results.push(f(obj[key], key))
  }
  return results
}

/**
 * @param {Object<string,any>} obj
 * @return {number}
 */
const lib0_object_length = obj => object_keys(obj).length

/**
 * @param {Object<string,any>} obj
 * @param {function(any,string):boolean} f
 * @return {boolean}
 */
const lib0_object_some = (obj, f) => {
  for (const key in obj) {
    if (f(obj[key], key)) {
      return true
    }
  }
  return false
}

/**
 * @param {Object|undefined} obj
 */
const isEmpty = obj => {
  for (const _k in obj) {
    return false
  }
  return true
}

/**
 * @param {Object<string,any>} obj
 * @param {function(any,string):boolean} f
 * @return {boolean}
 */
const lib0_object_every = (obj, f) => {
  for (const key in obj) {
    if (!f(obj[key], key)) {
      return false
    }
  }
  return true
}

/**
 * Calls `Object.prototype.hasOwnProperty`.
 *
 * @param {any} obj
 * @param {string|symbol} key
 * @return {boolean}
 */
const object_hasProperty = (obj, key) => Object.prototype.hasOwnProperty.call(obj, key)

/**
 * @param {Object<string,any>} a
 * @param {Object<string,any>} b
 * @return {boolean}
 */
const lib0_object_equalFlat = (a, b) => a === b || (lib0_object_length(a) === lib0_object_length(b) && lib0_object_every(a, (val, key) => (val !== undefined || object_hasProperty(b, key)) && b[key] === val))

;// CONCATENATED MODULE: ./node_modules/lib0/url.js
/**
 * Utility module to work with urls.
 *
 * @module url
 */



/**
 * Parse query parameters from an url.
 *
 * @param {string} url
 * @return {Object<string,string>}
 */
const decodeQueryParams = url => {
  /**
   * @type {Object<string,string>}
   */
  const query = {}
  const urlQuerySplit = url.split('?')
  const pairs = urlQuerySplit[urlQuerySplit.length - 1].split('&')
  for (let i = 0; i < pairs.length; i++) {
    const item = pairs[i]
    if (item.length > 0) {
      const pair = item.split('=')
      query[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1] || '')
    }
  }
  return query
}

/**
 * @param {Object<string,string>} params
 * @return {string}
 */
const encodeQueryParams = params =>
  lib0_object_map(params, (val, key) => `${encodeURIComponent(key)}=${encodeURIComponent(val)}`).join('&')

;// CONCATENATED MODULE: ./node_modules/y-websocket/src/y-websocket.js
/* provided dependency */ var y_websocket_process = __webpack_require__(4155);
/**
 * @module provider/websocket
 */

/* eslint-env browser */

 // eslint-disable-line











const messageSync = 0
const messageQueryAwareness = 3
const messageAwareness = 1
const messageAuth = 2

/**
 *                       encoder,          decoder,          provider,          emitSynced, messageType
 * @type {Array<function(encoding.Encoder, decoding.Decoder, WebsocketProvider, boolean,    number):void>}
 */
const messageHandlers = []

messageHandlers[messageSync] = (
  encoder,
  decoder,
  provider,
  emitSynced,
  _messageType
) => {
  writeVarUint(encoder, messageSync)
  const syncMessageType = readSyncMessage(
    decoder,
    encoder,
    provider.doc,
    provider
  )
  if (
    emitSynced && syncMessageType === messageYjsSyncStep2 &&
    !provider.synced
  ) {
    provider.synced = true
  }
}

messageHandlers[messageQueryAwareness] = (
  encoder,
  _decoder,
  provider,
  _emitSynced,
  _messageType
) => {
  writeVarUint(encoder, messageAwareness)
  writeVarUint8Array(
    encoder,
    encodeAwarenessUpdate(
      provider.awareness,
      Array.from(provider.awareness.getStates().keys())
    )
  )
}

messageHandlers[messageAwareness] = (
  _encoder,
  decoder,
  provider,
  _emitSynced,
  _messageType
) => {
  applyAwarenessUpdate(
    provider.awareness,
    readVarUint8Array(decoder),
    provider
  )
}

messageHandlers[messageAuth] = (
  _encoder,
  decoder,
  provider,
  _emitSynced,
  _messageType
) => {
  readAuthMessage(
    decoder,
    provider.doc,
    (_ydoc, reason) => permissionDeniedHandler(provider, reason)
  )
}

// @todo - this should depend on awareness.outdatedTime
const messageReconnectTimeout = 30000

/**
 * @param {WebsocketProvider} provider
 * @param {string} reason
 */
const permissionDeniedHandler = (provider, reason) =>
  console.warn(`Permission denied to access ${provider.url}.\n${reason}`)

/**
 * @param {WebsocketProvider} provider
 * @param {Uint8Array} buf
 * @param {boolean} emitSynced
 * @return {encoding.Encoder}
 */
const readMessage = (provider, buf, emitSynced) => {
  const decoder = createDecoder(buf)
  const encoder = createEncoder()
  const messageType = readVarUint(decoder)
  const messageHandler = provider.messageHandlers[messageType]
  if (/** @type {any} */ (messageHandler)) {
    messageHandler(encoder, decoder, provider, emitSynced, messageType)
  } else {
    console.error('Unable to compute message')
  }
  return encoder
}

/**
 * @param {WebsocketProvider} provider
 */
const setupWS = (provider) => {
  if (provider.shouldConnect && provider.ws === null) {
    const websocket = new provider._WS(provider.url)
    websocket.binaryType = 'arraybuffer'
    provider.ws = websocket
    provider.wsconnecting = true
    provider.wsconnected = false
    provider.synced = false

    websocket.onmessage = (event) => {
      provider.wsLastMessageReceived = getUnixTime()
      const encoder = readMessage(provider, new Uint8Array(event.data), true)
      if (encoding_length(encoder) > 1) {
        websocket.send(toUint8Array(encoder))
      }
    }
    websocket.onerror = (event) => {
      provider.emit('connection-error', [event, provider])
    }
    websocket.onclose = (event) => {
      provider.emit('connection-close', [event, provider])
      provider.ws = null
      provider.wsconnecting = false
      if (provider.wsconnected) {
        provider.wsconnected = false
        provider.synced = false
        // update awareness (all users except local left)
        removeAwarenessStates(
          provider.awareness,
          Array.from(provider.awareness.getStates().keys()).filter((client) =>
            client !== provider.doc.clientID
          ),
          provider
        )
        provider.emit('status', [{
          status: 'disconnected'
        }])
      } else {
        provider.wsUnsuccessfulReconnects++
      }
      // Start with no reconnect timeout and increase timeout by
      // using exponential backoff starting with 100ms
      setTimeout(
        setupWS,
        min(
          pow(2, provider.wsUnsuccessfulReconnects) * 100,
          provider.maxBackoffTime
        ),
        provider
      )
    }
    websocket.onopen = () => {
      provider.wsLastMessageReceived = getUnixTime()
      provider.wsconnecting = false
      provider.wsconnected = true
      provider.wsUnsuccessfulReconnects = 0
      provider.emit('status', [{
        status: 'connected'
      }])
      // always send sync step 1 when connected
      const encoder = createEncoder()
      writeVarUint(encoder, messageSync)
      writeSyncStep1(encoder, provider.doc)
      websocket.send(toUint8Array(encoder))
      // broadcast local awareness state
      if (provider.awareness.getLocalState() !== null) {
        const encoderAwarenessState = createEncoder()
        writeVarUint(encoderAwarenessState, messageAwareness)
        writeVarUint8Array(
          encoderAwarenessState,
          encodeAwarenessUpdate(provider.awareness, [
            provider.doc.clientID
          ])
        )
        websocket.send(toUint8Array(encoderAwarenessState))
      }
    }
    provider.emit('status', [{
      status: 'connecting'
    }])
  }
}

/**
 * @param {WebsocketProvider} provider
 * @param {ArrayBuffer} buf
 */
const broadcastMessage = (provider, buf) => {
  const ws = provider.ws
  if (provider.wsconnected && ws && ws.readyState === ws.OPEN) {
    ws.send(buf)
  }
  if (provider.bcconnected) {
    publish(provider.bcChannel, buf, provider)
  }
}

/**
 * Websocket Provider for Yjs. Creates a websocket connection to sync the shared document.
 * The document name is attached to the provided url. I.e. the following example
 * creates a websocket connection to http://localhost:1234/my-document-name
 *
 * @example
 *   import * as Y from 'yjs'
 *   import { WebsocketProvider } from 'y-websocket'
 *   const doc = new Y.Doc()
 *   const provider = new WebsocketProvider('http://localhost:1234', 'my-document-name', doc)
 *
 * @extends {Observable<string>}
 */
class WebsocketProvider extends observable_Observable {
  /**
   * @param {string} serverUrl
   * @param {string} roomname
   * @param {Y.Doc} doc
   * @param {object} opts
   * @param {boolean} [opts.connect]
   * @param {awarenessProtocol.Awareness} [opts.awareness]
   * @param {Object<string,string>} [opts.params]
   * @param {typeof WebSocket} [opts.WebSocketPolyfill] Optionall provide a WebSocket polyfill
   * @param {number} [opts.resyncInterval] Request server state every `resyncInterval` milliseconds
   * @param {number} [opts.maxBackoffTime] Maximum amount of time to wait before trying to reconnect (we try to reconnect using exponential backoff)
   * @param {boolean} [opts.disableBc] Disable cross-tab BroadcastChannel communication
   */
  constructor (serverUrl, roomname, doc, {
    connect = true,
    awareness = new Awareness(doc),
    params = {},
    WebSocketPolyfill = WebSocket,
    resyncInterval = -1,
    maxBackoffTime = 2500,
    disableBc = false
  } = {}) {
    super()
    // ensure that url is always ends with /
    while (serverUrl[serverUrl.length - 1] === '/') {
      serverUrl = serverUrl.slice(0, serverUrl.length - 1)
    }
    const encodedParams = encodeQueryParams(params)
    this.maxBackoffTime = maxBackoffTime
    this.bcChannel = serverUrl + '/' + roomname
    this.url = serverUrl + '/' + roomname +
      (encodedParams.length === 0 ? '' : '?' + encodedParams)
    this.roomname = roomname
    this.doc = doc
    this._WS = WebSocketPolyfill
    this.awareness = awareness
    this.wsconnected = false
    this.wsconnecting = false
    this.bcconnected = false
    this.disableBc = disableBc
    this.wsUnsuccessfulReconnects = 0
    this.messageHandlers = messageHandlers.slice()
    /**
     * @type {boolean}
     */
    this._synced = false
    /**
     * @type {WebSocket?}
     */
    this.ws = null
    this.wsLastMessageReceived = 0
    /**
     * Whether to connect to other peers or not
     * @type {boolean}
     */
    this.shouldConnect = connect

    /**
     * @type {number}
     */
    this._resyncInterval = 0
    if (resyncInterval > 0) {
      this._resyncInterval = /** @type {any} */ (setInterval(() => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          // resend sync step 1
          const encoder = createEncoder()
          writeVarUint(encoder, messageSync)
          writeSyncStep1(encoder, doc)
          this.ws.send(toUint8Array(encoder))
        }
      }, resyncInterval))
    }

    /**
     * @param {ArrayBuffer} data
     * @param {any} origin
     */
    this._bcSubscriber = (data, origin) => {
      if (origin !== this) {
        const encoder = readMessage(this, new Uint8Array(data), false)
        if (encoding_length(encoder) > 1) {
          publish(this.bcChannel, toUint8Array(encoder), this)
        }
      }
    }
    /**
     * Listens to Yjs updates and sends them to remote peers (ws and broadcastchannel)
     * @param {Uint8Array} update
     * @param {any} origin
     */
    this._updateHandler = (update, origin) => {
      if (origin !== this) {
        const encoder = createEncoder()
        writeVarUint(encoder, messageSync)
        writeUpdate(encoder, update)
        broadcastMessage(this, toUint8Array(encoder))
      }
    }
    this.doc.on('update', this._updateHandler)
    /**
     * @param {any} changed
     * @param {any} _origin
     */
    this._awarenessUpdateHandler = ({ added, updated, removed }, _origin) => {
      const changedClients = added.concat(updated).concat(removed)
      const encoder = createEncoder()
      writeVarUint(encoder, messageAwareness)
      writeVarUint8Array(
        encoder,
        encodeAwarenessUpdate(awareness, changedClients)
      )
      broadcastMessage(this, toUint8Array(encoder))
    }
    this._unloadHandler = () => {
      removeAwarenessStates(
        this.awareness,
        [doc.clientID],
        'window unload'
      )
    }
    if (typeof window !== 'undefined') {
      window.addEventListener('unload', this._unloadHandler)
    } else if (typeof y_websocket_process !== 'undefined') {
      y_websocket_process.on('exit', this._unloadHandler)
    }
    awareness.on('update', this._awarenessUpdateHandler)
    this._checkInterval = /** @type {any} */ (setInterval(() => {
      if (
        this.wsconnected &&
        messageReconnectTimeout <
          getUnixTime() - this.wsLastMessageReceived
      ) {
        // no message received in a long time - not even your own awareness
        // updates (which are updated every 15 seconds)
        /** @type {WebSocket} */ (this.ws).close()
      }
    }, messageReconnectTimeout / 10))
    if (connect) {
      this.connect()
    }
  }

  /**
   * @type {boolean}
   */
  get synced () {
    return this._synced
  }

  set synced (state) {
    if (this._synced !== state) {
      this._synced = state
      this.emit('synced', [state])
      this.emit('sync', [state])
    }
  }

  destroy () {
    if (this._resyncInterval !== 0) {
      clearInterval(this._resyncInterval)
    }
    clearInterval(this._checkInterval)
    this.disconnect()
    if (typeof window !== 'undefined') {
      window.removeEventListener('unload', this._unloadHandler)
    } else if (typeof y_websocket_process !== 'undefined') {
      y_websocket_process.off('exit', this._unloadHandler)
    }
    this.awareness.off('update', this._awarenessUpdateHandler)
    this.doc.off('update', this._updateHandler)
    super.destroy()
  }

  connectBc () {
    if (this.disableBc) {
      return
    }
    if (!this.bcconnected) {
      subscribe(this.bcChannel, this._bcSubscriber)
      this.bcconnected = true
    }
    // send sync step1 to bc
    // write sync step 1
    const encoderSync = createEncoder()
    writeVarUint(encoderSync, messageSync)
    writeSyncStep1(encoderSync, this.doc)
    publish(this.bcChannel, toUint8Array(encoderSync), this)
    // broadcast local state
    const encoderState = createEncoder()
    writeVarUint(encoderState, messageSync)
    writeSyncStep2(encoderState, this.doc)
    publish(this.bcChannel, toUint8Array(encoderState), this)
    // write queryAwareness
    const encoderAwarenessQuery = createEncoder()
    writeVarUint(encoderAwarenessQuery, messageQueryAwareness)
    publish(
      this.bcChannel,
      toUint8Array(encoderAwarenessQuery),
      this
    )
    // broadcast local awareness state
    const encoderAwarenessState = createEncoder()
    writeVarUint(encoderAwarenessState, messageAwareness)
    writeVarUint8Array(
      encoderAwarenessState,
      encodeAwarenessUpdate(this.awareness, [
        this.doc.clientID
      ])
    )
    publish(
      this.bcChannel,
      toUint8Array(encoderAwarenessState),
      this
    )
  }

  disconnectBc () {
    // broadcast message with local awareness state set to null (indicating disconnect)
    const encoder = createEncoder()
    writeVarUint(encoder, messageAwareness)
    writeVarUint8Array(
      encoder,
      encodeAwarenessUpdate(this.awareness, [
        this.doc.clientID
      ], new Map())
    )
    broadcastMessage(this, toUint8Array(encoder))
    if (this.bcconnected) {
      unsubscribe(this.bcChannel, this._bcSubscriber)
      this.bcconnected = false
    }
  }

  disconnect () {
    this.shouldConnect = false
    this.disconnectBc()
    if (this.ws !== null) {
      this.ws.close()
    }
  }

  connect () {
    this.shouldConnect = true
    if (!this.wsconnected && this.ws === null) {
      setupWS(this)
      this.connectBc()
    }
  }
}

;// CONCATENATED MODULE: ./node_modules/@jupyter/docprovider/lib/requests.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/


/**
 * Document session endpoint provided by `jupyter_collaboration`
 * See https://github.com/jupyterlab/jupyter_collaboration
 */
const DOC_SESSION_URL = 'api/collaboration/session';
async function requestDocSession(format, type, path) {
    const { makeSettings, makeRequest, ResponseError } = services_7_0_singleton_.ServerConnection;
    const settings = makeSettings();
    const url = coreutils_6_0_singleton_.URLExt.join(settings.baseUrl, DOC_SESSION_URL, encodeURIComponent(path));
    const data = {
        method: 'PUT',
        body: JSON.stringify({ format, type })
    };
    const response = await makeRequest(url, data, settings);
    if (response.status !== 200 && response.status !== 201) {
        throw new ResponseError(response);
    }
    return response.json();
}

;// CONCATENATED MODULE: ./node_modules/@jupyter/docprovider/lib/yprovider.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/





/**
 * A class to provide Yjs synchronization over WebSocket.
 *
 * We specify custom messages that the server can interpret. For reference please look in yjs_ws_server.
 *
 */
class WebSocketProvider {
    /**
     * Construct a new WebSocketProvider
     *
     * @param options The instantiation options for a WebSocketProvider
     */
    constructor(options) {
        this._onConnectionClosed = (event) => {
            if (event.code === 1003) {
                console.error('Document provider closed:', event.reason);
                (0,apputils_4_0_singleton_.showErrorMessage)(this._trans.__('Session expired'), this._trans.__('The document session expired. You need to reload this browser tab.'), [apputils_4_0_singleton_.Dialog.okButton({ label: this._trans.__('Reload') })])
                    .then((r) => {
                    if (r.button.accept) {
                        window.location.reload();
                    }
                })
                    .catch(e => window.location.reload());
                // Dispose shared model immediately. Better break the document model,
                // than overriding data on disk.
                this._sharedModel.dispose();
            }
        };
        this._ready = new coreutils_2_0_singleton_.PromiseDelegate();
        this._isDisposed = false;
        this._path = options.path;
        this._contentType = options.contentType;
        this._format = options.format;
        this._serverUrl = options.url;
        this._sharedModel = options.model;
        this._awareness = options.model.awareness;
        this._yWebsocketProvider = null;
        this._trans = options.translator;
        const user = options.user;
        user.ready
            .then(() => {
            this._onUserChanged(user);
        })
            .catch(e => console.error(e));
        user.userChanged.connect(this._onUserChanged, this);
        this._connect();
    }
    /**
     * Test whether the object has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A promise that resolves when the document provider is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Dispose of the resources held by the object.
     */
    dispose() {
        var _a, _b;
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        (_a = this._yWebsocketProvider) === null || _a === void 0 ? void 0 : _a.off('connection-close', this._onConnectionClosed);
        (_b = this._yWebsocketProvider) === null || _b === void 0 ? void 0 : _b.destroy();
        signaling_2_0_singleton_.Signal.clearData(this);
    }
    _connect() {
        requestDocSession(this._format, this._contentType, this._path)
            .then((session) => {
            this._yWebsocketProvider = new WebsocketProvider(this._serverUrl, `${session.format}:${session.type}:${session.fileId}`, this._sharedModel.ydoc, {
                disableBc: true,
                params: { sessionId: session.sessionId },
                awareness: this._awareness
            });
            this._yWebsocketProvider.on('connection-close', this._onConnectionClosed);
        })
            .then(r => this._ready.resolve())
            .catch(e => console.warn(e));
    }
    _onUserChanged(user) {
        this._awareness.setLocalStateField('user', user.identity);
    }
}

;// CONCATENATED MODULE: ./node_modules/@jupyter/docprovider/lib/ydrive.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * The url for the default drive service.
 */
const DOCUMENT_PROVIDER_URL = 'api/collaboration/room';
/**
 * A Collaborative implementation for an `IDrive`, talking to the
 * server using the Jupyter REST API and a WebSocket connection.
 */
class YDrive extends services_7_0_singleton_.Drive {
    /**
     * Construct a new drive object.
     *
     * @param user - The user manager to add the identity to the awareness of documents.
     */
    constructor(user, translator) {
        super({ name: 'RTC' });
        this._onCreate = (options, sharedModel) => {
            if (typeof options.format !== 'string') {
                return;
            }
            try {
                const provider = new WebSocketProvider({
                    url: coreutils_6_0_singleton_.URLExt.join(this.serverSettings.wsUrl, DOCUMENT_PROVIDER_URL),
                    path: options.path,
                    format: options.format,
                    contentType: options.contentType,
                    model: sharedModel,
                    user: this._user,
                    translator: this._trans
                });
                const key = `${options.format}:${options.contentType}:${options.path}`;
                this._providers.set(key, provider);
                sharedModel.disposed.connect(() => {
                    const provider = this._providers.get(key);
                    if (provider) {
                        provider.dispose();
                        this._providers.delete(key);
                    }
                });
                for (const provider of this._providers.keys()) {
                    if (provider === key) {
                        continue;
                    }
                    const path = provider.split(':')[2];
                    if (options.path === path) {
                        (0,apputils_4_0_singleton_.showDialog)({
                            title: this._trans.__('Warning'),
                            body: this._trans.__('Opening a document with multiple views simultaneously is not supported.Please, close one view otherwise, you might lose some of your changes.'),
                            buttons: [apputils_4_0_singleton_.Dialog.okButton()]
                        });
                    }
                }
            }
            catch (error) {
                // Falling back to the contents API if opening the websocket failed
                //  This may happen if the shared document is not a YDocument.
                console.error(`Failed to open websocket connection for ${options.path}.\n:${error}`);
            }
        };
        this._user = user;
        this._trans = translator;
        this._providers = new Map();
        this.sharedModelFactory = new SharedModelFactory(this._onCreate);
    }
    /**
     * Dispose of the resources held by the manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._providers.forEach(p => p.dispose());
        this._providers.clear();
        super.dispose();
    }
    /**
     * Get a file or directory.
     *
     * @param localPath: The path to the file.
     *
     * @param options: The options used to fetch the file.
     *
     * @returns A promise which resolves with the file content.
     *
     * Uses the [Jupyter Notebook API](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyter/notebook/master/notebook/services/api/api.yaml#!/contents) and validates the response model.
     */
    async get(localPath, options) {
        if (options && options.format && options.type) {
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._providers.get(key);
            if (provider) {
                const model = super.get(localPath, { ...options, content: false });
                await provider.ready;
                return model;
            }
        }
        return super.get(localPath, options);
    }
    /**
     * Save a file.
     *
     * @param localPath - The desired file path.
     *
     * @param options - Optional overrides to the model.
     *
     * @returns A promise which resolves with the file content model when the
     *   file is saved.
     */
    async save(localPath, options = {}) {
        // Check that there is a provider - it won't e.g. if the document model is not collaborative.
        if (options.format && options.type) {
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._providers.get(key);
            if (provider) {
                // Save is done from the backend
                return this.get(localPath, { ...options, content: false });
            }
        }
        return super.save(localPath, options);
    }
}
/**
 * Yjs sharedModel factory for real-time collaboration.
 */
class SharedModelFactory {
    /**
     * Shared model factory constructor
     *
     * @param _onCreate Callback on new document model creation
     */
    constructor(_onCreate) {
        this._onCreate = _onCreate;
        /**
         * Whether the IDrive supports real-time collaboration or not.
         */
        this.collaborative = true;
        this._documentFactories = new Map();
    }
    /**
     * Register a SharedDocumentFactory.
     *
     * @param type Document type
     * @param factory Document factory
     */
    registerDocumentFactory(type, factory) {
        if (this._documentFactories.has(type)) {
            throw new Error(`The content type ${type} already exists`);
        }
        this._documentFactories.set(type, factory);
    }
    /**
     * Create a new `ISharedDocument` instance.
     *
     * It should return `undefined` if the factory is not able to create a `ISharedDocument`.
     */
    createNew(options) {
        if (typeof options.format !== 'string') {
            console.warn(`Only defined format are supported; got ${options.format}.`);
            return;
        }
        if (!options.collaborative) {
            // Bail if the document model does not support collaboration
            // the `sharedModel` will be the default one.
            return;
        }
        if (this._documentFactories.has(options.contentType)) {
            const factory = this._documentFactories.get(options.contentType);
            const sharedModel = factory(options);
            this._onCreate(options, sharedModel);
            return sharedModel;
        }
        return;
    }
}

;// CONCATENATED MODULE: ./node_modules/@jupyter/docprovider/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The collaborative drive.
 */
const ICollaborativeDrive = new coreutils_2_0_singleton_.Token('@jupyter/collaboration-extension:ICollaborativeDrive');

;// CONCATENATED MODULE: ./node_modules/@jupyter/docprovider/lib/index.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module docprovider
 */





/***/ })

}]);