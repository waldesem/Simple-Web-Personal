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

const parser = fallbackParser(schemaResume)
const resume = computed(() => parser(props.resume));

const fields = [
  {
    element: "input",
    key: "surname",
    label: "Фамилия",
    required: true,
  },
  {
    element: "input",
    key: "firstname",
    label: "Имя",
    required: true,
  },
  {
    element: "input",
    key: "patronymic",
    label: "Отчество",
  },
  {
    element: "input",
    key: "birthday",
    label: "Дата рождения",
    type: "date",
    required: true,
  },
  {
    element: "input",
    key: "birthplace",
    label: "Место рождения",
  },
  {
    element: "input",
    key: "citizenship",
    label: "Гражданство",
  },
  {
    element: "input",
    key: "dual",
    label: "Двойное гражданство",
  },
  {
    element: "input",
    key: "snils",
    label: "СНИЛС",
  },
  {
    element: "input",
    key: "inn",
    label: "ИНН",
  },
  {
    element: "input",
    key: "marital",
    label: "Семейное положение",
  },
  {
    element: "textarea",
    key: "addition",
    label: "Дополнительно",
  },
] as FormField[];
</script>

<template>
  <FormCard
    :schema="schemaResume"
    :fields="fields"
    :item="resume"
    @submit="emit('update', parserResume($event))"
  />
</template>
