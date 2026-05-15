<script setup lang="ts">
import { computed, PropType } from "vue";
import { localStr } from "@/utils";
import type { ItemField, Passport } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    required: true,
  },
  fields: {
    type: Array as PropType<ItemField[]>,
    required: true,
  },
});

const doc = computed(() => {
  return {
    ...props.item,
    issue: localStr(props.item.issue),
  };
});
</script>

<template>
  <ItemCard :fields="props.fields" :item="doc" />
</template>
