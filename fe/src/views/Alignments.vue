<template>
  <div>
    <!-- <div class="d-flex">
      <div class="text-h3 mt-5 align-self-start">
        <v-img src="@/assets/logo.png" width="50px" height="50px" />
      </div>
      <div class="text-h3 mt-5 ml-3">
        Hello, <span class="text-capitalize">{{ username }}!</span>
        <div class="text-subtitle-1 mt-2 pl-1">Let's make it parallel</div>
      </div>
    </div> -->

    <div class="text-h4 mt-10 font-weight-bold">
      <v-icon color="blue" large>mdi-text-box-multiple</v-icon> Documents
    </div>
    <v-alert type="info" class="mt-6" v-show="showAlert">
      There are no uploaded documents yet. Please upload some using the
      Documents section.
    </v-alert>
    <div class="mt-6">
      <v-row>
        <v-col cols="12" sm="6">
          <RawPanel
            v-if="items[langCodeFrom].length > 0"
            @uploadFile="uploadFile"
            @onFileChange="onFileChange"
            @selectAndLoadPreview="selectAndLoadPreview"
            @performDelete="performDeleteRawFile"
            :info="LANGUAGES[langCodeFrom]"
            :items="items"
            :isLoading="isLoading"
          >
          </RawPanel>
        </v-col>
        <v-col cols="12" sm="6">
          <RawPanel
            v-if="items[langCodeFrom].length > 0"
            @uploadFile="uploadFile"
            @onFileChange="onFileChange"
            @selectAndLoadPreview="selectAndLoadPreview"
            @performDelete="performDeleteRawFile"
            :info="LANGUAGES[langCodeTo]"
            :items="items"
            :isLoading="isLoading"
          >
          </RawPanel>
        </v-col>
      </v-row>
    </div>

    <div class="text-h4 mt-10 font-weight-bold">
      <v-row>
        <v-col>
          <v-icon color="blue" large>mdi-align-horizontal-center</v-icon>
          Alignment
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
      Alignment process is going step by step. Create the alignment with choosen
      parameters and start working with it in the work area section.
    </v-alert>

    <div class="text-h5 mt-10 font-weight-bold">Documents to align</div>

    <v-row class="mt-6">
      <v-col cols="12" sm="6">
        <InfoPanel
          :info="LANGUAGES[langCodeFrom]"
          :splitted="splitted"
          :selected="selected"
        >
        </InfoPanel>
      </v-col>
      <v-col cols="12" sm="6">
        <InfoPanel
          :info="LANGUAGES[langCodeTo]"
          :splitted="splitted"
          :selected="selected"
        >
        </InfoPanel>
      </v-col>
    </v-row>

    <v-alert
      type="info"
      border="left"
      colored-border
      color="blue"
      elevation="2"
      v-if="!selected[langCodeFrom] || !selected[langCodeTo]"
      class="mt-5"
    >
      Please, select two items in the Documents section.
    </v-alert>
    <div v-else class="mt-5">
      <div v-if="!processingExists">
        <v-btn class="primary" @click="showCreateAlignmentDialog = true">
          Create alignment
        </v-btn>
        <CreateAlignmentDialog
          v-model="showCreateAlignmentDialog"
          @createAlignment="createAlignment"
        />
      </div>
      <v-alert
        v-else
        type="info"
        border="left"
        colored-border
        color="blue"
        elevation="2"
      >
        Alignment created. Select it below and start working.
      </v-alert>
    </div>

    <!-- <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2"
      v-if="!itemsProcessing || !itemsProcessing[langCodeFrom] || (itemsProcessing[langCodeFrom].length == 0)">
      There are no previously aligned documents yet.
    </v-alert> -->

    <div class="text-h4 mt-10 font-weight-bold">
      <v-icon color="blue" large>mdi-pencil</v-icon> Work area
    </div>

    <v-alert
      type="info"
      border="left"
      colored-border
      color="blue"
      class="mt-6"
      elevation="2"
      v-if="
        !itemsProcessing ||
        !itemsProcessing[langCodeFrom] ||
        itemsProcessing[langCodeFrom].length == 0
      "
    >
      There are no previously aligned documents yet.
    </v-alert>
    <div v-else class="mt-5">
      <div class="text-h5 mt-10 font-weight-bold">Alignments</div>
      <v-card class="mt-6">
        <div class="green lighten-5" dark>
          <v-card-title>Alignments</v-card-title>
          <v-card-text
            >List of previosly aligned documents [{{ langCodeFrom }}-{{
              langCodeTo
            }}]</v-card-text
          >
          <!-- {{itemsProcessing}} -->
        </div>
        <v-divider />
        <v-list flat class="pa-0">
          <v-list-item-group mandatory v-model="selectedListItem">
            <v-list-item
              v-for="(item, i) in itemsProcessing[langCodeFrom]"
              :key="i"
              @change="selectProcessing(item, item.guid)"
              @mouseover="hoverAlignmentIndex = i"
              @mouseleave="hoverAlignmentIndex = -1"
              class="lighten-4"
              :class="{ yellow: item.guid == selectedProcessingId }"
            >
              <v-list-item-icon>
                <v-icon
                  v-if="
                    item.state[0] == PROC_INIT ||
                    item.state[0] == PROC_IN_PROGRESS
                  "
                  color="blue"
                >
                  mdi-clock-outline</v-icon
                >
                <v-icon v-else-if="item.state[0] == PROC_ERROR" color="error"
                  >mdi-alert-circle</v-icon
                >
                <v-icon
                  v-else-if="item.state[0] == PROC_IN_PROGRESS_DONE"
                  color="blue"
                  >mdi-check</v-icon
                >
                <v-icon v-else color="green">mdi-check-circle-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title
                  >{{ item.name
                  }}<v-chip
                    class="ml-4"
                    color="grey"
                    text-color="black"
                    small
                    outlined
                  >
                    {{ item.state[2] }} / {{ item.state[1] }}</v-chip
                  >
                </v-list-item-title>
                <!-- {{item.state}} -->
                <!-- ---{{item.guid}}--- {{item.guid_from}} {{item.guid_to}} -->
              </v-list-item-content>
              <v-icon
                v-show="hoverAlignmentIndex == i"
                class="ml-2"
                @click.stop.prevent="
                  (hoveredAlignmentItem = item),
                    (showConfirmDeleteAlignmentDialog = true)
                "
                >mdi-close</v-icon
              >
              <!-- progress bar -->
              <v-progress-linear
                stream
                buffer-value="0"
                :value="(item.state[2] / item.state[1]) * 100"
                color="green"
                :active="
                  item.state[0] == PROC_INIT ||
                  item.state[0] == PROC_IN_PROGRESS
                "
                absolute
                bottom
              >
              </v-progress-linear>
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <ConfirmDeleteDialog
          v-model="showConfirmDeleteAlignmentDialog"
          :itemName="hoveredAlignmentItem.name"
          @confirmDelete="performDeleteAlignment"
        />
      </v-card>

      <!-- PROCESSING DOCUMENTS LIST BLOCK -->
      <v-row>
        <v-col class="text-center text-h4 mt-12">
          <span>{{ selectedProcessing.name }}</span>
        </v-col>
      </v-row>
      <!-- VISUALIZATION -->
      <div class="text-h5 mt-10 font-weight-bold">Visualization</div>
      <v-alert
        v-if="
          !processingMeta ||
          !processingMeta.meta ||
          processingMeta.meta.batch_ids.length == 0
        "
        type="info"
        border="left"
        colored-border
        color="purple"
        class="mt-6"
        elevation="2"
      >
        Images will start showing after the first batch completion.
      </v-alert>
      <div v-else class="mt-6">
        <!-- VISUAL CAROUSEL -->
        <swiper class="swiper pb-8" :options="swiperOption" ref="mySwiper">
          <swiper-slide
            v-for="(batch_id, i) in processingMeta.meta.batch_ids"
            :key="i"
          >
            <v-card class="vis-card" flat>
              <div class="green lighten-5">
                <v-card-title class="text-subtitle-2 pa-3 pb-3">
                  <span>batch {{ batch_id + 1 }} </span>
                  <v-spacer></v-spacer>
                  <span class="refresh-vis-icon">
                    <v-icon @click="refreshVis(batch_id)">mdi-refresh</v-icon>
                  </span>
                </v-card-title>
              </div>
              <v-divider></v-divider>
              <div
                class="vis-card-img"
                style="height: 100%"
                @click="
                  showRecalculateBatchDialog = true;
                  currentBatchId = batch_id;
                "
              >
                <img
                  width="100%"
                  :src="getImgUrl(batch_id)"
                  lazy-src="@/assets/vis_placeholder.png"
                  class="_swiper-lazy"
                />
                <!-- <div class="swiper-lazy-preloader"></div> -->
              </div>
            </v-card>
          </swiper-slide>
          <div class="swiper-scrollbar" slot="scrollbar"></div>
        </swiper>
        <RecalculateBatchDialog
          v-model="showRecalculateBatchDialog"
          :batch_id="currentBatchId"
          :inProgress="userAlignInProgress"
          @recalculateBatch="recalculateBatch"
          @resolveConflictsBatch="resolveConflictsBatch"
        />
      </div>

      <!-- ALIGNMENT SETTINGS -->
      <div class="text-h5 mt-12 font-weight-bold">Alignment</div>
      <v-row class="mt-5">
        <v-col>
          <v-card>
            <div class="green lighten-5">
              <v-card-title> Settings </v-card-title>
              <v-card-text>
                Choose alignment settings for selected document
              </v-card-text>
            </div>
            <v-divider></v-divider>
            <div class="pa-6">
              <v-row>
                <v-col cols="12" sm="4">
                  <v-card flat>
                    <div>
                      <v-card-title class="text-subtitle-1 pa-3 pt-0">
                        Batches to align:
                        <span class="font-weight-bold px-2">{{
                          batchesToAlign
                        }}</span>
                      </v-card-title>
                    </div>
                    <div class="pa-3">
                      <v-slider
                        v-model="batchesToAlign"
                        @change="customAlignmentSettings = null"
                        min="1"
                        max="5"
                        step="1"
                        ticks="always"
                        tick-size="1"
                      >
                      </v-slider>
                    </div>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-card flat>
                    <div>
                      <v-card-title class="text-subtitle-1 pa-3 pt-0">
                        Shift:
                        <span class="font-weight-bold px-2">{{
                          alignShift
                        }}</span>
                      </v-card-title>
                    </div>
                    <div class="pa-3">
                      <v-slider
                        v-model="alignShift"
                        min="-500"
                        max="500"
                        step="20"
                        thumb-label
                      >
                      </v-slider>
                    </div>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-card flat>
                    <div>
                      <v-card-title class="text-subtitle-1 pa-3 pt-0">
                        Window:
                        <span class="font-weight-bold px-2">{{
                          alignWindow
                        }}</span>
                      </v-card-title>
                    </div>
                    <div class="pa-3">
                      <v-slider
                        v-model="alignWindow"
                        min="20"
                        max="100"
                        step="10"
                        thumb-label
                      >
                      </v-slider>
                    </div>
                  </v-card>
                </v-col>
              </v-row>
              <div
                v-if="
                  selectedProcessing.proxy_to_loaded ||
                  selectedProcessing.proxy_from_loaded
                "
              >
                <v-card-title class="text-subtitle-1 pa-3 pt-0">
                  Align and resolve through the subscript:
                </v-card-title>
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-card
                      v-if="selectedProcessing.proxy_from_loaded"
                      flat
                      color="lighten-5 pa-1 rounded-xl"
                      :class="{ blue: useProxyFrom, grey: !useProxyFrom }"
                    >
                      <v-checkbox
                        :disabled="selectedProcessing.proxy_from_loaded == '0'"
                        class="pl-5"
                        v-model="useProxyFrom"
                        label="For the left text"
                      ></v-checkbox>
                    </v-card>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-card
                      v-if="selectedProcessing.proxy_to_loaded"
                      flat
                      color="lighten-5 pa-1 rounded-xl"
                      :class="{ blue: useProxyTo, grey: !useProxyTo }"
                    >
                      <v-checkbox
                        :disabled="selectedProcessing.proxy_to_loaded == '0'"
                        class="pl-5"
                        v-model="useProxyTo"
                        label="For the right text"
                      ></v-checkbox>
                    </v-card>
                  </v-col>
                </v-row>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- ALIGNMENT BUTTON -->
      <v-alert
        type="info"
        border="left"
        colored-border
        color="orange"
        class="mt-5"
        elevation="2"
        v-if="customAlignmentSettings"
      >
        Alignment settings was changed. Batches to align: from
        <span class="font-weight-bold">{{
          customAlignmentSettings.start + 1
        }}</span>
        to
        <span class="font-weight-bold">{{
          customAlignmentSettings.end + 1
        }}</span
        >.
      </v-alert>
      <v-row>
        <v-col class="text-right">
          <v-btn
            class="primary mt-4 mr-3 btn-min-w"
            @click="
              $refs.custAlignDialog.init();
              showCustomAlignmentSettingsDialog = true;
            "
          >
            Customize
          </v-btn>
          <CustomAlignmentSettingsDialog
            ref="custAlignDialog"
            v-model="showCustomAlignmentSettingsDialog"
            :totalBatches="selectedProcessingTotalBatches"
            @applySettings="applyCustomAlignmentSettings"
          />
          <v-btn
            v-if="customAlignmentSettings && !userAlignInProgress"
            class="success mt-4 btn-min-w"
            :loading="isLoading.align || isLoading.alignStopping"
            :disabled="isLoading.resolve"
            @click="alignCustom()"
          >
            Align custom
          </v-btn>
          <v-btn
            v-else-if="!userAlignInProgress"
            class="success mt-4 btn-min-w"
            :loading="isLoading.align || isLoading.alignStopping"
            :disabled="
              (selectedProcessing &&
                selectedProcessing.state[1] == selectedProcessing.state[2]) ||
              isLoading.resolve
            "
            @click="alignBatches()"
          >
            Align next
          </v-btn>
          <v-btn
            v-else
            v-show="selected[langCodeFrom] && selected[langCodeTo]"
            class="error mt-4 btn-min-w"
            @click="stopAlignment()"
          >
            Stop alignment
          </v-btn>
        </v-col>
      </v-row>

      <!-- CONFLICTS RESOLVING SECTION -->
      <div class="text-h5 mt-5 font-weight-bold">Conflicts</div>

      <div class="mt-5">
        <div class="font-weight-bold">
          {{ conflictsAmount() }} conflicts found
        </div>
      </div>

      <div class="text-center" v-if="isLoading.resolve || isLoading.conflicts">
        <v-progress-circular indeterminate color="green"></v-progress-circular>
      </div>
      <v-alert
        v-else-if="
          !processing ||
          !processing.items ||
          processing.items.length == 0 ||
          userAlignInProgress
        "
        type="info"
        border="left"
        colored-border
        color="info"
        class="mt-6"
        elevation="2"
      >
        There is nothing to show yet.
      </v-alert>
      <div v-else-if="conflictsAmount() > 0">
        <v-row class="mt-2">
          <v-col> Conflict {{ currConflictId + 1 }}: </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
            <v-card>
              <div v-for="(d, i) in conflictDetails.from" :key="i">
                <div class="d-table fill-height">
                  <div
                    class="d-table-cell grey lighten-4 pa-2 text-center"
                    style="min-width: 45px"
                  >
                    {{ i }}
                  </div>
                  <v-divider class="d-table-cell" vertical></v-divider>
                  <div class="d-table-cell pa-2">
                    {{ d }}
                  </div>
                </div>
                <v-divider />
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6">
            <v-card>
              <div v-for="(d, i) in conflictDetails.to" :key="i">
                <div class="d-table fill-height">
                  <div
                    class="d-table-cell grey lighten-4 pa-2 text-center"
                    style="min-width: 45px"
                  >
                    {{ i }}
                  </div>
                  <v-divider class="d-table-cell" vertical></v-divider>
                  <div class="d-table-cell pa-2">
                    {{ d }}
                  </div>
                </div>
                <v-divider />
              </div>
            </v-card>
          </v-col>
        </v-row>
      </div>
      <v-alert
        v-else
        type="info"
        border="left"
        colored-border
        color="info"
        class="mt-6"
        elevation="2"
      >
        All conflicts resolved.
      </v-alert>

      <!-- CHECK CONFLICTS BUTTON -->
      <v-row>
        <v-btn
          class="primary mt-4 ml-3 mr-5 btn-min-w-120"
          :disabled="
            isLoading.resolve || userAlignInProgress || currConflictId == 0
          "
          @click="showPrevConflict()"
        >
          Previous
        </v-btn>
        <v-btn
          class="primary mt-4 btn-min-w-120"
          :disabled="
            isLoading.resolve ||
            userAlignInProgress ||
            conflictsAmount() == 0 ||
            currConflictId == conflictsAmount() - 1
          "
          @click="showNextConflict()"
        >
          Next
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          class="primary mt-4 mr-3 btn-min-w"
          :disabled="isLoading.resolve || userAlignInProgress"
          @click="refreshConflicts()"
        >
          Refresh
        </v-btn>
        <v-btn
          class="primary mt-4 mr-3 btn-min-w"
          :disabled="
            isLoading.resolve || userAlignInProgress || conflictsAmount() == 0
          "
          @click="findLinePositionAndGotoEditor()"
        >
          Open in editor
        </v-btn>
        <v-btn
          class="success mt-4 mr-3 btn-min-w"
          :loading="isLoading.resolve"
          :disabled="
            isLoading.resolve || userAlignInProgress || conflictsAmount() == 0
          "
          @click="resolveConflictsBatch(-1)"
        >
          Resolve all
        </v-btn>
      </v-row>

      <!-- EDITOR SECTION -->
      <div class="text-h5 mt-10 font-weight-bold">Editor</div>

      <div class="text-center" v-if="isLoading.processing">
        <v-progress-circular indeterminate color="green"></v-progress-circular>
      </div>
      <v-alert
        v-else-if="
          selectedProcessing && selectedProcessing.state[0] == PROC_ERROR
        "
        type="error"
        border="left"
        colored-border
        color="error"
        class="mt-6"
        elevation="2"
      >
        Error occured. Please, write to @averkij.
      </v-alert>
      <v-alert
        v-else-if="
          !processing || !processing.items || processing.items.length == 0
        "
        type="info"
        border="left"
        colored-border
        color="info"
        class="mt-6"
        elevation="2"
      >
        There is nothing to show yet.
      </v-alert>

      <!-- EDIT ITEMS block-->
      <div v-else>
        <v-alert
          type="info"
          border="left"
          colored-border
          color="info"
          class="mt-6"
          elevation="2"
        >
          Pay attention to the beginning and the end of alignment. Some
          undetected conflicts can still be there.
        </v-alert>
        <v-card class="mt-2">
          <div class="green lighten-5" dark>
            <!-- title -->
            <v-card-title class="pr-3">
              {{ selectedProcessing.name }}
              <v-spacer></v-spacer>

              <v-icon>mdi-translate</v-icon>
              <v-switch
                color="green"
                value="true"
                v-model="showProxyTo"
                class="mx-2"
              ></v-switch>

              <v-btn icon @click="collapseEditItems">
                <v-icon>mdi-collapse-all</v-icon>
              </v-btn>
              <v-btn icon @click="expandEditItems">
                <v-icon>mdi-expand-all</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text
              >Review and edit automatically aligned document</v-card-text
            >
          </div>
          <v-divider></v-divider>

          <!-- items -->
          <div v-for="(line, i) in processing.items" :key="i">
            <EditItem
              @editProcessing="editProcessing"
              @editAddUpEnd="editAddUpEnd"
              @editAddDownEnd="editAddDownEnd"
              @editDeleteLine="editDeleteLine"
              @editAddEmptyLineBefore="editAddEmptyLineBefore"
              @editAddEmptyLineAfter="editAddEmptyLineAfter"
              @editClearLine="editClearLine"
              @getCandidates="getCandidates"
              @editAddCandidateEnd="editAddCandidateEnd"
              :item="line"
              :prevItem="i == 0 ? processing.items[0] : processing.items[i - 1]"
              :collapse="triggerCollapseEditItem"
              :expand="triggerExpandEditItem"
              :clearCandidates="triggerClearCandidates"
              :showProxyTo="showProxyTo"
              :panelColor="'green'"
              :proxy_from_dict="processing.proxy_from_dict"
              :proxy_to_dict="processing.proxy_to_dict"
            >
            </EditItem>
            <v-divider></v-divider>
          </div>

          <!-- pagination -->
          <v-row class="py-1 px-5">
            <v-col cols="12" sm="2"></v-col>
            <v-col cols="12" sm="8">
              <v-pagination
                v-model="processing.meta.page"
                :length="processing.meta.total_pages"
                total-visible="10"
                @input="onProcessingPageChange(processing.meta.page)"
              >
              </v-pagination>
            </v-col>
            <v-col cols="12" sm="2" class="text-right">
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="mt-1"
                    v-bind="attrs"
                    v-on="on"
                    @click="showGoToDialog = true"
                  >
                    <v-icon left color="grey">mdi-page-next-outline</v-icon>Go
                    to
                  </v-btn>
                </template>
                <span>Go to the specific page</span>
              </v-tooltip>
            </v-col>
            <GoToDialog v-model="showGoToDialog" @goToPage="goToPage" />
          </v-row>
        </v-card>
      </div>

      <!-- PROXY SECTION -->
      <div class="text-h5 mt-10 font-weight-bold">Subscript</div>

      <v-alert
        type="info"
        border="left"
        colored-border
        color="blue"
        class="mt-6"
        elevation="2"
      >
        You can optionally add the translation of the splitted text. Translation
        should contain the same amount of lines.
      </v-alert>
      <v-row class="mt-3">
        <v-col cols="12" sm="6">
          <ProxyPanel
            @onPreviewPageChange="onPreviewPageChange"
            @onProxyFileChange="onProxyFileChange"
            @downloadSplitted="downloadSplitted"
            @uploadProxyFile="uploadProxyFile"
            :info="LANGUAGES[langCodeFrom]"
            :splitted="splitted"
            :isLoading="isLoading"
            :showUploadProxyBtn="true"
          >
          </ProxyPanel>
        </v-col>
        <v-col cols="12" sm="6">
          <ProxyPanel
            @onPreviewPageChange="onPreviewPageChange"
            @onProxyFileChange="onProxyFileChange"
            @downloadSplitted="downloadSplitted"
            @uploadProxyFile="uploadProxyFile"
            :info="LANGUAGES[langCodeTo]"
            :splitted="splitted"
            :isLoading="isLoading"
            :showUploadProxyBtn="true"
          >
          </ProxyPanel>
        </v-col>
      </v-row>

      <div class="text-h4 mt-10 font-weight-bold">
        <v-icon color="blue" large>mdi-puzzle</v-icon> Unused strings
      </div>

      <div class="text-center" v-if="isLoading.processing">
        <v-progress-circular indeterminate color="green"></v-progress-circular>
      </div>
      <v-alert
        v-else-if="
          !processing || !processing.items || processing.items.length == 0
        "
        type="info"
        border="left"
        colored-border
        color="info"
        class="mt-6"
        elevation="2"
      >
        There is nothing to show yet.
      </v-alert>

      <div v-else>
        <v-alert
          v-if="
            (!unusedFromLines || unusedFromLines.length == 0) &&
            (!unusedToLines || unusedToLines.length == 0)
          "
          type="info"
          border="left"
          colored-border
          color="info"
          class="mt-6"
          elevation="2"
        >
          All sentences are in use.
        </v-alert>
        <div v-else>
          <v-card
            v-if="unusedFromLines && unusedFromLines.length > 0"
            class="mt-6"
          >
            <div class="blue lighten-5">
              <v-card-title
                >{{ LANGUAGES[langCodeFrom].name }}
                <!-- <v-spacer></v-spacer>
                <span class="text-button blue--text">show all</span>
                <v-switch value="true" false-value="false" v-model="showAllFrom" class="ml-2"></v-switch> -->
              </v-card-title>
              <v-card-text>{{ unusedFromLines.length }} lines </v-card-text>
            </div>
            <v-divider></v-divider>
            <div v-for="(line, i) in unusedFromLines" :key="i">
              <template>
                <div
                  v-show="
                    showAllFrom == 'true' || !conflictSplittedFrom[line].e
                  "
                >
                  <v-row justify="center" no-gutters>
                    <v-col class="text-left" cols="12">
                      <div class="d-table fill-height">
                        <div
                          class="d-table-cell grey lighten-4 pa-2 text-center"
                          style="min-width: 45px"
                        >
                          {{ line }}
                        </div>
                        <v-divider class="d-table-cell" vertical></v-divider>
                        <div
                          class="d-table-cell pa-2"
                          style="width: 100%"
                          :class="[
                            conflictSplittedFrom[line].e
                              ? ['grey', 'grey--text', 'lighten-5']
                              : '',
                          ]"
                        >
                          {{ conflictSplittedFrom[line].t }}
                          <div
                            v-if="conflictSplittedFrom[line].p"
                            class="
                              mt-3
                              proxy-to-subtitles
                              grey
                              lighten-3
                              font-weight-medium
                            "
                          >
                            {{ conflictSplittedFrom[line].p }}
                          </div>
                        </div>
                        <!-- <v-divider class="d-table-cell" vertical></v-divider>
                        <div class="d-table-cell grey lighten-5 pl-2 pt-2 text-center">
                          <v-checkbox hide-details color="blue" class="ma-1 pa-0" v-model="conflictSplittedFrom[line].e" @click.stop="markUnused('from', line)"></v-checkbox>
                        </div> -->
                      </div>
                    </v-col>
                  </v-row>
                  <v-divider></v-divider>
                </div>
              </template>
            </div>
          </v-card>
          <v-card v-if="unusedToLines && unusedToLines.length > 0" class="mt-6">
            <div class="blue lighten-5">
              <v-card-title
                >{{ LANGUAGES[langCodeTo].name }}
                <!-- <v-spacer></v-spacer>
                <span class="text-button blue--text">show all</span>
                <v-switch value="true" v-model="showAllTo" class="ml-2"></v-switch> -->
              </v-card-title>
              <v-card-text>{{ unusedToLines.length }} lines </v-card-text>
            </div>
            <v-divider></v-divider>
            <div v-for="(line, i) in unusedToLines" :key="i">
              <template>
                <div
                  v-show="showAllTo == 'true' || !conflictSplittedTo[line].e"
                >
                  <v-row justify="center" no-gutters>
                    <v-col class="text-left" cols="12">
                      <div class="d-table fill-height">
                        <div
                          class="d-table-cell grey lighten-4 pa-2 text-center"
                          style="min-width: 45px"
                        >
                          {{ line }}
                        </div>
                        <v-divider class="d-table-cell" vertical></v-divider>
                        <div
                          class="d-table-cell pa-2"
                          style="width: 100%"
                          :class="[
                            conflictSplittedTo[line].e
                              ? ['grey', 'grey--text', 'lighten-5']
                              : '',
                          ]"
                        >
                          {{ conflictSplittedTo[line].t }}
                          <div
                            v-if="conflictSplittedTo[line].p"
                            class="
                              mt-3
                              proxy-to-subtitles
                              grey
                              lighten-3
                              font-weight-medium
                            "
                          >
                            {{ conflictSplittedTo[line].p }}
                          </div>
                        </div>
                        <!-- <v-divider class="d-table-cell" vertical></v-divider>
                        <div class="d-table-cell grey lighten-5 pl-2 pt-2 text-center">
                          <v-checkbox hide-details color="blue" class="ma-1 pa-0" v-model="conflictSplittedTo[line].e" @click.stop.prevent="markUnused('to', line)"></v-checkbox>
                        </div> -->
                      </div>
                    </v-col>
                  </v-row>
                  <v-divider></v-divider>
                </div>
              </template>
            </div>
          </v-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RawPanel from "@/components/RawPanel";
import InfoPanel from "@/components/InfoPanel";
import ProxyPanel from "@/components/ProxyPanel";
import EditItem from "@/components/EditItem";
import GoToDialog from "@/components/GoToDialog";
import CreateAlignmentDialog from "@/components/CreateAlignmentDialog";
import RecalculateBatchDialog from "@/components/RecalculateBatchDialog";
import ConfirmDeleteDialog from "@/components/ConfirmDeleteDialog";
import CustomAlignmentSettingsDialog from "@/components/CustomAlignmentSettingsDialog";
import { mapGetters } from "vuex";
import { DEFAULT_BATCHSIZE, TEST_LIMIT, API_URL } from "@/common/config";
import {
  LANGUAGES,
  DEFAULT_FROM,
  DEFAULT_TO,
  LanguageHelper,
} from "@/common/language.helper";
import { SettingsHelper } from "@/common/settings.helper";
import {
  RESULT_OK,
  RESULT_ERROR,
  PROC_INIT,
  PROC_IN_PROGRESS,
  PROC_IN_PROGRESS_DONE,
  PROC_DONE,
  PROC_ERROR,
  EDIT_ADD_PREV_END,
  EDIT_ADD_NEXT_END,
  EDIT_ADD_CANDIDATE_END,
  EDIT_DELETE_LINE,
  EDIT_CLEAR_LINE,
  EDIT_LINE,
  ADD_EMPTY_LINE_BEFORE,
  ADD_EMPTY_LINE_AFTER,
} from "@/common/constants";
import {
  INIT_USERSPACE,
  FETCH_ITEMS,
  FETCH_ITEMS_PROCESSING,
  UPLOAD_FILES,
  DELETE_DOCUMENT,
  GET_SPLITTED,
  GET_DOC_INDEX,
  GET_PROCESSING,
  GET_PROCESSING_META,
  GET_CANDIDATES,
  GET_CONFLICTS,
  GET_CONFLICT_DETAILS,
  GET_CONFLICT_SPLITTED_FROM,
  GET_CONFLICT_SPLITTED_TO,
  // GET_CONFLICT_FLOW_TO,
  STOP_ALIGNMENT,
  EDIT_PROCESSING,
  EDIT_PROCESSING_MARK_UNUSED,
  CREATE_ALIGNMENT,
  DELETE_ALIGNMENT,
  ALIGN_SPLITTED,
  RESOLVE_CONFLICTS,
  DOWNLOAD_SPLITTED,
  UPDATE_VISUALIZATION,
  FIND_LINE_POSITION_IN_INDEX,
} from "@/store/actions.type";
import { SET_ITEMS_PROCESSING, SET_SPLITTED } from "@/store/mutations.type";

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
        upload: LanguageHelper.initGeneralBools(),
        uploadProxy: LanguageHelper.initGeneralBools(),
        align: false,
        resolve: false,
        processing: false,
        processingMeta: false,
        conflicts: false,
      },
      triggerCollapseEditItem: false,
      triggerExpandEditItem: false,
      triggerClearCandidates: false,
      userAlignInProgress: false,
      showProxyTo: SettingsHelper.getShowProxyTo(),
      showAllTo: SettingsHelper.getShowAllTo(),
      showAllFrom: SettingsHelper.getShowAllFrom(),
      selectedListItem: 0,
      currentBatchId: 0,

      //dialogs
      showGoToDialog: false,
      showCreateAlignmentDialog: false,
      showRecalculateBatchDialog: false,
      showConfirmDeleteAlignmentDialog: false,
      showCustomAlignmentSettingsDialog: false,

      //conflicts
      unusedFromLines: [],
      unusedToLines: [],
      usedFromLinesSet: new Set(),
      usedToLinesSet: new Set(),
      usedToLinesFlow: [],
      currConflictId: 0,

      hoverAlignmentIndex: -1,
      hoveredAlignmentItem: { name: "" },

      swiperOption: {
        slidesPerView: 5,
        spaceBetween: 20,
        // mousewheel: {
        //   sensitivity:5
        // },
        scrollbar: {
          el: ".swiper-scrollbar",
          draggable: true,
        },
        // preloadImages: false,
        // lazy: true
      },
      batchesToAlign: 5,
      alignShift: 0,
      alignWindow: 50,
      cacheKey: Math.random(),

      customAlignmentSettings: null,
      selectedProcessingTotalBatches: 0,
      useProxyFrom: false,
      useProxyTo: false,
    };
  },
  methods: {
    toSlide(index) {
      this.$refs.mySwiper.$swiper.slideTo(index, 0);
    },
    applyCustomAlignmentSettings(settings) {
      this.customAlignmentSettings = settings;
    },
    findLinePositionAndGotoEditor() {
      if (this.conflictDetails) {
        let lineId = Object.keys(this.conflictDetails["from"])[0];
        this.$store
          .dispatch(FIND_LINE_POSITION_IN_INDEX, {
            alignId: this.selectedProcessingId,
            username: this.$route.params.username,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo,
            langCode: this.langCodeFrom,
            lineId: lineId,
          })
          .then(() => {
            let editorPageSize = 10;
            let pageNumber =
              Math.floor(this.linePositionInIndex / editorPageSize) + 1;
            this.goToPage(pageNumber);
          });
      } else {
        alert("There are no conflicts.");
      }
    },
    downloadSplitted(langCode, openInBrowser) {
      this.$store.dispatch(DOWNLOAD_SPLITTED, {
        alignId: this.selectedProcessingId,
        fileName: this.selectedProcessingId + ".txt",
        username: this.$route.params.username,
        langCodeFrom: this.langCodeFrom,
        langCodeTo: this.langCodeTo,
        langCodeDownload: langCode,
        fromDb: true,
        openInBrowser,
      });
    },
    getImgUrl(batch_id) {
      return `${API_URL}/static/img/${this.username}/${this.processingMeta.meta.align_guid}.best_${batch_id}.png?rnd=${this.cacheKey}`;
    },
    prepareUsedToLines() {
      let foo = new Set();
      let bar = [];

      this.docIndex.forEach(function (ix, i) {
        let arr = JSON.parse(ix[3]);
        arr.forEach((to) => {
          foo.add(to);
          bar.push([i + 1, to]);
        });
      });

      this.usedToLinesSet = foo;
      this.usedToLinesFlow = bar;
    },
    prepareUsedFromLines() {
      let foo = new Set();
      this.docIndex.forEach(function (ix) {
        let arr = JSON.parse(ix[1]);
        arr.forEach((from) => {
          foo.add(from);
        });
      });

      this.usedFromLinesSet = foo;
    },
    updateUnusedLines() {
      this.prepareUsedFromLines();
      this.prepareUsedToLines();

      let unusedFromLines = [];
      let unusedToLines = [];

      if (!this.docIndex) {
        return;
      }
      let lastLine = this.docIndex[this.docIndex.length - 1];
      let lastLineFromIndex = JSON.parse(lastLine[1]);
      let lastLineToIndex = JSON.parse(lastLine[3]);

      //calculate unused lines
      for (let i = 1; i < lastLineFromIndex[0]; i++) {
        if (!this.usedFromLinesSet.has(i)) {
          unusedFromLines.push(i);
        }
      }
      for (let i = 1; i < lastLineToIndex[0]; i++) {
        if (!this.usedToLinesSet.has(i)) {
          unusedToLines.push(i);
        }
      }

      this.$store
        .dispatch(GET_CONFLICT_SPLITTED_FROM, {
          username: this.$route.params.username,
          ids: JSON.stringify(unusedFromLines),
          alignId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
        })
        .then(() => {
          this.unusedFromLines = unusedFromLines;
        });
      this.$store
        .dispatch(GET_CONFLICT_SPLITTED_TO, {
          username: this.$route.params.username,
          ids: JSON.stringify(unusedToLines),
          alignId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
        })
        .then(() => {
          this.unusedToLines = unusedToLines;
        });
    },
    refreshVis(batch_id) {
      this.$store
        .dispatch(UPDATE_VISUALIZATION, {
          username: this.$route.params.username,
          id: this.selectedProcessingId,
          batchIds: [batch_id],
          updateAll: "",
        })
        .then(() => {
          this.cacheKey = Math.random();
          this.$refs.mySwiper.$swiper.lazy.load();
          console.log(this.$refs.mySwiper.$swiper.lazy.load);
        });
    },
    createAlignment(name) {
      this.$store
        .dispatch(CREATE_ALIGNMENT, {
          username: this.$route.params.username,
          idFrom: this.selectedIds[this.langCodeFrom],
          idTo: this.selectedIds[this.langCodeTo],
          name: name,
        })
        .then(() => {
          this.$store
            .dispatch(FETCH_ITEMS_PROCESSING, {
              username: this.$route.params.username,
              langCodeFrom: this.langCodeFrom,
              langCodeTo: this.langCodeTo,
            })
            .then(() => {
              this.cacheKey = Math.random();
              this.selectFirstProcessingDocument();
            });
        });
    },
    startAlignment(
      batch_ids = [0],
      shift = 0,
      nextOnly = true,
      amount = 1,
      window = 50
    ) {
      this.isLoading.align = true;
      this.initProcessingDocument();
      this.currentlyProcessingId = this.selectedProcessingId;
      this.userAlignInProgress = true;

      this.$store
        .dispatch(ALIGN_SPLITTED, {
          username: this.$route.params.username,
          id: this.selectedProcessingId,
          nextOnly: nextOnly,
          batchIds: batch_ids,
          batchShift: shift,
          amount: amount,
          window: window,
          alignAll: "",
          useProxyFrom: this.useProxyFrom,
          useProxyTo: this.useProxyTo,
        })
        .then(() => {
          this.isLoading.align = false;
          console.log("fetchItemsProcessingTimer set");
          this.fetchItemsProcessingTimer();
        });
    },
    alignBatches() {
      this.startAlignment(
        [0],
        this.alignShift,
        true,
        this.batchesToAlign,
        this.alignWindow
      );
    },
    alignCustom() {
      let batch_ids = this.getRange(
        this.customAlignmentSettings.start,
        this.customAlignmentSettings.end
      );
      this.startAlignment(
        batch_ids,
        this.alignShift,
        false,
        1,
        this.alignWindow
      );
    },
    getRange(start, stop, step = 1) {
      return Array.from(
        { length: (stop - start) / step + 1 },
        (_, i) => start + i * step
      );
    },
    recalculateBatch(batch_id, shift) {
      this.startAlignment([batch_id], shift, false, 1, this.alignWindow);
    },
    resolveConflictsBatch(batch_id) {
      this.isLoading.resolve = true;
      this.initProcessingDocument();
      this.currentlyProcessingId = this.selectedProcessingId;
      this.$store
        .dispatch(RESOLVE_CONFLICTS, {
          username: this.$route.params.username,
          id: this.selectedProcessingId,
          batchIds: [batch_id],
          resolveAll: "",
          useProxyFrom: this.useProxyFrom,
          useProxyTo: this.useProxyTo,
        })
        .then(() => {
          console.log("fetchItemsProcessingTimer set");
          this.fetchItemsProcessingTimer();
        });
    },
    fetchItemsProcessingTimer() {
      setTimeout(() => {
        this.$store
          .dispatch(FETCH_ITEMS_PROCESSING, {
            username: this.$route.params.username,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo,
          })
          .then(() => {
            let in_progress_items = this.itemsProcessing[
              this.langCodeFrom
            ].filter((x) => x.state[0] == 0 || x.state[0] == 1);
            if (in_progress_items.length > 0) {
              this.selectCurrentlyProcessingDocument(this.selectedProcessing);
              this.fetchItemsProcessingTimer();
            } else {
              this.cacheKey = Math.random();
              this.userAlignInProgress = false;
              this.isLoading.alignStopping = false;
              this.isLoading.resolve = false;
              let currItem = this.itemsProcessing[this.langCodeFrom].filter(
                (x) => x.guid == this.currentlyProcessingId
              );
              if (currItem.length > 0) {
                this.selectCurrentlyProcessingDocument(currItem[0]);
              } else {
                this.selectCurrentlyProcessingDocument(this.selectedProcessing);
              }
            }
          });
      }, 6000);
    },
    initProcessingDocument() {
      let processingItemsCopy = JSON.parse(
        JSON.stringify(this.itemsProcessing[this.langCodeFrom])
      );
      let selectedProcessingStateCopy = JSON.parse(
        JSON.stringify(this.selectedProcessing.state)
      );
      let currentIndex = -1;
      if (this.itemsProcessingNotEmpty(this.langCodeFrom)) {
        currentIndex = processingItemsCopy.findIndex(
          (x) => x.guid == this.selectedProcessingId
        );
      }
      selectedProcessingStateCopy[0] = this.PROC_IN_PROGRESS;
      if (currentIndex >= 0) {
        processingItemsCopy.splice(currentIndex, 1, {
          imgs: [],
          name: this.selectedProcessing.name,
          state: selectedProcessingStateCopy,
        });
      } else {
        processingItemsCopy.push({
          imgs: [],
          name: this.selectedProcessing.name,
          state: selectedProcessingStateCopy,
        });
      }
      this.$store.commit(SET_ITEMS_PROCESSING, {
        items: processingItemsCopy,
        langCode: this.langCodeFrom,
      });
    },
    stopAlignment() {
      this.userAlignInProgress = false;
      this.isLoading.alignStopping = true;
      this.$store.dispatch(STOP_ALIGNMENT, {
        username: this.$route.params.username,
        langCodeFrom: this.langCodeFrom,
        langCodeTo: this.langCodeTo,
        alignId: this.currentlyProcessingId,
      });
    },
    onFileChange(file, langCode) {
      this.files[langCode] = file;
    },
    onProxyFileChange(file, langCode) {
      this.proxyFiles[langCode] = file;
    },
    onPreviewPageChange(page, langCode) {
      this.$store.dispatch(GET_SPLITTED, {
        username: this.$route.params.username,
        langCode,
        fileId: this.selectedIds[langCode],
        linesCount: 10,
        page: page,
      });
    },
    onProcessingPageChange(page) {
      let num = Math.min(page, this.processing.meta.total_pages);
      this.triggerClearCandidates = !this.triggerClearCandidates;
      this.$store.dispatch(GET_PROCESSING, {
        username: this.$route.params.username,
        langCodeFrom: this.langCodeFrom,
        langCodeTo: this.langCodeTo,
        fileId: this.selectedProcessingId,
        linesCount: 10,
        page: num,
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
    uploadProxyFile(langCode) {
      this.isLoading.uploadProxy[langCode] = true;
      this.$store
        .dispatch(UPLOAD_FILES, {
          alignId: this.selectedProcessingId,
          file: this.proxyFiles[langCode],
          username: this.$route.params.username,
          langCode,
          isProxy: true,
        })
        .then(() => {
          this.isLoading.uploadProxy[langCode] = false;
          this.$store
            .dispatch(FETCH_ITEMS_PROCESSING, {
              username: this.$route.params.username,
              langCodeFrom: this.langCodeFrom,
              langCodeTo: this.langCodeTo,
            })
            .then(() => {
              this.refreshCurrentlyProcessingDocument();
            });
        });
    },
    getCandidates(indexId, textType, countBefore, countAfter, callback) {
      this.$store
        .dispatch(GET_CANDIDATES, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId: indexId,
          fileId: this.selectedProcessingId,
          textType: textType,
          countBefore: countBefore,
          countAfter: countAfter,
        })
        .then(function (response) {
          callback(RESULT_OK, response.data);
        })
        .catch(() => {
          callback(RESULT_ERROR);
        });
    },
    selectAndLoadPreview(langCode, name, fileId) {
      this.selected[langCode] = name;
      this.selectedIds[langCode] = fileId;
      this.$store.dispatch(GET_SPLITTED, {
        username: this.$route.params.username,
        langCode,
        fileId,
        linesCount: 10,
        page: 1,
      });
    },
    showNextConflict() {
      if (this.currConflictId < this.conflictsAmount()) {
        this.currConflictId += 1;
        this.showConflict(this.currConflictId);
      }
    },
    showPrevConflict() {
      if (this.currConflictId > 0) {
        this.currConflictId -= 1;
        this.showConflict(this.currConflictId);
      }
    },
    showConflict(conflictId) {
      this.$store
        .dispatch(GET_CONFLICT_DETAILS, {
          username: this.$route.params.username,
          alignId: this.selectedProcessingId,
          conflictId: conflictId,
        })
        .then(() => {
          this.isLoading.conflicts = false;
        });
    },
    selectProcessing(item, fileId) {
      // if (fileId == this.selectedProcessingId) {
      //   return;
      // }

      this.selectedListItem = fileId;
      this.isLoading.processing = true;
      this.isLoading.processingMeta = true;
      this.isLoading.conflicts = true;
      this.selectedProcessing = item;
      this.selectedProcessingId = fileId;
      this.selectedProcessingTotalBatches = item.state[1];
      this.customAlignmentSettings = null;

      this.$store
        .dispatch(GET_PROCESSING_META, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          fileId,
        })
        .then(() => {
          this.isLoading.processingMeta = false;
        });

      this.$store
        .dispatch(GET_DOC_INDEX, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          fileId,
        })
        .then(() => {
          this.$store
            .dispatch(GET_PROCESSING, {
              username: this.$route.params.username,
              langCodeFrom: this.langCodeFrom,
              langCodeTo: this.langCodeTo,
              fileId,
              linesCount: 10,
              page: 1,
            })
            .then(() => {
              this.isLoading.processing = false;
            });
        });
      this.$store
        .dispatch(GET_CONFLICTS, {
          username: this.$route.params.username,
          alignId: this.selectedProcessingId,
        })
        .then(() => {
          this.currConflictId = 0;
          if (this.conflictsAmount() > 0) {
            this.$store
              .dispatch(GET_CONFLICT_DETAILS, {
                username: this.$route.params.username,
                alignId: this.selectedProcessingId,
                conflictId: 0,
              })
              .then(() => {
                this.isLoading.conflicts = false;
              });
          } else {
            this.isLoading.conflicts = false;
          }
        });
    },
    refreshConflicts() {
      this.isLoading.conflicts = true;
      this.$store
        .dispatch(GET_CONFLICTS, {
          username: this.$route.params.username,
          alignId: this.selectedProcessingId,
        })
        .then(() => {
          this.currConflictId = 0;
          if (this.conflictsAmount() > 0) {
            this.$store
              .dispatch(GET_CONFLICT_DETAILS, {
                username: this.$route.params.username,
                alignId: this.selectedProcessingId,
                conflictId: 0,
              })
              .then(() => {
                this.isLoading.conflicts = false;
              });
          } else {
            this.isLoading.conflicts = false;
          }
        });
    },
    refreshProcessingPage() {
      this.$store.dispatch(GET_PROCESSING, {
        username: this.$route.params.username,
        langCodeFrom: this.langCodeFrom,
        langCodeTo: this.langCodeTo,
        fileId: this.selectedProcessingId,
        linesCount: 10,
        page: this.processing.meta.page,
      });
    },
    editAddCandidateEnd(
      indexId,
      textType,
      candidateLineId,
      candidateText,
      batchId,
      batchIndexId
    ) {
      let langCode = textType == "from" ? this.langCodeFrom : this.langCodeTo;
      this.$store
        .dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          candidateLineId: candidateLineId,
          candidateText: this.LANGUAGES[langCode].noSpaceBetweenSentences
            ? candidateText
            : " " + candidateText,
          text_type: textType,
          operation: EDIT_ADD_CANDIDATE_END,
          target: "previous",
        })
        .then(() => {
          this.refreshProcessingPage();
        });
    },
    editAddUpEnd(indexId, editItemText, textType, batchId, batchIndexId) {
      let langCode = textType == "from" ? this.langCodeFrom : this.langCodeTo;
      this.$store
        .dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          text: this.LANGUAGES[langCode].noSpaceBetweenSentences
            ? editItemText
            : " " + editItemText,
          text_type: textType,
          operation: EDIT_ADD_PREV_END,
          target: "previous",
        })
        .then(() => {
          this.refreshProcessingPage();
        });
    },
    editAddDownEnd(indexId, editItemText, textType, batchId, batchIndexId) {
      let langCode = textType == "from" ? this.langCodeFrom : this.langCodeTo;
      this.$store
        .dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          text: this.LANGUAGES[langCode].noSpaceBetweenSentences
            ? editItemText
            : " " + editItemText,
          text_type: textType,
          operation: EDIT_ADD_NEXT_END,
          target: "next",
        })
        .then(() => {
          this.refreshProcessingPage();
        });
    },
    editAddEmptyLineBefore(indexId, batchId, batchIndexId) {
      this.$store
        .dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          operation: ADD_EMPTY_LINE_BEFORE,
        })
        .then(() => {
          this.refreshProcessingPage();
        });
    },
    editAddEmptyLineAfter(indexId, batchId, batchIndexId) {
      this.$store
        .dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          operation: ADD_EMPTY_LINE_AFTER,
        })
        .then(() => {
          this.refreshProcessingPage();
        });
    },
    editDeleteLine(indexId, batchId, batchIndexId) {
      this.$store
        .dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          operation: EDIT_DELETE_LINE,
        })
        .then(() => {
          this.refreshProcessingPage();
        });
    },
    editClearLine(indexId, textType, batchId, batchIndexId) {
      this.$store
        .dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          text_type: textType,
          operation: EDIT_CLEAR_LINE,
        })
        .then(() => {
          this.refreshProcessingPage();
        });
    },
    editProcessing(
      indexId,
      editItemText,
      textType,
      batchId,
      batchIndexId,
      callback
    ) {
      this.$store
        .dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          text: editItemText,
          text_type: textType,
          operation: EDIT_LINE,
        })
        .then(function () {
          callback(RESULT_OK);
        })
        .catch(() => {
          callback(RESULT_ERROR);
        });
    },
    markUnused(textType, lineId) {
      this.$store
        .dispatch(EDIT_PROCESSING_MARK_UNUSED, {
          username: this.$route.params.username,
          guid: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          lineId,
          textType,
        })
        .then(() => {
          console.log("Marked as unused");
        });
    },
    //dialogs
    goToPage(pageNumber) {
      this.onProcessingPageChange(pageNumber);
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
      }
    },
    selectFirstProcessingDocument() {
      if (this.itemsProcessingNotEmpty(this.langCodeFrom)) {
        this.selectProcessing(
          this.itemsProcessing[this.langCodeFrom][0],
          this.itemsProcessing[this.langCodeFrom][0].guid
        );
      }
    },
    getSelectedProcessingDocument() {
      if (this.itemsProcessingNotEmpty(this.langCodeFrom)) {
        if (this.selectedProcessingId) {
          let ids = this.itemsProcessing[this.langCodeFrom].filter(
            (x) => x.guid == this.selectedProcessingId
          );
          if (ids.length > 0) {
            let item_index = this.itemsProcessing[this.langCodeFrom].indexOf(
              ids[0]
            );
            return this.itemsProcessing[this.langCodeFrom][item_index];
          }
        }
      }
      return 0;
    },
    selectCurrentlyProcessingDocument(item) {
      if (this.itemsProcessingNotEmpty(this.langCodeFrom)) {
        if (this.currentlyProcessingId) {
          this.selectProcessing(item, this.currentlyProcessingId);
        }
      }
    },
    refreshCurrentlyProcessingDocument() {
      this.selectProcessing(
        this.getSelectedProcessingDocument(),
        this.selectedProcessingId
      );
    },
    collapseEditItems() {
      this.triggerCollapseEditItem = !this.triggerCollapseEditItem;
    },
    expandEditItems() {
      this.triggerExpandEditItem = !this.triggerExpandEditItem;
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
      this.$store
        .dispatch(FETCH_ITEMS_PROCESSING, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
        })
        .then(() => {
          let in_progress_items = this.itemsProcessing[
            this.langCodeFrom
          ].filter((x) => x.state[0] == 0 || x.state[0] == 1);
          if (in_progress_items.length > 0) {
            this.cacheKey = Math.random();
            let item_index = this.itemsProcessing[this.langCodeFrom].indexOf(
              in_progress_items[0]
            );
            this.currentlyProcessingId =
              this.itemsProcessing[this.langCodeFrom][item_index].guid;
            this.userAlignInProgress = true;
            this.fetchItemsProcessingTimer();
            this.selectCurrentlyProcessingDocument(
              this.itemsProcessing[this.langCodeFrom][item_index]
            );
          } else {
            this.selectFirstProcessingDocument();
          }
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
    performDeleteAlignment() {
      this.$store
        .dispatch(DELETE_ALIGNMENT, {
          username: this.$route.params.username,
          guid: this.hoveredAlignmentItem.guid,
        })
        .then(() => {
          this.$store
            .dispatch(FETCH_ITEMS_PROCESSING, {
              username: this.$route.params.username,
              langCodeFrom: this.langCodeFrom,
              langCodeTo: this.langCodeTo,
            })
            .then(() => {
              this.selectFirstProcessingDocument();
            });
        });
    },
    conflictsAmount() {
      let res = 0;
      if (this.conflicts && this.conflicts.length > 0) {
        this.conflicts.forEach((x) => (res += x[1]));
      }
      return res;
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
    showProxyTo(value) {
      localStorage.showProxyTo = value;
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
    docIndex() {
      this.updateUnusedLines();
    },
  },
  computed: {
    ...mapGetters([
      "items",
      "itemsProcessing",
      "splitted",
      "processing",
      "docIndex",
      "conflicts",
      "conflictDetails",
      "conflictSplittedFrom",
      "conflictSplittedTo",
      "conflictFlowTo",
      "processingMeta",
      "linePositionInIndex",
    ]),
    username() {
      return this.$route.params.username;
    },
    showAlert() {
      if (
        !this.items |
        !this.items[this.langCodeFrom] |
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
  },
  components: {
    EditItem,
    RawPanel,
    InfoPanel,
    ProxyPanel,
    GoToDialog,
    CreateAlignmentDialog,
    RecalculateBatchDialog,
    ConfirmDeleteDialog,
    CustomAlignmentSettingsDialog,
  },
};
</script>
