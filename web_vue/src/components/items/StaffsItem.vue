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
  { key: "position", label: "Должность" },
  { key: "department", label: "Департамент" },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" :item="props.item" />
</template>
