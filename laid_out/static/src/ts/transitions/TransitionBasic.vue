<script setup lang="ts">

</script>

<template>
<Transition appear mode="out-in">
  <slot></slot>
</Transition>
</template>

<style scoped>
.v-enter-active {
  transition: opacity 100ms ease-out;
}

.v-leave-active {
  transition: opacity 90ms ease-out;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

@keyframes grow-in {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}
</style>
