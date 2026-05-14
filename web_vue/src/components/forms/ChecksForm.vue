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
    attrs: { placeholder: "Проверка по местам работы", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "document",
    label: "Проверка документов",
    attrs: { placeholder: "Проверка документов", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "debt",
    label: "Проверка задолженностей",
    attrs: { placeholder: "Проверка задолженностей", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "bankruptcy",
    label: "Проверка банкротства",
    attrs: { placeholder: "Проверка банкротства", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "bki",
    label: "Проверка Кредитной истории",
    attrs: { placeholder: "Проверка Кредитной истории", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "courts",
    label: "Проверка судебных дел",
    attrs: { placeholder: "Проверка судебных дел", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "affilation",
    label: "Проверка аффилированности",
    attrs: { placeholder: "Проверка аффилированности", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "terrorist",
    label: "Проверка в списке террористов",
    attrs: { placeholder: "Проверка в списке террористов", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "internet",
    label: "Проверка в открытых источниках",
    attrs: { placeholder: "Проверка в открытых источниках", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "cronos",
    label: "Проверка в Кронос",
    attrs: { placeholder: "Проверка в Кронос", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "addition",
    label: "Дополнительная информация",
    attrs: { placeholder: "Дополнительная информация", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "comment",
    label: "Комментарий",
    attrs: { placeholder: "Комментарий", maxlength: 4096 },
  },
  {
    element: "select",
    key: "conclusion",
    label: "Результат",
    items: Object.values(conclusions),
    attrs: { placeholder: "Выберите результат", required: true },
  },
] as FormField[];
</script>

<template>
  <UFormField>
    <USwitch v-model="noNegative" label="Негатива нет" />
  </UFormField>
  <FormCard :fields="fields" :item="form" @submit="emit('update', $event)" />
</template>
