<script setup lang="ts">
import { computed, PropType } from "vue";
import { localStr } from "@/utils";
import type { ItemField, Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    required: true,
  },
  fields: {
    type: Array as PropType<ItemField[]>,
    required: true,
  },
});

const inquiry = computed(() => {
  return {
    ...props.item,
    created: localStr(props.item.created),
  };
});
</script>

<template>
  <ItemCard :fields="props.fields" :item="inquiry" />
</template>
