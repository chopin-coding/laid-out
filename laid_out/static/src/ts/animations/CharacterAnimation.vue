<script setup lang="ts">
import {ref, onMounted} from 'vue';
import {sprite} from './sprite';

let characterSprite: Sprite;
const characterAnimation = ref(null);
const width = 480;
const height = 320;

interface Sprite {
  render: Function;
  update: Function;
}

interface Action {
  name: string;
  numberOfFrames: number;
  ticksPerFrame: number;
  loop: boolean;
}

interface CharacterAnimationProps {
  character: string;
  action: Action;

}

let props = defineProps<CharacterAnimationProps>();

function animate() {
  requestAnimationFrame(animate)
  characterSprite.update()
  characterSprite.render()
}

onMounted(() => {
  characterAnimation.value.width = width;
  characterAnimation.value.height = height;
  const characterImage = document.getElementById('myImage');

  characterSprite = sprite({
    context: characterAnimation.value.getContext("2d"),
    width,
    height,
    image: characterImage,
    numberOfFrames: props.action.numberOfFrames,
    ticksPerFrame: props.action.ticksPerFrame,
    loop: props.action.loop,
  });
  characterSprite.render()
  animate()
});
</script>

<template>
  <canvas id="myCanvas" ref="characterAnimation"></canvas>
</template>

<style scoped>
canvas {
  height: 128px;
}
</style>
