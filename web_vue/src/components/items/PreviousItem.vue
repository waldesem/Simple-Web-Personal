<script setup lang="ts">
import type { Previous } from "@/types";
import { PropType } from "vue";

const props = defineProps({
  item: {
    type: Object as PropType<Previous>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Фамилия" :value="props.item.surname" />
  <LabelValue label="Имя" :value="props.item.firstname" />
  <LabelValue
    v-if="props.item.patronymic"
    label="Отчество"
    :value="props.item.patronymic"
  />
  <LabelValue
    v-if="props.item.changed"
    label="Год изменения"
    :value="props.item.changed"
  />
  <LabelValue
    v-if="props.item.reason"
    label="Причина"
    :value="props.item.reason"
  />
</template>
