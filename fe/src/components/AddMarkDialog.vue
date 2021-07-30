<template>
  <v-dialog v-model="show" max-width="800px">
    <v-card>
      <v-card-title> Add new mark </v-card-title>
      <!-- <v-row class="ma-0 mt-5">
        <v-col cols="12" sm="6">
          <v-card flat>
            <v-card-title class="justify-center pa-0">{{
              langFrom
            }}</v-card-title>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6">
          <v-card flat>
            <v-card-title class="justify-center pa-0">{{
              langTo
            }}</v-card-title>
          </v-card>
        </v-col>
      </v-row> -->
      <!-- MARK TYPE -->
      <v-row class="ma-0 mt-5 px-7">
        <v-col class="pa-0" cols="12" sm="12">
          <v-card flat>
            <v-card-text class="mt-0 pa-0">
              <v-select
              v-model="markItem"
              :items="markTypes"
              item-text="name"
              item-value="type"
              label="Type"></v-select>
              <v-text-field
                label="Paragraph"
                type="number"
                v-model="parId"
                v-on:keyup.enter="addMark"
              >
              </v-text-field>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row class="ma-0 mt-5">
        <v-col cols="12" sm="6">
          <v-card flat>
            <v-card-title class="justify-center pa-0">{{
              langFrom
            }}</v-card-title>
            <v-card-text class="mt-0 pt-0">
              <v-text-field
                label="Value"
                v-model="valueFrom"
                v-on:keyup.enter="addMark"
              >
              </v-text-field>
              <!-- <v-text-field
                label="Paragraph"
                type="number"
                v-model="name"
                v-on:keyup.enter="addMark"
              >
              </v-text-field> -->
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6">
          <v-card flat>
            <v-card-title class="justify-center pa-0">{{
              langTo
            }}</v-card-title>
            <v-card-text class="mt-0 pt-0">
              <v-text-field
                label="Value"
                v-model="valueTo"
                v-on:keyup.enter="addMark"
              >
              </v-text-field>
              <!-- <v-text-field
                label="Paragraph"
                type="number"
                v-model="name"
                v-on:keyup.enter="addMark"
              >
              </v-text-field> -->
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-card-actions>
        <v-btn color="primary" text @click="show = false"> Close </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" dark width="120px" @click="addMark"> Add </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { MARK_NAMES } from "@/common/helper";
export default {
  name: "AddMarkDialog",
  props: {
    value: Boolean,
    langFrom: String,
    langTo: String,
  },
  data() {
    return {
      markTypes: MARK_NAMES,
      valueFrom: "",
      valueTo: "",
      parId: "",
      markItem: MARK_NAMES[0].type
    };
  },
  methods: {
    addMark() {
      if (this.valueFrom != "" && this.valueTo != "" && this.parId != "") {
        this.show = false;
        this.$emit("addMark", this.markItem, this.valueFrom, this.valueTo, this.parId - 1, this.parId - 1);
      } else {
        alert("Please, fill the whole form");
      }
    },
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
};
</script>
