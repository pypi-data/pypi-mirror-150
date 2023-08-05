(self["webpackChunknerfviewer"] = self["webpackChunknerfviewer"] || []).push([["lib_widget_js"],{

/***/ "./lib/ReactWidget.js":
/*!****************************!*\
  !*** ./lib/ReactWidget.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
/* eslint-disable @typescript-eslint/no-unused-vars */
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const widget_model_1 = __webpack_require__(/*! ./hooks/widget-model */ "./lib/hooks/widget-model.js");
const Navigator_1 = __importDefault(__webpack_require__(/*! ./components/Navigator */ "./lib/components/Navigator.js"));
const Viewer_1 = __importDefault(__webpack_require__(/*! ./components/Viewer */ "./lib/components/Viewer.js"));
const AppBar_1 = __importDefault(__webpack_require__(/*! ./components/AppBar */ "./lib/components/AppBar.js"));
function ReactWidget(props) {
    const [view, setView] = react_1.useState(props.view);
    // Global state for current positioning of the camera
    // const [cameraPosition, setCameraPosition] = useModelState(
    //   'currentCameraPosition'
    // );
    // const [textToDisplay] = useModelState('value');
    // const [foo] = useModelState('foo');
    //const [path, setPath] = useState<IPathDatum[]>([]);
    const [{ theta, phi, radius }, setCameraPosition] = widget_model_1.useModelState('cameraCoordinates');
    const [imageArray] = widget_model_1.useModelState('imageArray');
    const [keyframes, setKeyFrames] = widget_model_1.useModelState('keyframes');
    const [videoNum, setVideoNum] = widget_model_1.useModelState('videoNum');
    //const [playNum, setPlayNum] = useModelState('playNum');
    const [videoString, setVideoString] = widget_model_1.useModelState('videoString');
    console.log(keyframes);
    return (react_1.default.createElement("div", null,
        react_1.default.createElement(AppBar_1.default, { setView: setView }),
        view === 'navigation' && (react_1.default.createElement(Navigator_1.default, { cameraPosition: { theta, phi, radius }, setCameraPosition: setCameraPosition, 
            /* TODO: should not hardcode these */
            image: imageArray, keyframes: keyframes, setKeyFrames: setKeyFrames })),
        view === 'rendering' && (react_1.default.createElement(Viewer_1.default, { videoNum: videoNum, setVideoNum: setVideoNum, videoString: videoString, setVideoString: setVideoString }))));
}
function withModelContext(Component) {
    return (props) => (react_1.default.createElement(widget_model_1.WidgetModelContext.Provider, { value: props.model },
        react_1.default.createElement(Component, Object.assign({}, props))));
}
exports["default"] = withModelContext(ReactWidget);
//# sourceMappingURL=ReactWidget.js.map

/***/ }),

/***/ "./lib/components/AppBar.js":
/*!**********************************!*\
  !*** ./lib/components/AppBar.js ***!
  \**********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const AppBar_1 = __importDefault(__webpack_require__(/*! @mui/material/AppBar */ "./node_modules/@mui/material/AppBar/index.js"));
const Box_1 = __importDefault(__webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/index.js"));
const Toolbar_1 = __importDefault(__webpack_require__(/*! @mui/material/Toolbar */ "./node_modules/@mui/material/Toolbar/index.js"));
const IconButton_1 = __importDefault(__webpack_require__(/*! @mui/material/IconButton */ "./node_modules/@mui/material/IconButton/index.js"));
const Typography_1 = __importDefault(__webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/index.js"));
const Menu_1 = __importDefault(__webpack_require__(/*! @mui/material/Menu */ "./node_modules/@mui/material/Menu/index.js"));
const Avatar_1 = __importDefault(__webpack_require__(/*! @mui/material/Avatar */ "./node_modules/@mui/material/Avatar/index.js"));
const Button_1 = __importDefault(__webpack_require__(/*! @mui/material/Button */ "./node_modules/@mui/material/Button/index.js"));
const Tooltip_1 = __importDefault(__webpack_require__(/*! @mui/material/Tooltip */ "./node_modules/@mui/material/Tooltip/index.js"));
const MenuItem_1 = __importDefault(__webpack_require__(/*! @mui/material/MenuItem */ "./node_modules/@mui/material/MenuItem/index.js"));
const Menu_2 = __importDefault(__webpack_require__(/*! @mui/icons-material/Menu */ "./node_modules/@mui/icons-material/Menu.js"));
const Container_1 = __importDefault(__webpack_require__(/*! @mui/material/Container */ "./node_modules/@mui/material/Container/index.js"));
const Logo_1 = __importDefault(__webpack_require__(/*! ./Logo */ "./lib/components/Logo.js"));
const pages = ['navigation', 'rendering', 'documentation'];
const settings = ['Profile', 'Account', 'Dashboard', 'Logout'];
const ResponsiveAppBar = (props) => {
    const { setView } = props;
    function updateView(view) {
        if (view === 'documentation') {
            const DOCUMENTATION_URL = 'https://docs.google.com/document/d/e/2PACX-1vQHMxWNyofNTgSDszydqM5oKJoMRm_g8p3p4amkaNo_4iMm8LM8GTVEItgNK02CBVY6fXECIax_3Xqf/pub';
            const newWindow = window.open(DOCUMENTATION_URL, '_blank', 'noopener,noreferrer');
            if (newWindow) {
                newWindow.opener = null;
            }
        }
        else {
            setView(view);
        }
    }
    const [anchorElNav, setAnchorElNav] = React.useState(null);
    const [anchorElUser, setAnchorElUser] = React.useState(null);
    const handleOpenNavMenu = (event) => {
        setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event) => {
        setAnchorElUser(event.currentTarget);
    };
    const handleMenuClick = (viewName) => {
        setView(viewName);
    };
    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };
    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };
    return (React.createElement(AppBar_1.default, { position: "static" },
        React.createElement(Container_1.default, { maxWidth: "xl" },
            React.createElement(Toolbar_1.default, { disableGutters: true },
                React.createElement(Box_1.default, { sx: { flexGrow: 1, display: { xs: 'flex', md: 'none' } } },
                    React.createElement(IconButton_1.default, { size: "large", "aria-label": "account of current user", "aria-controls": "menu-appbar", "aria-haspopup": "true", onClick: handleOpenNavMenu, color: "inherit" },
                        React.createElement(Menu_2.default, null)),
                    React.createElement(Menu_1.default, { id: "menu-appbar", anchorEl: anchorElNav, anchorOrigin: {
                            vertical: 'bottom',
                            horizontal: 'left',
                        }, keepMounted: true, transformOrigin: {
                            vertical: 'top',
                            horizontal: 'left',
                        }, open: Boolean(anchorElNav), onClose: handleCloseNavMenu, sx: {
                            display: { xs: 'block', md: 'none' },
                        } }, pages.map((page) => (React.createElement(MenuItem_1.default, { key: page, onClick: () => updateView(page) },
                        React.createElement(Typography_1.default, { textAlign: "center" }, page)))))),
                React.createElement(Box_1.default, { sx: { flexGrow: 0 } },
                    React.createElement(IconButton_1.default, { size: "large", "aria-label": "account of current user", "aria-controls": "menu-appbar", "aria-haspopup": "true", onClick: () => handleMenuClick('home'), color: "inherit" },
                        React.createElement(Logo_1.default, null))),
                React.createElement(Box_1.default, { sx: { flexGrow: 1, display: { xs: 'none', md: 'flex' } } }, pages.map((page) => (React.createElement(Button_1.default, { key: page, onClick: () => updateView(page), sx: { my: 2, color: 'white', display: 'block' } }, page)))),
                React.createElement(Box_1.default, { sx: { flexGrow: 0 } },
                    React.createElement(Tooltip_1.default, { title: "Open settings" },
                        React.createElement(IconButton_1.default, { onClick: handleOpenUserMenu, sx: { p: 0 } },
                            React.createElement(Avatar_1.default, { alt: "Remy Sharp", src: "/static/images/avatar/2.jpg" }))),
                    React.createElement(Menu_1.default, { sx: { mt: '45px' }, id: "menu-appbar", anchorEl: anchorElUser, anchorOrigin: {
                            vertical: 'top',
                            horizontal: 'right',
                        }, keepMounted: true, transformOrigin: {
                            vertical: 'top',
                            horizontal: 'right',
                        }, open: Boolean(anchorElUser), onClose: handleCloseUserMenu }, settings.map((setting) => (React.createElement(MenuItem_1.default, { key: setting, onClick: handleCloseUserMenu },
                        React.createElement(Typography_1.default, { textAlign: "center" }, setting))))))))));
};
exports["default"] = ResponsiveAppBar;
//# sourceMappingURL=AppBar.js.map

/***/ }),

/***/ "./lib/components/KeyframeCard.js":
/*!****************************************!*\
  !*** ./lib/components/KeyframeCard.js ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.KeyframeCard = void 0;
//@ts-nocheck
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const Card_1 = __importDefault(__webpack_require__(/*! @mui/material/Card */ "./node_modules/@mui/material/Card/index.js"));
const Grid_1 = __importDefault(__webpack_require__(/*! @mui/material/Grid */ "./node_modules/@mui/material/Grid/index.js"));
const CardContent_1 = __importDefault(__webpack_require__(/*! @mui/material/CardContent */ "./node_modules/@mui/material/CardContent/index.js"));
const Box_1 = __importDefault(__webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/index.js"));
const CardMedia_1 = __importDefault(__webpack_require__(/*! @mui/material/CardMedia */ "./node_modules/@mui/material/CardMedia/index.js"));
const Typography_1 = __importDefault(__webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/index.js"));
const image_js_1 = __webpack_require__(/*! image-js */ "webpack/sharing/consume/default/image-js/image-js");
function KeyframeCard(props) {
    const { keyframe } = props;
    const keyframeCoordinates = keyframe.coordinates;
    const newImage = new image_js_1.Image(100, 100, keyframe.image, { kind: 'RGB' })
        .resize({ factor: 2 })
        .toDataURL();
    return (react_1.default.createElement("div", { style: { paddingTop: '8px', paddingBottom: '8px' } },
        react_1.default.createElement(Card_1.default, { sx: { display: 'flex' } },
            react_1.default.createElement(Grid_1.default, { container: true, justifyContent: 'space-between' },
                react_1.default.createElement(Grid_1.default, { item: true },
                    react_1.default.createElement(Box_1.default, { sx: { display: 'flex', flexDirection: 'column' } },
                        react_1.default.createElement(CardContent_1.default, { sx: { flex: '1 0 auto' } },
                            react_1.default.createElement(Typography_1.default, { variant: "body2", color: "text.secondary" },
                                "Theta: ",
                                keyframeCoordinates.theta),
                            react_1.default.createElement(Typography_1.default, { variant: "body2", color: "text.secondary" },
                                "Phi: ",
                                keyframeCoordinates.phi),
                            react_1.default.createElement(Typography_1.default, { variant: "body2", color: "text.secondary" },
                                "Radius: ",
                                keyframeCoordinates.radius)))),
                react_1.default.createElement(Grid_1.default, { item: true },
                    react_1.default.createElement(CardMedia_1.default, { height: '100%', component: "img", sx: { width: 100 }, image: newImage, alt: "Live from space album cover" }))))));
}
exports.KeyframeCard = KeyframeCard;
//# sourceMappingURL=KeyframeCard.js.map

/***/ }),

/***/ "./lib/components/KeyframeList.js":
/*!****************************************!*\
  !*** ./lib/components/KeyframeList.js ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
//@ts-nocheck
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const KeyframeCard_1 = __webpack_require__(/*! ./KeyframeCard */ "./lib/components/KeyframeCard.js");
const react_beautiful_dnd_1 = __webpack_require__(/*! react-beautiful-dnd */ "webpack/sharing/consume/default/react-beautiful-dnd/react-beautiful-dnd");
const material_1 = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
function KeyframeList(props) {
    const { keyframes, setKeyFrames } = props;
    const moveCard = react_1.useCallback((dragIndex, hoverIndex) => {
        const dragCard = keyframes[dragIndex];
        const keyframeCopy = [...keyframes];
        keyframeCopy.splice(dragIndex, 1); // removing what you are dragging.
        keyframeCopy.splice(hoverIndex, 0, dragCard); // inserting it into hoverIndex.
        setKeyFrames(keyframeCopy);
    }, [keyframes]);
    function reorder(startIndex, endIndex) {
        const result = Array.from(keyframes);
        const [removed] = result.splice(startIndex, 1);
        result.splice(endIndex, 0, removed);
        return result;
    }
    function onDragEnd(result) {
        // dropped outside the list
        if (!result.destination) {
            return;
        }
        moveCard(result.source.index, result.destination.index);
    }
    return (react_1.default.createElement("div", null,
        react_1.default.createElement(react_beautiful_dnd_1.DragDropContext, { onDragEnd: onDragEnd },
            react_1.default.createElement(react_beautiful_dnd_1.Droppable, { droppableId: "droppable" }, (provided, snapshot) => (react_1.default.createElement("div", Object.assign({}, provided.droppableProps, { ref: provided.innerRef }),
                keyframes &&
                    keyframes.map((item, index) => (react_1.default.createElement(react_beautiful_dnd_1.Draggable, { key: JSON.stringify(item.coordinates), draggableId: JSON.stringify(item.coordinates), index: index }, (provided, snapshot) => (react_1.default.createElement("div", Object.assign({ ref: provided.innerRef, style: { 'margin-bottom': '5px' } }, provided.draggableProps, provided.dragHandleProps),
                        react_1.default.createElement(KeyframeCard_1.KeyframeCard, { keyframe: item })))))),
                provided.placeholder)))),
        react_1.default.createElement("div", { style: { paddingTop: '16px' } }, keyframes && keyframes.length > 0 && (react_1.default.createElement(material_1.Button, { contained: true, onClick: () => {
                let keyframeCopy = [...keyframes];
                keyframeCopy = keyframeCopy.map((keyframe) => {
                    keyframe.image = [];
                    return keyframe;
                });
                copyText(JSON.stringify(keyframeCopy));
            } }, "Copy Keyframes")))));
}
exports["default"] = KeyframeList;
function copyText(text) {
    return __awaiter(this, void 0, void 0, function* () {
        if (navigator.clipboard) {
            yield navigator.clipboard.writeText(text);
            return;
        }
    });
}
//# sourceMappingURL=KeyframeList.js.map

/***/ }),

/***/ "./lib/components/Logo.js":
/*!********************************!*\
  !*** ./lib/components/Logo.js ***!
  \********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const Logo = () => {
    return (react_1.default.createElement("svg", { width: "34", height: "20", viewBox: "0 0 170 100", fill: "none", xmlns: "http://www.w3.org/2000/svg" },
        react_1.default.createElement("path", { d: "M62.3 50.54V99.4H35V0H56.28L96.18 50.54V0H123.48V99.4H101.78L62.3 50.54Z", fill: "white" }),
        react_1.default.createElement("path", { d: "M113 22L152 22L151.961 2.04318e-07L113 1.90735e-06L113 22Z", fill: "white" }),
        react_1.default.createElement("path", { d: "M170 11.5L152 22L151.9 -7.91176e-07L170 11.5Z", fill: "white" }),
        react_1.default.createElement("path", { d: "M0 99.4L40 99.4L39.9598 78.4L-9.17939e-07 78.4L0 99.4Z", fill: "white" })));
};
exports["default"] = Logo;
//# sourceMappingURL=Logo.js.map

/***/ }),

/***/ "./lib/components/Navigator.js":
/*!*************************************!*\
  !*** ./lib/components/Navigator.js ***!
  \*************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const material_1 = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const Grid_1 = __importDefault(__webpack_require__(/*! @mui/material/Grid */ "./node_modules/@mui/material/Grid/index.js"));
const Box_1 = __importDefault(__webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/index.js"));
const Tooltip_1 = __importDefault(__webpack_require__(/*! @mui/material/Tooltip */ "./node_modules/@mui/material/Tooltip/index.js"));
const image_js_1 = __webpack_require__(/*! image-js */ "webpack/sharing/consume/default/image-js/image-js");
const KeyframeList_1 = __importDefault(__webpack_require__(/*! ./KeyframeList */ "./lib/components/KeyframeList.js"));
const Navigator = (props) => {
    const [isImageLoading, setIsImageLoading] = react_1.useState(false);
    const { keyframes, image, setCameraPosition, setKeyFrames } = props;
    react_1.useEffect(() => {
        setIsImageLoading(false);
    }, [image]);
    function updateCameraPosition(variable, value) {
        setIsImageLoading(true);
        const newCameraPosition = Object.assign({}, props.cameraPosition);
        newCameraPosition[variable] = value;
        setCameraPosition(newCameraPosition);
    }
    const newImage = new image_js_1.Image(100, 100, image, { kind: 'RGB' });
    return (react_1.default.createElement("div", null,
        react_1.default.createElement(Grid_1.default, { container: true, spacing: 2 },
            react_1.default.createElement(Grid_1.default, { item: true, xs: 7, md: 7 },
                react_1.default.createElement(Grid_1.default, { md: 12 },
                    react_1.default.createElement("div", null,
                        "Theta",
                        react_1.default.createElement(material_1.Slider, { min: 0, defaultValue: 100, max: 360, "aria-label": "Default", valueLabelDisplay: "auto", onChange: (_, theta) => updateCameraPosition('theta', theta) }),
                        "Phi",
                        react_1.default.createElement(material_1.Slider, { min: -90, defaultValue: -30, max: 0, "aria-label": "Default", valueLabelDisplay: "auto", onChange: (_, phi) => updateCameraPosition('phi', phi) }),
                        "Radius",
                        react_1.default.createElement(material_1.Slider, { step: 0.1, min: 3, defaultValue: 4, max: 5, "aria-label": "Default", valueLabelDisplay: "auto", onChange: (_, radius) => updateCameraPosition('radius', radius) }))),
                react_1.default.createElement(Grid_1.default, { item: true, xs: 12, md: 12 },
                    react_1.default.createElement(Box_1.default, { component: "img", sx: {
                            height: 500,
                            width: 500,
                            maxHeight: { xs: 700, md: 700 },
                            maxWidth: { xs: 700, md: 700 },
                        }, style: isImageLoading ? { opacity: 0.7 } : {}, alt: "The house from the offer.", src: newImage.resize({ factor: 2 }).toDataURL() })),
                react_1.default.createElement(Grid_1.default, { md: 12 },
                    react_1.default.createElement(Tooltip_1.default, { title: isImageLoading ? 'Loading new frame' : 'Save Keyframe' },
                        react_1.default.createElement(material_1.Button, { variant: "contained", disabled: isImageLoading, onClick: () => {
                                const clonedKeyframes = [...(props.keyframes || [])];
                                clonedKeyframes.push({
                                    image: props.image,
                                    coordinates: props.cameraPosition,
                                });
                                props.setKeyFrames(clonedKeyframes);
                            } }, "Save Frame")))),
            react_1.default.createElement(Grid_1.default, { item: true, xs: 5, md: 5 },
                react_1.default.createElement(KeyframeList_1.default, { keyframes: keyframes, setKeyFrames: setKeyFrames })))));
};
exports["default"] = Navigator;
//# sourceMappingURL=Navigator.js.map

/***/ }),

/***/ "./lib/components/Viewer.js":
/*!**********************************!*\
  !*** ./lib/components/Viewer.js ***!
  \**********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const material_1 = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
const Viewer = ({ setVideoNum, setVideoString, videoNum, 
// playNum,
videoString, }) => {
    const [isViewerReady, setIsViewerReady] = react_1.useState(false);
    react_1.useEffect(() => {
        if (videoString) {
            setIsViewerReady(true);
        }
        else {
            setIsViewerReady(false);
        }
    }, [videoString]);
    return (react_1.default.createElement("div", null,
        react_1.default.createElement(material_1.Grid, { container: true, justifyContent: 'center' },
            react_1.default.createElement(material_1.Grid, { md: 12 },
                react_1.default.createElement("div", null, isViewerReady ? (react_1.default.createElement("video", { width: 400, controls: true, autoPlay: true, loop: true },
                    react_1.default.createElement("source", { src: 'data:video/mp4;base64,' + videoString, type: 'video/mp4' }))) : (react_1.default.createElement("video", { width: 400, controls: true, autoPlay: true, loop: true })))),
            react_1.default.createElement(material_1.Grid, { justifyContent: 'space-between', md: 12 },
                react_1.default.createElement(material_1.Button, { variant: "contained", onClick: () => {
                        setVideoNum(videoNum + 1);
                    } }, "Load Video")))));
};
exports["default"] = Viewer;
//# sourceMappingURL=Viewer.js.map

/***/ }),

/***/ "./lib/hooks/widget-model.js":
/*!***********************************!*\
  !*** ./lib/hooks/widget-model.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.useModel = exports.useModelEvent = exports.useModelState = exports.WidgetModelContext = void 0;
const react_1 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
exports.WidgetModelContext = react_1.createContext(undefined);
// HOOKS
//============================================================================================
/**
 *
 * @param name property name in the Python model object.
 * @returns model state and set state function.
 */
function useModelState(name) {
    const model = useModel();
    const [state, setState] = react_1.useState(model === null || model === void 0 ? void 0 : model.get(name));
    useModelEvent(`change:${name}`, (model) => {
        setState(model.get(name));
    }, [name]);
    function updateModel(val, options) {
        model === null || model === void 0 ? void 0 : model.set(name, val, options);
        model === null || model === void 0 ? void 0 : model.save_changes();
    }
    return [state, updateModel];
}
exports.useModelState = useModelState;
/**
 * Subscribes a listener to the model event loop.
 * @param event String identifier of the event that will trigger the callback.
 * @param callback Action to perform when event happens.
 * @param deps Dependencies that should be kept up to date within the callback.
 */
function useModelEvent(event, callback, deps) {
    const model = useModel();
    const dependencies = deps === undefined ? [model] : [...deps, model];
    react_1.useEffect(() => {
        const callbackWrapper = (e) => model && callback(model, e);
        model === null || model === void 0 ? void 0 : model.on(event, callbackWrapper);
        return () => void (model === null || model === void 0 ? void 0 : model.unbind(event, callbackWrapper));
    }, dependencies);
}
exports.useModelEvent = useModelEvent;
/**
 * An escape hatch in case you want full access to the model.
 * @returns Python model
 */
function useModel() {
    return react_1.useContext(exports.WidgetModelContext);
}
exports.useModel = useModel;
//# sourceMappingURL=widget-model.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Dylan Wootton and Josh Pollock
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Dylan Wootton and Josh Pollock
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ExampleView = exports.ExampleModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const ReactWidget_1 = __importDefault(__webpack_require__(/*! ./ReactWidget */ "./lib/ReactWidget.js"));
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_dom_1 = __importDefault(__webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom"));
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
class ExampleModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: ExampleModel.model_name, _model_module: ExampleModel.model_module, _model_module_version: ExampleModel.model_module_version, _view_name: ExampleModel.view_name, _view_module: ExampleModel.view_module, _view_module_version: ExampleModel.view_module_version });
    }
}
exports.ExampleModel = ExampleModel;
ExampleModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
ExampleModel.model_name = 'ExampleModel';
ExampleModel.model_module = version_1.MODULE_NAME;
ExampleModel.model_module_version = version_1.MODULE_VERSION;
ExampleModel.view_name = 'ExampleView'; // Set to null if no view
ExampleModel.view_module = version_1.MODULE_NAME; // Set to null if no view
ExampleModel.view_module_version = version_1.MODULE_VERSION;
class ExampleView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add('custom-widget');
        const component = react_1.default.createElement(ReactWidget_1.default, {
            model: this.model,
            view: 'home',
        });
        react_dom_1.default.render(component, this.el);
    }
}
exports.ExampleView = ExampleView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"nerfviewer","version":"0.0.1","description":"A ipywidget for viewing the output of a nerf.","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com//nerfviewer","bugs":{"url":"https://github.com//nerfviewer/issues"},"license":"BSD-3-Clause","author":{"name":"Dylan Wootton and Josh Pollock","email":"dwootton@mit.edu"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com//nerfviewer"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf nerfviewer/labextension","clean:nbextension":"rimraf nerfviewer/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@emotion/react":"^11.9.0","@emotion/styled":"^11.8.1","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@mui/icons-material":"^5.6.2","@mui/material":"^5.6.3","image-js":"^0.34.0","react":"^17.0.2","react-beautiful-dnd":"^13.1.0","react-colorful":"^5.5.1","react-dnd":"^16.0.1","react-dnd-html5-backend":"^16.0.1","react-dom":"^17.0.2"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@babel/preset-react":"^7.14.5","@babel/preset-typescript":"^7.14.5","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/react":"^17.0.11","@types/react-dom":"^17.0.8","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","babel-loader":"^8.2.2","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"babel":{"presets":["@babel/preset-env","@babel/preset-react","@babel/preset-typescript"]},"jupyterlab":{"extension":"lib/plugin","outputDir":"nerfviewer/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.98c9f7398b51e815b014.js.map