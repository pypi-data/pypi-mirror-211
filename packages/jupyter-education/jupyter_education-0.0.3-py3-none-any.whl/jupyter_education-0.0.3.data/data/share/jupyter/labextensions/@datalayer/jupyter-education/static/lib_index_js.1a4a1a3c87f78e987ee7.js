"use strict";
(self["webpackChunk_datalayer_jupyter_education"] = self["webpackChunk_datalayer_jupyter_education"] || []).push([["lib_index_js"],{

/***/ "../../../node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!*********************************************************************!*\
  !*** ../../../node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \*********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n\n.dla-Container {\n    overflow-y: visible;\n}\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;;;;CAIC;;AAED;IACI,mBAAmB;AACvB","sourcesContent":["/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n\n.dla-Container {\n    overflow-y: visible;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../../node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!**********************************************************************!*\
  !*** ../../../node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \**********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../../../../node_modules/css-loader/dist/cjs.js!./base.css */ "../../../node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../icons/react/default/esm/DaskIcon.js":
/*!*************************************************!*\
  !*** ../../icons/react/default/esm/DaskIcon.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function DaskIcon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    fill: colored ? 'none' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('none') ? 'white' : 'currentColor'),
    "aria-hidden": "true",
    viewBox: "0 0 20 20",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#FFC11E' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#FFC11E') ? 'white' : 'currentColor'),
    fillRule: "evenodd",
    d: "M5.383 6.332l5.094-2.902a.158.158 0 00.082-.137V1.551a.822.822 0 00-.317-.668.819.819 0 00-.898-.059L2.219 4.883a.801.801 0 00-.406.691l-.004 9.164c0 .258.109.512.316.668.27.203.613.223.898.059l1.512-.856a.17.17 0 00.078-.14l.004-6.828c0-.543.293-1.04.766-1.309zm0 0",
    clipRule: "evenodd"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#EF1161' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#EF1161') ? 'white' : 'currentColor'),
    fillRule: "evenodd",
    d: "M17.594 5.016a.826.826 0 00-.809 0L9.656 9.074a.8.8 0 00-.402.692l-.004 9.199c0 .289.152.547.406.691a.808.808 0 00.809 0l7.125-4.058a.796.796 0 00.406-.692L18 5.711c0-.29-.152-.55-.406-.695zm0 0",
    clipRule: "evenodd"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#FC6E6B' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#FC6E6B') ? 'white' : 'currentColor'),
    fillRule: "evenodd",
    d: "M9.297 8.457L14 5.781a.16.16 0 00.082-.14l.004-2.024a.828.828 0 00-.316-.668.805.805 0 00-.899-.058L10.918 4 5.742 6.945a.807.807 0 00-.406.696v6.921l-.004 2.243c0 .254.11.511.316.668a.82.82 0 00.899.058l1.902-1.082a.164.164 0 00.082-.14V9.766c.004-.54.293-1.04.766-1.309zm0 0",
    clipRule: "evenodd"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(DaskIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../../icons/react/default/esm/PyTorchIcon.js":
/*!****************************************************!*\
  !*** ../../icons/react/default/esm/PyTorchIcon.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function PyTorchIcon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    fill: colored ? 'none' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('none') ? 'white' : 'currentColor'),
    viewBox: "0 0 20 20",
    "aria-hidden": "true",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#EE4C2C' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#EE4C2C') ? 'white' : 'currentColor'),
    d: "M15.882 5.877L14.43 7.33a6.218 6.218 0 010 8.782 6.218 6.218 0 01-8.782 0 6.218 6.218 0 010-8.782L9.52 3.457l.484-.553V0L4.127 5.877a8.221 8.221 0 000 11.686 8.22 8.22 0 0011.685 0c3.32-3.25 3.32-8.505.07-11.686z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#EE4C2C' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#EE4C2C') ? 'white' : 'currentColor'),
    d: "M12.977 5.462a1.106 1.106 0 100-2.212 1.106 1.106 0 000 2.212z"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(PyTorchIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../../icons/react/default/esm/TensorFlowIcon.js":
/*!*******************************************************!*\
  !*** ../../icons/react/default/esm/TensorFlowIcon.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function TensorFlowIcon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    fill: colored ? 'none' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('none') ? 'white' : 'currentColor'),
    "aria-hidden": "true",
    viewBox: "0 0 20 20",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#E55B2D' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#E55B2D') ? 'white' : 'currentColor'),
    d: "M11.332 3.077v3.077l5.33 3.077V6.154l-5.33-3.077zM.674 6.154V9.23l2.664 1.538V7.692L.674 6.154zm7.993 1.538L6.003 9.231v9.23L8.667 20v-6.154l2.665 1.539v-3.077l-2.665-1.539V7.692z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#ED8E24' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#ED8E24') ? 'white' : 'currentColor'),
    d: "M11.332 3.077L3.338 7.692v3.077l5.33-3.077v3.077l2.664-1.538V3.077zm7.994 1.538l-2.665 1.539V9.23l2.665-1.539V4.615zm-5.33 6.154l-2.664 1.539v3.077l2.665-1.539V10.77zm-2.664 4.616l-2.665-1.539V20l2.665-1.538v-3.077z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#F8BF3C' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#F8BF3C') ? 'white' : 'currentColor'),
    d: "M11.332 0L.674 6.154l2.664 1.538 7.994-4.615 5.33 3.077 2.665-1.539L11.331 0zm0 9.23l-2.665 1.54 2.665 1.538 2.665-1.539-2.665-1.538z"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(TensorFlowIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "./lib/component/MockComponent.js":
/*!****************************************!*\
  !*** ./lib/component/MockComponent.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react */ "webpack/sharing/consume/default/@primer/react/@primer/react");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_primer_react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/octicons-react */ "webpack/sharing/consume/default/@primer/octicons-react/@primer/octicons-react?85dd");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/UnderlineNav2/index.js");
/* harmony import */ var _store__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./../store */ "./lib/store/index.js");
/* harmony import */ var _MockTab1__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./MockTab1 */ "./lib/component/MockTab1.js");
/* harmony import */ var _MockTab2__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./MockTab2 */ "./lib/component/MockTab2.js");
/* harmony import */ var _MockTab3__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./MockTab3 */ "./lib/component/MockTab3.js");
/* harmony import */ var _MockTab4__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./MockTab4 */ "./lib/component/MockTab4.js");
/* harmony import */ var _MockTab5__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./MockTab5 */ "./lib/component/MockTab5.js");











const MockComponent = () => {
    const [tab, setTab] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(1);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_store__WEBPACK_IMPORTED_MODULE_4__.TimerView, { timer: _store__WEBPACK_IMPORTED_MODULE_4__.timer }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.ThemeProvider, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.BaseStyles, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.Box, { style: { maxWidth: 700 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.Box, { mb: 3, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.UnderlineNav, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.UnderlineNav.Item, { "aria-current": "page", icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_3__.CpuIcon, onSelect: e => { e.preventDefault(); setTab(1); }, children: "Kernels" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.UnderlineNav.Item, { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_3__.CodeIcon, counter: 6, onSelect: e => { e.preventDefault(); setTab(2); }, children: "Notebooks" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.UnderlineNav.Item, { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_3__.AlertIcon, onSelect: e => { e.preventDefault(); setTab(3); }, children: "Warnings" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.UnderlineNav.Item, { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_3__.HistoryIcon, counter: 7, onSelect: e => { e.preventDefault(); setTab(4); }, children: "History" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.UnderlineNav.Item, { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_3__.CommentDiscussionIcon, onSelect: e => { e.preventDefault(); setTab(5); }, children: "More" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__.Box, { children: [(tab === 1) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_MockTab1__WEBPACK_IMPORTED_MODULE_6__["default"], {}), (tab === 2) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_MockTab2__WEBPACK_IMPORTED_MODULE_7__["default"], {}), (tab === 3) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_MockTab3__WEBPACK_IMPORTED_MODULE_8__["default"], {}), (tab === 4) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_MockTab4__WEBPACK_IMPORTED_MODULE_9__["default"], {}), (tab === 5) && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_MockTab5__WEBPACK_IMPORTED_MODULE_10__["default"], {})] })] }) }) })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MockComponent);


/***/ }),

/***/ "./lib/component/MockTab1.js":
/*!***********************************!*\
  !*** ./lib/component/MockTab1.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "webpack/sharing/consume/default/@primer/react/@primer/react");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_primer_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/octicons-react */ "webpack/sharing/consume/default/@primer/octicons-react/@primer/octicons-react?85dd");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @datalayer/icons-react/default */ "../../icons/react/default/esm/DaskIcon.js");
/* harmony import */ var _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @datalayer/icons-react/default */ "../../icons/react/default/esm/PyTorchIcon.js");
/* harmony import */ var _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @datalayer/icons-react/default */ "../../icons/react/default/esm/TensorFlowIcon.js");




const MockTab1 = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu.Button, { children: "Kernels" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu.Overlay, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { onSelect: event => console.log('New file'), children: "New kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: "Copy kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: "Edit kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Divider, {}), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { variant: "danger", children: "Delete kernel" })] }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_3__["default"], {}) }), "Dask kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_4__["default"], {}) }), "PyTorch Kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_5__["default"], {}) }), "Tensorflow Kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Box, { borderColor: "border.default", borderBottomWidth: 1, borderBottomStyle: "solid", pb: 3 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.LinkIcon, {}) }), "Starting..."] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ProgressBar, { progress: 80 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Box, { borderColor: "border.default", borderBottomWidth: 1, borderBottomStyle: "solid", pb: 3 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Avatar, { src: "https://github.com/mona.png" }) }), "Me"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { variant: "danger", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.AlertIcon, {}) }), "4 vulnerabilities"] })] })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MockTab1);


/***/ }),

/***/ "./lib/component/MockTab2.js":
/*!***********************************!*\
  !*** ./lib/component/MockTab2.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "webpack/sharing/consume/default/@primer/react/@primer/react");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_primer_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/TreeView/TreeView.js");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/octicons-react */ "webpack/sharing/consume/default/@primer/octicons-react/@primer/octicons-react?85dd");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__);




const MockTab2 = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.Item, { id: "", defaultExpanded: true, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.DirectoryIcon, {}) }), "Notebooks", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.SubTree, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.Item, { id: "src/Avatar.tsx", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.FileIcon, {}) }), "Deep learing", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.TrailingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.StyledOcticon, { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.DiffAddedIcon, color: "success.fg", "aria-label": "added" }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.Item, { id: "", current: true, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.FileIcon, {}) }), "AI for fun", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.TrailingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.StyledOcticon, { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.DiffModifiedIcon, color: "attention.fg", "aria-label": "modified" }) })] })] })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.Item, { id: "", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.FileIcon, {}) }), "README.mdx", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_3__.TreeView.TrailingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.StyledOcticon, { icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.DiffModifiedIcon, color: "attention.fg", "aria-label": "modified" }) })] })] }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MockTab2);


/***/ }),

/***/ "./lib/component/MockTab3.js":
/*!***********************************!*\
  !*** ./lib/component/MockTab3.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "webpack/sharing/consume/default/@primer/react/@primer/react");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_primer_react__WEBPACK_IMPORTED_MODULE_1__);


const MockTab3 = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Box, { style: { width: 300, paddingTop: 20 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Box, { justifyContent: "center", display: "flex", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Button, { variant: "primary", children: "Hello!" }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Popover, { relative: true, open: true, caret: "top", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Popover.Content, { sx: { mt: 2 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Heading, { sx: { fontSize: 2 }, children: "Popover heading" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Text, { as: "p", children: "Message about this particular piece of UI." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Button, { children: "Got it!" })] }) })] }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MockTab3);


/***/ }),

/***/ "./lib/component/MockTab4.js":
/*!***********************************!*\
  !*** ./lib/component/MockTab4.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "webpack/sharing/consume/default/@primer/react/@primer/react");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_primer_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @datalayer/icons-react/default */ "../../icons/react/default/esm/PyTorchIcon.js");
/* harmony import */ var _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @datalayer/icons-react/default */ "../../icons/react/default/esm/TensorFlowIcon.js");
/* harmony import */ var _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @datalayer/icons-react/default */ "../../icons/react/default/esm/DaskIcon.js");



const MockTab4 = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Box, { m: 1, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.SubNav, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.SubNav.Links, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.SubNav.Link, { href: "#", selected: true, children: "All" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.SubNav.Link, { href: "#", children: "Recent" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.SubNav.Link, { href: "#", children: "Older" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline.Badge, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.StyledOcticon, { icon: _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_2__["default"] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline.Body, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Link, { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "You" }), "created one ", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Link, { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "PyTorch Kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Link, { href: "#", color: "fg.muted", muted: true, children: "Just now" })] })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline.Badge, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.StyledOcticon, { icon: _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_3__["default"] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline.Body, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Link, { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "You" }), "created one ", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Link, { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "TensorFlow Kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Link, { href: "#", color: "fg.muted", muted: true, children: "5m ago" })] })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline.Badge, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.StyledOcticon, { icon: _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_4__["default"] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Timeline.Body, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Link, { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "You" }), "created one ", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Link, { href: "#", sx: { fontWeight: 'bold', color: 'fg.default', mr: 1 }, muted: true, children: "Dask Kernel" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Link, { href: "#", color: "fg.muted", muted: true, children: "7m ago" })] })] })] })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MockTab4);


/***/ }),

/***/ "./lib/component/MockTab5.js":
/*!***********************************!*\
  !*** ./lib/component/MockTab5.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @primer/react */ "webpack/sharing/consume/default/@primer/react/@primer/react");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_primer_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/octicons-react */ "webpack/sharing/consume/default/@primer/octicons-react/@primer/octicons-react?85dd");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @datalayer/icons-react/default */ "../../icons/react/default/esm/DaskIcon.js");
/* harmony import */ var _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @datalayer/icons-react/default */ "../../icons/react/default/esm/PyTorchIcon.js");
/* harmony import */ var _datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @datalayer/icons-react/default */ "../../icons/react/default/esm/TensorFlowIcon.js");




const MockTab5 = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu.Button, { children: "Menu" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionMenu.Overlay, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { onSelect: event => console.log('New file'), children: "New file" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: "Copy link" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: "Edit file" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Divider, {}), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { variant: "danger", children: "Delete file" })] }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_3__["default"], {}) }), "Dask kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_4__["default"], {}) }), "PyTorch Kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_default__WEBPACK_IMPORTED_MODULE_5__["default"], {}) }), "Tensorflow Kernel"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.LinkIcon, {}) }), "github.com/primer"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { variant: "danger", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_octicons_react__WEBPACK_IMPORTED_MODULE_2__.AlertIcon, {}) }), "4 vulnerabilities"] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.Item, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ActionList.LeadingVisual, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Avatar, { src: "https://github.com/mona.png" }) }), "mona"] })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.ProgressBar, { progress: 80 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Box, { style: { width: 300, paddingTop: 20 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Box, { justifyContent: "center", display: "flex", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Button, { variant: "primary", children: "Hello!" }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Popover, { relative: true, open: true, caret: "top", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Popover.Content, { sx: { mt: 2 }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Heading, { sx: { fontSize: 2 }, children: "Popover heading" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Text, { as: "p", children: "Message about this particular piece of UI." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_1__.Button, { children: "Got it!" })] }) })] })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MockTab5);


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyter_education', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IJupyterEducation": () => (/* binding */ IJupyterEducation),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "jupyterDocker": () => (/* binding */ jupyterDocker)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _ws__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./ws */ "./lib/ws.js");
/* harmony import */ var _store__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./store */ "./lib/store/index.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");










const IJupyterEducation = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.Token('@datalayer/jupyter-education:plugin');
const jupyterDocker = {
    timer: _store__WEBPACK_IMPORTED_MODULE_6__.timer,
    TimerView: _store__WEBPACK_IMPORTED_MODULE_6__.TimerView,
};
/**
 * The command IDs used by the jupyter-education-widget plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'create-jupyter-education-widget';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the @datalayer/jupyter-education extension.
 */
const plugin = {
    id: '@datalayer/jupyter-education:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher],
    provides: IJupyterEducation,
    activate: (app, palette, settingRegistry, launcher) => {
        const { commands } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: 'Show Jupyter Education',
            label: 'Jupyter Education',
            icon: (args) => _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.reactIcon,
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_7__.DatalayerWidget();
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
                widget.title.label = 'Jupyter Education';
                widget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.reactIcon;
                app.shell.add(widget, 'main');
            }
        });
        const category = 'Jupyter Education';
        palette.addItem({ command, category, args: { origin: 'from palette' } });
        if (launcher) {
            launcher.add({
                command,
                category: 'Datalayer',
                rank: -1,
            });
        }
        console.log('JupyterLab extension @datalayer/jupyter-education is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('@datalayer/jupyter-education settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for @datalayer/jupyter-education.', reason);
            });
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_8__.requestAPI)('get_example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The jupyter_education server extension appears to be missing.\n${reason}`);
        });
        (0,_ws__WEBPACK_IMPORTED_MODULE_9__.connect)('ws://localhost:8888/jupyter_education/echo', true);
        return jupyterDocker;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/store/index.js":
/*!****************************!*\
  !*** ./lib/store/index.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Timer": () => (/* binding */ Timer),
/* harmony export */   "TimerView": () => (/* binding */ TimerView),
/* harmony export */   "timer": () => (/* binding */ timer)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var mobx__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! mobx */ "webpack/sharing/consume/default/mobx/mobx?e3fc");
/* harmony import */ var mobx__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(mobx__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var mobx_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! mobx-react */ "webpack/sharing/consume/default/mobx-react/mobx-react");
/* harmony import */ var mobx_react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(mobx_react__WEBPACK_IMPORTED_MODULE_2__);



class Timer {
    secondsPassed = 0;
    constructor() {
        (0,mobx__WEBPACK_IMPORTED_MODULE_1__.makeAutoObservable)(this);
    }
    reset() {
        this.secondsPassed = 0;
    }
    increaseTimer() {
        this.secondsPassed += 1;
    }
}
const timer = new Timer();
setInterval(() => {
    timer.increaseTimer();
}, 1000);
const TimerView = (0,mobx_react__WEBPACK_IMPORTED_MODULE_2__.observer)(({ timer }) => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)("button", { onClick: () => timer.reset(), children: ["Jupyter Education: ", timer.secondsPassed] })));


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DatalayerWidget": () => (/* binding */ DatalayerWidget)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _component_MockComponent__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./component/MockComponent */ "./lib/component/MockComponent.js");



class DatalayerWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor() {
        super();
        this.addClass('dla-Container');
    }
    render() {
        return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_component_MockComponent__WEBPACK_IMPORTED_MODULE_2__["default"], {});
    }
}


/***/ }),

/***/ "./lib/ws.js":
/*!*******************!*\
  !*** ./lib/ws.js ***!
  \*******************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "connect": () => (/* binding */ connect),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
const connect = (address, retry) => {
    const ws = new WebSocket(address);
    ws.onerror = (event) => {
        console.log('---', event);
    };
    ws.onmessage = (message) => {
        console.log('---', message);
    };
    ws.onopen = (event) => {
        console.log('---', event);
        ws.send('ping');
    };
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (connect);


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../../node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ })

}]);
//# sourceMappingURL=lib_index_js.1a4a1a3c87f78e987ee7.js.map