<script setup lang="ts">
import { empty } from "@/schema";
import { PropType, toRef } from "vue";
import type { FormField } from "@/types";

const emit = defineEmits(["submit"]);

const props = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
  fields: {
    type: Array as PropType<FormField[]>,
    required: true,
  },
  schema: {
    type: Object,
    default: () => empty,
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" :schema="schema" @submit.prevent="emit('submit', form)">
    <UFormField
      v-for="field in fields"
      :key="field.key"
      :label="field.label"
      :name="field.key"
      :required="field.required ?? false"
    >
      <UInput
        v-if="field.element === 'input'"
        v-model.trim.lazy="form[field.key]"
        :placeholder="field.label"
        :maxlength="field.maxlength ?? 255"
        :type="field.type ?? 'text'"
        :pattern="field.pattern ?? '.*'"
        :required="field.required ?? false"
      />
      <USelect
        v-else-if="field.element === 'select'"
        v-model="form[field.key]"
        :items="field.items"
        :placeholder="field.label"
        :required="field.required ?? false"
      />
      <UTextarea
        v-else-if="field.element === 'textarea'"
        v-model.trim.lazy="form[field.key]"
        :placeholder="field.label"
        :maxlength="field.maxlength ?? 4096"
        :required="field.required ?? false"
        autoresize
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
