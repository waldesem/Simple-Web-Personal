<script setup lang="ts">
import { computed, PropType } from "vue";
import { decisions, localDateStr } from "@/utils";
import type { ItemField, Pfo } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    required: true,
  },
});

const fields = [
  { key: "theme", label: "Тема проверки" },
  { key: "results", label: "Результаты" },
  { key: "conclusion", label: "Заключение", slot: true },
  { key: "created", label: "Дата записи" },
] as ItemField[];

const pfo = computed(() => {
  return {
    ...props.item,
    created: localDateStr(props.item.created),
  };
});
</script>

<template>
  <ItemCard :fields="fields" :item="pfo">
    <template #conclusion v-if="props.item.conclusion">
      <UBadge
        :color="
          props.item.conclusion === decisions.agreed
            ? 'success'
            : props.item.conclusion === decisions.comments
              ? 'warning'
              : props.item.conclusion === decisions.cancel
                ? 'neutral'
                : 'error'
        "
        :label="props.item.conclusion"
      />
    </template>
  </ItemCard>
</template>
