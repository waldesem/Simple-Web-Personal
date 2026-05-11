<script setup lang="ts">
import { PropType, ref, toRef, watch } from "vue";
import { conclusions } from "@/utils";
import type { FormField, Verification } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    default: () => ({}),
  },
});

const form = toRef(props.item);

// Переключатель для автоматического заполнения полей по умолчанию
const noNegative = ref(false);

watch(noNegative, () => {
  Object.assign(form.value, {
    workplace: "Негатив по местам работы не выявлен",
    document: "Среди недействительных документов не значится",
    debt: "Задолженности не обнаружены",
    bankruptcy: "Решений о признании банкротом не имеется",
    bki: "Кредитная история положительная",
    courts: "Судебные дела не обнаружены",
    affilation: "Аффилированность не выявлена",
    terrorist: "В списке террористов не обнаружен",
    internet: "В открытых источниках негатив не обнаружен",
    cronos: "В Кронос негатив не выявлен",
    conclusion: conclusions.agreed,
  });
});

const fields = [
  {
    element: "textarea",
    key: "workplace",
    label: "Проверка по местам работы",
  },
  {
    element: "textarea",
    key: "document",
    label: "Проверка документов",
  },
  {
    element: "textarea",
    key: "debt",
    label: "Проверка задолженностей",
  },
  {
    element: "textarea",
    key: "bankruptcy",
    label: "Проверка банкротства",
  },
  {
    element: "textarea",
    key: "bki",
    label: "Проверка Кредитной истории",
  },
  {
    element: "textarea",
    key: "courts",
    label: "Проверка судебных дел",
  },
  {
    element: "textarea",
    key: "affilation",
    label: "Проверка аффилированности",
  },
  {
    element: "textarea",
    key: "terrorist",
    label: "Проверка в списке террористов",
  },
  {
    element: "textarea",
    key: "internet",
    label: "Проверка в открытых источниках",
  },
  {
    element: "textarea",
    key: "cronos",
    label: "Проверка в Кронос",
  },
  {
    element: "textarea",
    key: "addition",
    label: "Дополнительная информация",
  },
  {
    element: "textarea",
    key: "comment",
    label: "Комментарий",
  },
  {
    element: "select",
    key: "conclusion",
    label: "Результат",
    items: Object.values(conclusions),
    required: true,
  },
] as FormField[];
</script>

<template>
  <UFormField>
    <USwitch v-model="noNegative" label="Негатива нет" />
  </UFormField>
  <FormCard :fields="fields" :item="form" @submit="emit('update', $event)" />
</template>
