<script setup lang="ts">
import { PropType } from "vue";
import { decisions, localDateStr } from "@/utils";
import type { Pfo } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Тема проверки" :value="props.item.theme" />
  <LabelValue label="Результаты" :value="props.item.results" />
  <LabelSlot v-if="props.item.conclusion" label="Заключение">
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
  </LabelSlot>
  <LabelValue label="Дата записи" :value="localDateStr(props.item.created)" />
</template>
