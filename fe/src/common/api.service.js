import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import {
  API_URL
} from "@/common/config";

const ApiService = {
  init() {
    Vue.use(VueAxios, axios);
    Vue.axios.defaults.baseURL = API_URL;
  },
  query(resource, params) {
    return Vue.axios.get(resource, params).catch(error => {
      throw new Error(`ApiService ${error}`);
    });
  },
  get(resource, slug = "") {
    return Vue.axios.get(`${resource}/${slug}`).catch(error => {
      throw new Error(`ApiService ${error}`);
    });
  },
  download(resource, slug = "") {
    return Vue.axios.get(`${resource}/${slug}`, {
      responseType: 'blob'
    }).catch(error => {
      throw new Error(`ApiService ${error}`);
    });
  },
  post(resource, slug, params) {
    return Vue.axios.post(`${resource}/${slug}`, params).catch(error => {
      throw new Error(`ApiService ${error}`);
    });
  },
  update(resource, slug, params) {
    return Vue.axios.put(`${resource}/${slug}`, params);
  },
  put(resource, params) {
    return Vue.axios.put(`${resource}`, params);
  },
  delete(resource) {
    return Vue.axios.delete(resource).catch(error => {
      throw new Error(`ApiService ${error}`);
    });
  }
};

export default ApiService;

export const ItemsService = {
  initUserspace(params) {
    return ApiService.get("items", `${params.username}/init`);
  },
  fetchItems(params) {
    return ApiService.get("items",
      `${params.username}/raw/${params.langCode}`);
  },
  fetchItemsProcessing(params) {
    return ApiService.get(
      "items",
      `${params.username}/processing/list/${params.langCodeFrom}/${params.langCodeTo}`
    );
  },
  upload(params) {
    //check filesize
    if (!params.file) {
      alert("File is empty");
      return Promise.resolve();
    }
    if (params.file.size > 5 * 1024 * 1024) {
      alert("File is too big (> 5MB)");
      return Promise.resolve();
    }
    let form = new FormData();
    form.append(params.langCode, params.file);
    form.append("type", params.isProxy ? "proxy" : "raw");
    form.append("align_guid", params.alignGuid);
    return ApiService.post("items",
      `${params.username}/raw/${params.langCode}`,
      form);
  },
  downloadSplitted(params) {
    return ApiService.get(
      "items",
      `${params.username}/splitted/${params.langCode}/${params.fileId}/download`
    ).then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data],{encoding:"UTF-8",type:"text/plain;charset=UTF-8"}));
      const link = document.createElement('a');
      link.href = url;
      if (!params.openInBrowser) {
        link.setAttribute('download', params.fileName);
      }
      document.body.appendChild(link);
      link.click();
    });
  },
  downloadSplittedFromDb(params) {
    return ApiService.get(
      "items",
      `${params.username}/splitted/${params.langCodeFrom}/${params.langCodeTo}/${params.align_guid}/download/${params.langCodeDownload}`
    ).then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data],{encoding:"UTF-8",type:"text/plain;charset=UTF-8"}));
      const link = document.createElement('a');
      link.href = url;
      if (!params.openInBrowser) {
        link.setAttribute('download', params.fileName);
      }
      document.body.appendChild(link);
      link.click();
    });
  },
  downloadProcessing(params) {
    return ApiService.post(
      "items",
      `${params.username}/processing/${params.langCodeFrom}/${params.langCodeTo}/${params.align_guid}/download/${params.langCodeDownload}/${params.format}`
    ).then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', params.fileName);
      document.body.appendChild(link);
      link.click();
    });
  },  
  downloadBook(params) {
    let form = new FormData();
    form.append("par_direction", params.parStructureDirection);
    form.append("left_lang", params.leftLang);
    form.append("style", params.style);
    return ApiService.post(
      "items",
      `${params.username}/create/${params.langCodeFrom}/${params.langCodeTo}/${params.align_guid}/download`,
      form
    ).then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', params.fileName);
      document.body.appendChild(link);
      link.click();
    });
  },  
  getBookPreview(params) {
    let form = new FormData();
    form.append("par_direction", params.parStructureDirection);
    form.append("left_lang", params.leftLang);
    form.append("style", params.style);
    return ApiService.post(
      "items",
      `${params.username}/create/${params.langCodeFrom}/${params.langCodeTo}/${params.align_guid}/preview`,
      form
    );
  },
  getSplitted(params) {
    return ApiService.get(
      "items",
      `${params.username}/splitted/${params.langCode}/${params.fileId}/${params.linesCount}/${params.page}`
    );
  },
  getMarks(params) {
    return ApiService.get(
      "items",
      `${params.username}/marks/${params.langCode}/${params.fileId}`
    );
  },
  getProcessing(params) {
    return ApiService.get(
      "items",
      `${params.username}/processing/${params.langCodeFrom}/${params.langCodeTo}/${params.fileId}/${params.linesCount}/${params.page}`
    );
  },
  getProcessingMeta(params) {
    return ApiService.get(
      "items",
      `${params.username}/processing/${params.langCodeFrom}/${params.langCodeTo}/${params.fileId}/meta`
    );
  },
  getProcessingByIds(params) {
    let form = new FormData();
    form.append("index_ids", params.index_ids);
    return ApiService.post(
      "items",
      `${params.username}/processing/${params.langCodeFrom}/${params.langCodeTo}/${params.align_guid}`,
      form
    );
  },
  getCandidates(params) {
    return ApiService.get(
      "items",
      `${params.username}/processing/${params.langCodeFrom}/${params.langCodeTo}/${params.fileId}/candidates/${params.textType}/${params.indexId}/${params.countBefore}/${params.countAfter}`
    );
  },
  getConflicts(params) {
    return ApiService.get(
      "items",
      `${params.username}/alignment/conflicts/${params.align_guid}`
    );
  },
  getConflictDetails(params) {
    return ApiService.get(
      "items",
      `${params.username}/alignment/conflicts/${params.align_guid}/show/${params.conflictId}`
    );
  },
  getDocIndex(params) {
    return ApiService.get(
      "items",
      `${params.username}/processing/${params.langCodeFrom}/${params.langCodeTo}/${params.fileId}/index`
    );
  },
  getSplittedByIds(params, type) {
    let form = new FormData();
    form.append("ids", params.ids);
    return ApiService.post(
      "items",
      `${params.username}/splitted/${type}/${params.langCodeFrom}/${params.langCodeTo}/${params.align_guid}`,
      form
    );
  },
  stopAlignment(params) {
    return ApiService.post(
      "items",
      `${params.username}/align/stop/${params.langCodeFrom}/${params.langCodeTo}/${params.alignId}`
    );
  },
  startAlignment(params) {
    let form = new FormData();
    form.append("id", params.id);
    form.append("align_all", params.alignAll);
    form.append("batch_ids", JSON.stringify(params.batchIds))
    form.append("batch_shift", params.batchShift)
    form.append("amount", params.amount)
    form.append("window", params.window)
    if (params.nextOnly) {
      console.log("calculating next batch")
      return ApiService.post(
        "items",
        `${params.username}/alignment/align/next`,
        form
      );
    }
    else {
      return ApiService.post(
        "items",
        `${params.username}/alignment/align`,
        form
      );

    }
  },
  createAlignment(params) {
    let form = new FormData();
    form.append("id_from", params.idFrom);
    form.append("id_to", params.idTo);
    form.append("name", params.name);
    return ApiService.post(
      "items",
      `${params.username}/alignment/create`,
      form
    );
  },
  resolveConflicts(params) {
    let form = new FormData();
    form.append("id", params.id);
    form.append("resolve_all", params.resolveAll);
    form.append("batch_ids", JSON.stringify(params.batchIds))
    return ApiService.post(
      "items",
      `${params.username}/alignment/resolve`,
      form
    );
  },
  deleteAlignment(params) {
    let form = new FormData();
    form.append("align_guid", params.guid);
    return ApiService.post(
      "items",
      `${params.username}/alignment/delete`,
      form
    );
  },
  deleteDocument(params) {
    let form = new FormData();
    form.append("guid", params.guid);
    form.append("lang", params.langCode);
    form.append("filename", params.filename);
    return ApiService.post(
      "items",
      `${params.username}/raw/delete`,
      form
    );
  },
  editProcessing(params) {
    let form = new FormData();
    form.append("text", params.text);
    form.append("text_type", params.text_type);
    form.append("operation", params.operation);
    form.append("index_id", params.indexId);
    form.append("target", params.target);
    form.append("candidate_line_id", params.candidateLineId);
    form.append("candidate_text", params.candidateText);
    form.append("batch_id", params.batchId);
    form.append("batch_index_id", params.batchIndexId);

    return ApiService.post(
      "items",
      `${params.username}/processing/${params.langCodeFrom}/${params.langCodeTo}/${params.fileId}/edit`,
      form
    );
  },
  editProcessingMarkUnused(params) {
    let form = new FormData();
    form.append("text_type", params.textType);
    form.append("line_id", params.lineId);
    return ApiService.post(
      "items",
      `${params.username}/edit/exclude/${params.langCodeFrom}/${params.langCodeTo}/${params.guid}`,
      form
    );
  },
  getContents() {
    return ApiService.get(
      "items",
      `contents`
    );
  }
};
