<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card>
      <v-card-title> Edit mark for {{lang}} language</v-card-title>
      <v-row class="ma-0 mt-5 px-7">
        <v-col class="pa-0" cols="12" sm="12">
          <v-card flat>
            <v-card-text class="mt-0 pa-0">
              <v-text-field
                label="Paragraph"
                type="number"
                v-model="parId"
                v-on:keyup.enter="editMark"
                disabled
              >
              </v-text-field>
              <v-text-field
                label="Value"
                v-model="markValue"
                v-on:keyup.enter="editMark"
              >
              </v-text-field>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-card-actions class="mt-10">
        <v-btn color="primary" text @click="show = false"> Close </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" dark width="120px" @click="editMark"> Save </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "EditMarkDialog",
  props: {
    value: Boolean,
    lang: String,
    direction: String,
    mark: Array
  },
  data() {
    return {
      markValue: "",
      parId: ""
    };
  },
  methods: {
    editMark() {
      if (this.markValue != "" && this.parId != "") {
        this.show = false;
        this.$emit("editMark", this.mark, "edit", this.direction, this.markValue, this.parId - 1);
      } else {
        alert("Please, fill the whole form");
      }
    },
    init(mark) {
      this.markValue = mark[0];
      this.parId = mark[3] + 1;
    }
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
  }
};
</script>
