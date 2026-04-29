<script setup lang="ts">
import { PropType } from "vue";
import { Conclusions, localStr } from "@/utils";
import type { Verification } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Проверка по местам работы" :value="props.item.workplace" />
  <LabelValue label="Проверка документов" :value="props.item.document" />
  <LabelValue label="Проверка задолженностей" :value="props.item.debt" />
  <LabelValue label="Проверка банкротства" :value="props.item.bankruptcy" />
  <LabelValue label="Проверка по БКИ" :value="props.item.bki" />
  <LabelValue label="Проверка судебных решений" :value="props.item.courts" />
  <LabelValue
    label="Проверка аффилированности"
    :value="props.item.affilation"
  />
  <LabelValue
    label="Проверка списка террористов"
    :value="props.item.terrorist"
  />
  <LabelValue
    label="Проверка в открытых источниках"
    :value="props.item.internet"
  />
  <LabelValue label="Проверка Кронос" :value="props.item.cronos" />
  <LabelValue label="Дополнительная информация" :value="props.item.addition" />
  <LabelValue label="Комментарии" :value="props.item.comment" />
  <LabelSlot v-if="props.item.conclusion" label="Результат">
    <UBadge
      :color="
        props.item.conclusion === Conclusions.agreed
          ? 'success'
          : props.item.conclusion === Conclusions.comments
            ? 'warning'
            : props.item.conclusion === Conclusions.cancel
              ? 'neutral'
              : 'error'
      "
      :label="props.item.conclusion"
    />
  </LabelSlot>
  <LabelValue label="Дата записи" :value="localStr(props.item.created)" />
</template>
