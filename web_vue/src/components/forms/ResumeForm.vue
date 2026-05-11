<script setup lang="ts">
import { ref, PropType } from "vue";
import { parserResume, schemaResume } from "@/schema";
import type { FormField, Person } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  resume: {
    type: Object as PropType<Person>,
    default: () => ({}),
  },
});

const form = ref({
  surname: props.resume.surname ?? "",
  firstname: props.resume.firstname ?? "",
  patronymic: props.resume.patronymic ?? "",
  birthday: props.resume.birthday ?? "",
  birthplace: props.resume.birthplace ?? "",
  citizenship: props.resume.citizenship ?? "",
  dual: props.resume.dual ?? "",
  snils: props.resume.snils ?? "",
  inn: props.resume.inn ?? "",
  marital: props.resume.marital ?? "",
  addition: props.resume.addition ?? "",
});

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
    :item="form"
    @submit="emit('update', parserResume(form))"
  />
</template>
