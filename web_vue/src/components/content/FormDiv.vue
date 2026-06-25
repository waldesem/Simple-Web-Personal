<script setup lang="ts">
import { type PropType, resolveComponent, ref } from "vue";
import type { FormElemAttrs, FormFields } from "@/types";

const emit = defineEmits(["submit"]);

const props = defineProps({
  fields: {
    type: Array as PropType<FormFields<Record<string, any>>[]>,
    required: true,
  },
  item: {
    type: Object as PropType<any>,
    default: () => ({}),
  },
});

const form = ref(props.item);

const resolveFormElement = (element: keyof FormElemAttrs = "input") => {
  const html = {
    input: resolveComponent("UInput"),
    select: resolveComponent("USelect"),
    textarea: resolveComponent("UTextarea"),
  };
  return html[element];
};
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('submit', form)">
    <UFormField
      v-for="field in fields"
      :key="field.key"
      :label="field.label"
      :name="field.key"
      :required="field.props.required ?? false"
    >
      <component
        :is="resolveFormElement(field.element)"
        v-model.lazy.trim="form[field.key]"
        v-bind="field.props"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
