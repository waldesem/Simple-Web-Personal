<script setup lang="ts">
import * as v from "valibot";
import type { Person } from "@/types";
import { PropType, toRef } from "vue";

const emit = defineEmits(["update"]);

const props = defineProps({
  resume: {
    type: Object as PropType<Person>,
    default: () => ({}),
  },
});

const form = toRef(props.resume);

const schema = v.object({
  surname: v.optional(
    v.pipe(
      v.string(),
      v.nonEmpty("Обязательное поле!"),
      v.regex(/^[А-ЯЁ][А-ЯЁIV\-.,'()\s]*[А-ЯЁ]$/, "Недопустимые символы!"),
      v.maxLength(255, "Не более 255 символов!"),
    ),
    "",
  ),
  firstname: v.optional(
    v.pipe(
      v.string(),
      v.nonEmpty("Обязательное поле!"),
      v.regex(/^[А-ЯЁ][А-ЯЁIV\-.,'()\s]*[А-ЯЁ]$/, "Недопустимые символы!"),
      v.maxLength(255, "Не более 255 символов!"),
    ),
    "",
  ),
  patronymic: v.fallback(
    v.pipe(
      v.string(),
      v.regex(/^[А-ЯЁ][А-ЯЁIV\-.,'()\s]*[А-ЯЁ]$/, "Недопустимые символы!"),
      v.maxLength(255, "Не более 255 символов!"),
    ),
    "",
  ),
  birthday: v.optional(
    v.pipe(
      v.string(),
      v.nonEmpty("Обязательное поле!"),
      v.toDate(),
      v.maxValue(new Date(), "Проверьте дату!"),
      v.minValue(new Date(1900, 0, 1), "Проверьте дату!"),
    ),
    "",
  ),
  birthplace: v.fallback(
    v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
    "",
  ),
  citizenship: v.fallback(
    v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
    "",
  ),
  dual: v.fallback(
    v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
    "",
  ),
  snils: v.fallback(
    v.pipe(v.string(), v.regex(/[0-9]{11}/, "Только 11 цифр!")),
    "",
  ),
  inn: v.fallback(
    v.pipe(v.string(), v.regex(/[0-9]{12}/, "Только 12 цифр!")),
    "",
  ),
  marital: v.fallback(
    v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
    "",
  ),
  addition: v.fallback(v.string(), ""),
});
</script>

<template>
  <UForm :state="form" :schema="schema" @submit.prevent="emit('update', form)">
    <UFormField label="Фамилия" name="surname" required>
      <UInput v-model.lazy.trim="form.surname" placeholder="Фамилия" />
    </UFormField>
    <UFormField label="Имя" name="firstname" required>
      <UInput v-model.lazy.trim="form.firstname" placeholder="Имя" />
    </UFormField>
    <UFormField label="Отчество" name="patronymic">
      <UInput v-model.lazy.trim="form.patronymic" placeholder="Отчество" />
    </UFormField>
    <UFormField label="Дата рождения" name="birthday" required>
      <UInput v-model="form.birthday" type="date" />
    </UFormField>
    <UFormField label="Место рождения" name="birthplace">
      <UInput
        v-model.lazy.trim="form.birthplace"
        placeholder="Место рождения"
      />
    </UFormField>
    <UFormField label="Гражданство" name="citizenship">
      <UInput v-model.lazy.trim="form.citizenship" placeholder="Гражданство" />
    </UFormField>
    <UFormField label="Двойное гражданство" name="dual">
      <UInput v-model.lazy.trim="form.dual" placeholder="Двойное гражданство" />
    </UFormField>
    <UFormField label="СНИЛС" name="snils">
      <UInput v-model.lazy.trim="form.snils" placeholder="СНИЛС" />
    </UFormField>
    <UFormField label="ИНН" name="inn">
      <UInput v-model.lazy.trim="form.inn" placeholder="ИНН" />
    </UFormField>
    <UFormField label="Семейное положение" name="marital">
      <UInput
        v-model.lazy.trim="form.marital"
        placeholder="Семейное положение"
      />
    </UFormField>
    <UFormField label="Дополнительно" name="addition">
      <UTextarea
        v-model.lazy.trim="form.addition"
        placeholder="Дополнительно"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
