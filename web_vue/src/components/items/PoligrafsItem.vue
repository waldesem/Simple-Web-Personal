<script setup lang="ts">
import { PropType } from "vue";
import { Decisions, localStr } from "@/utils";
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
  <LabelValue label="Заключение">
    <UBadge
      :color="
        props.item.conclusion === Decisions.agreed
          ? 'success'
          : props.item.conclusion === Decisions.comments
            ? 'warning'
            : props.item.conclusion === Decisions.cancel
              ? 'neutral'
              : 'error'
      "
      :label="props.item.conclusion"
    />
  </LabelValue>
  <LabelValue label="Дата записи">
    {{ localStr(props.item.created) }}
  </LabelValue>
</template>
