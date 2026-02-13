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
  <LabelValue label="Отчество" :value="props.item.patronymic" />
  <LabelValue label="Год изменения" :value="props.item.changed" />
  <LabelValue label="Причина" :value="props.item.reason" />
</template>
