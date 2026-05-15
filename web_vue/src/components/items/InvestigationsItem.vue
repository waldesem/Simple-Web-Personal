<script setup lang="ts">
import { computed, PropType } from "vue";
import { localStr } from "@/utils";
import type { Inquisition, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    required: true,
  },
  fields: {
    type: Array as PropType<ItemField[]>,
    required: true,
  },
});

const investigation = computed(() => {
  return {
    ...props.item,
    created: localStr(props.item.created),
  };
});
</script>

<template>
  <ItemCard :fields="props.fields" :item="investigation" />
</template>
