"use strict";
(self["webpackChunkjupysql_plugin"] = self["webpackChunkjupysql_plugin"] || []).push([["lib_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/widget.css":
/*!****************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/widget.css ***!
  \****************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".custom-widget {\n    background-color: lightseagreen;\n    padding: 0px 2px;\n}", "",{"version":3,"sources":["webpack://./style/widget.css"],"names":[],"mappings":"AAAA;IACI,+BAA+B;IAC/B,gBAAgB;AACpB","sourcesContent":[".custom-widget {\n    background-color: lightseagreen;\n    padding: 0px 2px;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./lib/comm.js":
/*!*********************!*\
  !*** ./lib/comm.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   registerCommTargets: () => (/* binding */ registerCommTargets)
/* harmony export */ });
// Opens a comm from the frontend to the kernel
const registerCommTargets = (context) => {
    var _a;
    const sessionContext = context.sessionContext;
    const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
    if (!kernel)
        return;
    // Listen to updateTableWidget event
    document.addEventListener("onUpdateTableWidget", async (event) => {
        const customEvent = event;
        const data = customEvent.detail.data;
        // Register to table_widget handler in the JupySQL kernel
        const comm = kernel.createComm("comm_target_handle_table_widget");
        await comm.open('initializing connection').done;
        // Send data to the Kernel to recevice rows to display
        comm.send(data);
        // Handle recevied rows
        comm.onMsg = (msg) => {
            const content = msg.content;
            const data = content.data;
            // Raise event to update table with new rows
            let customEvent = new CustomEvent('onTableWidgetRowsReady', {
                bubbles: true,
                cancelable: true,
                composed: false,
                detail: {
                    data: data
                }
            });
            document.body.dispatchEvent(customEvent);
        };
    });
};


/***/ }),

/***/ "./lib/connector.js":
/*!**************************!*\
  !*** ./lib/connector.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CompletionConnector: () => (/* binding */ CompletionConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
// Modified from jupyterlab/packages/completer/src/connector.ts

/**
 * A multi-connector connector for completion handlers.
 */
class CompletionConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new connector for completion requests.
     *
     * @param connectors - Connectors to request matches from, ordered by metadata preference (descending).
     */
    constructor(connectors) {
        super();
        this._connectors = connectors;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     * @returns Completion reply
     */
    fetch(request) {
        return Promise.all(this._connectors.map((connector) => connector.fetch(request))).then((replies) => {
            const definedReplies = replies.filter((reply) => !!reply);
            return Private.mergeReplies(definedReplies);
        });
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Merge results from multiple connectors.
     *
     * @param replies - Array of completion results.
     * @returns IReply with a superset of all matches.
     */
    function mergeReplies(replies) {
        // Filter replies with matches.
        const repliesWithMatches = replies.filter((rep) => rep.matches.length > 0);
        // If no replies contain matches, return an empty IReply.
        if (repliesWithMatches.length === 0) {
            return replies[0];
        }
        // If only one reply contains matches, return it.
        if (repliesWithMatches.length === 1) {
            return repliesWithMatches[0];
        }
        // Collect unique matches from all replies.
        const matches = new Set();
        repliesWithMatches.forEach((reply) => {
            reply.matches.forEach((match) => matches.add(match));
        });
        // Note that the returned metadata field only contains items in the first member of repliesWithMatches.
        return { ...repliesWithMatches[0], matches: [...matches] };
    }
    Private.mergeReplies = mergeReplies;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/customconnector.js":
/*!********************************!*\
  !*** ./lib/customconnector.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CustomConnector: () => (/* binding */ CustomConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _keywords_json__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./keywords.json */ "./lib/keywords.json");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A custom connector for completion handlers.
 */
class CustomConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new custom connector for completion requests.
     *
     * @param options - The instatiation options for the custom connector.
     */
    constructor(options) {
        super();
        this._editor = options.editor;
        this._sessionContext = options.sessionContext;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     * @returns Completion reply
     */
    fetch(request) {
        if (!this._editor) {
            return Promise.reject('No editor');
        }
        return new Promise((resolve) => {
            resolve(Private.completionHint(this._editor, this._sessionContext));
        });
    }
}
/**
 * A namespace for Private functionality.
 */
var Private;
(function (Private) {
    /**
     * Get a list of mocked completion hints.
     *
     * @param editor Editor
     * @returns Completion reply
     */
    function completionHint(editor, sessionContext) {
        // Find the token at the cursor
        const cursor = editor.getCursorPosition();
        const token = editor.getTokenForPosition(cursor);
        var newTokenList = _keywords_json__WEBPACK_IMPORTED_MODULE_1__.keywords;
        const completionList = newTokenList.filter((t) => t.value.startsWith(token.value.toUpperCase())).map((t) => t.value);
        // Remove duplicate completions from the list
        const matches = Array.from(new Set(completionList));
        return {
            start: token.offset,
            end: token.offset + token.value.length,
            matches,
            metadata: {},
        };
    }
    Private.completionHint = completionHint;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/formatter.js":
/*!**************************!*\
  !*** ./lib/formatter.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   JupyterlabNotebookCodeFormatter: () => (/* binding */ JupyterlabNotebookCodeFormatter)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sql_formatter__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sql-formatter */ "webpack/sharing/consume/default/sql-formatter/sql-formatter");
/* harmony import */ var sql_formatter__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sql_formatter__WEBPACK_IMPORTED_MODULE_1__);


class JupyterlabNotebookCodeFormatter {
    constructor(notebookTracker) {
        this.notebookTracker = notebookTracker;
    }
    async formatAllCodeCells(config, formatter, notebook) {
        return this.formatCells(false, config, formatter, notebook);
    }
    getCodeCells(selectedOnly = true, notebook) {
        if (!this.notebookTracker.currentWidget) {
            return [];
        }
        const codeCells = [];
        notebook = notebook || this.notebookTracker.currentWidget.content;
        notebook.widgets.forEach((cell) => {
            if (cell.model.type === 'code') {
                if (!selectedOnly || notebook.isSelectedOrActive(cell)) {
                    codeCells.push(cell);
                }
            }
        });
        return codeCells;
    }
    async formatCells(selectedOnly, config, formatter, notebook) {
        if (this.working) {
            return;
        }
        try {
            this.working = true;
            const selectedCells = this.getCodeCells(selectedOnly, notebook);
            if (selectedCells.length === 0) {
                this.working = false;
                return;
            }
            for (let i = 0; i < selectedCells.length; ++i) {
                const cell = selectedCells[i];
                const text = cell.model.value.text;
                if (text.startsWith("%%sql")) {
                    const lines = text.split("\n");
                    const sqlCommand = lines.shift();
                    try {
                        const query = (0,sql_formatter__WEBPACK_IMPORTED_MODULE_1__.format)(lines.join("\n"), { language: 'sql', keywordCase: 'upper' });
                        cell.model.value.text = sqlCommand + "\n" + query;
                    }
                    catch (error) {
                    }
                }
            }
        }
        catch (error) {
            await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Jupysql plugin formatting', error);
        }
        this.working = false;
    }
    applicable(formatter, currentWidget) {
        const currentNotebookWidget = this.notebookTracker.currentWidget;
        // TODO: Handle showing just the correct formatter for the language later
        return currentNotebookWidget && currentWidget === currentNotebookWidget;
    }
}


/***/ }),

/***/ "./lib/index-widgets.js":
/*!******************************!*\
  !*** ./lib/index-widgets.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   widgetExports: () => (/* binding */ widgetExports)
/* harmony export */ });
/* harmony import */ var _widgets_form__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./widgets/form */ "./lib/widgets/form.js");
/* harmony import */ var _widgets_table__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widgets/table */ "./lib/widgets/table.js");


const widgetExports = {
    ..._widgets_form__WEBPACK_IMPORTED_MODULE_0__,
    ..._widgets_table__WEBPACK_IMPORTED_MODULE_1__,
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FormattingExtension: () => (/* binding */ FormattingExtension),
/* harmony export */   MODULE_NAME: () => (/* reexport safe */ _version__WEBPACK_IMPORTED_MODULE_11__.MODULE_NAME),
/* harmony export */   MODULE_VERSION: () => (/* reexport safe */ _version__WEBPACK_IMPORTED_MODULE_11__.MODULE_VERSION),
/* harmony export */   RegisterNotebookCommListener: () => (/* binding */ RegisterNotebookCommListener),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/completer */ "webpack/sharing/consume/default/@jupyterlab/completer");
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _connector__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./connector */ "./lib/connector.js");
/* harmony import */ var _customconnector__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./customconnector */ "./lib/customconnector.js");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! underscore */ "webpack/sharing/consume/default/underscore/underscore");
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(underscore__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _formatter__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./formatter */ "./lib/formatter.js");
/* harmony import */ var _comm__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./comm */ "./lib/comm.js");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _index_widgets__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./index-widgets */ "./lib/index-widgets.js");
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./version */ "./lib/version.js");




// for syntax highlighting









/**
 * The command IDs used by the console plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.invoke = 'completer:invoke';
    CommandIDs.invokeNotebook = 'completer:invoke-notebook';
    CommandIDs.select = 'completer:select';
    CommandIDs.selectNotebook = 'completer:select-notebook';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the extension.
 */
const extension = {
    id: 'completer',
    autoStart: true,
    requires: [_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: async (app, completionManager, notebooks) => {
        console.log('JupyterLab extension jupysql-plugin is activated!');
        // Modelled after completer-extension's notebooks plugin
        notebooks.widgetAdded.connect((sender, panel) => {
            var _a, _b;
            let editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
            const session = panel.sessionContext.session;
            const sessionContext = panel.sessionContext;
            const options = { session, editor, sessionContext };
            const connector = new _connector__WEBPACK_IMPORTED_MODULE_7__.CompletionConnector([]);
            const handler = completionManager.register({
                connector,
                editor,
                parent: panel,
            });
            const updateConnector = () => {
                var _a, _b;
                editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
                options.session = panel.sessionContext.session;
                options.sessionContext = panel.sessionContext;
                options.editor = editor;
                handler.editor = editor;
                const kernel = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.KernelConnector(options);
                const context = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ContextConnector(options);
                const custom = new _customconnector__WEBPACK_IMPORTED_MODULE_8__.CustomConnector(options);
                handler.connector = new _connector__WEBPACK_IMPORTED_MODULE_7__.CompletionConnector([
                    kernel,
                    context,
                    custom
                ]);
            };
            // Update the handler whenever the prompt or session changes
            panel.content.activeCellChanged.connect(updateConnector);
            panel.sessionContext.sessionChanged.connect(updateConnector);
        });
        // Add notebook completer command.
        app.commands.addCommand(CommandIDs.invokeNotebook, {
            execute: () => {
                var _a;
                const panel = notebooks.currentWidget;
                if (panel && ((_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.type) === 'code') {
                    return app.commands.execute(CommandIDs.invoke, { id: panel.id });
                }
            },
        });
        // Add notebook completer select command.
        app.commands.addCommand(CommandIDs.selectNotebook, {
            execute: () => {
                const id = notebooks.currentWidget && notebooks.currentWidget.id;
                if (id) {
                    return app.commands.execute(CommandIDs.select, { id });
                }
            },
        });
        // Set enter key for notebook completer select command.
        app.commands.addKeyBinding({
            command: CommandIDs.selectNotebook,
            keys: ['Enter'],
            selector: '.jp-Notebook .jp-mod-completer-active',
        });
    },
};
// %%sql highlighting
class SqlCodeMirror {
    constructor(app, tracker, code_mirror) {
        var _a, _b;
        this.app = app;
        this.tracker = tracker;
        this.code_mirror = code_mirror;
        (_b = (_a = this.tracker) === null || _a === void 0 ? void 0 : _a.activeCellChanged) === null || _b === void 0 ? void 0 : _b.connect(() => {
            var _a;
            if (((_a = this.tracker) === null || _a === void 0 ? void 0 : _a.activeCell) !== null) {
                const cell = this.tracker.activeCell;
                if (cell !== null && (cell === null || cell === void 0 ? void 0 : cell.model.type) === 'code') {
                    const code_mirror_editor = cell === null || cell === void 0 ? void 0 : cell.editor;
                    const debounced_on_change = underscore__WEBPACK_IMPORTED_MODULE_3__.debounce(() => {
                        var _a;
                        // check for editor with first line starting with %%sql
                        const line = (_a = code_mirror_editor
                            .getLine(code_mirror_editor.firstLine())) === null || _a === void 0 ? void 0 : _a.trim();
                        if (line === null || line === void 0 ? void 0 : line.startsWith('%%sql')) {
                            code_mirror_editor.editor.setOption('mode', 'text/x-sql');
                        }
                        else {
                            code_mirror_editor.editor.setOption('mode', 'text/x-ipython');
                        }
                    }, 300);
                    code_mirror_editor.editor.on('change', debounced_on_change);
                    debounced_on_change();
                }
            }
        });
    }
}
function activate_syntax(app, tracker, code_mirror) {
    new SqlCodeMirror(app, tracker, code_mirror);
    console.log('SQLCodeMirror loaded.');
}
/**
 * Initialization data for the jupyterlabs_sql_codemirror extension.
 * this is based on:
 * https://github.com/surdouski/jupyterlabs_sql_codemirror
 */
const extension_sql = {
    id: '@ploomber/sql-syntax-highlighting',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker, _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.ICodeMirror],
    optional: [],
    activate: activate_syntax
};
/**
 * A notebook widget extension that adds a button to the toolbar.
 */
class FormattingExtension {
    constructor(tracker) {
        this.notebookCodeFormatter = new _formatter__WEBPACK_IMPORTED_MODULE_9__.JupyterlabNotebookCodeFormatter(tracker);
    }
    createNew(panel, context) {
        const clearOutput = () => {
            this.notebookCodeFormatter.formatAllCodeCells(undefined, undefined, panel.content);
        };
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__.ToolbarButton({
            className: 'format-sql-button',
            label: 'Format SQL',
            onClick: clearOutput,
            tooltip: 'Format all %%sql cells',
        });
        panel.toolbar.insertItem(10, 'formatSQL', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
class RegisterNotebookCommListener {
    /**
     * Register notebook comm
     *
     * @param panel Notebook panel
     * @param context Notebook context
     * @returns Disposable on the added button
     */
    createNew(panel, context) {
        setTimeout(() => {
            (0,_comm__WEBPACK_IMPORTED_MODULE_10__.registerCommTargets)(context);
        }, 5000);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__.DisposableDelegate(() => {
        });
    }
}
/**
 * Activate the extension.
 *
 * @param app Main application object
 */
const formatting_plugin = {
    activate: (app, tracker) => {
        app.docRegistry.addWidgetExtension('Notebook', new FormattingExtension(tracker));
        app.docRegistry.addWidgetExtension('Notebook', new RegisterNotebookCommListener());
    },
    autoStart: true,
    id: "formatting",
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker,
    ]
};
const EXTENSION_ID = 'jupysql-plugin:plugin';
/**
 * The example plugin.
 */
const examplePlugin = {
    id: EXTENSION_ID,
    requires: [_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_6__.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true,
};
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.
// export default examplePlugin;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: _version__WEBPACK_IMPORTED_MODULE_11__.MODULE_NAME,
        version: _version__WEBPACK_IMPORTED_MODULE_11__.MODULE_VERSION,
        exports: _index_widgets__WEBPACK_IMPORTED_MODULE_12__.widgetExports,
    });
}

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([extension, extension_sql, formatting_plugin, examplePlugin]);


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MODULE_NAME: () => (/* binding */ MODULE_NAME),
/* harmony export */   MODULE_VERSION: () => (/* binding */ MODULE_VERSION)
/* harmony export */ });
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
const MODULE_VERSION = data.version;
/*
 * The current package name.
 */
const MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widgets/form.js":
/*!*****************************!*\
  !*** ./lib/widgets/form.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FormModel: () => (/* binding */ FormModel),
/* harmony export */   FormView: () => (/* binding */ FormView)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../version */ "./lib/version.js");
/* harmony import */ var _style_widget_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../style/widget.css */ "./style/widget.css");


// Import the CSS

class FormModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: FormModel.model_name,
            _model_module: FormModel.model_module,
            _model_module_version: FormModel.model_module_version,
            _view_name: FormModel.view_name,
            _view_module: FormModel.view_module,
            _view_module_version: FormModel.view_module_version,
            value: 'Hello World',
        };
    }
}
FormModel.serializers = {
    ..._jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel.serializers,
};
FormModel.model_name = 'FormModel';
FormModel.model_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME;
FormModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
FormModel.view_name = 'FormView'; // Set to null if no view
FormModel.view_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME; // Set to null if no view
FormModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
class FormView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetView {
    render() {
        this.el.classList.add('custom-widget');
        const template = `
        <form id="myForm">
        <label for="dropdown">Select an option:</label>
        <select id="dropdown" name="dropdown">
          <option value="A">Option A</option>
          <option value="B">Option B</option>
        </select>
      
        <label for="port">Enter a port:</label>
        <input type="number" id="port" name="port">

        <div id="confirmationMessage"></div>
      
        <button type="submit">Submit</button>
      </form>
      
`;
        this.el.innerHTML = template;
        // Add event listener for form submission
        const form = this.el.querySelector('#myForm');
        form.addEventListener('submit', this.handleFormSubmit.bind(this));
        // Listen for messages from the Python backend
        this.model.on('msg:custom', this.handleMessage.bind(this));
    }
    handleFormSubmit(event) {
        event.preventDefault();
        // Extract form data
        const form = event.target;
        const formData = new FormData(form);
        // Convert form data to a plain object
        const formValues = {};
        for (const [key, value] of formData.entries()) {
            formValues[key] = value.toString();
        }
        // Call the function to send form data to the Python backend
        this.sendFormData(formValues);
    }
    sendFormData(formData) {
        // Create a message to send to the Python backend
        const message = {
            method: 'submit_form',
            data: formData
        };
        // Send the message to the Python backend
        this.send(message);
    }
    handleMessage(content) {
        if (content.method === 'display_confirmation_message') {
            const confirmationMessage = this.el.querySelector('#confirmationMessage');
            if (confirmationMessage) {
                confirmationMessage.textContent = content.message;
            }
        }
    }
}


/***/ }),

/***/ "./lib/widgets/table.js":
/*!******************************!*\
  !*** ./lib/widgets/table.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TableModel: () => (/* binding */ TableModel),
/* harmony export */   TableView: () => (/* binding */ TableView)
/* harmony export */ });
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../version */ "./lib/version.js");
/* harmony import */ var bootstrap_dist_css_bootstrap_min_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var bootstrap__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! bootstrap */ "webpack/sharing/consume/default/bootstrap/bootstrap");
/* harmony import */ var bootstrap__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(bootstrap__WEBPACK_IMPORTED_MODULE_2__);




class TableModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: TableModel.model_name,
            _model_module: TableModel.model_module,
            _model_module_version: TableModel.model_module_version,
            _view_name: TableModel.view_name,
            _view_module: TableModel.view_module,
            _view_module_version: TableModel.view_module_version,
            value: 'Hello World',
        };
    }
}
TableModel.serializers = {
    ..._jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetModel.serializers,
};
TableModel.model_name = 'TableModel';
TableModel.model_module = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_NAME;
TableModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_VERSION;
TableModel.view_name = 'TableView'; // Set to null if no view
TableModel.view_module = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_NAME; // Set to null if no view
TableModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_VERSION;
class TableView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetView {
    render() {
        const stockData = [
            { symbol: 'AAPL', price: 142.34, change: 1.25 },
            { symbol: 'GOOGL', price: 2725.45, change: -4.56 },
            { symbol: 'MSFT', price: 259.43, change: 2.78 },
            { symbol: 'AMZN', price: 3310.98, change: -7.92 },
        ];
        this.el.innerHTML = `
      <table class="table">
        <thead>
          <tr>
            <th data-bs-toggle="tooltip" data-bs-placement="top" title="symbol">Symbol</th>
            <th data-bs-toggle="tooltip" data-bs-placement="top" title="price">Price</th>
            <th data-bs-toggle="tooltip" data-bs-placement="top" title="change">Change</th>
          </tr>
        </thead>
        <tbody>
          ${stockData.map((stock) => `
            <tr>
              <td>${stock.symbol}</td>
              <td>${stock.price}</td>
              <td>${stock.change}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
        const tooltipTriggerList = Array.from(this.el.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.forEach((tooltipTriggerEl) => {
            const column = tooltipTriggerEl.getAttribute('title');
            const tooltipContent = stockData.map((stock) => stock[column]).join(', ');
            new bootstrap__WEBPACK_IMPORTED_MODULE_2__.Tooltip(tooltipTriggerEl, {
                title: tooltipContent,
            });
        });
    }
}


/***/ }),

/***/ "./style/widget.css":
/*!**************************!*\
  !*** ./style/widget.css ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./style/widget.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./lib/keywords.json":
/*!***************************!*\
  !*** ./lib/keywords.json ***!
  \***************************/
/***/ ((module) => {

module.exports = JSON.parse('{"keywords":[{"value":"ADD"},{"value":"ADD CONSTRAINT"},{"value":"ALL"},{"value":"ALTER"},{"value":"ALTER COLUMN"},{"value":"ALTER TABLE"},{"value":"AND"},{"value":"ANY"},{"value":"AS"},{"value":"ASC"},{"value":"BACKUP DATABASE"},{"value":"BETWEEN"},{"value":"CASE"},{"value":"CHECK"},{"value":"COLUMN"},{"value":"CONSTRAINT"},{"value":"CREATE"},{"value":"CREATE DATABASE"},{"value":"CREATE INDEX"},{"value":"CREATE OR REPLACE VIEW"},{"value":"CREATE TABLE"},{"value":"CREATE PROCEDURE"},{"value":"CREATE UNIQUE INDEX"},{"value":"CREATE VIEW"},{"value":"DATABASE"},{"value":"DEFAULT"},{"value":"DELETE"},{"value":"DESC"},{"value":"DISTINCT"},{"value":"DROP"},{"value":"DROP COLUMN"},{"value":"DROP CONSTRAINT"},{"value":"DROP DATABASE"},{"value":"DROP DEFAULT"},{"value":"DROP INDEX"},{"value":"DROP TABLE"},{"value":"DROP VIEW"},{"value":"EXEC"},{"value":"EXISTS"},{"value":"FOREIGN KEY"},{"value":"FROM"},{"value":"FULL OUTER JOIN"},{"value":"GROUP BY"},{"value":"HAVING"},{"value":"IN"},{"value":"INDEX"},{"value":"INNER JOIN"},{"value":"INSERT INTO"},{"value":"INSERT INTO SELECT"},{"value":"IS NULL"},{"value":"IS NOT NULL"},{"value":"JOIN"},{"value":"LEFT JOIN"},{"value":"LIKE"},{"value":"LIMIT"},{"value":"NOT"},{"value":"NOT NULL"},{"value":"OR"},{"value":"ORDER BY"},{"value":"OUTER JOIN"},{"value":"PRIMARY KEY"},{"value":"PROCEDURE"},{"value":"RIGHT JOIN"},{"value":"ROWNUM"},{"value":"SELECT"},{"value":"SELECT DISTINCT"},{"value":"SELECT INTO"},{"value":"SELECT TOP"},{"value":"SET"},{"value":"TABLE"},{"value":"TOP"},{"value":"TRUNCATE TABLE"},{"value":"UNION"},{"value":"UNION ALL"},{"value":"UNIQUE"},{"value":"UPDATE"},{"value":"VALUES"},{"value":"VIEW"},{"value":"WHERE"}]}');

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"jupysql-plugin","version":"0.1.3","description":"Jupyterlab extension for JupySQL","keywords":["jupyter","jupyterlab","jupyterlab-extension"],"homepage":"https://github.com/ploomber/jupysql-plugin.git","bugs":{"url":"https://github.com/ploomber/jupysql-plugin.git/issues"},"license":"BSD-3-Clause","author":{"name":"Ploomber","email":"contact@ploomber.io"},"files":["lib/**/*.{d.ts,eot,gif,html,jpg,js,js.map,json,png,svg,woff2,ttf}","style/**/*.{css,js,eot,gif,html,jpg,json,png,svg,woff2,ttf}"],"main":"lib/index.js","types":"lib/index.d.ts","style":"style/index.css","repository":{"type":"git","url":"https://github.com/ploomber/jupysql-plugin.git.git"},"scripts":{"build":"jlpm build:lib && jlpm build:labextension:dev","build:prod":"jlpm clean && jlpm build:lib:prod && jlpm build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc --sourceMap","build:lib:prod":"tsc","clean":"jlpm clean:lib","clean:lib":"rimraf lib tsconfig.tsbuildinfo","clean:lintcache":"rimraf .eslintcache .stylelintcache","clean:labextension":"rimraf jupysql_plugin/labextension jupysql_plugin/_version.py","clean:all":"jlpm clean:lib && jlpm clean:labextension && jlpm clean:lintcache","eslint":"jlpm eslint:check --fix","eslint:check":"eslint . --cache --ext .ts,.tsx","install:extension":"jlpm build","lint":"jlpm stylelint && jlpm prettier && jlpm eslint","lint:check":"jlpm stylelint:check && jlpm prettier:check && jlpm eslint:check","prettier":"jlpm prettier:base --write --list-different","prettier:base":"prettier \\"**/*{.ts,.tsx,.js,.jsx,.css,.json,.md}\\"","prettier:check":"jlpm prettier:base --check","stylelint":"jlpm stylelint:check --fix","stylelint:check":"stylelint --cache \\"style/**/*.css\\"","test":"jest --coverage","watch":"run-p watch:src watch:labextension","watch:src":"tsc -w","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^6.0.4","@jupyterlab/application":"^3.6.2","@jupyterlab/codeeditor":"^3.6.2","@jupyterlab/codemirror":"^3.6.3","@jupyterlab/completer":"^3.6.2","@jupyterlab/notebook":"^3.6.2","@jupyterlab/statedb":"^3.6.2","@lumino/widgets":"<2.0.0","@types/codemirror":"^5.60.7","@types/underscore":"^1.11.4","bootstrap":"^5.2.3","sql-formatter":"^12.2.0","underscore":"^1.13.6"},"devDependencies":{"@babel/core":"^7.0.0","@babel/preset-env":"^7.0.0","@jupyterlab/builder":"^3.1.0","@jupyterlab/testutils":"^3.0.0","@types/bootstrap":"^5.2.6","@types/jest":"^26.0.0","@typescript-eslint/eslint-plugin":"^4.8.1","@typescript-eslint/parser":"^4.8.1","eslint":"^7.14.0","eslint-config-prettier":"^6.15.0","eslint-plugin-prettier":"^3.1.4","jest":"^26.0.0","npm-run-all":"^4.1.5","prettier":"^2.1.1","rimraf":"^3.0.2","stylelint":"^14.3.0","stylelint-config-prettier":"^9.0.4","stylelint-config-recommended":"^6.0.0","stylelint-config-standard":"~24.0.0","stylelint-prettier":"^2.0.0","ts-jest":"^26.0.0","typescript":"~4.1.3"},"sideEffects":["style/*.css","style/index.js"],"styleModule":"style/index.js","publishConfig":{"access":"public"},"jupyterlab":{"extension":true,"outputDir":"jupysql_plugin/labextension","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.3a926c06d05407c0044f.js.map