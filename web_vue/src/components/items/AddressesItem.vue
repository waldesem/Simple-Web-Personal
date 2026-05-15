<script setup lang="ts">
import { PropType } from "vue";
import type { Address, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    required: true,
  },
  fields: {
    type: Array as PropType<ItemField[]>,
    required: true,
  },
});
</script>

<template>
  <ItemCard :fields="props.fields" :item="props.item" />
</template>
