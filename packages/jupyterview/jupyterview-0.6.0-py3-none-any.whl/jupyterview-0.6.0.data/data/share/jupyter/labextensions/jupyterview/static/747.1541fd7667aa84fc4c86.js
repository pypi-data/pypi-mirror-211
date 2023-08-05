"use strict";
(self["webpackChunkjupyterview"] = self["webpackChunkjupyterview"] || []).push([[747],{

/***/ 1150:
/***/ ((module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Z: () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_noSourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(8081);
/* harmony import */ var _node_modules_css_loader_dist_runtime_noSourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_noSourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(3645);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_noSourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".jpview-Spinner {\n  position: absolute;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  z-index: 10;\n  left: 0;\n  top: 0;\n  width: 100%;\n  height: 100%;\n  outline: none;\n  background: #00000075;\n}\n\n.jpview-SpinnerContent {\n  border: solid #27b9f39e;\n  margin: 50px auto;\n  text-indent: -9999em;\n  width: 6em;\n  height: 6em;\n  border-radius: 50%;\n  position: relative;\n  animation: load3 1s infinite linear, fadeIn 1s;\n}\n\n.jpview-SpinnerContent:before {\n  width: 50%;\n  height: 50%;\n  background: #f3762605;\n  border-radius: 100% 0 100% 0;\n  box-shadow: inset 6px 5px 0 1px #27b9f3;\n  position: absolute;\n  top: 0;\n  left: 0;\n  content: '';\n}\n\n.jpview-SpinnerContent:after {\n  width: 75%;\n  height: 75%;\n  border-radius: 50%;\n  content: '';\n  margin: auto;\n  position: absolute;\n  top: 0;\n  left: 0;\n  bottom: 0;\n  right: 0;\n}\n\n.jpview-view-toolbar {\n  position: absolute;\n  z-index: 1;\n  left: 10px;\n  top: 10px;\n  background-color: rgba(0, 0, 0, 0.4);\n  display: flex;\n  flex-direction: row;\n}\n.jpview-button {\n  border: none;\n  background-color: var(--jp-layout-color2);\n  color: var(--jp-content-font-color1);\n  min-width: 60px;\n}\n.jpview-button:hover {\n  background-color: var(--jp-layout-color3);\n}\n.jpview-toolbar-button {\n  background: none;\n  color: rgb(187, 187, 187);\n  border-radius: var(--jp-border-radius);\n  font-size: var(--jp-ui-font-size1);\n  display: inline-flex;\n  flex-direction: row;\n  border: none;\n  cursor: pointer;\n  align-items: center;\n  justify-content: center;\n  text-align: left;\n  vertical-align: middle;\n  min-height: 24px;\n  min-width: 12px;\n  font-size: 12px;\n  padding: 0 4px;\n}\n\n.jpview-toolbar-button.dark:hover {\n  background-color: #424242;\n}\n\n.jpview-toolbar-button:active {\n  border: none;\n  box-shadow: none;\n  background-color: var(--jp-warn-color-active, rgba(153, 153, 153, 0.2));\n}\n.jpview-control-panel-title {\n  border-bottom: solid var(--jp-border-width) var(--jp-border-color1);\n  box-shadow: var(--jp-toolbar-box-shadow);\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  min-height: 24px;\n  height: var(--jp-debugger-header-height);\n  background-color: var(--jp-layout-color2);\n}\n\n.jpview-control-panel-title h2 {\n  text-transform: uppercase;\n  font-weight: 600;\n  font-size: var(--jp-ui-font-size0);\n  color: var(--jp-ui-font-color1);\n  padding-left: 8px;\n  padding-right: 4px;\n}\n\n.jpview-control-panel {\n  color: var(--jp-ui-font-color1);\n  background: var(--jp-layout-color1);\n  height: 100%;\n}\n.jpview-control-panel * {\n  font-family: var(--jp-ui-font-family);\n}\n\n.jpview-control-panel-component {\n  font-size: var(--jp-ui-font-size1);\n}\n.jpview-control-panel .MuiAccordion-root.Mui-expanded {\n  margin: 0px 0px !important;\n}\n.jpview-control-panel .MuiAccordionSummary-contentGutters {\n  margin: 10px 0 !important;\n}\n.jpview-control-panel .Mui-expanded .MuiAccordionSummary-gutters {\n  min-height: 38px !important;\n}\n.jpview-control-panel .MuiAccordionSummary-root.MuiAccordionSummary-gutters {\n  min-height: 38px !important;\n}\n\n.jpview-control-panel\n  .MuiAccordionSummary-content.MuiAccordionSummary-contentGutters\n  > span {\n  text-transform: uppercase;\n}\n\n.jpview-input-wrapper {\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  background-color: var(--jp-layout-color1);\n  margin: 3px;\n  font-size: var(--jp-ui-font-size1);\n}\n\n.jpview-input {\n  background: transparent;\n  color: var(--jp-ui-font-color0);\n  background: var(--jp-input-background);\n  outline: none;\n  font-size: var(--jp-ui-font-size1);\n  border: var(--jp-border-width) solid var(--jp-border-color0);\n  width: 95%;\n}\n\n.jpview-slider {\n  -webkit-appearance: none;\n  appearance: none;\n  width: 100%;\n  height: 5px;\n  border-radius: 5px;\n  background: var(--jp-layout-color3);\n  outline: none;\n}\n\n.jpview-slider::-webkit-slider-thumb {\n  -webkit-appearance: none;\n  appearance: none;\n  width: 10px;\n  height: 10px;\n  border-radius: 50%;\n  background: var(--jp-ui-font-color2);\n  cursor: pointer;\n}\n\n.jpview-slider::-moz-range-thumb {\n  width: 10px;\n  height: 10px;\n  border-radius: 50%;\n  background: var(--jp-ui-font-color2);\n  cursor: pointer;\n}\n\n.jpcad-camera-client {\n  width: 15px;\n  height: 15px;\n  position: absolute;\n  z-index: 10;\n  background-color: var(--jp-private-notebook-active-color);\n  border-radius: 50%;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n", ""]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ 3645:
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ 8081:
/***/ ((module) => {



module.exports = function (i) {
  return i[1];
};

/***/ }),

/***/ 3379:
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ 569:
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ 609:
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ 3565:
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ 7795:
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ 4589:
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ 9747:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXTERNAL MODULE: ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js
var injectStylesIntoStyleTag = __webpack_require__(3379);
var injectStylesIntoStyleTag_default = /*#__PURE__*/__webpack_require__.n(injectStylesIntoStyleTag);
// EXTERNAL MODULE: ./node_modules/style-loader/dist/runtime/styleDomAPI.js
var styleDomAPI = __webpack_require__(7795);
var styleDomAPI_default = /*#__PURE__*/__webpack_require__.n(styleDomAPI);
// EXTERNAL MODULE: ./node_modules/style-loader/dist/runtime/insertBySelector.js
var insertBySelector = __webpack_require__(569);
var insertBySelector_default = /*#__PURE__*/__webpack_require__.n(insertBySelector);
// EXTERNAL MODULE: ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js
var setAttributesWithoutAttributes = __webpack_require__(3565);
var setAttributesWithoutAttributes_default = /*#__PURE__*/__webpack_require__.n(setAttributesWithoutAttributes);
// EXTERNAL MODULE: ./node_modules/style-loader/dist/runtime/insertStyleElement.js
var insertStyleElement = __webpack_require__(609);
var insertStyleElement_default = /*#__PURE__*/__webpack_require__.n(insertStyleElement);
// EXTERNAL MODULE: ./node_modules/style-loader/dist/runtime/styleTagTransform.js
var styleTagTransform = __webpack_require__(4589);
var styleTagTransform_default = /*#__PURE__*/__webpack_require__.n(styleTagTransform);
// EXTERNAL MODULE: ./node_modules/css-loader/dist/cjs.js!./style/base.css
var base = __webpack_require__(1150);
;// CONCATENATED MODULE: ./style/base.css

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (styleTagTransform_default());
options.setAttributes = (setAttributesWithoutAttributes_default());

      options.insert = insertBySelector_default().bind(null, "head");
    
options.domAPI = (styleDomAPI_default());
options.insertStyleElement = (insertStyleElement_default());

var update = injectStylesIntoStyleTag_default()(base/* default */.Z, options);




       /* harmony default export */ const style_base = (base/* default */.Z && base/* default.locals */.Z.locals ? base/* default.locals */.Z.locals : undefined);

;// CONCATENATED MODULE: ./style/index.js



/***/ })

}]);