<template>
  <div>
    <div class="text-h4 mt-10 font-weight-bold">
      <v-icon color="blue" large>mdi-text-box-multiple</v-icon> Documents
    </div>
    <v-alert type="info" class="mt-6" v-show="showAlert">
      There are no uploaded documents yet. Please upload some using the form
      below.
    </v-alert>
    <div class="mt-6">
      <v-row>
        <v-col cols="12" sm="6">
          <RawPanel
            @uploadFile="uploadFile"
            @onFileChange="onFileChange"
            @selectAndLoadPreview="selectAndLoadPreview"
            @performDelete="performDeleteRawFile"
            :info="LANGUAGES[langCodeFrom]"
            :items="items"
            :isLoading="isLoading"
            :uploadEnabled="true"
          >
          </RawPanel>
        </v-col>
        <v-col cols="12" sm="6">
          <RawPanel
            @uploadFile="uploadFile"
            @onFileChange="onFileChange"
            @selectAndLoadPreview="selectAndLoadPreview"
            @performDelete="performDeleteRawFile"
            :info="LANGUAGES[langCodeTo]"
            :items="items"
            :isLoading="isLoading"
            :uploadEnabled="true"
          >
          </RawPanel>
        </v-col>
      </v-row>
    </div>

    <div class="text-h4 mt-10 font-weight-bold">
      <v-row>
        <v-col>
          <v-icon color="blue" large>mdi-file-find</v-icon> Preview
        </v-col>
        <v-col align="right">
          <!-- page count menu -->
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <template v-for="item in [10, 20, 50]">
                <v-list-item
                  :class="{
                    blue: item == splittedPanelPageCount,
                    'lighten-3': item == splittedPanelPageCount,
                  }"
                  link
                  :key="item"
                  @click="setSplittedPanelPageCount(item)"
                >
                  <v-list-item-title>{{ item }} lines</v-list-item-title>
                </v-list-item>
              </template>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>
    </div>
    <v-alert
      type="info"
      border="left"
      colored-border
      color="blue"
      class="mt-6"
      elevation="2"
    >
      Documents are splitted by sentences using language specific rules.
    </v-alert>
    <v-row>
      <v-col cols="12" sm="6">
        <SplittedPanel
          @onPreviewPageChange="onPreviewPageChange"
          @downloadSplitted="downloadSplitted"
          :info="LANGUAGES[langCodeFrom]"
          :splitted="splitted"
          :selected="selected"
          :isLoading="isLoading"
        >
        </SplittedPanel>
      </v-col>
      <v-col cols="12" sm="6">
        <SplittedPanel
          @onPreviewPageChange="onPreviewPageChange"
          @downloadSplitted="downloadSplitted"
          :info="LANGUAGES[langCodeTo]"
          :splitted="splitted"
          :selected="selected"
          :isLoading="isLoading"
        >
        </SplittedPanel>
      </v-col>
    </v-row>
    <div class="text-h4 mt-10 font-weight-bold">
      <v-row
        ><v-col>
          <v-icon color="blue" large>mdi-format-header-1</v-icon> Marks </v-col
        ><v-col align="right">
          <div class="d-inline-flex">
            <v-icon class="mr-2">mdi-format-horizontal-align-center</v-icon>
            <v-switch
              color="blue"
              value="true"
              v-model="isMarksInRow"
              class="mx-2"
            ></v-switch></div></v-col
      ></v-row>
    </div>
    <v-alert
      v-if="
        !marks ||
        (marks[langCodeFrom].length == 0 && marks[langCodeTo].length == 0)
      "
      type="info"
      border="left"
      colored-border
      color="info"
      class="mt-6"
      elevation="2"
    >
      No marks besides paragraphs were found in selected documents.
    </v-alert>

    <div v-else class="mt-0">
      <div v-if="isMarksInRow == 'true'">
        <v-row v-for="(pair, i) in mergedMarks" :key="i">
          <v-col cols="12" sm="6">
            <v-card outlined v-if="pair[0]">
              <MarkItem :mark="pair[0]" :id="i" :showParId="false"></MarkItem>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6">
            <v-card outlined v-if="pair[1]">
              <MarkItem :mark="pair[1]" :id="i" :showParId="false"></MarkItem>
            </v-card>
          </v-col>
        </v-row>
      </div>
      <div v-else>
        <v-row>
          <v-col cols="12" sm="6">
            <v-card>
              <div v-for="(mark, i) in marks[langCodeFrom]" :key="i">
                <MarkItem :mark="mark" :id="i" :showParId="false"></MarkItem>
                <v-divider />
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6">
            <v-card>
              <div v-for="(mark, i) in marks[langCodeTo]" :key="i">
                <MarkItem :mark="mark" :id="i" :showParId="false"></MarkItem>
                <v-divider />
              </div>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
import RawPanel from "@/components/RawPanel";
import SplittedPanel from "@/components/SplittedPanel";
import MarkItem from "@/components/MarkItem";
import { mapGetters } from "vuex";
import { DEFAULT_BATCHSIZE, TEST_LIMIT, API_URL } from "@/common/config";
import {
  LANGUAGES,
  DEFAULT_FROM,
  DEFAULT_TO,
  LanguageHelper,
} from "@/common/language.helper";
import { SettingsHelper } from "@/common/settings.helper";
import { Helper } from "@/common/helper";

import {
  INIT_USERSPACE,
  FETCH_ITEMS,
  UPLOAD_FILES,
  DELETE_DOCUMENT,
  GET_SPLITTED,
  GET_FILE_MARKS,
  DOWNLOAD_SPLITTED,
} from "@/store/actions.type";
import { SET_SPLITTED, SET_MARKS } from "@/store/mutations.type";

export default {
  data() {
    return {
      LANGUAGES,
      DEFAULT_FROM,
      DEFAULT_TO,
      DEFAULT_BATCHSIZE,
      TEST_LIMIT,
      API_URL,
      files: LanguageHelper.initGeneralVars(),
      proxyFiles: LanguageHelper.initGeneralVars(),
      selected: LanguageHelper.initGeneralVars(),
      selectedIds: LanguageHelper.initGeneralVars(),
      splittedPanelPageCount: SettingsHelper.getSplittedPanelPageCount(),
      isLoading: {
        upload: LanguageHelper.initGeneralBools(),
        uploadProxy: LanguageHelper.initGeneralBools(),
        download: LanguageHelper.initGeneralBools(),
        align: false,
        processing: false,
        processingMeta: false,
      },
      isMarksInRow: SettingsHelper.getIsMarksInRow(),
    };
  },
  methods: {
    getImgUrl(batch_id) {
      return `${API_URL}/static/img/${this.username}/${
        this.processingMeta.meta.align_guid
      }.best_${batch_id}.png?rnd=${Math.random()}`;
    },
    onFileChange(file, langCode) {
      this.files[langCode] = file;
    },
    onProxyFileChange(file, langCode) {
      this.proxyFiles[langCode] = file;
    },
    selectAndLoadPreview(langCode, name, fileId) {
      this.selected[langCode] = name;
      this.selectedIds[langCode] = fileId;
      this.$store.dispatch(GET_SPLITTED, {
        username: this.$route.params.username,
        langCode,
        fileId,
        linesCount: this.splittedPanelPageCount,
        page: 1,
      });
      this.$store.dispatch(GET_FILE_MARKS, {
        username: this.$route.params.username,
        langCode,
        fileId: this.selectedIds[langCode],
      });
    },
    onPreviewPageChange(page, langCode) {
      this.$store.dispatch(GET_SPLITTED, {
        username: this.$route.params.username,
        langCode,
        fileId: this.selectedIds[langCode],
        linesCount: this.splittedPanelPageCount,
        page: page,
      });
    },
    uploadFile(langCode) {
      this.isLoading.upload[langCode] = true;
      this.$store
        .dispatch(UPLOAD_FILES, {
          file: this.files[langCode],
          username: this.$route.params.username,
          langCode,
        })
        .then(() => {
          this.$store
            .dispatch(FETCH_ITEMS, {
              username: this.$route.params.username,
              langCode: langCode,
            })
            .then(() => {
              this.selectFirstDocument(langCode);
              this.isLoading.upload[langCode] = false;
            });
        });
    },
    //helpers
    itemsNotEmpty(langCode) {
      if (!this.items | !this.items[langCode]) {
        return false;
      }
      return this.items[langCode].length != 0;
    },
    selectFirstDocument(langCode) {
      if (this.itemsNotEmpty(langCode)) {
        this.selectAndLoadPreview(
          langCode,
          this.items[langCode][0].name,
          this.items[langCode][0].guid
        );
      } else {
        let data = { items: {}, meta: {} };
        data["items"][langCode] = [];
        data["meta"][langCode] = {};
        this.$store.commit(SET_SPLITTED, {
          data,
          langCode,
        });
        this.selected[langCode] = null;
        this.$store.commit(SET_MARKS, {
          data: { items: [] },
          langCode: this.langCodeFrom,
        });
        this.$store.commit(SET_MARKS, {
          data: { items: [] },
          langCode: this.langCodeTo,
        });
      }
    },
    fetchAll() {
      this.$store
        .dispatch(FETCH_ITEMS, {
          username: this.$route.params.username,
          langCode: this.langCodeFrom,
        })
        .then(() => {
          this.selectFirstDocument(this.langCodeFrom);
        });
      this.$store
        .dispatch(FETCH_ITEMS, {
          username: this.$route.params.username,
          langCode: this.langCodeTo,
        })
        .then(() => {
          this.selectFirstDocument(this.langCodeTo);
        });
    },
    downloadSplitted(langCode, openInBrowser) {
      this.$store.dispatch(DOWNLOAD_SPLITTED, {
        fileId: this.selectedIds[langCode],
        fileName: this.selected[langCode],
        username: this.$route.params.username,
        langCode,
        fromDb: false,
        openInBrowser,
      });
    },
    //deletion
    performDeleteRawFile(item, langCode) {
      this.$store
        .dispatch(DELETE_DOCUMENT, {
          username: this.$route.params.username,
          filename: item.name,
          guid: item.guid,
          langCode,
        })
        .then(() => {
          this.$store
            .dispatch(FETCH_ITEMS, {
              username: this.$route.params.username,
              langCode: langCode,
            })
            .then(() => {
              this.selectFirstDocument(langCode);
            });
        });
    },
    setSplittedPanelPageCount(pageCount) {
      this.splittedPanelPageCount = pageCount;
      this.onPreviewPageChange(1, this.langCodeFrom);
      this.onPreviewPageChange(1, this.langCodeTo);
    },
  },
  mounted() {
    this.$store
      .dispatch(INIT_USERSPACE, {
        username: this.$route.params.username,
      })
      .then(() => {
        this.fetchAll();
      });
  },
  watch: {
    isMarksInRow(value) {
      localStorage.isMarksInRow = value ? true : false;
    },
    splittedPanelPageCount(value) {
      SettingsHelper.setSplittedPanelPageCount(value);
    },
    langCodeFrom() {
      this.fetchAll();
    },
    langCodeTo() {
      this.fetchAll();
    },
    docIndex() {
      this.updateUnusedLines();
    },
  },
  computed: {
    ...mapGetters([
      "items",
      "itemsProcessing",
      "splitted",
      "marks",
      "processing",
      "docIndex",
      "conflictSplittedFrom",
      "conflictSplittedTo",
      "conflictFlowTo",
      "processingMeta",
    ]),
    mergedMarks() {
      let res = Helper.mergeMarks(this.marks[this.langCodeFrom], this.marks[this.langCodeTo])
      return res;
    },
    username() {
      return this.$route.params.username;
    },
    showAlert() {
      if (
        !this.items ||
        !this.items[this.langCodeFrom] ||
        !this.items[this.langCodeTo]
      ) {
        return true;
      }
      return (
        (this.items[this.langCodeFrom].length == 0) &
        (this.items[this.langCodeTo].length == 0)
      );
    },
    langCodeFrom() {
      let langCode = this.$route.params.from;
      if (this.LANGUAGES[langCode]) {
        return langCode;
      }
      return DEFAULT_FROM;
    },
    langCodeTo() {
      let langCode = this.$route.params.to;
      if (this.LANGUAGES[langCode]) {
        return langCode;
      }
      return DEFAULT_TO;
    },
    thresholdText() {
      if (this.downloadThreshold == 0) {
        return "no threshold";
      } else if (this.downloadThreshold == 100) {
        return "realy?";
      }
      return (this.downloadThreshold / 100).toFixed(2);
    },
    processingExists() {
      let selected_progress_item = this.itemsProcessing[
        this.langCodeFrom
      ].filter(
        (x) =>
          x.guid_from == this.selectedIds[this.langCodeFrom] &&
          x.guid_to == this.selectedIds[this.langCodeTo]
      );
      if (selected_progress_item.length > 0) {
        return true;
      }
      return false;
    },
    corporaSizeRelative() {
      return 5;
      // return this.selectedProcessing['sim_grades'][this.downloadThreshold] / this.selectedProcessing['sim_grades'][
      //   0
      // ] * 100;
    },
    corporaSizeAbsolute() {
      return 10;
      // return this.selectedProcessing['sim_grades'][this.downloadThreshold];
    },
  },
  components: {
    RawPanel,
    SplittedPanel,
    MarkItem,
  },
};
</script>
