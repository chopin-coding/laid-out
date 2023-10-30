<script setup lang="ts">

</script>

<template>
<Transition appear mode="out-in">
  <slot></slot>
</Transition>
</template>

<style scoped>
.v-enter-active {
  transition: opacity 0.3s ease-out;
  animation: grow-in 0.3s;
}

.v-leave-active {
  transition: opacity 0.15s ease-out;
  animation: grow-in 0.15s reverse;
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