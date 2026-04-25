<script setup lang="ts">
import type { Verification } from "@/types";
import { Conclusions } from "../../types";
import { PropType } from "vue";

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    required: true,
  },
});
</script>

<template>
  <LabelValue
    v-if="props.item.workplace"
    label="Проверка по местам работы"
    :value="props.item.workplace"
  />
  <LabelValue
    v-if="props.item.document"
    label="Проверка документов"
    :value="props.item.document"
  />
  <LabelValue
    v-if="props.item.debt"
    label="Проверка задолженностей"
    :value="props.item.debt"
  />
  <LabelValue
    v-if="props.item.bankruptcy"
    label="Проверка банкротства"
    :value="props.item.bankruptcy"
  />
  <LabelValue
    v-if="props.item.bki"
    label="Проверка по БКИ"
    :value="props.item.bki"
  />
  <LabelValue
    v-if="props.item.courts"
    label="Проверка судебных решений"
    :value="props.item.courts"
  />
  <LabelValue
    v-if="props.item.affilation"
    label="Проверка аффилированности"
    :value="props.item.affilation"
  />
  <LabelValue
    v-if="props.item.terrorist"
    label="Проверка по списку террористов"
    :value="props.item.terrorist"
  />
  <LabelValue
    v-if="props.item.internet"
    label="Проверка в открытых источниках"
    :value="props.item.internet"
  />
  <LabelValue
    v-if="props.item.cronos"
    label="Проверка Кронос"
    :value="props.item.cronos"
  />
  <LabelValue
    v-if="props.item.addition"
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <LabelValue
    v-if="props.item.comment"
    label="Комментарии"
    :value="props.item.comment"
  />
  <LabelValue label="Результат">
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
  </LabelValue>
  <LabelValue label="Дата записи">
    {{ new Date(props.item.created).toLocaleDateString() }}
  </LabelValue>
</template>
