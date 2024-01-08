<script setup lang="ts">
import {computed, onMounted, ref} from 'vue';
import {sprite} from './sprite';
import {actions} from "./actions";
import {Action, Sprite} from "./models";


interface CharacterAnimationProps {
  character: string;
}

let props = defineProps<CharacterAnimationProps>();


const allActions: Action[] = actions[props.character]
let characterSprite: Sprite;
const characterAnimation = ref(null);
const width = 480;
const height = 320;
const scaleFactor = 0.3;
let tickCount = 0;
let currentAction: Action = actions[props.character][0]

// Function to choose a random action based on probabilities and multipliers
function chooseRandomAction(actionsList: Action[]): Action {
  // Calculate the total sum of probabilities with multipliers
  const totalProbability = actionsList.reduce((sum, action) => sum + action.probabilityMultiplier, 0);

  // Generate a random value between 0 and the total sum of probabilities
  const randomValue = Math.random() * totalProbability;

  // Initialize cumulative probability
  let cumulativeProbability = 0;

  // Iterate through actions and choose the one with the corresponding probability
  let selectedAction: Action;
  for (const action of actionsList) {
    cumulativeProbability += action.probabilityMultiplier;
    if (randomValue <= cumulativeProbability) {
      selectedAction = action;
      break;
    }
  }
  return selectedAction;
}

function animate() {
  requestAnimationFrame(animate)
  tickCount++;
  if (tickCount >= currentAction.ticksPerFrame * currentAction.numberOfFrames) {
    tickCount = 0
    currentAction = chooseRandomAction(allActions)

    characterSprite = sprite({
      context: characterAnimation.value.getContext("2d"),
      width,
      height,
      image: document.getElementById(`${props.character}_${currentAction.name}`),
      action: currentAction,
    });
  }

  characterSprite.update()
  characterSprite.render()
}

onMounted(() => {
  characterAnimation.value.width = width;
  characterAnimation.value.height = height;

  // initiate with the base animation
  characterSprite = sprite({
    context: characterAnimation.value.getContext("2d"),
    width,
    height,
    image: document.getElementById(`${props.character}_${currentAction.name}`),
    action: currentAction,
  });
  animate()
});
</script>

<template>
  <canvas
      id="myCanvas"
      ref="characterAnimation"
      class="z-10"
      :style="{ height: `${height * scaleFactor}px`,
      width: `${width * scaleFactor}px`
  }"
  ></canvas>
</template>

<style scoped>
</style>
