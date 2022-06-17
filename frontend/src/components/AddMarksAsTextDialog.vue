<template>
  <v-dialog v-model="show" max-width="800px">
    <v-card>
      <v-card-title> Add multiple image marks </v-card-title>
      <!-- MARK TYPE -->
      <v-row class="ma-0 mt-3 px-7">
        <v-col class="pa-0" cols="12" sm="12">
          <v-card flat>
            <v-card-text class="mt-0 mb-5 pa-0"
              >Line format: <span>image_url, paragraph_id, comment</span>. One
              image info per line. Images should be paired (amount of images
              should be even).
            </v-card-text>
            <v-card-text class="mt-0 mb-5 pa-0">
              <v-textarea
                type="number"
                v-model="rawInfo"
                v-on:keyup.enter="addMark"
                class="ta-custom"
                auto-grow
                rows="5"
                text-wrap
                placeholder="image_url, paragraph_id, comment"
              >
              </v-textarea>
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
export default {
  name: "AddMarksAsTextDialog",
  props: {
    value: Boolean,
    langFrom: String,
    langTo: String,
  },
  data() {
    return {
      rawInfo: "",
    };
  },
  methods: {
    addMark() {
      if (this.rawInfo != "") {
        this.show = false;
        this.$emit("addMark", this.rawInfo);
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
