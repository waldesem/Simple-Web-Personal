<script setup lang="ts">
import { PropType } from "vue";
import type { Education } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Уровень образования" :value="props.item.view" />
  <LabelValue label="Учебное заведение" :value="props.item.institution" />
  <LabelValue label="Год окончания" :value="props.item.finished" />
  <LabelValue label="Специальность" :value="props.item.specialty" />
</template>
