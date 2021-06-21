<template>
  <div>
    <v-row justify="center" no-gutters>
      <v-col class="text-left" cols="12">
        <div class="d-table fill-height">
          <div class="d-table-cell grey lighten-4 pa-2 text-center" style="min-width:45px">
            {{ item[1] }}
          </div>
          <v-divider class="d-table-cell" vertical></v-divider>
          <div class="d-table-cell break-word pa-2" :class="{'font-weight-bold': item[0].au || item[0].ti || item[0].h1 || item[0].h2 || item[0].h3 || item[0].h4 || item[0].h5}">{{ item[0].text }}
            <v-chip v-if="item[0].au" class="ml-2" small label color="green" text-color="white">author</v-chip>
            <v-chip v-if="item[0].ti" class="ml-2" small label color="green" text-color="white">title</v-chip>
            <v-chip v-if="item[0].pa" class="ml-2" small label color="blue" text-color="white">paragraph</v-chip>
            <v-chip v-if="item[0].h1" class="ml-2" small label color="teal" text-color="white">h1</v-chip>
            <v-chip v-if="item[0].h2" class="ml-2" small label color="cyan" text-color="white">h2</v-chip>
            <v-chip v-if="item[0].h3" class="ml-2" small label color="lime" text-color="white">h3</v-chip>
            <v-chip v-if="item[0].h4" class="ml-2" small label color="lime" text-color="white">h4</v-chip>
            <v-chip v-if="item[0].h5" class="ml-2" small label color="lime" text-color="white">h5</v-chip>
            <v-chip v-if="item[0].qt" class="ml-2" small label color="purple" text-color="white">qtext</v-chip>
            <v-chip v-if="item[0].qn" class="ml-2" small label color="purple" text-color="white">qname</v-chip>
            <v-chip v-if="item[0].im" class="ml-2" small label color="orange" text-color="white">image</v-chip>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  export default {
    name: "PreviewItem",
    props: ["item"]
  };
</script>
