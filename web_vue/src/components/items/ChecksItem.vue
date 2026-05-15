<script setup lang="ts">
import { computed, PropType } from "vue";
import { conclusions, localStr } from "@/utils";
import type { ItemField, Verification } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    required: true,
  },
  fields: {
    type: Array as PropType<ItemField[]>,
    required: true,
  },
});

const check = computed(() => {
  return {
    ...props.item,
    created: localStr(props.item.created),
  };
});

const color = computed(() => {
  switch (props.item.conclusion) {
    case conclusions.agreed:
      return "success";
    case conclusions.comments:
      return "warning";
    case conclusions.denied:
      return "error";
    default:
      return "neutral";
  }
});
</script>

<template>
  <ItemCard :fields="props.fields" :item="check">
    <template #conclusion>
      <UBadge :color="color" :label="props.item.conclusion" />
    </template>
  </ItemCard>
</template>
