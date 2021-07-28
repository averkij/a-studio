<template>
  <div class="d-table fill-height">              
    <div class="d-table-cell grey lighten-4 pa-2 text-center" style="min-width:45px">
      {{ id+1 }}
    </div>
    <v-divider class="d-table-cell" vertical></v-divider>
    <div class="d-table-cell pa-2" style="width: 100%" :class="{'mark-title': mark[2]=='author' || mark[2]=='title', 'break-all': mark[2]=='image'}">
      <v-chip class="mx-1" small label :class="{
        'green': mark[2]=='author' || mark[2]=='title',
        'teal': mark[2] == 'h1',
        'cyan': mark[2] == 'h2',
        'lime': mark[2] == 'h3' || mark[2] == 'h4' || mark[2] == 'h5',
        'pr-5': mark[2] == 'h2' || mark[2] == 'h3' || mark[2] == 'h4' || mark[2] == 'h5',
        'purple': mark[2] == 'qtext' || mark[2] == 'qname',
        'orange': mark[2] == 'image' || mark[2] == 'divider'
        }"
        text-color="white">{{mark[2]}}</v-chip>
        {{mark[0]}}
    </div>
    <v-divider v-if="showParId" class="d-table-cell" vertical></v-divider>
    <div v-if="showParId" class="d-table-cell pa-2" style="min-width:60px; text-align:center;">
      {{mark[3]}}
    </div>
  </div>
</template>

<script>
  export default {
    name: "MarkItem",
    props: ["mark", "id", "showParId"]
  };
</script>
