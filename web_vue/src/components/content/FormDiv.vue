<script setup lang="ts">
import { type PropType, resolveComponent, ref } from "vue";
import type { FormElementAttrs, FormFields } from "@/types";

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

const resolveFormElement = (element: keyof FormElementAttrs = "input") => {
  const resolved = {
    input: resolveComponent("NUInput"),
    select: resolveComponent("NUSelect"),
    textarea: resolveComponent("NUTextarea"),
  };
  return resolved[element];
};
</script>

<template>
  <NUForm :state="form" @submit.prevent="emit('submit', form)">
    <NUFormField
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
    </NUFormField>
    <NUButton label="Принять" color="success" variant="outline" type="submit" />
  </NUForm>
</template>
