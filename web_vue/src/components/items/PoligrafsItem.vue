<script setup lang="ts">
import { computed, PropType } from "vue";
import { decisions, localStr } from "@/utils";
import type { ItemField, Pfo } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    required: true,
  },
  fields: {
    type: Array as PropType<ItemField[]>,
    required: true,
  },
});

const pfo = computed(() => {
  return {
    ...props.item,
    created: localStr(props.item.created),
  };
});

const color = computed(() => {
  switch (props.item.conclusion) {
    case decisions.agreed:
      return "success";
    case decisions.comments:
      return "warning";
    case decisions.cancel:
      return "neutral";
    default:
      return "error";
  }
});
</script>

<template>
  <ItemCard :fields="props.fields" :item="pfo">
    <template #conclusion>
      <UBadge :color="color" :label="props.item.conclusion" />
    </template>
  </ItemCard>
</template>
