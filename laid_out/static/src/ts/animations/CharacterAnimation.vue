<script setup lang="ts">
import {onMounted, ref, nextTick} from 'vue';
import {sprite} from './sprite';
import {actions} from "./actions";
import {Action, Sprite} from "./models";
import TransitionOutInGrow from "../transitions/TransitionOutInGrow.vue";


interface CharacterAnimationProps {
  character: string;
}

let props = defineProps<CharacterAnimationProps>();


const allActions: Action[] = actions[props.character]
let characterSprite: Sprite;
const characterAnimation = ref(null);
const showCat = ref(true);
const width = 480;
const height = 320;
const scaleFactor = 0.3;
let tickCount = 0;
let currentAction: Action = actions[props.character][0]
let lastShowCatTimestamp: number = 0;

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
  if (showCat.value) {
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

}

async function showCatHandler() {
  const currentTimestamp = Date.now();

  if (currentTimestamp - lastShowCatTimestamp < 200) {
    // Ignore the call if it's made within 200ms of the last call
    return;
  }

  lastShowCatTimestamp = currentTimestamp;

  showCat.value = !showCat.value
  await nextTick()
  if (showCat.value) {
    // characterAnimation is null without the timeout below :/
    await new Promise(r => setTimeout(r, 200));
    initStuff()
  }
}

function initStuff() {
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
}

onMounted(() => {
  initStuff()
});
</script>

<template>
  <div class="flex items-end gap-x-4 mb-[1px]">
    <div>
      <button v-on:click="showCatHandler"
              class="max-w-full bg-white justify-around gap-x-3 rounded px-3 py-2 mb-3 ring-1 ring-opacity-5 transition duration-100 ease-out primaryAction ring-primarylight text-textblackdim hover:bg-primarylight hover:text-black focus:outline-none">
        Toggle cat
      </button>
    </div>
    <TransitionOutInGrow>
      <canvas v-if="showCat"
              id="myCanvas"
              ref="characterAnimation"
              class="z-10 transition ease-out duration-300"
              :style="{ height: `${height * scaleFactor}px`,
      width: `${width * scaleFactor}px`
  }"
      ></canvas>
      <div v-else-if="!showCat" :style="{ height: `${height * scaleFactor}px`,
      width: `${width * scaleFactor}px`}">
      </div>
    </TransitionOutInGrow>


  </div>

</template>

<style scoped>
</style>
