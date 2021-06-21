<template>
  <div>
    <div v-for="(item, i) in contents" :key="i">
      <div><router-link :to="{ name: 'items', params: { username: item[0], from: item[1], to: item[2] } }">{{item[0]}} - {{item[4]}}</router-link></div>
    </div>
    <!-- <div class="mt-10">{{contents}}</div>     -->
  </div>
</template>

<script>
import { GET_CONTENTS } from "@/store/actions.type";
import {
    mapGetters
  } from "vuex";

export default {
  data() {
    return {
      // username: null
    };
  },
  mounted() {
      this.$store.dispatch(GET_CONTENTS);
    },
  methods: {
    // onSubmit: function(username) {
    //   this.$store
    //     .dispatch(LOGIN, {
    //       username
    //     })
    //     .then(() =>
    //       this.$router.push({
    //         path: `/user/${username}`
    //       })
    //     );
    // }
    // goToAlignment(username){

    // }
  },
  computed: {
      ...mapGetters(["contents"])
  }
};
</script>
