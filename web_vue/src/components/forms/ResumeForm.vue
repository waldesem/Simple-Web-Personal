<script setup lang="ts">
import { PropType, computed } from "vue";
import { fallbackParser, parserResume, schemaResume } from "@/schema";
import type { FormField, Person } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  resume: {
    type: Object as PropType<Person>,
    default: () => ({}),
  },
});

const fallback = computed(() => fallbackParser(schemaResume, props.resume));

const fields = [
  {
    element: "input",
    key: "surname",
    label: "Фамилия",
    attrs: { placeholder: "Фамилия", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "firstname",
    label: "Имя",
    attrs: { placeholder: "Имя", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "patronymic",
    label: "Отчество",
    attrs: { placeholder: "Отчество", maxlength: 255 },
  },
  {
    element: "input",
    key: "birthday",
    label: "Дата рождения",
    attrs: { type: "date", required: true },
  },
  {
    element: "input",
    key: "birthplace",
    label: "Место рождения",
    attrs: { placeholder: "Место рождения", maxlength: 255 },
  },
  {
    element: "input",
    key: "citizenship",
    label: "Гражданство",
    attrs: { placeholder: "Гражданство", maxlength: 255 },
  },
  {
    element: "input",
    key: "dual",
    label: "Двойное гражданство",
    attrs: { placeholder: "Двойное гражданство", maxlength: 255 },
  },
  {
    element: "input",
    key: "snils",
    label: "СНИЛС",
    attrs: { placeholder: "СНИЛС" },
  },
  {
    element: "input",
    key: "inn",
    label: "ИНН",
    attrs: { placeholder: "ИНН" },
  },
  {
    element: "input",
    key: "marital",
    label: "Семейное положение",
    attrs: { placeholder: "Семейное положение", maxlength: 255 },
  },
  {
    element: "textarea",
    key: "addition",
    label: "Дополнительно",
    attrs: { placeholder: "Дополнительная информация", maxlength: 4096 },
  },
] as FormField[];
</script>

<template>
  <FormCard
    :schema="schemaResume"
    :fields="props.fields"
    :item="fallback"
    @submit="emit('update', parserResume($event))"
  />
</template>
