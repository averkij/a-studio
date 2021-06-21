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
      There are no uploaded documents yet. Please upload some using the form
      below.
    </v-alert>
    <div class="mt-6">
      <v-row>
        <v-col cols="12" sm="6">
          <RawPanel @uploadFile="uploadFile" @onFileChange="onFileChange" @selectAndLoadPreview="selectAndLoadPreview" @performDelete="performDeleteRawFile"
            :info="LANGUAGES[langCodeFrom]" :items=items :isLoading=isLoading>
          </RawPanel>
        </v-col>
        <v-col cols="12" sm="6">
          <RawPanel @uploadFile="uploadFile" @onFileChange="onFileChange" @selectAndLoadPreview="selectAndLoadPreview" @performDelete="performDeleteRawFile"
            :info="LANGUAGES[langCodeTo]" :items=items :isLoading=isLoading>
          </RawPanel>
        </v-col>
      </v-row>
    </div>

    <div class="text-h4 mt-10 font-weight-bold">
      <v-icon color="blue" large>mdi-file-find</v-icon> Preview
    </div>
    <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2">
      Documents are splitted by sentences using language specific rules.
    </v-alert>
    <v-row>
      <v-col cols="12" sm="6">
        <SplittedPanel @onPreviewPageChange="onPreviewPageChange" @onProxyFileChange="onProxyFileChange"
          @downloadSplitted="downloadSplitted" @uploadProxyFile="uploadProxyFile" :info="LANGUAGES[langCodeFrom]"
          :splitted=splitted :selected=selected :isLoading=isLoading :showUploadProxyBtn=true>
        </SplittedPanel>
      </v-col>
      <v-col cols="12" sm="6">
        <SplittedPanel @onPreviewPageChange="onPreviewPageChange" @onProxyFileChange="onProxyFileChange"
          @downloadSplitted="downloadSplitted" @uploadProxyFile="uploadProxyFile" :info="LANGUAGES[langCodeTo]"
          :splitted=splitted :selected=selected :isLoading=isLoading :showUploadProxyBtn=true>
        </SplittedPanel>
      </v-col>
    </v-row>

    <div class="text-h4 mt-10 font-weight-bold">
      <v-icon color="blue" large>mdi-align-horizontal-center</v-icon> Alignment
    </div>
    <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2">
      Alignment process is going step by step. Create the alignment with choosen parameters and start working with it in
      the work area section.
    </v-alert>

    <div class="text-h5 mt-10 font-weight-bold">Documents to align</div>

    <v-row class="mt-6">
      <v-col cols="12" sm="6">
        <InfoPanel :info="LANGUAGES[langCodeFrom]" :splitted=splitted :selected=selected>
        </InfoPanel>
      </v-col>
      <v-col cols="12" sm="6">
        <InfoPanel :info="LANGUAGES[langCodeTo]" :splitted=splitted :selected=selected>
        </InfoPanel>
      </v-col>
    </v-row>

    <v-alert type="info" border="left" colored-border color="blue" elevation="2"
      v-if="!selected[langCodeFrom] || !selected[langCodeTo]" class="mt-5">
      Please, select two items in the Documents section.
    </v-alert>
    <div v-else class="mt-5">
      <div v-if="!processingExists">
        <v-btn class="primary" @click="showCreateAlignmentDialog=true">
          Create alignment
        </v-btn>
        <CreateAlignmentDialog v-model="showCreateAlignmentDialog" @createAlignment="createAlignment" />
      </div>
      <v-alert v-else type="info" border="left" colored-border color="blue" elevation="2">
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

    <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2"
      v-if="!itemsProcessing || !itemsProcessing[langCodeFrom] || (itemsProcessing[langCodeFrom].length == 0)">
      There are no previously aligned documents yet.
    </v-alert>
    <div v-else class="mt-5">

      <div class="text-h5 mt-10 font-weight-bold">Alignments</div>
      <v-card class="mt-6">
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
              @mouseleave="hoverAlignmentIndex = -1">
              <v-list-item-icon>
                <v-icon v-if="item.state[0]==PROC_INIT || item.state[0]==PROC_IN_PROGRESS" color="blue">
                  mdi-clock-outline</v-icon>
                <v-icon v-else-if="item.state[0]==PROC_ERROR" color="error">mdi-alert-circle</v-icon>
                <v-icon v-else-if="item.state[0]==PROC_IN_PROGRESS_DONE" color="blue">mdi-check</v-icon>
                <v-icon v-else color="teal">mdi-check</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{item.name}}<v-chip class="ml-4" color="grey" text-color="black" small outlined>
                    {{item.state[2]}} / {{item.state[1]}}</v-chip>
                </v-list-item-title>
                <!-- {{item.state}} -->
                <!-- ---{{item.guid}}--- {{item.guid_from}} {{item.guid_to}} -->
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

      <!-- PROCESSING DOCUMENTS LIST BLOCK -->
      <div class="text-h5 mt-12 font-weight-bold">
        {{selectedProcessing.name}}
      </div>

      <!-- ALIGNMENT BUTTON -->
      <v-btn v-if="!userAlignInProgress" class="success mt-6"
        :loading="isLoading.align || isLoading.alignStopping"
        :disabled="selectedProcessing && selectedProcessing.state[1]==selectedProcessing.state[2]"
        @click="startAlignment()">
        Align next batch
      </v-btn>
      <v-btn v-else v-show="selected[langCodeFrom] && selected[langCodeTo]" class="error mt-6" @click="stopAlignment()">
        Stop alignment
      </v-btn>

      <v-alert v-if="!processingMeta || !processingMeta.meta || processingMeta.meta.batch_ids.length == 0" type="info"
        border="left" colored-border color="purple" class="mt-6" elevation="2">
        Images will start showing after the first batch completion.
      </v-alert>
      <v-row v-else class="mt-6">
        <v-col v-for="(batch_id, i) in processingMeta.meta.batch_ids" :key=i cols="12" sm="3">
          <v-hover v-slot="{ hover }">
            <v-card :class="{ 'batch-card-hover': hover }"
              @click="showRecalculateBatchDialog=true; currentBatchId=batch_id">
              <div class="grey lighten-5">
                <v-card-title>
                  batch {{batch_id+1}}
                  <v-spacer></v-spacer>
                  <v-chip color="grey" text-color="black" small outlined>
                    {{DEFAULT_BATCHSIZE * i + 1}} — {{DEFAULT_BATCHSIZE * (i + 1)}}
                  </v-chip>
                </v-card-title>
              </div>
              <v-divider></v-divider>
              <!-- <v-img :src="`${API_URL}/static/img/${username}/${processingMeta.meta.align_guid}.best_${batch_id}.png`"
                :lazy-src="`${API_URL}/static/proc_img_stub.jpg`">
                <template v-slot:placeholder>
                  <v-row class="fill-height ma-0" align="center" justify="center">
                    <v-progress-circular indeterminate color="green"></v-progress-circular>
                  </v-row>
                </template>
              </v-img> -->
              <div>
                <img width=100% :src="getImgUrl(batch_id)">
              </div>
            </v-card>
          </v-hover>
        </v-col>
        <RecalculateBatchDialog v-model="showRecalculateBatchDialog"
          :batch_id=currentBatchId
          :inProgress="userAlignInProgress"
          @recalculateBatch="recalculateBatch"
          @resolveConflictsBatch="resolveConflictsBatch"/>
      </v-row>

      <div class="text-h5 mt-10 font-weight-bold">Edit</div>

      <div class="text-center" v-if="isLoading.processing">
        <v-progress-circular indeterminate color="green"></v-progress-circular>
      </div>
      <v-alert v-else-if="selectedProcessing && selectedProcessing.state[0]==PROC_ERROR" type="error" border="left"
        colored-border color="error" class="mt-6" elevation="2">
        Error occured. Please, write to @averkij.
      </v-alert>
      <v-alert v-else-if="!processing || !processing.items || processing.items.length == 0" type="info" border="left"
        colored-border color="info" class="mt-6" elevation="2">
        Please, wait. Alignment is in progress.
      </v-alert>

      <!-- EDIT ITEMS block-->
      <v-card v-else class="mt-6">
        <div class="green lighten-5" dark>

          <!-- title -->
          <v-card-title class="pr-3">
            {{selectedProcessing.name}}
            <v-spacer></v-spacer>

            <v-icon>mdi-translate</v-icon>
            <v-switch color="green" value="true" v-model="showProxyTo" class="mx-2"></v-switch>
            <!-- <div>showTranslation: {{clientSettings}}</div> -->

            <v-btn icon @click="collapseEditItems">
              <v-icon>mdi-collapse-all</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>Review and edit automatically aligned document</v-card-text>
        </div>
        <v-divider></v-divider>

        <!-- items -->
        <div v-for="(line, i) in processing.items" :key="i">
          <EditItem @editProcessing="editProcessing" @editAddUpEnd="editAddUpEnd" @editAddDownEnd="editAddDownEnd"
            @editDeleteLine="editDeleteLine" @editAddEmptyLineBefore="editAddEmptyLineBefore"
            @editAddEmptyLineAfter="editAddEmptyLineAfter" @editClearLine="editClearLine" @getCandidates="getCandidates"
            @editAddCandidateEnd="editAddCandidateEnd" :item="line"
            :prevItem="i == 0 ? processing.items[0] : processing.items[i-1]" :collapse="triggerCollapseEditItem"
            :clearCandidates="triggerClearCandidates" :showProxyTo="showProxyTo" :panelColor="'green'"
            :proxy_from_dict="processing.proxy_from_dict" :proxy_to_dict="processing.proxy_to_dict">
          </EditItem>
          <v-divider></v-divider>
        </div>

        <!-- pagination -->
        <v-row class="py-1 px-5">
          <v-col cols="12" sm="2"></v-col>
          <v-col cols="12" sm="8">
            <v-pagination v-model="processing.meta.page" :length="processing.meta.total_pages" total-visible="10"
              @input="onProcessingPageChange(processing.meta.page)">
            </v-pagination>
          </v-col>
          <v-col cols="12" sm="2" class="text-right">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn class="mt-1" v-bind="attrs" v-on="on" @click="showGoToDialog=true">
                  <v-icon left color="grey">mdi-page-next-outline</v-icon>Go to
                </v-btn>
              </template>
              <span>Go to the specific page</span>
            </v-tooltip>

          </v-col>
          <GoToDialog v-model="showGoToDialog" @goToPage="goToPage" />
        </v-row>
      </v-card>

      <!-- TO DO -->
      <!-- <div class="text-h4 mt-10 font-weight-bold">
        <v-icon color="blue" large>mdi-puzzle</v-icon> Conflicts
      </div> -->
      <div class="text-h4 mt-10 font-weight-bold">
        <v-icon color="blue" large>mdi-puzzle</v-icon> Unused strings
      </div>

      <div class="text-center" v-if="isLoading.processing">
        <v-progress-circular indeterminate color="green"></v-progress-circular>
      </div>
      <v-alert v-else-if="!processing || !processing.items || processing.items.length == 0" type="info" border="left"
        colored-border color="info" class="mt-6" elevation="2">
        Please, wait. Alignment is in progress.
      </v-alert>
      <div v-else>

        <!-- TO DO -->
        <!-- <v-alert type="info" border="left" colored-border color="info" class="mt-6" elevation="2">
          To proceed to the next batch all conflicts need to be resolved. Lines without identifiers are not considered
          during the conflicts detection.
        </v-alert>

        <div class="text-h5 mt-10 font-weight-bold">Flow breaks</div>

        <v-alert v-if="!flowBreakGroups || flowBreakGroups.length==0" type="info" border="left" colored-border color="info"
          class="mt-6" elevation="2">
          No unhandled flow breaks detected.
        </v-alert>
        <div class="mt-6">
          <v-card>
            <div class="blue lighten-5" dark>

              <v-card-title class="pr-3">
                <v-spacer></v-spacer>

                <v-icon>mdi-translate</v-icon>
                <v-switch value="true" v-model="showProxyTo" class="mx-2"></v-switch>

                <v-btn icon @click="collapseEditItems">
                  <v-icon>mdi-collapse-all</v-icon>
                </v-btn>
              </v-card-title>
            </div>
            <v-divider></v-divider>

            <div v-for="(group,i) in flowBreakGroups" :key="i">
              <div class="pa-3 blue lighten-5 font-weight-bold text-caption">conflict on line {{group['lineId']}}</div>
              <v-divider></v-divider>
              <EditItem @editProcessing="editProcessing" @editAddUpEnd="editAddUpEnd" @editAddDownEnd="editAddDownEnd"
                @editDeleteLine="editDeleteLine" @editAddEmptyLineBefore="editAddEmptyLineBefore"
                @editAddEmptyLineAfter="editAddEmptyLineAfter" @editClearLine="editClearLine"
                @getCandidates="getCandidates" @editAddCandidateEnd="editAddCandidateEnd"
                :item="conflictFlowTo[group['prev']]"
                :prevItem="group['prev'] == 0 ? conflictFlowTo[0] : conflictFlowTo[group['prev']-1]"
                :collapse="triggerCollapseEditItem" :clearCandidates="triggerClearCandidates" :showProxyTo="showProxyTo"
                :panelColor="'blue'">
              </EditItem>
              <v-divider></v-divider>
              <EditItem @editProcessing="editProcessing" @editAddUpEnd="editAddUpEnd" @editAddDownEnd="editAddDownEnd"
                @editDeleteLine="editDeleteLine" @editAddEmptyLineBefore="editAddEmptyLineBefore"
                @editAddEmptyLineAfter="editAddEmptyLineAfter" @editClearLine="editClearLine"
                @getCandidates="getCandidates" @editAddCandidateEnd="editAddCandidateEnd"
                :item="conflictFlowTo[group['curr']]"
                :prevItem="group['curr'] == 0 ? conflictFlowTo[0] : conflictFlowTo[group['curr']-1]"
                :collapse="triggerCollapseEditItem" :clearCandidates="triggerClearCandidates" :showProxyTo="showProxyTo"
                :panelColor="'red'">
              </EditItem>
              <v-divider></v-divider>
            </div>
          </v-card>
        </div> -->

        <!-- <div class="text-h5 mt-10 font-weight-bold">Unused strings</div> -->

        <v-alert v-if="(!unusedFromLines || unusedFromLines.length==0) && (!unusedToLines || unusedToLines.length==0)"
          type="info" border="left" colored-border color="info" class="mt-6" elevation="2">
          All sentences are in use.
        </v-alert>
        <div v-else>
          <v-card v-if="unusedFromLines && unusedFromLines.length > 0" class="mt-6">
            <div class="blue lighten-5">
              <v-card-title>{{LANGUAGES[langCodeFrom].name}}
                <v-spacer></v-spacer>
                <span class="text-button blue--text">show all</span>
                <v-switch value="true" false-value="false" v-model="showAllFrom" class="ml-2"></v-switch>
              </v-card-title>
              <v-card-text>{{unusedFromLines.length}} lines
              </v-card-text>
            </div>
            <v-divider></v-divider>
            <div v-for="(line,i) in unusedFromLines" :key="i">
              <template>
                <div v-show="showAllFrom == 'true' || !conflictSplittedFrom[line].e">
                  <v-row justify="center" no-gutters>
                    <v-col class="text-left" cols="12">
                      <div class="d-table fill-height">
                        <div class="d-table-cell grey lighten-4 pa-2 text-center" style="min-width:45px">
                          {{ line }}
                        </div>
                        <v-divider class="d-table-cell" vertical></v-divider>
                        <div class="d-table-cell pa-2" style="width:100%"
                            :class="[conflictSplittedFrom[line].e ? ['grey','grey--text','lighten-5']:'']">{{ conflictSplittedFrom[line].t}}
                          <div v-if="conflictSplittedFrom[line].p"
                            class="mt-3 proxy-to-subtitles grey lighten-3 font-weight-medium">
                            {{conflictSplittedFrom[line].p}}
                          </div>
                        </div>
                        <v-divider class="d-table-cell" vertical></v-divider>
                        <div class="d-table-cell grey lighten-5 pl-2 pt-2 text-center">
                          <v-checkbox hide-details color="blue" class="ma-1 pa-0" v-model="conflictSplittedFrom[line].e" @click.stop="markUnused('from', line)"></v-checkbox>
                        </div>
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
              <v-card-title>{{LANGUAGES[langCodeTo].name}}
                <v-spacer></v-spacer>
                <span class="text-button blue--text">show all</span>
                <v-switch value="true" v-model="showAllTo" class="ml-2"></v-switch>
              </v-card-title>
              <v-card-text>{{unusedToLines.length}} lines
              </v-card-text>
            </div>
            <v-divider></v-divider>
            <div v-for="(line,i) in unusedToLines" :key="i">
              <template>
                <div v-show="showAllTo == 'true' || !conflictSplittedTo[line].e">
                  <v-row justify="center" no-gutters>
                    <v-col class="text-left" cols="12">
                      <div class="d-table fill-height">
                        <div class="d-table-cell grey lighten-4 pa-2 text-center" style="min-width:45px">
                          {{ line }}
                        </div>
                        <v-divider class="d-table-cell" vertical></v-divider>
                        <div class="d-table-cell pa-2" style="width:100%"
                          :class="[conflictSplittedTo[line].e ? ['grey','grey--text','lighten-5']:'']">{{ conflictSplittedTo[line].t}}
                          <div v-if="conflictSplittedTo[line].p"
                            class="mt-3 proxy-to-subtitles grey lighten-3 font-weight-medium">
                            {{conflictSplittedTo[line].p}}
                          </div>
                        </div>
                        <v-divider class="d-table-cell" vertical></v-divider>
                        <div class="d-table-cell grey lighten-5 pl-2 pt-2 text-center">
                          <v-checkbox hide-details color="blue" class="ma-1 pa-0" v-model="conflictSplittedTo[line].e" @click.stop.prevent="markUnused('to', line)"></v-checkbox>
                        </div>
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

      <div class="text-h4 mt-10 font-weight-bold">
        <v-icon color="blue" large>mdi-cloud-download</v-icon> Corpora
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
        <div class="text-h5 mt-10 font-weight-bold">Corpora in TMX format</div>
        <v-btn class="primary mt-5" @click="downloadProcessingTmx()"><v-icon left color="white">mdi-download</v-icon>Download</v-btn>
      </div>
    </div>
  </div>
</template>

<script>
  import RawPanel from "@/components/RawPanel";
  import DownloadPanel from "@/components/DownloadPanel";
  import SplittedPanel from "@/components/SplittedPanel";
  import InfoPanel from "@/components/InfoPanel";
  import EditItem from "@/components/EditItem";
  import GoToDialog from "@/components/GoToDialog";
  import CreateAlignmentDialog from "@/components/CreateAlignmentDialog"
  import RecalculateBatchDialog from "@/components/RecalculateBatchDialog"
  import ConfirmDeleteDialog from "@/components/ConfirmDeleteDialog"
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
    SettingsHelper
  } from "@/common/settings.helper";
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
    ADD_EMPTY_LINE_AFTER
  } from "@/common/constants"
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
    GET_CONFLICT_SPLITTED_FROM,
    GET_CONFLICT_SPLITTED_TO,
    // GET_CONFLICT_FLOW_TO,
    STOP_ALIGNMENT,
    EDIT_PROCESSING,
    EDIT_PROCESSING_MARK_UNUSED,
    CREATE_ALIGNMENT,
    DELETE_ALIGNMENT,
    ALIGN_SPLITTED,
    DOWNLOAD_SPLITTED,
    DOWNLOAD_PROCESSING,
    RESOLVE_CONFLICTS
  } from "@/store/actions.type";
  import {
    SET_ITEMS_PROCESSING,
    SET_SPLITTED
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
          upload: LanguageHelper.initGeneralBools(),
          uploadProxy: LanguageHelper.initGeneralBools(),
          download: LanguageHelper.initGeneralBools(),
          align: false,
          processing: false,
          processingMeta: false
        },
        triggerCollapseEditItem: false,
        triggerClearCandidates: false,
        userAlignInProgress: false,
        satisfactionEmojis: ['😍', '😄', '😁', '😊', '🙂', '😐', '🙁', '☹️', '😢', '😭'],
        downloadThreshold: 9,
        showProxyTo: SettingsHelper.getShowProxyTo(),
        showAllTo: SettingsHelper.getShowAllTo(),
        showAllFrom: SettingsHelper.getShowAllFrom(),
        selectedListItem: 0,
        currentBatchId: 0,

        //dialogs
        showGoToDialog: false,
        showCreateAlignmentDialog: false,
        showRecalculateBatchDialog: false,
        showConfirmDeleteAlignmentDialog:false,

        //conflicts
        unusedFromLines: [],
        unusedToLines: [],
        // flowBreakGroups: [],
        usedFromLinesSet: new Set(),
        usedToLinesSet: new Set(),
        usedToLinesFlow: [],

        hoverAlignmentIndex: -1,
        hoveredAlignmentItem: {"name": ""},
      };
    },
    methods: {
      getImgUrl(batch_id) {
        return `${API_URL}/static/img/${this.username}/${this.processingMeta.meta.align_guid}.best_${batch_id}.png?rnd=${Math.random()}`;
      },
      prepareUsedToLines() {
        let foo = new Set();
        let bar = [];

        this.docIndex.forEach(function (ix, i) {
          let arr = JSON.parse(ix[3]);
          arr.forEach(to => {
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
          arr.forEach(from => {
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
        // let flowBreaks = new Set();
        // let flowBreakGroups = [];

        if (!this.docIndex) {
          return;
        }
        let lastLine = this.docIndex[this.docIndex.length - 1];
        let lastLineFromIndex = JSON.parse(lastLine[1]);
        let lastLineToIndex = JSON.parse(lastLine[3]);

        //calculate unused lines
        for (let i = 1; i < lastLineFromIndex[0]; i++) {
          if (!this.usedFromLinesSet.has(i)) {
            unusedFromLines.push(i)
          }
        }
        for (let i = 1; i < lastLineToIndex[0]; i++) {
          if (!this.usedToLinesSet.has(i)) {
            unusedToLines.push(i)
          }
        }

        //calculate flow breaks
        // let counter = this.usedToLinesFlow[0][1];
        // this.usedToLinesFlow.forEach(item => {
        //   if (item[1] != counter) {
        //     flowBreaks.add(item[0] - 2);
        //     flowBreaks.add(item[0] - 1);

        //     flowBreakGroups.push({
        //       "lineId": item[0] - 1,
        //       "prev": item[0] - 2,
        //       "curr": item[0] - 1
        //     })
        //     counter = item[1];
        //   }
        //   counter = counter + 1;
        // });

        this.$store
          .dispatch(GET_CONFLICT_SPLITTED_FROM, {
            username: this.$route.params.username,
            ids: JSON.stringify(unusedFromLines),
            align_guid: this.selectedProcessingId,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo
          }).then(() => {
            this.unusedFromLines = unusedFromLines;
          });
        this.$store
          .dispatch(GET_CONFLICT_SPLITTED_TO, {
            username: this.$route.params.username,
            ids: JSON.stringify(unusedToLines),
            align_guid: this.selectedProcessingId,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo
          }).then(() => {
            this.unusedToLines = unusedToLines;
          });
        // this.$store
        //   .dispatch(GET_CONFLICT_FLOW_TO, {
        //     username: this.$route.params.username,
        //     index_ids: JSON.stringify([...flowBreaks]),
        //     align_guid: this.selectedProcessingId,
        //     langCodeFrom: this.langCodeFrom,
        //     langCodeTo: this.langCodeTo
        //   }).then(() => {
        //     this.flowBreakGroups = flowBreakGroups;
        //   });
      },
      createAlignment(name) {
        this.$store
          .dispatch(CREATE_ALIGNMENT, {
            username: this.$route.params.username,
            idFrom: this.selectedIds[this.langCodeFrom],
            idTo: this.selectedIds[this.langCodeTo],
            name: name
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
      startAlignment(batch_id = 0, shift = 0, nextOnly = true) {
        this.isLoading.align = true;
        this.initProcessingDocument();
        this.currentlyProcessingId = this.selectedProcessingId;
        this.userAlignInProgress = true;
        this.$store
          .dispatch(ALIGN_SPLITTED, {
            username: this.$route.params.username,
            id: this.selectedProcessingId,
            nextOnly: nextOnly,
            batchIds: [batch_id],
            batchShift: shift,
            alignAll: ''
          })
          .then(() => {
            this.isLoading.align = false;
            console.log("fetchItemsProcessingTimer set")
            this.fetchItemsProcessingTimer();
          });
      },
      recalculateBatch(batch_id, shift) {
        this.startAlignment(batch_id, shift, false)
      },
      resolveConflictsBatch(batch_id) {
        this.isLoading.align = true;
        this.initProcessingDocument();
        this.currentlyProcessingId = this.selectedProcessingId;
        this.userAlignInProgress = true;
        this.$store
          .dispatch(RESOLVE_CONFLICTS, {
            username: this.$route.params.username,
            id: this.selectedProcessingId,
            batchIds: [batch_id],
            resolveAll: ''
          })
          .then(() => {
            this.isLoading.align = false;
            console.log("fetchItemsProcessingTimer set")
            this.fetchItemsProcessingTimer();
          });        
      },
      fetchItemsProcessingTimer() {
        setTimeout(() => {
          this.$store.dispatch(FETCH_ITEMS_PROCESSING, {
            username: this.$route.params.username,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo
          }).then(() => {
            let in_progress_items = this.itemsProcessing[this.langCodeFrom].filter(x => x.state[0] == 0 || x
              .state[0] == 1)
            if (in_progress_items.length > 0) {
              this.selectCurrentlyProcessingDocument(this.selectedProcessing);
              this.fetchItemsProcessingTimer();
            } else {
              this.userAlignInProgress = false;
              this.isLoading.alignStopping = false;
              let currItem = this.itemsProcessing[this.langCodeFrom].filter(x => x.guid == this
                .currentlyProcessingId)
              if (currItem.length > 0) {
                this.selectCurrentlyProcessingDocument(currItem[0]);
              } else {
                this.selectCurrentlyProcessingDocument(this.selectedProcessing);
              }
            }
          });
        }, 5000)
      },
      initProcessingDocument() {
        let processingItemsCopy = JSON.parse(JSON.stringify(this.itemsProcessing[this.langCodeFrom]));
        let selectedProcessingStateCopy = JSON.parse(JSON.stringify(this.selectedProcessing.state));
        let currentIndex = -1;
        if (this.itemsProcessingNotEmpty(this.langCodeFrom)) {
          currentIndex = processingItemsCopy.findIndex(x => x.guid == this.selectedProcessingId);
        }
        selectedProcessingStateCopy[0] = this.PROC_IN_PROGRESS;
        if (currentIndex >= 0) {
          processingItemsCopy.splice(currentIndex, 1, {
            "imgs": [],
            "name": this.selectedProcessing.name,
            "state": selectedProcessingStateCopy
          });
        } else {
          processingItemsCopy.push({
            "imgs": [],
            "name": this.selectedProcessing.name,
            "state": selectedProcessingStateCopy
          });
        }
        this.$store
          .commit(SET_ITEMS_PROCESSING, {
            items: processingItemsCopy,
            langCode: this.langCodeFrom
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
          page: page
        });
      },
      onProcessingPageChange(page) {
        let num = Math.min(page, this.processing.meta.total_pages)
        this.triggerClearCandidates = !this.triggerClearCandidates;
        this.$store.dispatch(GET_PROCESSING, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          fileId: this.selectedProcessingId,
          linesCount: 10,
          page: num
        });
      },
      uploadFile(langCode) {
        this.isLoading.upload[langCode] = true;
        this.$store.dispatch(UPLOAD_FILES, {
            file: this.files[langCode],
            username: this.$route.params.username,
            langCode
          })
          .then(() => {
            this.$store.dispatch(FETCH_ITEMS, {
              username: this.$route.params.username,
              langCode: langCode
            }).then(() => {
              this.selectFirstDocument(langCode);
              this.isLoading.upload[langCode] = false;
            });
          });
      },
      uploadProxyFile(langCode) {
        this.isLoading.uploadProxy[langCode] = true;
        this.$store
          .dispatch(UPLOAD_FILES, {
            file: this.proxyFiles[langCode],
            username: this.$route.params.username,
            langCode,
            isProxy: true,
            rawFileName: this.selected[langCode]
          })
          .then(() => {
            this.isLoading.uploadProxy[langCode] = false;
          });
      },
      getCandidates(indexId, textType, countBefore, countAfter, callback) {
        this.$store.dispatch(GET_CANDIDATES, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId: indexId,
          fileId: this.selectedProcessingId,
          textType: textType,
          countBefore: countBefore,
          countAfter: countAfter
        }).then(function (response) {
          callback(RESULT_OK, response.data)
        }).catch(() => {
          callback(RESULT_ERROR)
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
          align_guid: this.selectedProcessingId,
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
          align_guid: this.selectedProcessingId,
          fileName: this.selectedProcessingId + ".tmx",
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          langCodeDownload: this.langCodeFrom,
          format: "tmx"
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
          page: 1
        });
      },
      selectProcessing(item, fileId) {
        this.selectedListItem = fileId;
        this.isLoading.processing = true;
        this.isLoading.processingMeta = true;
        this.selectedProcessing = item;
        this.selectedProcessingId = fileId;

        this.$store.dispatch(GET_PROCESSING_META, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          fileId
        }).then(() => {
          this.isLoading.processingMeta = false;
        });

        this.$store.dispatch(GET_DOC_INDEX, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          fileId
        }).then(() => {
          this.$store.dispatch(GET_PROCESSING, {
            username: this.$route.params.username,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo,
            fileId,
            linesCount: 10,
            page: 1
          }).then(() => {
            this.isLoading.processing = false;
          });
        });
      },
      refreshProcessingPage() {
        this.$store.dispatch(GET_PROCESSING, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          fileId: this.selectedProcessingId,
          linesCount: 10,
          page: this.processing.meta.page
        });
      },
      editAddCandidateEnd(indexId, textType, candidateLineId, candidateText, batchId, batchIndexId) {
        let langCode = textType == "from" ? this.langCodeFrom : this.langCodeTo;
        this.$store.dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          candidateLineId: candidateLineId,
          candidateText: this.LANGUAGES[langCode].noSpaceBetweenSentences ? candidateText : " " + candidateText,
          text_type: textType,
          operation: EDIT_ADD_CANDIDATE_END,
          target: "previous"
        }).then(() => {
          this.refreshProcessingPage();
        });
      },
      editAddUpEnd(indexId, editItemText, textType, batchId, batchIndexId) {
        let langCode = textType == "from" ? this.langCodeFrom : this.langCodeTo;
        this.$store.dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          text: this.LANGUAGES[langCode].noSpaceBetweenSentences ? editItemText : " " + editItemText,
          text_type: textType,
          operation: EDIT_ADD_PREV_END,
          target: "previous"
        }).then(() => {
          this.refreshProcessingPage();
        });
      },
      editAddDownEnd(indexId, editItemText, textType, batchId, batchIndexId) {
        let langCode = textType == "from" ? this.langCodeFrom : this.langCodeTo;
        this.$store.dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          text: this.LANGUAGES[langCode].noSpaceBetweenSentences ? editItemText : " " + editItemText,
          text_type: textType,
          operation: EDIT_ADD_NEXT_END,
          target: "next"
        }).then(() => {
          this.refreshProcessingPage();
        });
      },
      editAddEmptyLineBefore(indexId, batchId, batchIndexId) {
        this.$store.dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          operation: ADD_EMPTY_LINE_BEFORE
        }).then(() => {
          this.refreshProcessingPage()
        });
      },
      editAddEmptyLineAfter(indexId, batchId, batchIndexId) {
        this.$store.dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          operation: ADD_EMPTY_LINE_AFTER
        }).then(() => {
          this.refreshProcessingPage()
        });
      },
      editDeleteLine(indexId, batchId, batchIndexId) {
        this.$store.dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          operation: EDIT_DELETE_LINE
        }).then(() => {
          this.refreshProcessingPage()
        });
      },
      editClearLine(indexId, textType, batchId, batchIndexId) {
        this.$store.dispatch(EDIT_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          indexId,
          batchId,
          batchIndexId,
          text_type: textType,
          operation: EDIT_CLEAR_LINE
        }).then(() => {
          this.refreshProcessingPage()
        });
      },
      editProcessing(indexId, editItemText, textType, batchId, batchIndexId, callback) {
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
            operation: EDIT_LINE
          }).then(function () {
            callback(RESULT_OK)
          }).catch(() => {
            callback(RESULT_ERROR)
          });
      },
      markUnused(textType, lineId) {
        this.$store.dispatch(EDIT_PROCESSING_MARK_UNUSED, {
          username: this.$route.params.username,
          guid: this.selectedProcessingId,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          lineId,
          textType
        }).then(() => {
          console.log("Marked as unused")
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
          this.selectAndLoadPreview(langCode, this.items[langCode][0].name, this.items[langCode][0].guid);
        } else {
          let data = {"items": {}, "meta": {}};
          data["items"][langCode] = []
          data["meta"][langCode] = {}
          this.$store.commit(SET_SPLITTED, {
            data,
            langCode
          });
          this.selected[langCode] = null;
        }
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
        this.$store.dispatch(FETCH_ITEMS, {
          username: this.$route.params.username,
          langCode: this.langCodeFrom
        }).then(() => {
          this.selectFirstDocument(this.langCodeFrom);
        });
        this.$store.dispatch(FETCH_ITEMS, {
          username: this.$route.params.username,
          langCode: this.langCodeTo
        }).then(() => {
          this.selectFirstDocument(this.langCodeTo);
        });
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
      },

      //deletion
      performDeleteRawFile(item, langCode) {
        this.$store.dispatch(DELETE_DOCUMENT, {
            username: this.$route.params.username,
            filename: item.name,
            guid: item.guid,
            langCode
          })
          .then(() => {
            this.$store.dispatch(FETCH_ITEMS, {
              username: this.$route.params.username,
              langCode: langCode
            }).then(() => {
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
      docIndex() {
        this.updateUnusedLines();
      }
    },
    computed: {
      ...mapGetters(["items", "itemsProcessing", "splitted", "processing", "docIndex", "conflictSplittedFrom",
        "conflictSplittedTo", "conflictFlowTo", "processingMeta"
      ]),
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
      EditItem,
      RawPanel,
      DownloadPanel,
      SplittedPanel,
      InfoPanel,
      GoToDialog,
      CreateAlignmentDialog,
      RecalculateBatchDialog,
      ConfirmDeleteDialog
    }
  };
</script>
