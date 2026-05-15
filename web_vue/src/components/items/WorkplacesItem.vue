<script setup lang="ts">
import { computed, PropType } from "vue";
import { localStr } from "@/utils";
import type { ItemField, Work } from "@/types";
import ItemCard from "../element/ItemCard.vue";

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    required: true,
  },
  fields: {
    type: Array as PropType<ItemField[]>,
    required: true,
  },
});

const work = computed(() => {
  return {
    ...props.item,
    nowWork: props.item.finished ? "Нет" : "Да",
    starts: localStr(props.item.starts),
    finished: localStr(props.item.finished),
  };
});
</script>

<template>
  <ItemCard :fields="props.fields" :item="work" />
</template>
