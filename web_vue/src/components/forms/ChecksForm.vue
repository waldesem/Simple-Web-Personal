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
  fields: {
    type: Array as PropType<FormField[]>,
    required: true,
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
</script>

<template>
  <UFormField>
    <USwitch v-model="noNegative" label="Негатива нет" />
  </UFormField>
  <FormCard :fields="props.fields" :item="form" @submit="emit('update', $event)" />
</template>
