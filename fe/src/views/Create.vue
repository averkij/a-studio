<template>
  <div>
    <div class="text-h4 mt-10 font-weight-bold">
      <v-icon color="blue" large>mdi-pencil</v-icon> Alignments
    </div>

    <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2"
      v-if="!itemsProcessing || !itemsProcessing[langCodeFrom] || (itemsProcessing[langCodeFrom].length == 0)">
      There are no previously aligned documents yet.
    </v-alert>
    <div v-else class="mt-5">

      <v-card class="mt-10">
        <div class="green lighten-5" dark>
          <v-card-title>Alignments</v-card-title>
          <v-card-text>List of previosly aligned documents [{{langCodeFrom}}-{{langCodeTo}}]</v-card-text>
          <!-- {{itemsProcessing}} -->
        </div>
        <v-divider/>
        <v-list flat class="pa-0">
          <v-list-item-group mandatory v-model="selectedListItem">
            <v-list-item v-for="(item, i) in itemsProcessing[langCodeFrom]" :key="i"
              @change="selectProcessing(item, item.guid)"
              @mouseover="hoverAlignmentIndex = i"
              @mouseleave="hoverAlignmentIndex = -1" class="lighten-3" :class="{'grey':item.guid==selectedProcessingId}">
              <v-list-item-icon>
                <v-icon v-if="item.state[0]==PROC_INIT || item.state[0]==PROC_IN_PROGRESS" color="blue">
                  mdi-clock-outline</v-icon>
                <v-icon v-else-if="item.state[0]==PROC_ERROR" color="error">mdi-alert-circle</v-icon>
                <v-icon v-else-if="item.state[0]==PROC_IN_PROGRESS_DONE" color="blue">mdi-check</v-icon>
                <v-icon v-else color="green">mdi-check-circle-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{item.name}}<v-chip class="ml-4" color="grey" text-color="black" small outlined>
                    {{item.state[2]}} / {{item.state[1]}}</v-chip>
                </v-list-item-title>
              </v-list-item-content>
              <v-icon v-show="hoverAlignmentIndex == i" class="ml-2" @click.stop.prevent="hoveredAlignmentItem=item, showConfirmDeleteAlignmentDialog=true">mdi-close</v-icon>
              <!-- progress bar -->
              <v-progress-linear stream buffer-value="0" :value="item.state[2]/item.state[1] * 100" color="green"
                :active="item.state[0]==PROC_INIT || item.state[0]==PROC_IN_PROGRESS" absolute bottom>
              </v-progress-linear>
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <ConfirmDeleteDialog v-model="showConfirmDeleteAlignmentDialog"
          :itemName=hoveredAlignmentItem.name
          @confirmDelete="performDeleteAlignment" />
      </v-card>

      <div class="text-h4 mt-10 font-weight-bold">
        <v-icon color="blue" large>mdi-format-header-1</v-icon> Edit marks
      </div>

      <v-alert v-if="!alignmentMarks || (alignmentMarks[langCodeFrom].length==0 && alignmentMarks[langCodeTo].length==0)" type="info" border="left" colored-border color="info" class="mt-6" elevation="2">
        Selected alignment doesn't have marks.
      </v-alert>
      
      <div v-else-if="showAlignmentMarks" class="mt-6">
        <v-row>
          <v-col cols="12" sm="6">
            <v-card>
            <div v-for="(mark,i) in orderedMarksFrom" :key="i">    
              <MarkItem :mark=mark :id=i :showParId="true"></MarkItem>
              <v-divider/>
            </div>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6">
            <v-card>
            <div v-for="(mark,i) in orderedMarksTo" :key="i">            
              <MarkItem :mark=mark :id=i :showParId="true"></MarkItem>
              <v-divider/>
            </div>
            </v-card>
          </v-col>  
        </v-row>
        <v-row>
          <v-col class="text-right">
            <v-btn class="primary mt-4 btn-min-w" @click="showAddMarkDialog=true">
              Add new mark
            </v-btn>
          </v-col>          
          <AddMarkDialog v-model="showAddMarkDialog" :langFrom=LANGUAGES[langCodeFrom].name :langTo=LANGUAGES[langCodeTo].name @addMark="addMark"/>
        </v-row>
      </div>

      <div v-else>
        <v-btn class="mt-9 btn-min-w" @click="showAlignmentMarks=true">
          Show marks
        </v-btn>
      </div>

      <!-- PROCESSING DOCUMENTS LIST BLOCK -->
      <v-row>
        <v-col v-if="selectedProcessing" class="text-center text-h4 mt-12">
          {{selectedProcessing.name}}
        </v-col>
      </v-row>

      <div class="text-h4 mt-10 font-weight-bold">
        <v-icon color="blue" large>mdi-bookshelf</v-icon> Book
      </div>
      
       <v-row class="mt-6">
        <v-col>
          <v-card>
            <div class="green lighten-5">
              <v-card-title>
                Settings
              </v-card-title>
              <v-card-text>
                Choose alignment settings for selected document
              </v-card-text>
            </div>
            <v-divider></v-divider>
            <div class="pa-6">
              <v-row>
                <v-col cols="12" sm="4">
                  <v-card flat>
                    <div class="white lighten-5">
                      <v-card-title class="text-subtitle-1 pa-3 pt-0">
                        Paragraph structure: <span class="font-weight-bold px-2">{{parStructureDirection}}</span>
                      </v-card-title>
                    </div>
                    <div class="white lighten-3 pa-3 pt-0">
                      <v-radio-group
                        v-model="parStructureDirection"
                        row
                      >
                        <v-radio
                          :label="langNameFrom"
                          value="from"
                        ></v-radio>
                        <v-radio
                          :label="langNameTo"
                          value="to"
                        ></v-radio>
                      </v-radio-group>
                    </div>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-card flat>
                    <div class="white lighten-5">
                      <v-card-title class="text-subtitle-1 pa-3 pt-0">
                        Lang order: <span class="font-weight-bold px-2">{{bookOrder(bookLeftLang)}}</span>
                      </v-card-title>
                    </div>
                    <div class="white lighten-3 pa-3 pt-0">
                      <v-radio-group
                        v-model="bookLeftLang"
                        row
                      >
                        <v-radio
                          :label="bookOrder('from')"
                          value="from"
                        ></v-radio>
                        <v-radio
                          :label="bookOrder('to')"
                          value="to"
                        ></v-radio>
                      </v-radio-group>
                    </div>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-card flat>
                    <div class="white lighten-5">
                      <v-card-title class="text-subtitle-1 pa-3 pt-0">
                        Style: <span class="font-weight-bold px-2">{{bookStyle}}</span>
                      </v-card-title>
                    </div>
                    <div class="white lighten-3 pa-3 pt-0">
                      <v-select
                        v-model="bookStyle"
                        :items="bookStyles"
                      ></v-select>
                    </div>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col class="text-right">
          <v-btn class="primary mt-4 btn-min-w" @click="getBookPreview()">
            Generate preview
          </v-btn>
        </v-col>
      </v-row>

      <div class="text-h5 mt-10 font-weight-bold">Preview</div>
      <v-alert v-if="!bookPreview" type="info" border="left" colored-border color="info" class="mt-6" elevation="2">
        Adjust the settings and generate book preview.
      </v-alert>
      <div v-else class="mt-10" v-html="bookPreview">
      </div>

      <div class="text-h4 mt-10 font-weight-bold">
        <v-icon color="blue" large>mdi-cloud-download</v-icon> Download
      </div>

      <v-alert v-if="!processing || !processing.items || processing.items.length == 0" type="info" border="left"
        colored-border color="info" class="mt-6" elevation="2">
        Please, wait. Alignment is in progress.
      </v-alert>
      <div v-else>
        <!-- <div class="mt-10">
          <v-row>
            <v-col cols="12">
              <v-subheader class="pl-0">Similarity threshold: {{thresholdText}}</v-subheader>
              <v-slider v-model="downloadThreshold" thumb-label :thumb-size="24">
                <template v-slot:thumb-label="{ value }">
                  {{ satisfactionEmojis[Math.min(Math.floor(value / 10), 9)] }}
                </template>
              </v-slider>
            </v-col>
          </v-row>
          <div class="text-center">
            <v-progress-circular :rotate="360" :size="260" :width="15" :value="corporaSizeRelative" color="teal">
              <div class="text-h2 black--text mt-4" style="line-height:2rem !important;">{{corporaSizeAbsolute}} <br />
                <span class="text-h5 grey--text">sentences</span></div>
            </v-progress-circular>
          </div>
        </div> -->
        <div class="mt-10">
          <v-row class="mt-5">
            <v-col cols="12" sm="6">
              <v-card>
                <div class="blue lighten-5">
                  <v-card-title>📕 Book</v-card-title>
                </div>
                <v-divider></v-divider>
                <v-card-title>Download</v-card-title>
                <v-card-text>Book in html format.</v-card-text>
                <v-divider class="mt-10"></v-divider>
                <v-card-actions>
                  <v-btn class="mt-5" @click="downloadBook()"><v-icon left color="grey">mdi-download</v-icon>Download</v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6">
              <v-card>
                <div class="blue lighten-5">
                  <v-card-title>📘 TMX corpora</v-card-title>
                </div>
                <v-divider></v-divider>
                <v-card-title>Download</v-card-title>
                <v-card-text>Aligned corpora in TMX format.</v-card-text>
                <v-divider class="mt-10"></v-divider>
                <v-card-actions>
                  <v-btn class="mt-5" @click="downloadProcessingTmx()"><v-icon left color="grey">mdi-download</v-icon>Download</v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6">
              <DownloadPanel @downloadFile="downloadProcessing" :info="LANGUAGES[langCodeFrom]" :isLoading=isLoading
                :count=100 :countOrig=splitted[langCodeFrom].meta.lines_count>
              </DownloadPanel>
            </v-col>
            <v-col cols="12" sm="6">
              <DownloadPanel @downloadFile="downloadProcessing" :info="LANGUAGES[langCodeTo]" :isLoading=isLoading
                :count=100 :countOrig=splitted[langCodeTo].meta.lines_count>
              </DownloadPanel>
            </v-col>
          </v-row>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import DownloadPanel from "@/components/DownloadPanel";
  import ConfirmDeleteDialog from "@/components/ConfirmDeleteDialog"
  import MarkItem from "@/components/MarkItem";
  import AddMarkDialog from "@/components/AddMarkDialog";
  import {
    mapGetters
  } from "vuex";
  import {
    DEFAULT_BATCHSIZE,
    TEST_LIMIT,
    API_URL
  } from "@/common/config";
  import {
    LANGUAGES,
    DEFAULT_FROM,
    DEFAULT_TO,
    LanguageHelper,
  } from "@/common/language.helper";
  import {
    BOOK_STYLES
  } from "@/common/helper";
  // import {
  //   SettingsHelper
  // } from "@/common/settings.helper";
  import {
    PROC_INIT,
    PROC_IN_PROGRESS,
    PROC_IN_PROGRESS_DONE,
    PROC_DONE,
    PROC_ERROR,
  } from "@/common/constants"
  import {
    INIT_USERSPACE,
    FETCH_ITEMS_PROCESSING,
    GET_DOC_INDEX,
    GET_PROCESSING,
    GET_PROCESSING_META,
    GET_BOOK_PREVIEW,
    GET_ALIGNMENT_MARKS,
    DELETE_ALIGNMENT,
    DOWNLOAD_SPLITTED,
    DOWNLOAD_PROCESSING,
    DOWNLOAD_BOOK,
    ADD_ALIGNMENT_MARK
  } from "@/store/actions.type";
  import {
    SET_BOOK_PREVIEW,
  } from "@/store/mutations.type";

  export default {
    data() {
      return {
        LANGUAGES,
        DEFAULT_FROM,
        DEFAULT_TO,
        DEFAULT_BATCHSIZE,
        TEST_LIMIT,
        API_URL,
        PROC_INIT,
        PROC_IN_PROGRESS,
        PROC_IN_PROGRESS_DONE,
        PROC_ERROR,
        PROC_DONE,
        files: LanguageHelper.initGeneralVars(),
        proxyFiles: LanguageHelper.initGeneralVars(),
        selected: LanguageHelper.initGeneralVars(),
        selectedProcessing: null,
        selectedProcessingId: null,
        currentlyProcessingId: null,
        selectedIds: LanguageHelper.initGeneralVars(),
        isLoading: {
          download: LanguageHelper.initGeneralBools(),
          processing: false,
          processingMeta: false,
          alignmentMarks: false
        },
        satisfactionEmojis: ['😍', '😄', '😁', '😊', '🙂', '😐', '🙁', '☹️', '😢', '😭'],
        downloadThreshold: 9,
        selectedListItem: 0,
        hoverAlignmentIndex: -1,
        hoveredAlignmentItem: {"name": ""},
        //dialogs
        showConfirmDeleteAlignmentDialog:false,
        showAddMarkDialog: false,
        parStructureDirection: "to",
        bookLeftLang: "from",
        bookStyle: BOOK_STYLES[0],
        bookStyles: BOOK_STYLES,
        showAlignmentMarks: true
      };
    },
    methods: {
      addMark(type, valueFrom, valueTo, parIdFrom, parIdTo) {
        this.$store.dispatch(ADD_ALIGNMENT_MARK, {
          alignId: this.selectedProcessingId,
          username: this.$route.params.username,
          type,
          valueFrom,
          valueTo,
          parIdFrom,
          parIdTo,
          occurence:0
        });
      },
      bookOrder(dir) {
        if (dir == "from") {
          return this.langCodeFrom + "-" + this.langCodeTo
        } else {
          return this.langCodeTo + "-" + this.langCodeFrom
        }
      },
      getBookPreview() {
        this.$store.dispatch(GET_BOOK_PREVIEW, {
          alignId: this.selectedProcessingId,
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          parStructureDirection: this.parStructureDirection,
          leftLang: this.bookLeftLang,
          style: this.bookStyle
        });
      },
      downloadBook() {
        this.$store.dispatch(DOWNLOAD_BOOK, {
          alignId: this.selectedProcessingId,
          fileName: this.selectedProcessingId + ".html",
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          parStructureDirection: this.parStructureDirection,
          leftLang: this.bookLeftLang,
          style: this.bookStyle
        });
      },
      downloadSplitted(langCode, openInBrowser) {
        this.$store.dispatch(DOWNLOAD_SPLITTED, {
          fileId: this.selectedIds[langCode],
          fileName: this.selected[langCode],
          username: this.$route.params.username,
          langCode,
          openInBrowser
        });
      },
      downloadProcessing(langCode) {
        this.$store.dispatch(DOWNLOAD_PROCESSING, {
          alignId: this.selectedProcessingId,
          fileName: this.selectedProcessingId + ".txt",
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          langCodeDownload: langCode,
          format: "txt"
        });
      },
      downloadProcessingTmx() {
        this.$store.dispatch(DOWNLOAD_PROCESSING, {
          alignId: this.selectedProcessingId,
          fileName: this.selectedProcessingId + ".tmx",
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          langCodeDownload: this.langCodeFrom,
          format: "tmx"
        });
      },
      selectProcessing(item, alignId) {
        this.selectedListItem = alignId;
        this.isLoading.processing = true;
        this.isLoading.processingMeta = true;
        this.isLoading.alignmentMarks = true;
        this.selectedProcessing = item;
        this.selectedProcessingId = alignId;

        this.$store.dispatch(GET_PROCESSING_META, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          fileId: alignId
        }).then(() => {
          this.isLoading.processingMeta = false;
        });

        this.$store.dispatch(GET_DOC_INDEX, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          fileId: alignId
        }).then(() => {
          this.$store.dispatch(GET_PROCESSING, {
            username: this.$route.params.username,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo,
            fileId: alignId,
            linesCount: 10,
            page: 1
          }).then(() => {
            this.isLoading.processing = false;
          });
        });

        this.$store.dispatch(GET_ALIGNMENT_MARKS, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          alignId
        }).then(() => {
          this.isLoading.alignmentMarks = false;
        });
      },
      //helpers
      itemsNotEmpty(langCode) {
        if (!this.items | !this.items[langCode]) {
          return false;
        }
        return this.items[langCode].length != 0;
      },
      itemsProcessingNotEmpty(langCode) {
        if (!this.itemsProcessing | !this.itemsProcessing[langCode]) {
          return false;
        }
        return this.itemsProcessing[langCode].length != 0;
      },
      selectFirstProcessingDocument() {
        if (this.itemsProcessingNotEmpty(this.langCodeFrom)) {
          this.selectProcessing(this.itemsProcessing[this.langCodeFrom][0], this.itemsProcessing[this.langCodeFrom][0]
            .guid);
        }
      },
      selectCurrentlyProcessingDocument(item) {
        if (this.itemsProcessingNotEmpty(this.langCodeFrom)) {
          if (this.currentlyProcessingId) {
            this.selectProcessing(item, this.currentlyProcessingId);
          }
        }
      },
      collapseEditItems() {
        this.triggerCollapseEditItem = !this.triggerCollapseEditItem;
      },
      fetchAll() {
        this.$store.dispatch(FETCH_ITEMS_PROCESSING, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo
        }).then(() => {
          let in_progress_items = this.itemsProcessing[this.langCodeFrom].filter(x => x.state[0] == 0 || x.state[
              0] ==
            1)
          if (in_progress_items.length > 0) {
            let item_index = this.itemsProcessing[this.langCodeFrom].indexOf(in_progress_items[0])
            this.currentlyProcessingId = this.itemsProcessing[this.langCodeFrom][item_index].guid
            this.userAlignInProgress = true;
            this.fetchItemsProcessingTimer();
            this.selectCurrentlyProcessingDocument(this.itemsProcessing[this.langCodeFrom][item_index]);
          } else {
            this.selectFirstProcessingDocument();
          }
        });
        this.$store
          .commit(SET_BOOK_PREVIEW, {
            items: ""
        });        
      },

      //deletion
      performDeleteAlignment() {
        this.$store
          .dispatch(DELETE_ALIGNMENT, {
            username: this.$route.params.username,
            guid: this.hoveredAlignmentItem.guid,
          })
          .then(() => {
            this.$store.dispatch(FETCH_ITEMS_PROCESSING, {
              username: this.$route.params.username,
              langCodeFrom: this.langCodeFrom,
              langCodeTo: this.langCodeTo
            }).then(() => {
              this.selectFirstProcessingDocument();
            });
          });
      },
    },
    mounted() {
      this.$store.dispatch(INIT_USERSPACE, {
        username: this.$route.params.username
      }).then(() => {
        this.fetchAll();
      });
    },
    watch: {
      showProxyTo(value) {
        localStorage.showProxyTo = value
      },
      showAllTo(value) {
        localStorage.showAllTo = value ? true : false;
      },
      showAllFrom(value) {
        localStorage.showAllFrom = value ? true : false;
      },
      langCodeFrom() {
        this.fetchAll();
      },
      langCodeTo() {
        this.fetchAll();
      },
    },
    computed: {
      ...mapGetters(["items", "itemsProcessing", "splitted", "processing", "docIndex", "conflictSplittedFrom",
        "conflictSplittedTo", "conflictFlowTo", "processingMeta", "bookPreview", "alignmentMarks"
      ]),
      orderedMarksFrom() {
        //sort marks by paragraph id
        let marksCopy = JSON.parse(JSON.stringify(this.alignmentMarks[this.langCodeFrom]));
        marksCopy.sort((a,b) => {
          if (a[3] == b[3]) {
            return a[1] - b[1];
          }
          return a[3] - b[3];
        });
        return marksCopy;
      },
      orderedMarksTo() {
        //sort marks by paragraph id
        let marksCopy = JSON.parse(JSON.stringify(this.alignmentMarks[this.langCodeTo]));
        marksCopy.sort((a,b) => {
          if (a[3] == b[3]) {
            return a[1] - b[1];
          }
          return a[3] - b[3];
        });
        return marksCopy;
      },
      username() {
        return this.$route.params.username;
      },
      showAlert() {
        if (!this.items | !this.items[this.langCodeFrom] | !this.items[this.langCodeTo]) {
          return true;
        }
        return (this.items[this.langCodeFrom].length == 0) & (this.items[this.langCodeTo].length == 0);
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
      langNameFrom() {
        let langCode = this.$route.params.from;
        if (this.LANGUAGES[langCode]) {
          return this.LANGUAGES[langCode].name;
        }
        return this.LANGUAGES[DEFAULT_FROM].name;
      },
      langNameTo() {
        let langCode = this.$route.params.to;
        if (this.LANGUAGES[langCode]) {
          return this.LANGUAGES[langCode].name;
        }
        return this.LANGUAGES[DEFAULT_TO].name;
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
        let selected_progress_item = this.itemsProcessing[this.langCodeFrom].filter(x => x.guid_from == this
          .selectedIds[this.langCodeFrom] && x.guid_to == this.selectedIds[this.langCodeTo]);
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
      }
    },
    components: {
      DownloadPanel,
      ConfirmDeleteDialog,
      AddMarkDialog,
      MarkItem
    }
  };
</script>
