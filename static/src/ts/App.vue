<script setup lang="ts">
import Counter from "./Counter.vue";
</script>

<template>
  <h1>{{ message }}</h1>
  <Counter />
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  components: { Counter },
  data() {
    return {
      message: "Hi from App.vue!",
    };
  },
});
</script>
