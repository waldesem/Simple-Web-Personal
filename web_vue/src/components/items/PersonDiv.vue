<script setup lang="ts">
import { PropType } from "vue";
import { useClipboard } from "@vueuse/core";
import { localDateStr } from "@/utils";
import type { ItemField, Person } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Person>,
    required: true,
  },
});

const { copy, copied } = useClipboard();

const fields = [
  { key: "surname", label: "Фамилия", value: props.item.surname },
  { key: "firstname", label: "Имя", value: props.item.firstname },
  { key: "patronymic", label: "Отчество", value: props.item.patronymic },
  {
    key: "birthday",
    label: "Дата рождения",
    value: localDateStr(props.item.birthday),
  },
  { key: "birthplace", label: "Место рождения", value: props.item.birthplace },
  { key: "citizenship", label: "Гражданство", value: props.item.citizenship },
  { key: "dual", label: "Двойное гражданство", slot: true },
  { key: "snils", label: "СНИЛС", value: props.item.snils },
  { key: "inn", label: "ИНН", value: props.item.inn },
  { key: "marital", label: "Семейное положение", value: props.item.marital },
  {
    key: "created",
    label: "Дата записи",
    value: localDateStr(props.item.created),
  },
  {
    key: "addition",
    label: "Дополнительная информация",
    value: props.item.addition,
  },
  { key: "destination", label: "Материалы проверок", slot: true },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields">
    <template #dual v-if="props.item.dual">
      <UBadge variant="outline" color="info" :label="props.item.dual" />
    </template>
    <template #destination v-if="props.item.destination">
      <UButton
        variant="outline"
        :color="!copied ? 'info' : 'success'"
        size="sm"
        :label="!copied ? 'Копировать ссылку' : 'Скопировано'"
        @click="copy(props.item.destination)"
      />
    </template>
  </ItemCard>
</template>
