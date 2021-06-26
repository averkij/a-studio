import {
  ItemsService
} from "@/common/api.service";

import {
  LanguageHelper
} from "@/common/language.helper";

import {
  INIT_USERSPACE,
  FETCH_ITEMS,
  FETCH_ITEMS_PROCESSING,
  UPLOAD_FILES,
  DELETE_DOCUMENT,
  DOWNLOAD_SPLITTED,
  DOWNLOAD_PROCESSING,
  DOWNLOAD_BOOK,
  GET_SPLITTED,
  GET_MARKS,
  GET_DOC_INDEX,
  GET_PROCESSING,
  GET_PROCESSING_META,
  GET_CANDIDATES,
  GET_CONFLICTS,
  GET_CONFLICT_DETAILS,
  EDIT_PROCESSING,
  EDIT_PROCESSING_MARK_UNUSED,
  STOP_ALIGNMENT,
  ALIGN_SPLITTED,
  RESOLVE_CONFLICTS,
  CREATE_ALIGNMENT,
  DELETE_ALIGNMENT,
  GET_CONFLICT_SPLITTED_FROM,
  GET_CONFLICT_SPLITTED_TO,
  GET_CONFLICT_FLOW_TO,
  GET_CONTENTS,
  GET_BOOK_PREVIEW
} from "./actions.type";

import {
  SET_ITEMS,
  SET_ITEMS_PROCESSING,
  SET_SPLITTED,
  SET_MARKS,
  SET_PROCESSING,
  SET_PROCESSING_META,
  SET_DOC_INDEX,
  SET_CONFLICTS,
  SET_CONFLICT_DETAILS,
  SET_CONFLICT_SPLITTED_FROM,
  SET_CONFLICT_SPLITTED_TO,
  SET_CONFLICT_FLOW_TO,
  SET_CONTENTS,
  SET_BOOK_PREVIEW
} from "./mutations.type";

const initialState = {
  items: LanguageHelper.initItems(),
  itemsProcessing: LanguageHelper.initItems(),
  splitted: LanguageHelper.initSplitted(),
  marks: LanguageHelper.initMarks(),
  processing: LanguageHelper.initProcessing(),
  processingMeta: {},
  docIndex: [],
  conflictSplittedFrom: [],
  conflictSplittedTo: [],
  conflictFlowTo: [],
  contents: [],
  conflicts: {},
  conflictDetails: {"from": [], "to": []},
  bookPreview: ""
};

export const state = {
  ...initialState
};

export const actions = {
  async [INIT_USERSPACE](context, params) {
    await ItemsService.initUserspace(params);
  },
  async [FETCH_ITEMS](context, params) {
    const {
      data
    } = await ItemsService.fetchItems(params);
    context.commit(SET_ITEMS, {
      items: data.items,
      langCode: params.langCode
    });
    return data;
  },
  async [FETCH_ITEMS_PROCESSING](context, params) {
    const {
      data
    } = await ItemsService.fetchItemsProcessing(params);
    context.commit(SET_ITEMS_PROCESSING, {
      items: data.items[params.langCodeFrom],
      langCode: params.langCodeFrom
    });
    return data;
  },
  // params {file, username, langCode}
  async [UPLOAD_FILES](context, params) {
    await ItemsService.upload(params).then(
      function () {
      },
      function (error) {
        alert('File already exists')
        console.log(error);
        return;
      }
    );
  },
  // params {fileId, username, langCode, fileName}
  async [DOWNLOAD_SPLITTED](context, params) {
    if (params.fromDb) {
      await ItemsService.downloadSplittedFromDb(params);
    } else {
      ItemsService.downloadSplitted(params);
    }
  },
  // params {fileId, username, langCode, fileName}
  async [DOWNLOAD_PROCESSING](context, params) {
    await ItemsService.downloadProcessing(params);
  },
  async [DOWNLOAD_BOOK](context, params) {
    await ItemsService.downloadBook(params);
  },
  async [GET_BOOK_PREVIEW](context, params) {
    await ItemsService.getBookPreview(params).then(
      function (response) {
        context.commit(SET_BOOK_PREVIEW, response.data);
      },
      function () {
        console.log(`GET_BOOK_PREVIEW error.`);
      }
    );
  },
  // params {fileId, username, langCode, count, page}
  async [GET_SPLITTED](context, params) {
    const {
      data
    } = await ItemsService.getSplitted(params);
    context.commit(SET_SPLITTED, {
      data: data,
      langCode: params.langCode
    });
    return;
  },
  // params {fileId, username, langCode}
  async [GET_MARKS](context, params) {
    const {
      data
    } = await ItemsService.getMarks(params);
    context.commit(SET_MARKS, {
      data: data,
      langCode: params.langCode
    });
    return;
  },
  async [GET_DOC_INDEX](context, params) {
    await ItemsService.getDocIndex(params).then(
      function (response) {
        // console.log("setting index", response.data)
        context.commit(SET_DOC_INDEX, response.data);
      },
      function () {
        console.log(`Didn't find database.`);
      }
    );
  },
  async [GET_CONFLICTS](context, params) {
    await ItemsService.getConflicts(params).then(
      function (response) {
        context.commit(SET_CONFLICTS, response.data);
      },
      function () {
        console.log(`GET_CONFLICTS error.`);
      }
    );
  },
  async [GET_CONFLICT_DETAILS](context, params) {
    await ItemsService.getConflictDetails(params).then(
      function (response) {
        context.commit(SET_CONFLICT_DETAILS, response.data);
      },
      function () {
        console.log(`GET_CONFLICT_DETAILS error.`);
      }
    );
  },
  async [GET_PROCESSING](context, params) {
    await ItemsService.getProcessing(params).then(
      function (response) {
        context.commit(SET_PROCESSING, response.data);
      },
      function () {
        console.log(`Didn't find processing document.`);
      }
    );
    return;
  },
  async [GET_PROCESSING_META](context, params) {
    await ItemsService.getProcessingMeta(params).then(
      function (response) {
        context.commit(SET_PROCESSING_META, response.data);
      },
      function () {
        console.log(`Didn't find processing document.`);
      }
    );
    return;
  },
  async [GET_CONFLICT_FLOW_TO](context, params) {
    await ItemsService.getProcessingByIds(params).then(
      function (response) {
        context.commit(SET_CONFLICT_FLOW_TO, response.data);
      },
      function () {
        console.log(`GET_CONFLICT_FLOW_TO error.`);
      }
    );
    return;
  },
  async [GET_CONFLICT_SPLITTED_FROM](context, params) {
    await ItemsService.getSplittedByIds(params, "from").then(
      function (response) {
        context.commit(SET_CONFLICT_SPLITTED_FROM, response.data);
      },
      function () {
        console.log(`GET_CONFLICT_SPLITTED_FROM error.`);
      }
    );
    return;
  },
  async [GET_CONFLICT_SPLITTED_TO](context, params) {
    await ItemsService.getSplittedByIds(params, "to").then(
      function (response) {
        context.commit(SET_CONFLICT_SPLITTED_TO, response.data);
      },
      function () {
        console.log(`GET_CONFLICT_SPLITTED_TO error.`);
      }
    );
    return;
  },
  async [GET_CANDIDATES](context, params) {
    return await ItemsService.getCandidates(params);
  },
  async [STOP_ALIGNMENT](context, params) {
    await ItemsService.stopAlignment(params);
    return;
  },
  // params {fileId, username}
  async [EDIT_PROCESSING](context, params) {
    await ItemsService.editProcessing(params).then(
      () => {
        console.log(`EDIT_PROCESSING OK. Getting index.`);
        context.dispatch(GET_DOC_INDEX, {
          username: params.username,
          langCodeFrom: params.langCodeFrom,
          langCodeTo: params.langCodeTo,
          fileId: params.fileId
        })
      },
      function () {
        console.log(`Didn't find processing document.`);
      }
    );
    return;
  },
  async [EDIT_PROCESSING_MARK_UNUSED](context, params) {
    await ItemsService.editProcessingMarkUnused(params).then(() => {
    },
    () => {
      console.log("mark as unused error")
    });
  },
  async [ALIGN_SPLITTED](context, params) {
    await ItemsService.startAlignment(params).then(() => {
    },
    () => {
      console.log("alignment error")
    });
  },
  async [RESOLVE_CONFLICTS](context, params) {
    await ItemsService.resolveConflicts(params).then(() => {
    },
    () => {
      console.log("resolve conflicts error")
    });
  },
  async [CREATE_ALIGNMENT](context, params) {
    await ItemsService.createAlignment(params).then(() => {
    },
    () => {
      console.log("alignment creation error")
    });
  },
  async [DELETE_ALIGNMENT](context, params) {
    await ItemsService.deleteAlignment(params).then(() => {
    },
    () => {
      console.log("alignment deletion error")
    });
  },
  async [DELETE_DOCUMENT](context, params) {
    await ItemsService.deleteDocument(params).then(() => {
    },
    () => {
      console.log("document deletion error")
    });
  },
  async [GET_CONTENTS](context, params) {
    await ItemsService.getContents(params).then(
      function (response) {
        context.commit(SET_CONTENTS, response.data);
      },
      function () {
        console.log(`GET_CONTENTS error.`);
      }
    );
    return;
  }
};

export const mutations = {
  [SET_ITEMS](state, params) {
    state.items[params.langCode] = params.items[params.langCode];
  },
  [SET_ITEMS_PROCESSING](state, params) {
    state.itemsProcessing[params.langCode] = params.items;
  },
  [SET_SPLITTED](state, params) {
    if (params.data.items[params.langCode]) {
      state.splitted[params.langCode].lines = params.data.items[params.langCode];
    }
    if (params.data.meta[params.langCode]) {
      state.splitted[params.langCode].meta = params.data.meta[params.langCode];
    }
  },
  [SET_MARKS](state, params) {
    console.log("SET_MARKS", params)
    state.marks[params.langCode] = params.data.items;
  },
  [SET_PROCESSING](state, data) {
    state.processing = data;
  },
  [SET_PROCESSING_META](state, data) {
    state.processingMeta = data;
  },
  [SET_DOC_INDEX](state, data) {
    state.docIndex = data.items;
  },
  [SET_CONFLICTS](state, data) {
    state.conflicts = data.items;
  },
  [SET_CONFLICT_DETAILS](state, data) {
    state.conflictDetails = data;
  },
  [SET_CONFLICT_SPLITTED_FROM](state, data) {
    state.conflictSplittedFrom = data.items;
  },
  [SET_CONFLICT_SPLITTED_TO](state, data) {
    state.conflictSplittedTo = data.items;
  },
  [SET_CONFLICT_FLOW_TO](state, data) {
    // console.log("SET_CONFLICT_FLOW_TO:", data.items)
    state.conflictFlowTo = data.items;
  },
  [SET_CONTENTS](state, data) {
    state.contents = data.items;
  },
  [SET_BOOK_PREVIEW](state, data) {
    state.bookPreview = data.items;
  }
};

const getters = {
  items(state) {
    return state.items;
  },
  itemsProcessing(state) {
    return state.itemsProcessing;
  },
  splitted(state) {
    return state.splitted;
  },
  marks(state) {
    return state.marks;
  },
  processing(state) {
    return state.processing;
  },
  processingMeta(state) {
    return state.processingMeta;
  },
  docIndex(state) {
    return state.docIndex;
  },
  conflicts(state) {
    return state.conflicts;
  },
  conflictDetails(state) {
    return state.conflictDetails;
  },
  conflictSplittedFrom(state) {
    return state.conflictSplittedFrom;
  },
  conflictSplittedTo(state) {
    return state.conflictSplittedTo;
  },
  conflictFlowTo(state) {
    return state.conflictFlowTo;
  },
  contents(state) {
    return state.contents;
  },
  bookPreview(state) {
    return state.bookPreview;
  },
};

export default {
  state,
  actions,
  mutations,
  getters
};
