<template>
  <div>
    <v-row justify="center" class="edit-row" no-gutters>

      <!-- line menu -->
      <div class="cell-top-menu">
        <div class="px-2 py-0 font-weight-bold text-caption d-flex">
          <div class="px-2 cell-top-menu-item" @click="editAddEmptyLineAfter()">
            + строка
          </div>
          <!-- ↑ ↓ -->
          <div class="px-2 cell-top-menu-item" @click="editDeleteLine()">
            удалить
          </div>
          <v-spacer></v-spacer>
          <div class="px-2 cell-top-menu-item">
            строка {{item.index_id + 1}}
          </div>
        </div>
      </div>

      <!-- left side -->
      <v-col class="text-left" cols="6">
        <div class="d-table fill-height cell-edit">

          <!-- left line id column -->
          <div class="d-table-cell lighten-5 cell-edit-index text-center"
            :class="[{'red': panelColor=='red'},{'green': panelColor=='green'},{'blue': panelColor=='blue'}]">
            <div class="fill-height d-flex cell-edit-index-cont fix-height flex-column justify-space-between">
              <div class="pa-2 font-weight-medium line-num">
                {{ lineIdFrom }}
                <!-- [{{item.batch_id}}] [{{item.batch_index_id}}] -->
              </div>
              <div class="cell-edit-action-panel" :class="[{'c-red': panelColor=='red'},{'c-green': panelColor=='green'},{'c-blue': panelColor=='blue'}]">
                <div class="cell-edit-button" @click="editAddUpEnd('from')">
                  <v-icon>mdi-arrow-up-bold-circle</v-icon>
                </div>
                <div class="cell-edit-button" @click="editAddDownEnd('from')">
                  <v-icon>mdi-arrow-down-bold-circle</v-icon>
                </div>
                <div class="cell-edit-button" @click="editClearLine('from')">
                  <v-icon>mdi-eraser</v-icon>
                </div>
              </div>
              <!-- <div class="text-caption pa-1">
                {{ item.selected.sim | numeral("0.00") }}
              </div> -->
            </div>
          </div>

          <!-- left textarea -->
          <v-divider class="d-table-cell" vertical></v-divider>
          <div class="d-table-cell fill-width color-transition"
            :class="[{blue: changed_from},{'lighten-5': changed_from}]">
            <div class="pa-2 pb-8">
              <div class="d-table fill-height fill-width">
                <div class="d-table-cell">
                  <v-textarea class="ta-custom" auto-grow rows=1 text-wrap placeholder="Write your text here"
                    @click.native.stop @keyup.space.prevent @keydown.ctrl.83.prevent="$event.target.blur()"
                    @focus="setUneditedText($event)" @blur="editProcessing($event, 'from')"
                    @input="onTextChange($event, 'from')" :value="item.text_from">
                  </v-textarea>

                  <!-- PROXY TRANSLATION TEXT -->
                  <div v-if="showProxyTo == 'true'"
                    class="mt-3 proxy-to-subtitles grey lighten-3 font-weight-medium">
                    {{getProxyFromTexts()}}
                  </div>
                </div>

                <div class="d-table-cell" style="width:15px">
                  <i class="v-icon mdi mdi-chevron-down theme--light"
                    style="border-radius:50%; background:#f2f2f2; cursor:pointer;" @click="toggleShowLines('from')"
                    :class="{'icon-avtive':showLinesFrom}"></i>
                </div>
              </div>
            </div>

            <!-- CANDIDATES LEFT BLOCK -->
            <div v-show="showLinesFrom">
              <div class="candidates-cont" v-for="(t,i) in transFrom" :key="i">
                <v-divider></v-divider>
                <div class="d-table fill-height fill-width">

                  <!-- left candidates line id column -->
                  <div class="d-table-cell lighten-5 grey text-center font-weight-medium cell-edit-index">
                    <div class="fill-height lighten-5 d-flex flex-column justify-space-between cell-edit-index-cont">
                      <div class="pa-2 font-weight-medium line-num">
                        {{ t.id }}
                      </div>
                      <!-- candidates action panel -->
                      <div class="cell-edit-action-panel">
                        <div class="cell-edit-button" @click="editAddCandidateEnd('from', t.id, t.text)">
                          <v-icon>mdi-arrow-up-bold-circle</v-icon>
                        </div>
                      </div>
                      <!-- candidates similarity -->
                      <!-- <div class="text-caption pa-1">
                        {{ t.sim | numeral("0.00") }}
                      </div> -->
                    </div>
                  </div>

                  <v-divider class="d-table-cell" vertical></v-divider>

                  <!-- PROXY TRANSLATION CANDIDATES TEXT -->
                  <div class="d-table-cell yellow pa-2 fill-width candidate-text"
                    :class="[{'lighten-4': isLineIdFromSelected(t.id)}, {'lighten-5': !isLineIdFromSelected(t.id)}]">
                    {{ t.text }}
                    <div v-if="showProxyTo == 'true' && t.proxy"
                      class="mt-4 proxy-to-cand-subtitles font-weight-medium">
                      {{t.proxy}}
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </v-col>

      <!-- right side -->
      <v-col class="text-left" cols="6">
        <div class="d-table fill-height fill-width cell-edit">

          <v-divider class="d-table-cell" vertical></v-divider>
          <!-- <div class="d-table-cell lighten-5 text-center" style="min-width:45px" :class="{
                grey: item.selected.sim <= 0.3,
                green: item.selected.sim > 0.5,
                yellow: (item.selected.sim <= 0.5) && (item.selected.sim > 0.3)
              }"> -->

          <!-- right line id column -->
          <div class="d-table-cell lighten-5 cell-edit-index text-center"
            :class="[{'red': panelColor=='red'},{'green': panelColor=='green'},{'blue': panelColor=='blue'}]">
            <div class="fill-height d-flex cell-edit-index-cont fix-height flex-column justify-space-between">
              <div class="pa-2 font-weight-medium line-num">
                {{ lineIdTo }}
              </div>
              <div class="cell-edit-action-panel" :class="[{'c-red': panelColor=='red'},{'c-green': panelColor=='green'},{'c-blue': panelColor=='blue'}]">
                <div class="cell-edit-button" @click="editAddUpEnd('to')">
                  <v-icon>mdi-arrow-up-bold-circle</v-icon>
                </div>
                <div class="cell-edit-button" @click="editAddDownEnd('to')">
                  <v-icon>mdi-arrow-down-bold-circle</v-icon>
                </div>
                <div class="cell-edit-button" @click="editClearLine('to')">
                  <v-icon>mdi-eraser</v-icon>
                </div>
              </div>
              <!-- <div class="text-caption pa-1">
                {{ item.selected.sim | numeral("0.00") }}
              </div> -->
            </div>
          </div>

          <v-divider class="d-table-cell" vertical></v-divider>

          <!-- right textarea -->
          <div class="d-table-cell fill-width color-transition" :class="[{blue: changed_to},{'lighten-5': changed_to}]">
            <div class="pa-2 pb-8">
              <div class="d-table fill-height fill-width">
                <div class="d-table-cell">
                  <v-textarea class="ta-custom" auto-grow rows=1 text-wrap placeholder="Write your text here"
                    @click.native.stop @keyup.space.prevent @keydown.ctrl.83.prevent="$event.target.blur()"
                    @focus="setUneditedText($event)" @blur="editProcessing($event, 'to')"
                    @input="onTextChange($event, 'to')" :value="item.text_to">
                  </v-textarea>
                  <!-- prevItemLineId {{prevSelectedLineId}} -->

                  <!-- PROXY TRANSLATION TEXT -->
                  <div v-if="showProxyTo == 'true'"
                    class="mt-3 proxy-to-subtitles grey lighten-3 font-weight-medium">
                    {{getProxyToTexts()}}
                  </div>
                </div>
                <div class="d-table-cell" style="width:15px">
                  <i class="v-icon mdi mdi-chevron-down theme--light"
                    style="border-radius:50%; background:#f2f2f2; cursor:pointer;" @click="toggleShowLines('to')"
                    :class="{'icon-avtive':showLines}"></i>
                </div>
              </div>
            </div>

            <!-- CANDIDATES RIGHT BLOCK -->

            <!-- candidates animation -->
            <!-- <v-expand-transition> -->
            <!-- <v-slide-y-transition group hide-on-leave> -->
            <div v-show="showLines">
              <div class="candidates-cont" v-for="(t,i) in trans" :key="i">
                <v-divider></v-divider>
                <div class="d-table fill-height fill-width">

                  <!-- right candidates line id column -->
                  <div class="d-table-cell lighten-5 grey text-center font-weight-medium cell-edit-index">
                    <div class="fill-height lighten-5 d-flex flex-column justify-space-between cell-edit-index-cont">
                      <div class="pa-2 font-weight-medium line-num">
                        {{ t.id }}
                      </div>
                      <!-- candidates action panel -->
                      <div class="cell-edit-action-panel">
                        <div class="cell-edit-button" @click="editAddCandidateEnd('to', t.id, t.text)">
                          <v-icon>mdi-arrow-up-bold-circle</v-icon>
                        </div>
                      </div>
                      <!-- candidates similarity -->
                      <!-- <div class="text-caption pa-1">
                        {{ t.sim | numeral("0.00") }}
                      </div> -->
                    </div>
                  </div>

                  <!-- PROXY TRANSLATION CANDIDATES TEXT -->
                  <v-divider class="d-table-cell" vertical></v-divider>
                  <div class="d-table-cell yellow pa-2 fill-width candidate-text"
                    :class="[{'lighten-4': isLineIdToSelected(t.id)}, {'lighten-5': !isLineIdToSelected(t.id)}]">
                    {{ t.text }}
                    <div v-if="showProxyTo == 'true' && t.proxy"
                      class="mt-4 proxy-to-cand-subtitles font-weight-medium">
                      {{t.proxy}}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- </v-expand-transition> -->
            <!-- </v-slide-y-transition> -->
          </div>

        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import {
    // DEFAULT_VARIANTS_WINDOW_TO
  } from "@/common/config"
  import {
    STATE_SAVED,
    STATE_CHANGED,
    RESULT_OK
  } from "@/common/constants"
  import {
    Helper
  } from "@/common/helper"
  export default {
    name: "EditItem",
    props: ["item", "collapse", "clearCandidates", "showProxyTo", "prevItem", "fileId", "panelColor", "proxy_from_dict", "proxy_to_dict"],
    data() {
      return {
        state: STATE_SAVED,
        STATE_CHANGED,
        showLines: false,
        showLinesFrom: false,
        changed_from: false,
        changed_to: false,
        uneditedText: null,
        trans: [],
        transFrom: [],
        editedFromText: '',
        editedToText: ''
      }
    },
    methods: {
      getCandidates(textType) {
        this.$emit('getCandidates', this.item.index_id, textType, 1, 36, (res, data) => {
          if (res == RESULT_OK) {
            if (textType == "from") {
              this.transFrom = data.items;
            } else if (textType == "to") {
              this.trans = data.items;
            }
          } else {
            console.log("Edit error on getCandidates.")
          }
        });
      },
      editAddUpEnd(textType) {
        if (textType == "from") {
          let newText = this.editedFromText ? this.editedFromText : this.item.text_from;
          this.$emit('editAddUpEnd', this.item.index_id, newText, textType, this.item.batch_id, this.item
            .batch_index_id);
        } else if (textType == "to") {
          let newText = this.editedToText ? this.editedToText : this.item.text_to;
          this.$emit('editAddUpEnd', this.item.index_id, newText, textType, this.item.batch_id, this.item
            .batch_index_id);
        }
      },
      editAddDownEnd(textType) {
        if (textType == "from") {
          let newText = this.editedFromText ? this.editedFromText : this.item.text_from;
          this.$emit('editAddDownEnd', this.item.index_id, newText, textType, this.item.batch_id, this.item
            .batch_index_id);
        } else if (textType == "to") {
          let newText = this.editedToText ? this.editedToText : this.item.text_to;
          this.$emit('editAddDownEnd', this.item.index_id, newText, textType, this.item.batch_id, this.item
            .batch_index_id);
        }
      },
      editAddCandidateEnd(textType, lineId, text) {
        this.$emit('editAddCandidateEnd', this.item.index_id, textType, lineId, text, this.item.batch_id, this.item
          .batch_index_id);
      },
      editDeleteLine() {
        this.$emit('editDeleteLine', this.item.index_id, this.item.batch_id, this.item.batch_index_id);
      },
      editAddEmptyLineBefore() {
        this.$emit('editAddEmptyLineBefore', this.item.index_id, this.item.batch_id, this.item.batch_index_id);
      },
      editAddEmptyLineAfter() {
        this.$emit('editAddEmptyLineAfter', this.item.index_id, this.item.batch_id, this.item.batch_index_id);
      },
      editClearLine(textType) {
        this.$emit('editClearLine', this.item.index_id, textType, this.item.batch_id, this.item.batch_index_id);
      },
      editProcessing(event, textType) {
        // event.target.value = event.target.value .replace(/(\r\n|\n|\r)/gm, "")

        // #Не сохранять, если не изменилось
        let newText = event.target.value;
        if (Helper.trim(newText) != Helper.trim(this.uneditedText)) {
          this.$emit('editProcessing', this.item.index_id, newText, textType, this.item.batch_id, this.item
            .batch_index_id, (res) => {
              if (res == RESULT_OK) {
                this.state = STATE_SAVED;
                this.changed_from = false;
                this.changed_to = false;
              } else {
                console.log("Edit error on save.")
              }
            });
        }
      },
      setUneditedText(event) {
        this.uneditedText = event.target.value;
      },
      onTextChange(value, text_type) {
        this.state = STATE_CHANGED
        if (text_type == "from") {
          this.editedFromText = value;
          this.changed_from = true;
        } else {
          this.editedToText = value;
          this.changed_to = true;
        }
      },
      toggleShowLines(textType) {
        if (textType == "from") {
          this.showLinesFrom = !this.showLinesFrom;
          if (this.transFrom.length == 0) {
            this.getCandidates(textType);
          }
        } else if (textType == "to") {
          this.showLines = !this.showLines;
          if (this.trans.length == 0) {
            this.getCandidates(textType);
          }
        }
      },
      isLineIdToSelected(id) {
        return JSON.parse(this.item.line_id_to).includes(id);
      },
      isLineIdFromSelected(id) {
        return JSON.parse(this.item.line_id_from).includes(id);
      },
      getProxyFromTexts() {
        let res = JSON.parse(this.item.line_id_from).map(function (num) {
          return this.proxy_from_dict[num]
        }, this).join(" ")

        return res
      },
      getProxyToTexts() {
        let res = JSON.parse(this.item.line_id_to).map(function (num) {
          return this.proxy_to_dict[num]
        }, this).join(" ")

        return res
      }
    },
    computed: {
      lineIdFrom() {
        return JSON.parse(this.item.line_id_from).map(function (num) {
          return num
        }).join(", ");
      },
      lineIdTo() {
        return JSON.parse(this.item.line_id_to).map(function (num) {
          return num
        }).join(", ");
      },
      prevLineIdTo() {
        //correct
        return JSON.parse(this.prevItem.line_id_to)[0];
      },
      linesTo() {
        // let sid = this.item.selected.line_id;
        // let wnd = DEFAULT_VARIANTS_WINDOW_TO;
        // let wnd = 5;
        // not working with loadash _ (v-for is hiding)

        // let prevLineId = this.prevLineIdTo;
        // console.log("line_id:", this.selectedLineId, "prev_line_id:", prevLineId, DEFAULT_VARIANTS_WINDOW_TO)

        // if (this.showLines) {
        //   return this.item.trans.filter(function (tr) {

        //     return tr.processing_to_id >= prevLineId;
        //     // return tr.line_id < sid + wnd && tr.line_id > sid - wnd;
        //   })

        //   //sort by similarity
        //   // }).sort((a, b) => (a.sim > b.sim) ? -1 : ((b.sim > a.sim) ? 1 : 0))

        //   //get top values
        //   .slice(0, 5);
        // }

        return this.item.trans;

        // return [];
      }
    },
    watch: {
      collapse: function () {
        this.showLines = false;
        this.showLinesFrom = false;
      },
      clearCandidates: function () {
        this.trans = [];
        this.transFrom = [];
        this.showLines = false;
        this.showLinesFrom = false;
        this.editedFromText = '';
        this.editedToText = '';
      }
    }
  };
</script>
