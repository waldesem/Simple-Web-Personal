<script setup lang="ts">
import { toRef } from 'vue';

const props = defineProps({
  page: {
    type: Number,
    required: true,
  },
  hasNext: {
    type: Boolean,
    required: true,
  },
  isLoading: {
    type: Boolean,
    required: true,
  },
  limit: {
    type: Number,
    required: true,
  },
  stateLength: {
    type: Number,
    required: true,
  },
});

const limit = toRef(props.limit);

const emits = defineEmits(['next', 'previous', 'limit']);
</script>

<template>
  <div
    v-show="props.stateLength"
    class="flex justify-center border-t border-default pt-8"
  >
    <UButton
      class="me-2 rounded-full"
      :disabled="!props.page || props.isLoading"
      icon="i-lucide-arrow-left"
      title="Вперед"
      @click="emits('previous')"
    />
    <USelect
      v-model="limit"
      :items="[10, 30, 50]"
      title="Количество записей"
      :ui="{
        base: 'w-auto',
      }"
      @change="emits('limit', limit)"
    />
    <UButton
      class="ms-2 rounded-full"
      :disabled="!props.hasNext || props.isLoading"
      icon="i-lucide-arrow-right"
      title="Назад"
      @click="emits('next')"
    />
  </div>
</template>
