<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card>
      <v-card-title>
        Please, confirm
      </v-card-title>
      <v-card-text class="text-body-1 mt-2">Do you realy want do delete <span class="font-weight-bold">{{this.itemName}}</span>?</v-card-text>
      <v-card-actions class="mt-5">
        <v-btn color="primary" text @click="show=false">
          Close
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="red" dark @click="confirmDelete">
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    name: "ConfirmDeleteDialog",
    props: {
      value: Boolean,
      itemName: String
    },
    data() {
      return {
      }
    },
    methods: {
      confirmDelete() {
        this.show = false;
        this.$emit('confirmDelete')
      },
    },
    computed: {
      show: {
        get() {
          return this.value
        },
        set(value) {
          this.$emit('input', value)
        }
      }
    }
  }
</script>
