<script setup lang="ts">
import type { Person } from "@/types";
import { useClipboard } from "@vueuse/core";
import { PropType } from "vue";

const props = defineProps({
  item: {
    type: Object as PropType<Person>,
    default: () => {},
  },
});

const { copy, copied } = useClipboard();
</script>

<template>
  <LabelValue label="Фамилия" :value="props.item.surname" />
  <LabelValue label="Имя" :value="props.item.firstname" />
  <LabelValue
    v-if="props.item.patronymic"
    label="Отчество"
    :value="props.item.patronymic"
  />
  <LabelValue label="Дата рождения">
    {{ new Date(props.item.birthday).toLocaleDateString() }}
  </LabelValue>
  <LabelValue
    v-if="props.item.birthplace"
    label="Место рождения"
    :value="props.item.birthplace"
  />
  <LabelValue
    v-if="props.item.citizenship"
    label="Гражданство"
    :value="props.item.citizenship"
  />
  <LabelValue v-if="props.item.dual" label="Двойное гражданство">
    <UBadge variant="outline" color="info" :label="props.item.dual" />
  </LabelValue>
  <LabelValue v-if="props.item.snils" label="СНИЛС" :value="props.item.snils" />
  <LabelValue v-if="props.item.inn" label="ИНН" :value="props.item.inn" />
  <LabelValue
    v-if="props.item.marital"
    label="Семейное положение"
    :value="props.item.marital"
  />
  <LabelValue label="Дата записи">
    {{ new Date(props.item.created).toLocaleDateString() }}
  </LabelValue>
  <LabelValue
    v-if="props.item.addition"
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <LabelValue v-if="props.item.destination" label="Материалы проверок">
    <UButton
      variant="outline"
      :color="!copied ? 'info' : 'success'"
      size="sm"
      :label="!copied ? 'Копировать ссылку' : 'Скопировано'"
      @click="copy(props.item.destination)"
    />
  </LabelValue>
</template>
