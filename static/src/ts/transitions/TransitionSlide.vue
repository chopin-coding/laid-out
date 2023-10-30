<script setup lang="ts"></script>

<template>
  <Transition appear name="slide-fade">
    <slot></slot>
  </Transition>
</template>

<style scoped>
.slide-fade-enter-active {
  transition: all 150ms ease-out;
}

.slide-fade-leave-active {
  transition: all 150ms ease-out;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(-40px);
  opacity: 0;
}
</style>