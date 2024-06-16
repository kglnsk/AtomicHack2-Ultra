<template>
  <div class="chat">
    <div class="chat__restore" v-if="isRestoringChat">
      <a-button type="primary" @click="restoreChat">Восстановить чат</a-button>
      <a-button @click="startNewChat">Начать новый чат</a-button>
    </div>
    <div class="chat__body" ref="chatBodyRef">
      <h3 v-if="!messages.length" style="display: block; text-align: center; color: rgb(51, 51, 51);">Задайте свой первый вопрос</h3>
      <div class="chat__body-message"
        :style="{ 'justify-content': message.type === 'user' ? 'flex-end' : 'flex-start' }" v-for="message in messages"
        :key="message.id">
        <AppMessage :instruction="message.instruction" :type="message.type" :questions="message.questions" />
      </div>
    </div>

    <div class="chat__input">
      <transition>
        <span class="chat__input--loading" v-if="isLoading">Росатом бот обрабатывает ваш вопрос ...</span>
      </transition>
      <a-input-search v-model:value="userInput" :disabled="isLoading" placeholder="Задайте вопрос" size="large"
        @search="sendMessage">
        <template #enterButton>
          <a-button style="background-color: #0057b8; color: #fff"
            :style="{ 'background-color': !userInput.length ? '#ccc' : '#0057b8' }" :disabled="!userInput.length"
            size="large" :loading="isLoading">Отправить</a-button>
        </template>
      </a-input-search>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onBeforeMount, ref, watch } from 'vue'
import AppMessage from './AppMessage.vue'
import axios from 'axios';
import { notification } from 'ant-design-vue';

const userInput = ref('')
const chatBodyRef = ref<null | HTMLDivElement>(null)

const isLoading = ref(false)

const isRestoringChat = ref(false)
const messagesFromStore = ref([])

const messages = ref<
  {
    id: number
    instruction: string
    type: 'user' | 'bot'
    questions?: { question: string; answer: string }[]
  }[]
>([])


const restoreChat = () => {
  messages.value = messagesFromStore.value
  isRestoringChat.value = false
}

const startNewChat = () => {
  messages.value = []
  isRestoringChat.value = false
}


const sendMessage = async (val: any) => {
  if (!val.length) return

  messages.value.push({
    id: messages.value.length + 1,
    instruction: val,
    type: 'user'
  })
  isLoading.value = true


  try {
    const { data } = await axios.post('https://endless-presently-basilisk.ngrok-free.app/api/answer_question/', { text: val })

    userInput.value = ''
    if (data) {
      messages.value.push({
        id: messages.value.length + 1,
        instruction: data.instruction,
        type: 'bot',
        questions: data.questions
      })
    }
  } catch (error) {
    console.log('error', error)
    notification.error({
      message: 'При запросе произошла ошибка',
      duration: 3.5,
    });
  } finally {
    isLoading.value = false
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    const chatBody = chatBodyRef.value
    if (chatBody) {
      chatBody.scrollTop = chatBody.scrollHeight
    }
  })
}

watch(
  () => [...messages.value],
  (val) => {
    scrollToBottom()

    localStorage.setItem('chat_messages', JSON.stringify(val))
  }
)

onBeforeMount(() => {
  scrollToBottom()

  messagesFromStore.value = JSON.parse(localStorage.getItem('chat_messages') || '[]')
  if (messagesFromStore.value.length > 0) {
    isRestoringChat.value = true
  }
})



</script>

<style lang="scss">
.chat {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;

  &__restore {
    position: fixed;
    left: 0;
    top: 60px;
    width: 100vw;
    height: 100vh;
    background-color: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    z-index: 100;
  }

  &__body {
    position: relative;
    padding: 1rem;
    height: calc(100%);
    overflow: auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;

    &-message {
      display: flex;
      align-items: center;
    }
  }

  &__input {
    width: 100%;
    padding: 1rem;

    &--loading {
      display: block;
      margin-bottom: 1rem;
      color: rgb(166, 164, 164);
    }
  }
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
