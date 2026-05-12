<script setup lang="ts">
import { PropType } from "vue";
import type { ItemField, Staff } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Staff>,
    required: true,
  },
});

const fields = [
  { key: "position", label: "Должность", value: props.item.position },
  { key: "department", label: "Департамент", value: props.item.department },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" />
</template>
