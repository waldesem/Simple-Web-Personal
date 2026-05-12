<script setup lang="ts">
import { computed, PropType } from "vue";
import { useClipboard } from "@vueuse/core";
import { localStr } from "@/utils";
import type { ItemField, Person } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Person>,
    required: true,
  },
});

const { copy, copied } = useClipboard();

const fields = [
  { key: "surname", label: "Фамилия" },
  { key: "firstname", label: "Имя" },
  { key: "patronymic", label: "Отчество" },
  { key: "birthday", label: "Дата рождения" },
  { key: "birthplace", label: "Место рождения" },
  { key: "citizenship", label: "Гражданство" },
  { key: "dual", label: "Двойное гражданство" },
  { key: "snils", label: "СНИЛС" },
  { key: "inn", label: "ИНН" },
  { key: "marital", label: "Семейное положение" },
  { key: "created", label: "Дата записи" },
  { key: "addition", label: "Дополнительная информация" },
  { key: "destination", label: "Материалы проверок", slot: true },
] as ItemField[];

const person = computed(() => {
  return {
    ...props.item,
    birthday: localStr(props.item.birthday),
    created: localStr(props.item.created),
  };
});
</script>

<template>
  <ItemCard :fields="fields" :item="person">
    <template v-if="props.item.destination" #destination>
      <UButton
        variant="outline"
        size="sm"
        :color="copied ? 'success' : 'info'"
        :label="copied ? 'Скопировано' : 'Копировать'"
        @click="copy(props.item.destination)"
      />
    </template>
  </ItemCard>
</template>
