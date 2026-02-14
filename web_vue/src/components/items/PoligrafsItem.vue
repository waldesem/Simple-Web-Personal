<script setup lang="ts">
import type { Pfo } from "@/types";
import { Decisions } from "../../types";
import { PropType } from "vue";

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
    {{ new Date(props.item.created).toLocaleDateString() }}
  </LabelValue>
</template>
