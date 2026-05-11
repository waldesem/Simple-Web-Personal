<script setup lang="ts">
import { PropType, ref } from "vue";
import type { Previous } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Previous>,
    default: () => ({}),
  },
});

const form = ref({
  id: props.item.id ?? null,
  surname: props.item.surname ?? "",
  firstname: props.item.firstname ?? "",
  patronymic: props.item.patronymic ?? "",
  changed: props.item.changed ?? "",
  reason: props.item.reason ?? "",
});
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Фамилия" name="surname" required>
      <UInput v-model.trim.lazy="form.surname" placeholder="Фамилия" />
    </UFormField>
    <UFormField label="Имя" name="firstname" required>
      <UInput v-model.trim.lazy="form.firstname" placeholder="Имя" />
    </UFormField>
    <UFormField label="Отчество" name="patronymic">
      <UInput v-model.trim.lazy="form.patronymic" placeholder="Отчество" />
    </UFormField>
    <UFormField label="Год изменения" name="changed">
      <UInput
        v-model.trim.lazy="form.changed"
        placeholder="Год изменения"
        pattern="^\d{4}$"
      />
    </UFormField>
    <UFormField label="Причина изменения" name="reason">
      <UTextarea
        v-model.trim.lazy="form.reason"
        placeholder="Причина изменения"
        maxlength="4096"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
