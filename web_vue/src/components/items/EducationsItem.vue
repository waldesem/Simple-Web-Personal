<script setup lang="ts">
import { PropType } from "vue";
import type { Education, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Уровень образования", value: props.item.view },
  {
    key: "institution",
    label: "Учебное заведение",
    value: props.item.institution,
  },
  { key: "finished", label: "Год окончания", value: props.item.finished },
  { key: "specialty", label: "Специальность", value: props.item.specialty },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" />
</template>
