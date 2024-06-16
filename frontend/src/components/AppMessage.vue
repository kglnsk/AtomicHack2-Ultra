<template>
  <div class="message" :class="{ 'message--user': props.type === 'user' }">
    <div class="message__icon">
      <a-avatar v-if="props.type === 'bot'" :src="RoastomLogo" style="color: #f56a00; background-color: #fde3cf">
      </a-avatar>
      <a-avatar v-if="props.type === 'user'" style="color: #f56a00; background-color: #fde3cf">U</a-avatar>
    </div>
    <div class="message__answer" v-if="props.type === 'user'">
      <span class="message__text">{{ props.instruction }}</span>
    </div>

    <div class="message__answer message__answer--bot" v-if="props.type === 'bot'">
      <span class="message__text">{{ props.instruction }}</span>
      <template v-if="props.questions">
        <a-divider style="background-color: #fff; height: 2px; margin: 1rem 0"/>
        <h4>Похожие вопросы</h4>
        <a-collapse v-model:activeKey="activeKey" accordion :bordered="false" style="background: rgb(255, 255, 255)">
          <a-collapse-panel v-for="(question, idx) in props.questions" :key="idx" :header="question.question">
            <p>
              {{ question.answer }}
            </p>
          </a-collapse-panel>
        </a-collapse>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import RoastomLogo from '../assets/img/rosatom_logo.png?url'
type TProps = {
  instruction: string
  type: 'user' | 'bot'
  questions?: {question: string, answer: string}[]
}

const props = defineProps<TProps>()

const activeKey = ref()

</script>

<style lang="scss">
.message {
  display: flex;
  align-items: start;
  gap: 0.5rem;
  max-width: 80%;

  &--user {
    flex-direction: row-reverse;
  }

  &__answer {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #0057b8;

    h4 {
      display: block;
      text-align: center;
      color: #fff;
      margin-bottom: 1rem;
    }
  }

  &__text {
    display: block;
    color: #fff;
    line-height: 1.25rem;
  }
}
</style>
