<template>
  <v-alert
    type="info"
    border="left"
    colored-border
    color="blue"
    class="mt-6"
    elevation="2"
    v-if="!selected[side][info.langCode]"
  >
    Select file to align.
  </v-alert>
  <v-card v-else>
    <div class="yellow lighten-5">
      <v-card-title>{{ selected[side][info.langCode] }}</v-card-title>
      <v-card-text
        >{{
          splitted[side][info.langCode].meta.lines_count | separator
        }}
        lines</v-card-text
      >
    </div>
    <v-divider></v-divider>
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <tr>
            <td>File</td>
            <td>{{ selected[side][info.langCode] }}</td>
          </tr>
          <tr>
            <td>Lines</td>
            <td>
              {{ splitted[side][info.langCode].meta.lines_count | separator }}
            </td>
          </tr>
          <tr>
            <td>Symbols</td>
            <td>
              {{ splitted[side][info.langCode].meta.symbols_count | separator }}
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-card>
</template>

<script>
export default {
  name: "InfoPanel",
  props: ["info", "splitted", "selected", "side"],
};
</script>
