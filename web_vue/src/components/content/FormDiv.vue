<script setup lang="ts">
import { type PropType, toRef } from "vue";
import type { FormFields, Items } from "@/types";

const emit = defineEmits(["submit"]);

const props = defineProps({
  fields: {
    type: Array as PropType<FormFields<Items[keyof Items]>[]>,
    required: true,
  },
  item: {
    type: Object as PropType<Items[keyof Items]>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('submit', form)">
    <UFormField
      v-for="field in fields"
      :key="field.key"
      :name="field.key"
      :label="field.label"
      :required="field.props ? (field.props.required as boolean) : false"
    >
      <UInput
        v-if="field.element === 'input'"
        v-model.trim.lazy="form[field.key]"
        v-bind="{ ...field.props }"
      />
      <USelect
        v-else-if="field.element === 'select'"
        v-model="form[field.key]"
        v-bind="{ ...field.props }"
        :items="field.items"
      />
      <UTextarea
        v-else-if="field.element === 'textarea'"
        v-model.trim.lazy="form[field.key]"
        v-bind="{ ...field.props }"
        autoresize
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
